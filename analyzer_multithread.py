__author__ = "Nils Rodday"
__copyright__ = "Copyright 2018"
__credits__ = ["Nils Rodday"]
__email__ = "nils.rodday@unibw.de"
__status__ = "Experimental"


from multiprocessing import Pool, Queue, Manager
import multiprocessing as mp
from subprocess import call
import glob
import sys
import time
from functools import partial
import os
import logging


#This imports additional code
import result_aggregator



if len(sys.argv) != 4:
    print('Usage:')
    print('analyzer_multithread.py INPUT_FOLDER OUTPUT_FOLDER NUMBER_OF_PROCESSES')
    sys.exit()

#Input params
input_folder = sys.argv[1]
output_folder = sys.argv[2]
number_of_processes = int(sys.argv[3])

#output_folder = 'output/'
#input_folder = 'input/'
#number_of_processes = 4

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename= output_folder + 'analyzer_multithread.log',level=logging.DEBUG)
#sys.stdout.flush()

#Initiate subprocess
def crunch_file(q, filename):
    logging.debug('Starting with file: ' + filename)
    logging.debug('--------------------------')
    start_time = time.time()

    #Call analyzer
    call(["python3.6", "analyzer.py", filename, output_folder])

    #Add filename to Queue for result collection
    q.put(filename)

    end_time = time.time()
    temp = end_time - start_time
    hours = temp // 3600
    temp = temp - 3600 * hours
    minutes = temp // 60
    seconds = temp - 60 * minutes
    logging.debug('File ' +  filename + ' took (Hours:Minutes:Seconds): ' + '%d:%d:%d' % (hours, minutes, seconds))
    logging.debug('Done with file: ' + filename)
    logging.debug('--------------------------')


#
# MAIN PROGRAM
#
if __name__ == '__main__':
    pcap_gz_files = glob.glob(input_folder + '/**/*.pcap.gz', recursive=True)

    logging.debug('--------------------------')
    logging.debug('Files to process: ')
    for file in pcap_gz_files:
        logging.debug(file)
    logging.debug('--------------------------')

    #create directory for files
    if not os.path.exists(output_folder + "tmp"):
        call(["mkdir", output_folder + 'tmp'])

    with Pool(processes=number_of_processes) as p:
        #logging.debug('Process ID Multi' + str(os.getpid()))

        m = mp.Manager()
        result_files_queue = m.Queue()

        #Start asynchronous process for result collector
        p.apply_async(result_aggregator.result_collector, (result_files_queue, output_folder,))

        #Start worker processes for each pcap.gz file
        func = partial(crunch_file, result_files_queue)
        res  = p.map(func, pcap_gz_files, 1)

        #Wait for the queue to be empty before adding DONE to terminate the result_collector
        while not result_files_queue.empty():
            logging.debug('Result Collector is still running - waiting for shut down, sleeping for 2min')
            time.sleep(60)

        #Once worker processes are finished, let result_collector know via Queue
        logging.debug('Add DONE to Queue, all processes are finished.')
        result_files_queue.put('DONE')

        #clean up once all tasks are done
        p.close()
        p.join()


    logging.debug('All work done, now exiting!')

