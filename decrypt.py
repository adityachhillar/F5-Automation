import getpass
import paramiko
import time
import subprocess
from datetime import datetime
import os

#Checking "C:\F5_configs" is present or not
folder_path = "C:\F5_configs"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    #print(f"Folder {folder_path} created.")
    print("\nDecrypting Packet Captures Automatically from Big-IP v15.x\n")
else:
    #print(f"Folder {folder_path} already exists.")
    print("\nDecrypting Packet Captures Automatically from Big-IP v15.x\n")

device_ip = input("Enter the F5 device IP address: ")
username = input("Enter your username: ")
password = getpass.getpass()

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh_client.connect(device_ip, username=username, password=password)
    print("\nLogin successful!")
    
    # Code to continue with session
    
    now = datetime.now()
    pcap_file_name = "decrypt_"+ now.strftime("%Y-%m-%d_%H-%M-%S") + ".pcap"
    pms_file_name = "session_"+ now.strftime("%Y-%m-%d_%H-%M-%S") + ".pms"

    # enable TLS Session Secret Ethernet Trailers
    stdin, stdout, stderr = ssh_client.exec_command("tmsh modify sys db tcpdump.sslprovider value enable")
    print("\nTLS Session Secret Ethernet Trailers Enabled")
    time.sleep(2)

    # prompt user for virtual server IP and tcpdump time
    ip_addr = input("\nEnter Host IP address: ")
    port = input(("\nEnter Host Port number: "))
    tcpdump_time = input("\nEnter time for tcpdump (in seconds): ")

    # run tcpdump
    tcpdump_cmd = f"timeout {tcpdump_time} tcpdump -s0 -nni 0.0:nnn --f5 ssl host {ip_addr} and port {port} -vw /var/tmp/{pcap_file_name}"
    stdin, stdout, stderr = ssh_client.exec_command(tcpdump_cmd)

    print("\nGenerating tcpdump for", tcpdump_time, "seconds.")

    # sleep for user-specified time
    time.sleep(int(tcpdump_time) + 5)

    # disabling TLS Session Secret Ethernet Trailers
    stdin, stdout, stderr = ssh_client.exec_command("tmsh modify sys db tcpdump.sslprovider value disable")
    print("\nTLS Session Secret Ethernet Trailers Disabled")
    time.sleep(2)

    print("\nDownloading",pcap_file_name,"to local machine...")

    # download pcap file
    sftp_client = ssh_client.open_sftp()
    local_path = "C:\\F5_configs\\" + pcap_file_name
    remote_path = "/var/tmp/" + pcap_file_name
    sftp_client.get(remote_path, local_path)
    sftp_client.close()
    time.sleep(2)

    print("\nDownload successfull!")
    time.sleep(2)

    # Delete the PCAP file at /var/tmp/*.pcap
    stdin, stdout, stderr = ssh_client.exec_command(f"rm /var/tmp/{pcap_file_name}")
    time.sleep(5)

    print("\nCreating Pre-Master Secret (PMS) Log File.")

    # Extract the session master keys
    #keylog_cmd = '"c:\\Program Files\\Wireshark"\\tshark.exe -r C:\\F5_configs\\file_name -Y "f5ethtrailer.tls.keylog" -T fields -e f5ethtrailer.tls.keylog >> C:\\F5_configs\\{today}.pms'
    keylog_cmd = f'"c:\\Program Files\\Wireshark"\\tshark.exe -r C:\\F5_configs\\{pcap_file_name} -Y "f5ethtrailer.tls.keylog" -T fields -e f5ethtrailer.tls.keylog >> C:\\F5_configs\\{pms_file_name}'
    subprocess.run(keylog_cmd, shell=True)

    print("\nPCAP & PMS successfully stored at C:\F5_configs\\")
    print("\nLoad the Pre-Master Secret Log file into Wireshark and start decrypting Application Layer (L7) data. \n\n  1. In Wireshark Navigate to Edit > Preferences > Protocols > TLS \n  2. In the section labeled '(Pre)-Master-Secret log filename' browse to the pre_master_log.pms file and click OK. \n\nIf all goes well, you will now be observing decrypted L7 data.")

    input("\nPress any key to close the session")

except paramiko.ssh_exception.AuthenticationException:
    print("Wrong Username and password. Exiting.")
    exit()
