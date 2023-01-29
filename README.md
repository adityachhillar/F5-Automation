# F5-Automation
This repository contains scripts to automate repetitive tasks on F5 Big-IP, reducing the amount of time and effort typically required. This results in a faster SLA and increased efficiency. The scripts will benefit teams working on Big-IP, freeing up valuable time for learning and growth opportunities. 

# Roadmap
1. Support tasks: Automating day to day redundant support issues. ## This has been initiated with "Decrypting Packet Captures Automatically" script.
3. Configuration management: Automating the deployment and management of configurations across multiple Big-IP devices.
4. Health Monitoring: Automating the monitoring of the health and performance of Big-IP devices and their resources.
5. Load balancing: Automatically provision and manage load balancing virtual servers, pools, and pool members.
6. SSL Certificate Management: Automate the management of SSL certificates, including renewals, import, and export.
7. Automated Deployments: Automating the deployment of new Big-IP devices and software updates.
8. Reporting and Analytics: Collect and analyze data from Big-IP devices for reporting and trend analysis purposes.

# Decrypting Packet Captures Automatically from Big-IP v15.x
This use case can be achieved using `decrypt.py`.

Once starting the script, it will ask you for three things:

1. The virtual server Port under test
2. The virtual server Port under test
3. Time (seconds) to run TCPDUMP.

Once the tcpdump capture is started for you, you'll have to reproduce the issue within the time-frame entered by you. After finishing the tcpdump, it will download the *.pcap file to your local system and extract the *.pms file from it using tshark utility of Wireshark.

Both the files will be stored under `C:\F5_configs`. You can run the *.pcap file and load the *.pms file `following below instructions`.

>> Load Pre-Master Secret Log File Into Wireshark

>> In Wireshark Navigate to Edit > Preferences > Protocols > TLS

>> In the section labeled '(Pre)-Master-Secret log filename' browse to the pre_master_log.pms file and click OK.

>> If all goes well, you will now be observing decrypted L7 data.

# Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

# License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

## Contact

Your Name - [@adityachhillar](https://twitter.com/adityachhillar)

Project Link: [https://github.com/adityachhillar/F5-Automation](https://github.com/adityachhillar/F5-Automation)

# Acknowledgments
The Python Community

[Jason Rahm](https://github.com/f5-rahm)
