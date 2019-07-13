#! coding: utf8
import os

BASE_PATH = os.path.split(os.path.abspath(__file__))[0]

##log文件保存路径
LOGFILE_PATH = "/tmp/cache/"
#静态html报告保存路径
HTML_REPORT_PATH = "D:/git/SmartCare/html"

checking_rules = {
    'cpuload' : [25, 80, 90],
    }

test_logfile = "D:/git/SmartCare/log/HZMME48BNK.stats"
test_logdir = "D:/git/SmartCare/log"