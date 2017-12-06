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

methods = ['org.apache.commons.rng.core.source64.MersenneTwister64.next()',
               'org.apache.commons.math4.stat.descriptive.rank.Max.increment(double)',
               'org.apache.commons.math4.analysis.differentiation.DerivativeStructure.getPartialDerivative(int[])',
               'org.apache.commons.math4.ode.sampling.AbstractStepInterpolator.getGlobalCurrentTime()',
               'org.apache.commons.math4.dfp.Dfp.toString()']

methodsToFile = dict()
for m in methods:
    methodsToFile[m] = open(m+".log", "a")

# iterating zip files with traces text files
def traceToFuncName(trace):
    return trace.split(',', 1)[0]

def isSpecificMethod(trace):
    return traceToFuncName(trace) in methodsToFile

def writeToFile(trace):
    methodName = traceToFuncName(trace)
    methodsToFile[methodName].write(trace)

logger.info("start")
files = glob.glob("*.txt")
nfiles = len(files)
logger.info("found %s files", nfiles)
for idx, txtfilename in enumerate(files):
    logger.info('accessing txt file %s: %s / %s', txtfilename, idx+1, nfiles)
    with open(txtfilename, "r") as f:
        for trace in filter(isSpecificMethod, f):
            writeToFile(trace)

logging.info("closing files")
for m in methods:
    logging.info("closing file %s", m)
    methodsToFile[m] = open(m, "a")
logging.info("done")