import os
from agent.tools import get_ci_logs_from_file

def test_get_ci_logs_from_file():
    source = "data set text"
    tmp_file = "tmp.log"
    try:
        with open(tmp_file, 'w+') as f:
            f.write(source)
    except IOError as e:
        print(e)
    
    result = get_ci_logs_from_file(tmp_file)

    assert result == source
    try:
        os.remove(tmp_file)
    except IOError as e:
        print(e)
        
def test_get_ci_logs_from_missing_file():
    non_exist_file_path = "non_exist_file.log"
    result = get_ci_logs_from_file(non_exist_file_path)
    assert result == "File not found"
    