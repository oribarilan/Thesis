import rarfile
import logging
import sys
import collections
import pickle
import glob

log_format = '[%(asctime)s]|| [%(levelname)s]: %(message)s'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_console_channel = logging.StreamHandler(sys.stdout)
log_console_channel.setLevel(logging.DEBUG)
logger.addHandler(log_console_channel)

#iterating zip files with traces text files
def traceToFuncName(trace):
    return trace.split(',',1)[0]

counter = collections.Counter()
logger.info("start")
for txtfilename in glob.glob("*.txt"):
    logger.info('accessing txt file: %s', txtfilename)
    with open(txtfilename, "r") as f:
        counter.update(map(traceToFuncName, f))

logging.info("done updating counter")
logging.info("pickeling counter")
with open('counter.pkl', 'wb') as picklef:
    pickle.dump(counter, picklef)
logging.info("done pickeling counter")
logging.info("most comming 5 methods:")
logging.info(counter.most_common(5))