"""Class to manage the NuQ DB.
Basic PyMySQL implementation
"""
import logging
import pymysql
from pymysql import MySQLError
from pymysql.cursors import DictCursor

from util import utils

logger = logging.getLogger(__name__)


"""SQL STATEMENTS"""
# A Test
MAIN_SQL = 'CREATE TABLE test (' \
           'id INT NOT NULL AUTO_INCREMENT,' \
           'pseudo_test_id VARCHAR(10) NOT NULL,' \
           'cuid VARCHAR(8),' \
           'test_name VARCHAR(255),' \
           'mode VARCHAR(6),' \
           'volume INT,' \
           'rate VARCHAR(6),' \
           'url VARCHAR(255),' \
           'psm_file VARCHAR(255),' \
           'psm_scenario VARCHAR(255),' \
           'creation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,' \
           'comments VARCHAR(255),' \
           'status VARCHAR(255),' \
           'PRIMARY KEY (id));'

# NuQ results
NUQ_SQL = 'CREATE TABLE nuq_results (' \
          'id INT NOT NULL AUTO_INCREMENT,' \
          'pseudo_nuq_id VARCHAR(10) NOT NULL,' \
          'run_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,' \
          'throttle FLOAT(1,1),' \
          'loop_start DATETIME,' \
          'loop_end DATETIME,' \
          'start DATETIME,' \
          'end DATETIME,' \
          'oks INT,' \
          'kos INT,' \
          'total INT,' \
          'lap_count INT,' \
          'psm_errors INT,' \
          'PRIMARY KEY (id));'

# Test results - these come from NuQ
NUQ_RESULTS_SQL = 'CREATE TABLE test_results (' \
              'id INT NOT NULL AUTO_INCREMENT,' \
              'pseudo_test_id VARCHAR(10),' \
              'run_date DATETIME,' \
              'lap_time INT,' \
              'status_code INT,' \
              'PRIMARY KEY (id));'


class NuQDB:
    """Class to manage the NuQ DB. Basic PyMySQL implementation
    """
    def __init__(self):
        """connect to the database and setup the tables per SQL STATEMENTS above if they do not exist
        :except ConnectionError
        """
        try:
            self.db = pymysql.connect(host='localhost', port=3306, user='nuq', passwd='dstk2012', db='nuq')
        except ConnectionError:
            logger.error('Could not connect to NuQ Database')
            raise
        logger.info('Connected to NuQ Database')
        cursor = self.db.cursor()
        try:
            cursor.execute('SELECT 1 FROM test, test_results LIMIT 1;')
            logger.info('NuQ Database exists...')
        except pymysql.ProgrammingError:
            logger.info('Database exists, but there are no tables...')
            self.setup_db()
        finally:
            cursor.close()

    def setup_db(self):
        """setup the database with the required tables
        :except MySQLError
        """
        logger.info('Setting up NuQ DB tables.')
        cursor = self.db.cursor()
        try:
            logger.info('Test Table...')
            cursor.execute(MAIN_SQL)
            self.db.commit()
        except MySQLError:
            logger.error('Could not create Test Table')
            raise
        try:
            logger.info('NuQ Results Table...')
            cursor.execute(NUQ_SQL)
            self.db.commit()
        except MySQLError:
            logger.error('Could not create NuQ Results Table')
            raise
        try:
            logger.info('Test Results Table...')
            cursor.execute(NUQ_RESULTS_SQL)
            self.db.commit()
        except MySQLError:
            logger.error('Could not create Test Results Table(s)')
            raise
        cursor.close()
        logger.info('NuQ DB created')

    def create_test(self, cuid, test_name, mode, volume, rate, url, file, scenario):
        """create entry for this test with some basic info
        generates a "good enough" pseudo_test_id for the test from util.utils.pseudo_uid
        :parameter cuid a CUID
        :parameter test_name a 255 varchar for friendly name
        :parameter mode one of the available modes [apache, smpp, psm == 0.5.x]
        :parameter volume of NuQ requests to send
        :parameter rate to send at [fast, medium, slow, idle] - see rate calculator
        :parameter url to send requests to. Will default to settings.py if not specified
        :parameter file to load msisdns to use as PSM scenario targets
        :parameter scenario use in PSM tests, will default to settings.py
        :return ID or 0 on fail
        :except MySQLError
        """
        pseudo = utils.pseudo_uid()
        cursor = self.db.cursor()
        query = 'INSERT INTO test (pseudo_test_id, cuid, test_name, ' \
                'mode, volume, rate, url, psm_file, psm_scenario, status) ' \
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        args = (pseudo, cuid, test_name, mode, volume, rate, url, file, scenario, 'saved')
        try:
            cursor.execute(query, args)
            self.db.commit()
            if cursor.lastrowid:
                logger.info('Test: {} CREATED')
                return cursor.lastrowid
            else:
                logger.error('Could not add test')
                return 0
        except MySQLError:
            logger.error('Could not create test entry')
            raise
        finally:
            cursor.close()

    def create_nuq_results(self, pseudo_id, throttle, actual_start, loop_start, loop_end, actual_end,
                           oks, kos, total, lap_count, psm_errors):
        """create a new entry for this test run
        """
        query = 'INSERT INTO nuq_results (pseudo_nuq_id, throttle, ' \
                'start, loop_start, loop_end, end, ' \
                'oks, kos, total, lap_count, psm_errors) ' \
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        args = (pseudo_id, throttle, actual_start, loop_start, loop_end, actual_end,
                oks, kos, total, lap_count, psm_errors)
        cursor = self.db.cursor()
        try:
            cursor.execute(query, args)
            self.db.commit()
            if not cursor.lastrowid:
                logger.error('Could not add test results')
                return 0
            else:
                logger.info('Test {} results added'.format(pseudo_id))
                return cursor.lastrowid
        except MySQLError:
            logger.error('Could not add test results')
            return 0
        finally:
            cursor.close()

    def insert_results(self, pseudo_test_id, laps, run_date):
        """insert internal nuq results
        :parameter pseudo_test_id to identify the test
        :parameter laps a list of laps containing lap time in microseconds and response status code
        :parameter run_date date that this test run was started
        """
        cursor = self.db.cursor()
        for lap in laps:
            t = lap[0]  # t = time: elapsed time in microseconds
            c = lap[1]  # c = code: status code returned for this lap
            cursor.execute("INSERT INTO test_results (pseudo_test_id, run_date, lap_time, status_code)"
                           "VALUES (%s, %s, %s, %s)", (pseudo_test_id, run_date, t, c))

        self.db.commit()
        cursor.close()

    def get_test(self, test_id=0):
        """returns a list of tests in dict form
        :parameter test_id the test id primary key, defaults to 0
        :return a list of 1 or more dictionary objects containing test key/value pairs. 0 = SELECT *
        :return None if no results match
        :except MySQLError
        """
        if test_id != 0:
            query = 'SELECT * FROM test WHERE id = %s' % test_id
        else:
            query = 'SELECT * FROM test ORDER by id DESC'
        cursor = self.db.cursor(DictCursor)
        try:
            results = cursor.execute(query=query)
            if results is None:
                logger.error('Could not get results using: {}'.format(query))
                return None
        except MySQLError:
            logger.error('Could not get tests using: {}'.format(query))
            raise
        return cursor.fetchall()

    def delete_test(self, test_id):
        """deletes the specified test
        :parameter test_id mandatory primary key id of test
        :return True
        :except MySQLError
        """
        query = 'DELETE FROM test WHERE id = %s' % test_id
        cursor = self.db.cursor()
        try:
            cursor.execute(query=query)
            logger.info('Deleted test id: {}'.format(test_id))
            return True
        except MySQLError:
            logger.error('Could not delete test using: {}'.format(query))
            raise
