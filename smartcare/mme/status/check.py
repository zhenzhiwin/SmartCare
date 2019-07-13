#! coding: utf8
import os
import re

from .checkers import test_task
from .configer import LOGFILE_PATH, test_logdir

def get_filenames_with_pattern(path, pattern=".*"):
    """return the full pathname of the files which match the 'pattern' in the 'path' 
    """
    _files = [fname for fname in os.listdir(path) if re.match(pattern,fname)]
    
    return [os.path.join(path,fname) for fname in _files]

def check_logfiles(logdir):
    logfiles=get_filenames_with_pattern(logdir, "\S+\.stats")
    
    for logfile in logfiles:
        test_task(logfile)

    
if __name__ == "__main__":
    if test_logdir:
        check_logfiles(test_logdir)
    else:
        check_logfiles(LOGFILE_PATH)