"""
Module Description
"""
import subprocess
import re
import os
import logging
import json
from shutil import copyfile
from shutil import rmtree
from pathlib import Path
import plyj.parser as plyj
import plyj.model as model
from Utility.progress_bar import ProgressBar

#region CONSTS
TEST_FILES_LIST_PATH = r"C:\personal-git\Thesis\ThesisScripts\inputFiles.lst"
# TEST_FILES_LIST_PATH = r"C:\personal-git\apache\commons-math\target\maven-status\maven-compiler-plugin\testCompile\default-testCompile\inputFiles.lst"
PROJECT_ROOT_PATH = r"C:\personal-git\apache\commons-math"
TRACES_LOG_FILE_PATH = r"C:\personal-git\apache\commons-math\traces0.log"
DATA_PATH = r"C:\personal-git\Thesis\ThesisScripts\data"

MAX_SIZE_FOR_TRACE_FILE_IN_MB = 100

dostep1 = True
dostep2 = True
dostep3 = True
dostep4 = True
dostep5 = True

#endregion

#region Logger Setup
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s | %(levelname)s] - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
#endregion

class ExperimentInstance(object):
    def __init__(self, tinfo_lst):
        self.tinfo_lst = tinfo_lst

class TestInfo(object):
    def __init__(self, tfile_full_path, tfile_name, tmethod_name, tannotations_lst):
        self.tfile_full_path = tfile_full_path
        self.tfile_name = tfile_name
        self.tmethod_name = tmethod_name
        self.tannotations = tannotations_lst
        self.is_faulty = None

    def add_result_from_output(self, test_output_str_result):
        resultidx = test_output_str_result.rfind("Tests run: 1")
        result_dirty = test_output_str_result[resultidx:]
        result = result_dirty[:result_dirty.find('\n')]
        result_vector = re.findall('\\b\\d+\\b', result) #['19', '0', '0', '0']
        result_vector = list(map(int, result_vector))
        num_of_tests, failures, errors, skipped = result_vector
        if num_of_tests > 1:
            raise ValueError(f'expected only 1 test, received {num_of_tests} tests')
        self.is_faulty = (failures + errors > 0)
        if skipped > 0:
            raise ValueError(f"test was skipped")

class TestSuitInformation(object):
    def __init__(self, tfiles_list_path):
        self.tinfos = []
        with open(tfiles_list_path, "r") as tfiles_paths:
            for tfile_path in tfiles_paths:
                tfile_path = tfile_path.rstrip('\n')
                tfile_name = Path(tfile_path).stem
                tmethodnameTannotations = SimpleJavaTestFileParser.parse_and_return_methodnameTannotations(tfile_path)
                for (tmethod_name, annotations) in tmethodnameTannotations:
                    self.tinfos.append(TestInfo(tfile_path, tfile_name, tmethod_name, annotations))
    
    def filter_in_valid_tests(self):
        tinfos_filtered = []
        for tinfo in self.tinfos:
            isTest = 'Test' in tinfo.tannotations
            isDeprecated = 'Deprecated' in tinfo.tannotations
            isIgnore = 'Ignore' in tinfo.tannotations
            if isTest and not isDeprecated and not isIgnore:
                tinfos_filtered.append(tinfo)
        self.tinfos = tinfos_filtered
        
    def filter_out_big_trace_files(self, max_size_in_mb):
        deleted_count = 0
        for (idx, tinfo) in enumerate(self.tinfos):
            tmethod_dir_path = f"{DATA_PATH}\\{tinfo.tfile_name}\\{tinfo.tmethod_name}"
            traces_file_path = f"{tmethod_dir_path}\\test_method_traces.log"
            statinfo = os.stat(traces_file_path)
            size_b = statinfo.st_size
            size_mb = (size_b >> 20)
            logger.info(f"{traces_file_path} size: {size_mb} MB, max size allowed: {max_size_in_mb}")
            if size_mb > max_size_in_mb:
                deleted_count += 1
                logger.info(f"deleting {traces_file_path}. size: {size_mb} MB, max size allowed: {max_size_in_mb}")
                rmtree(tmethod_dir_path)
                del self.tinfos[idx]
        return deleted_count

class SimpleJavaTestFileParser(object):
    parser = plyj.Parser()

    @staticmethod
    def old_get_tmethods_lines(java_tfile_path):
        with open(java_tfile_path, 'r') as tfile:
            store_next_line = False
            tmethods_lines = []
            for idx, line in enumerate(tfile):
                if store_next_line:
                    tmethods_lines.append(line)
                    store_next_line = False
                    continue
                line = line.rstrip('\n').strip('\t').strip(' ')
                if line == '@Test':
                   store_next_line = True
        return tmethods_lines

    @staticmethod
    def old_parse(java_test_file_path):
        tmethods_lines = SimpleJavaTestFileParser.old_get_tmethods_lines(java_test_file_path)
        tmethod_names = []
        for line in tmethods_lines:
            line_split = line.rstrip('\n').strip('\t').strip(' ').split(' ')
            if line_split[0] != 'public':
                #is not a valid case (e.g. @ignore)
                continue
            methodname_w_brackets = list(filter(lambda w: '(' in w, line_split))[0]
            methodname = methodname_w_brackets[:-2]
            tmethod_names.append(methodname)
        return tmethod_names

    @classmethod
    def parse_and_return_methodnameTannotations(cls, java_test_file_path):
        with open(java_test_file_path, 'r') as tfile:
            tree = cls.parser.parse_file(tfile)
            for type_decl in tree.type_declarations:
                methodnameTannotations = [] #(method_name, ['Test', 'Deprecated'])
                for method_decl in [decl for decl in type_decl.body if type(decl) is model.MethodDeclaration]:
                    annotations = []
                    for modifier in method_decl.modifiers:
                        if type(modifier) is model.Annotation:
                            annotations.append(modifier.name.value)
                    methodnameTannotations.append((method_decl.name, annotations))
        return methodnameTannotations

def run_test_mock_fail():
    output = """
            [INFO] Scanning for projects...
            [INFO] 
            [INFO] ------------------------------------------------------------------------
            [INFO] Building Apache Commons Math 4.0-SNAPSHOT
            [INFO] ------------------------------------------------------------------------
            [INFO] 
            [INFO] --- maven-surefire-plugin:2.19.1:test (default-cli) @ commons-math4 ---

            -------------------------------------------------------
            T E S T S
            -------------------------------------------------------
            Running org.apache.commons.math4.analysis.differentiation.GradientFunctionTest
            Tests run: 1, Failures: 0, Errors: 1, Skipped: 0, Time elapsed: 1.304 sec <<< FAILURE! - in org.apache.commons.math4.analysis.differentiation.GradientFunctionTest
            test2DDistance(org.apache.commons.math4.analysis.differentiation.GradientFunctionTest)  Time elapsed: 1.266 sec  <<< ERROR!
            java.lang.NullPointerException
                at org.apache.commons.math4.analysis.differentiation.GradientFunctionTest.test2DDistance(GradientFunctionTest.java:39)


            Results :

            Tests in error: 
            GradientFunctionTest.test2DDistance:39 ╗ NullPointer

            Tests run: 1, Failures: 0, Errors: 1, Skipped: 0

            [INFO] ------------------------------------------------------------------------
            [INFO] BUILD FAILURE
            [INFO] ------------------------------------------------------------------------
            [INFO] Total time: 4.006 s
            [INFO] Finished at: 2017-12-12T20:24:30+02:00
            [INFO] Final Memory: 12M/243M
            [INFO] ------------------------------------------------------------------------
            [ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:2.19.1:test (default-cli) on project commons-math4: There are test failures.
            [ERROR] 
            [ERROR] Please refer to C:\personal-git\apache\commons-math\target\surefire-reports for the individual test results.
            [ERROR] -> [Help 1]
            [ERROR] 
            [ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
            [ERROR] Re-run Maven using the -X switch to enable full debug logging.
            [ERROR] 
            [ERROR] For more information about the errors and possible solutions, please read the following articles:
            [ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
            """
    return output

def run_test_mock_success():
    output = """
            [INFO] Scanning for projects...
            [INFO] 
            [INFO] ------------------------------------------------------------------------
            [INFO] Building Apache Commons Math 4.0-SNAPSHOT
            [INFO] ------------------------------------------------------------------------
            [INFO] 
            [INFO] --- maven-surefire-plugin:2.19.1:test (default-cli) @ commons-math4 ---

            -------------------------------------------------------
            T E S T S
            -------------------------------------------------------
            Running org.apache.commons.math4.analysis.FunctionUtilsTest
            Tests run: 19, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.266 sec - in org.apache.commons.math4.analysis.FunctionUtilsTest

            Results :

            Tests run: 19, Failures: 0, Errors: 0, Skipped: 0

            [INFO] ------------------------------------------------------------------------
            """
    return output

def run_test(test_class_name, test_method_name):
    '''
    Example:
    test_class_name = FunctionUtilsTest
    test_method_name = testCompose
    '''
    command = f"mvn surefire:test -Dtest={test_class_name}#{test_method_name}"
    command = command.split(' ')
    logger.debug(f"handling {test_class_name}, {test_method_name}")
    output = subprocess.run(command, stdout=subprocess.PIPE, shell=True, cwd=PROJECT_ROOT_PATH)
    surefire_output = output.stdout.decode(encoding='utf-8', errors='ignore')
    return surefire_output
    
def route_traces_to_test_folder(tfile_name, tmethod_name):
    test_dir = f"{DATA_PATH}\\{tfile_name}\\{tmethod_name}"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    copyfile(src=TRACES_LOG_FILE_PATH, dst=f"{test_dir}\\test_method_traces.log")
    os.remove(TRACES_LOG_FILE_PATH)

def get_methodset_for_tmethod_traces(tmethod_dir_path):    
    methodset = set()
    with open(f"{tmethod_dir_path}\\test_method_traces.log", 'r') as tmethod_file:
        for trace in tmethod_file:
            methodset.add(trace.split(',')[0])
    return methodset

def create_tmethod_info_files(tsuit_info):
    for tinfo in tsuit_info.tinfos:
            tmethod_dir_path = f"{DATA_PATH}\\{tinfo.tfile_name}\\{tinfo.tmethod_name}"
            methodset = get_methodset_for_tmethod_traces(tmethod_dir_path)
            with open(f"{tmethod_dir_path}\\tmethod_info.log", 'w') as tmethod_info_file:
                info = dict()
                info["methodset"] = []
                for method in methodset:
                    info["methodset"].append(method)
                info["isFaulty"] = tinfo.is_faulty
                tmethod_info_file.write(json.dumps(info))

logger.info("\n\nstart\n=================================================================================\n")

## Step 1
step1_desc = "step 1: analyzing test-suit"
if dostep1:
    logger.info(f"\n\n{step1_desc}\n=================================================================================\n")
    logger.info("populating test-suit-information")
    #populate test suit (get all test methods inside every test file)
    tsuit_info = TestSuitInformation(TEST_FILES_LIST_PATH)
    logger.info(f"found total of {len(tsuit_info.tinfos)} methods in test suit")
    logger.info("filtering in only valid tests (e.g. only @Tests without @Deprecated or @Ignore)")
    tsuit_info.filter_in_valid_tests()
    logger.info(f"total of {len(tsuit_info.tinfos)} valid test methods")
else:
    logger.info(f"\n\nskipping {step1_desc}")

## Step 2
step2_desc = "step 2: invoking individual tests with tracer"
if dostep2:
    logger.info(f"\n\n{step2_desc}\n=================================================================================\n")
    #run each test to get results
    pbar = ProgressBar(len(tsuit_info.tinfos))
    pbar.show_current()
    for tinfo in tsuit_info.tinfos:
        output = run_test(tinfo.tfile_name, tinfo.tmethod_name)
        tinfo.add_result_from_output(output)
        route_traces_to_test_folder(tinfo.tfile_name, tinfo.tmethod_name)
        pbar.advance(f"({tinfo.tfile_name}, {tinfo.tmethod_name})")
    logger.info(f'each test class and test method tracer were stored at: "{DATA_PATH}"')
else:
    logger.info(f"\nskipping {step2_desc}")

## Step 3
step3_desc = f"step 3: deleting tmethods with traces bigger than {MAX_SIZE_FOR_TRACE_FILE_IN_MB} MB"
if dostep3:
    logger.info(f"\n\n{step3_desc}\n=================================================================================\n")
    deleted_count = tsuit_info.filter_out_big_trace_files(MAX_SIZE_FOR_TRACE_FILE_IN_MB)
    logger.info(f'{deleted_count} tmethods were deleted due to their size')
else:
    logger.info(f"\nskipping {step3_desc}")

## Step 4
step4_desc = "step 4: building tmethod info file for every test method"
if dostep4:
    logger.info(f"\n\n{step4_desc}\n=================================================================================\n")
    logger.info('listing all methods participated in a test')
    create_tmethod_info_files(tsuit_info)
    logger.info(f'tmethod info file were stored at "{DATA_PATH}\\<test_class>\\<test_method>\\methodset.log"')
else:
    logger.info(f"\nskipping {step4_desc}")

## Step 5
step5_desc = "step 5: building experiment instances"
if dostep5:
    logger.info(f"\n\n{step5_desc}\n=================================================================================\n")

else:
    logger.info(f"\nskipping {step5_desc}")

# output = run_test_mock()
# testResult = SurefireSingleTestResults(output)
