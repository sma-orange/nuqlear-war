import subprocess
import logging

logger = logging.getLogger(__name__)


def background(test_id):
    """run nuq in a separate process in the background
    :parameter test_id ID of the test to load
    :return True if "runner.sh" starts successfully or False if it fails
    """
    nuq_command = "./../util/runner.sh {0}".format(test_id)
    try:
        subprocess.run(nuq_command, shell=True)
        return True
    except subprocess.CalledProcessError as error:
        logger.error(error)
        return False


def status():
    """find all processes relating to nuq
    :return True or False and an array of output from std.out or std.err
    """
    status_command = "ps -ef | grep nuq.py"
    completed = subprocess.CompletedProcess
    messages = []
    try:
        completed = subprocess.run(status_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        messages.append('Have {0} bytes in stdout'.format(len(completed.stdout)))
        messages.append(completed.stdout.decode('utf-8'))
        return True, messages
    except subprocess.CalledProcessError as error:
        logger.error(error)
        messages.append('Have {0} bytes in stderr'.format(len(completed.stdout)))
        messages.append(completed.stderr.decode('utf-8'))
        return False, messages
