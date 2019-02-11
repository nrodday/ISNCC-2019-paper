# Usage_of_DSCP_and_ECN
On the Usage of DSCP and ECN Codepoints in Internet Backbone Traffic Traces for IPv4 and IPv6





You will need:

input/ -> containing pcap.gz files

output/ -> containing pregenerated result files

Run the analyzer_multithread over the input folder containing pcap.gz files. Specify an output directory and the number of processes to run the script with. In the output directory you need pregenerated empty files for the analyzer script to work properly. You generate those files with the filegenerator script, specifying the output directory and option 1, for all files. The analyzer_multithread instanciates according to the number of processes you specified (-1 for the asynchronous queue process) child processes. Each child will run over one pcap.gz file in the input folder.


The generator works as follows:
python3.6 xlsx_file_generator.py output/
-> Choose Option 1

The analyzer_multithread as follows:
python3.6 analyzer_multithread.py input/ output/ 45
-> Works best for python3.6.6

If you prefer running the script unattended run:
nohup python3.6 analyzer_multithread.py input/ output/ 45 &


The following pip packages need to be installed:

pip3.6 list

Package         Version
--------------- -------
beautifulsoup4  4.6.1
bs4             0.0.1
et-xmlfile      1.0.1
jdcal           1.4
numpy           1.15.0
openpyxl        2.5.5
pandas          0.23.4
pip             18.0
pipp            0.0.1
psutil          5.4.6
python-dateutil 2.7.3
pytz            2018.5
scapy           2.4.0
setuptools      39.0.1
six             1.11.0
xlrd            1.1.0
