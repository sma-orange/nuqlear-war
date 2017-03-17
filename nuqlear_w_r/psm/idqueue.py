"""Class to manage an "ID Queue".
Loads MSISDNs from a file (1 MSISDN) per line for PSM API tests.
NuQ should reload the file if the volume of requests > MSISDNs in file.
"""
import logging
from queue import Queue, Empty

logger = logging.getLogger(__name__)


class IDQueue:
    """Class to read in a file of MSISDNs and populate into a queue"""
    def __init__(self):
        self.queue = Queue()
        self.file = None
        logger.info('Started ID Queue')

    def populate(self, source_file):
        """load the contents of a file into a queue
        each line of the file should be a single msisdn provisioned on the target platform
        :parameter source_file the name of the file to load
        """
        # TODO: fix path
        filename = '/home/ben/PycharmProjects/nuqlear_war/storage/inputs/msisdns/'
        filename.join(source_file)
        print(filename)
        print(source_file)
        self.file = open(filename, 'r')
        for line in self.file:
            self.queue.put(str(line).strip(), block=False, timeout=None)
        logger.info('ID Queue loaded')

    def reload(self):
        """reload the file into the queue"""
        with open(self.file):
            for line in self.file:
                self.queue.put(str(line).strip(), block=False, timeout=None)
            logger.info('ID Queue reloaded')
        return True

    def pop_off(self):
        """return a msisdn, if the queue is empty reload
        :return a MSISDN from the file or None on Empty queue
        """
        try:
            return self.queue.get(block=False, timeout=None)
        except Empty:
            logger.info('You should reload the ID Queue')
            return None
