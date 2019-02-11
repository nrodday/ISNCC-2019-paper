__author__ = "Nils Rodday"
__copyright__ = "Copyright 2018"
__credits__ = ["Nils Rodday"]
__email__ = "nils.rodday@unibw.de"
__status__ = "Experimental"


###################
####Download#######
######CAIDA########
#####Archives######
###################



from bs4 import BeautifulSoup
#from urllib.parse import urlparse

import urllib.request
import os
import pathlib
import sys
import time
import logging

# Install Modules:
# pip install beautifulsoup4

# Global variables:

CAIDA_links = []
Download_Path = ''

# Function to retrieve webpage content

def open_webpage(top_level_url):

	tries = 0
	while tries <= 20:

	# HTTP Request with Basic Auth

		username = "" #Add your credentials here
		password  = ""

		# create an authorization handler
		p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		p.add_password(None, top_level_url, username, password)

		auth_handler = urllib.request.HTTPBasicAuthHandler(p)

		opener = urllib.request.build_opener(auth_handler)

		urllib.request.install_opener(opener)

		try:
			result = opener.open(top_level_url)
			messages = result.read()
			#logging.info (messages)
			#logging.info ('----------------------------')
			return messages
		except Exception as e:
			logging.info(e)
			logging.info('Got an Error, going to sleep for 1 min and trying again to connect')
			time.sleep(60)
			tries += 1


def file_lookup(file_link):
	url_parts = file_link.split('/')
	file_path = Download_Path + '/'.join(url_parts[3:])

	logging.info ('Checking OS Path: ' + file_path)
	
	if os.path.exists(file_path):
		return file_path
	else:
		return None


def progress_bar(count, blockSize, totalSize):
	percent = int(count*blockSize*100/totalSize)
	sys.stdout.write("\r%d%%" % percent + ' complete')
	sys.stdout.flush()


def initiate_download(file_link):

	# Split the URL and compose the file path 
	url_parts = file_link.split('/')
	file_path = Download_Path + '/'.join(url_parts[3:])
	file_path_without_file = Download_Path + '/'.join(url_parts[3:-1])

	logging.info ('File Path: ' + file_path_without_file)

	# Create the file path if necessary
	pathlib.Path(file_path_without_file).mkdir(parents=True, exist_ok=True) 

	# Initiate the download and hook progress bar
	logging.info ('\n')

	tries = 0
	while tries <= 20:
		try:
			urllib.request.urlretrieve(file_link, file_path, reporthook=progress_bar)
			break
		except:
			logging.info('Got an Error, going to sleep for 1 min and trying again to connect')
			time.sleep(60)
			tries += 1



#PROGRAM STARTS HERE


print('Usage:')
print('downloader.py OUTPUT_FOLDER (INPUT_LINK)')


#Get output folder from parameter
Download_Path = sys.argv[1]

# If specific URL is given, use this one, otherwise read all links from file.
if len(sys.argv) == 3:
	CAIDA_links.append(sys.argv[2])
else:
	with open('resources.list', 'r') as f:
		CAIDA_links = [line.strip() for line in f]
		logging.info ('---CAIDA Links from File:---')
		logging.info (CAIDA_links)
		logging.info ('----------------------------')


# Go through all CAIDA links and find links (directories) starting with "equinix"

for CAIDA_link in CAIDA_links:

	# Logger
	logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='downloader_' + CAIDA_link.split('/')[-1] + ".log", level=logging.INFO)

	logging.info(CAIDA_link)
	data = open_webpage(CAIDA_link)

	soup = BeautifulSoup(data, 'html.parser')
	#logging.info (soup)
	#logging.info ('----------------------------')


	#logging.info ('----------------------------')
	#logging.info ('logging.infoing search result for "equinix" keyword in folder: ' + CAIDA_link)

	for link in soup.find_all('a'):
		if link.get('href').startswith("equinix"):
			#logging.info(link.get('href'))
			#logging.info ('----------------------------')
			#logging.info ('----------------------------')
			#logging.info ('\n')

			# Look for all subdirectories in each folder starting with "equinix"
			equinix_subfolder_link = CAIDA_link + '/' + link.get('href')
			equinix_folder_content = open_webpage(equinix_subfolder_link)

			equinix_soup = BeautifulSoup(equinix_folder_content, 'html.parser')
			#logging.info ('logging.infoing content of Equinix folder HTML: ')
			#logging.info (equinix_soup)
			#logging.info ('----------------------------')


			#logging.info ('----------------------------')
			#logging.info ('logging.infoing subfolders in folder: ' + equinix_subfolder_link)

			for link in equinix_soup.find_all('a'):
				if link.get('href').startswith("20"):

					#logging.info(link.get('href'))
					#logging.info ('----------------------------')
					#logging.info ('----------------------------')
					#logging.info ('----------------------------')
					#logging.info ('\n')


					# Look for all files in the subdirectory
					timestamp_subfolder_link = equinix_subfolder_link + link.get('href')
					timestamp_folder_content = open_webpage(timestamp_subfolder_link)

					timestamp_soup = BeautifulSoup(timestamp_folder_content, 'html.parser')
					#logging.info ('logging.infoing content of Timestamp folder HTML: ')
					#logging.info (timestamp_soup)
					#logging.info ('----------------------------')


					#logging.info ('----------------------------')
					#logging.info ('logging.infoing all files in folder: ' + timestamp_subfolder_link)


					for link in timestamp_soup.find_all('a'):
						if link.get('href').startswith("equinix") or link.get('href').startswith("md5"):


							# Check for each file if it has already been downloaded, if not create file/folder and start downloading.

							file_link = timestamp_subfolder_link + link.get('href')
							logging.info ('Checking file: ' + file_link)
							lookup_result = file_lookup(file_link)
							
							if lookup_result == None:
								logging.info ('Started downloading file: ' + file_link)
								start = time.clock()
								logging.info(file_link)
								initiate_download(file_link)
								stop = time.clock()
								logging.info ('Finished downloading file: ' + file_link)
								logging.info('Downloaded in minutes: ' + str(stop-start))
								logging.info ('Moving on...')
								logging.info ('----------------------------')
							else:
								logging.info ('File already present at: ' + lookup_result)
								logging.info ('Moving on...')
								logging.info ('----------------------------')

					logging.info ('----------------------------')
					logging.info ('----------------------------')
					logging.info ('----------------------------')
					logging.info ('----------------------------')
					logging.info ('\n')









