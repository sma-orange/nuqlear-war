"""NuQ Configuration File"""
import os
cwd = os.getcwd()

"""    SMPP Settings    """
# SMPP BASE URL DEFAULT
SMPP_URL = 'http://localhost:88'
# TODO: test this compo
COMPO = '/inject_mo?short_message=src&source_addr=4477665544&destination_addr=07980868013&' \
           'submit=Submit+Message&service_type=&source_addr_ton=1&source_addr_npi=1&dest_addr_ton=1' \
           '&dest_addr_npi=1&esm_class=0&protocol_ID=&priority_flag=&registered_delivery_flag=0&data_coding=0' \
           '&user_message_reference=&source_port=&destination_port=&sar_msg_ref_num=&sar_total_segments=' \
           '&sar_segment_seqnum=&user_response_code=&privacy_indicator=&payload_type=&message_payload=' \
           '&callback_num=&source_subaddress=&dest_subaddress=&language_indicator=&tlv1_tag=&tlv1_len=' \
           '&tlv1_val=&tlv2_tag=&tlv2_len=&tlv2_val=&tlv3_tag=&tlv3_len=&tlv3_val=&tlv4_tag=&tlv4_len=' \
           '&tlv4_val=&tlv5_tag=&tlv5_len=&tlv5_val=&tlv6_tag=&tlv6_len=&tlv6_val=&tlv7_tag=&tlv7_len=&tlv7_val='

# APACHE URL for benchmarking NuQ RATES
BENCHMARK_URL = 'http://localhost'

"""    Logs and files for parser    """
# HTTP HEAD Benchmark
# TODO: fix keys
# TODO: rework the whole file parsing->logs->db etc...IMPORTANT
OUT_FILE_DIRS = '/home/ben/PycharmProjects/nuqlear_war/storage/nuq_output_files/'
OUT_FILESTAMP = '%Y%m%d%H%M%S'

BENCHMARK_LOG = cwd + '/storage/logs/bench/<pseudo_key>.log'
BENCHMARK_LAP_FILE = cwd + '/storage/logs/bench/<pseudo_key>.csv'
BENCHMARK_NUQ_FILE = cwd + '/storage/logs/bench/<pseudo_key>_nuq.txt'

# NUQ
NUQ_FILE = cwd + '/storage/logs/nuq/nuq.log'
NUQ_NUQ_FILE = cwd + '/storage/logs/nuq/nuq_nuq.txt'
NUQ_LAP_FILE = cwd + '/storage/logs/nuq/nuq_lap.csv'
NUQ_QUE_FILE = cwd + '/storage/logs/nuq/nuq_queue_parse.txt'
NUQ_PRF_FILE = cwd + '/storage/logs/nuq/nuq_nuqing.csv'

# PSM
PSM_FILE = cwd + '/storage/logs/psm/psm_nuq.txt'
PSM_NUQ_FILE = cwd + '/storage/logs/psm/psm_nuq.txt'
PSM_LAP_FILE = cwd + '/storage/logs/psm/psm_lap.csv'
PSM_ERR_FILE = cwd + '/storage/logs/psm/errors.txt'

# SMPP
SMPP_LOG = cwd + '/storage/logs/smpp/smppsim0.log'
SMPP_CONFIG_OUT = cwd + '/storage/logs/smpp/smpp_config.json'
SMPP_MO_LINES = cwd + '/storage/logs/smpp/mo_parse.txt'
SMPP_LAP_FILE = cwd + '/storage/logs/smpp/mo_per_sec.csv'
SMPP_TIMESTAMP_FORMAT = '%Y.%m.%d %H:%M:%S %f'


"""NuQ "Carburettor" Parameters"""
CONCURRENT = 20
THREADS = 100
DEFAULT_VOLUME = 1000
DEFAULT_THROTTLE = 0
DEFAULT_MESSAGE = 'NuQ'
BAIL_LIMIT = 100

# HEAD -->
# MT01: 0.0 = 250-270ish
# MT01: 0.1 = 200-210ish
# MT01: 0.2 = 140-160ish
# MT01: 0.5 = 40ish
# POST -->
# MT01: 0.0 = 60ish
# MT01: 0.1 = 45ish
# MT01: 0.2 = 30ish
# MT01: 0.5 = 20ish
# TODO: fix this into a proper dictionary/numpy
RATES = ['fast', 'medium', 'slow', 'idle']
THROTTLES = [0, 0.1, 0.2, 0.5]
MODES = ['apache', 'smpp', 'psm']

# millisecond accurate stamps : HOUR-MINUTE_second.milliseconds.
TIMESTAMP = '%H:%M:%S.%f'

# used to strip numbers from text
NUMBERS = set('0123456789')

""" NuQ DB Stuff """
DB_TS_FORMAT = '%Y-%m-%d %H:%M:%S'
SQL_URL = 'mysql://localhost:3306/nuq'
MYSQL_DB = 'nuq'
MYSQL_USER = 'nuq'
MYSQL_PASS = 'dstk2012'

"""    PSM Settings    """
# credentials
PSM_USER = 'dstkTest'
PSM_PASS = '28112016'
# parameters used in post request
PSM_SVP = 900
SMS_VP = 60  # validity period
PSM_CHANNEL = 25  # aka Driver/ID
# use callbacks?
PSM_NOTIFICATION = True
# must provide a URL if notification is True
PSM_CALLBACK_URL = 'http://dstk-nuq.itn.ftgroup'
# used for psm callback server
HOST_NAME = 'http://dstk-nuq.itn.ftgroup'
PORT_NUMBER = 8080
# Push Service Manager Servlet URL
PSM_URL = 'http://10.117.160.252:8180/pm_webservices/PushManagerServlet'
# default file full of MSISDN targets
# TODO: fix path
DEFAULT_MSISDN_FILE = cwd + '/storage/inputs/msisdns/default_msisdns.txt'

# Scenario to be used
# PSM_SCENARIO = '20161129_NuQ'
# PSM_SCENARIO = 'NuQ2SMS'
PSM_SCENARIO = 'NuQ3SMS'

# Basic XML request template snarfed from wiki  - note you'll need to modify the "format" in NuQ post function
XML = '''
<request>
<request-name>SendUnitaryRequest</request-name>
<params>
<username>{0}</username>
<password>{1}</password>
<scenario-name>{2}</scenario-name>
<msisdn>{3}</msisdn>
<smsc-channel-driver-id>{4}</smsc-channel-driver-id>
<service-validity-period>{5}</service-validity-period>
<is-notification-required>{6}</is-notification-required>
<notification-URL>{7}</notification-URL>
<api-version>4.0</api-version>
</params>
</request>
'''

# More complex XML example snarfed from jTool PHP - note you'll need to modify the "format" in NuQ post function
BIG_XML = '''
'<request>
  <request-name>SendUnitaryRequest</request-name>
  <params>
    <username>"{0}"</username>
    <password>"{1}"</password>
    <scenario-xml>
    <global-scenario version="2.0">
    <created-from>gui</created-from>
    <mode>normal</mode>
    <comments></comments>
    <status-tag>Under design</status-tag>
    <branched>false</branched>
    <compatible-mode>false</compatible-mode>
    <personalized>false</personalized>
    <content>
        <generic-scenario-xml>
            <display-text id="1">
                <text>"{2}"</text>
            </display-text>
        </generic-scenario-xml>
    </content>
    </global-scenario>
    </scenario-xml>
    <msisdn>"{3}"</msisdn>
    <transaction-id>PUSH_MESSAGE_1</transaction-id>
    <service-validity-period>"{4}"</service-validity-period>
    <sms-validity-period>"{5}"</sms-validity-period>
    <smsc-channel-driver-id>"{6}"</smsc-channel-driver-id>
    <is-notification-required>"{7}"</is-notification-required>
    <notification-URL>{8}</notification-URL>
    <variable-order>first-name;hobby</variable-order>
    <personalized-data>John;football</personalized-data>
    <external-transaction-id>EXTID1</external-transaction-id>
    <request-priority>high</request-priority>
    <api-version>4.0</api-version>
  </params>
</request>'
'''
