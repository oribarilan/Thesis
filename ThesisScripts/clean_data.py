import os
from shutil import rmtree

TRACES_LOG_FILE_PATH = r"C:\personal-git\apache\commons-math\traces0.log"
DATA_FOLDER_PATH = r"C:\personal-git\Thesis\ThesisScripts\data"
BUGDB_PATH = r"C:\personal-git\Thesis\ThesisScripts\bugdbs"
if os.path.exists(TRACES_LOG_FILE_PATH):
    print(f'cleaning TRACES_LOG_FILE_PATH: "{TRACES_LOG_FILE_PATH}"')
    os.remove(TRACES_LOG_FILE_PATH)

if os.path.exists(DATA_FOLDER_PATH):
    print(f'cleaning DATA_FOLDER_PATH: "{DATA_FOLDER_PATH}"')
    rmtree(DATA_FOLDER_PATH)

if os.path.exists(BUGDB_PATH):
    print(f'cleaning BUGDB_PATH: "{BUGDB_PATH}"')
    for f in os.listdir(BUGDB_PATH):
        file_path = os.path.join(BUGDB_PATH, f)
        os.remove(file_path)