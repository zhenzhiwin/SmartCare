#! coding: utf8
import os

BASE_PATH = os.path.split(os.path.abspath(__file__))[0]

##log文件保存路径
LOGFILE_PATH = "/tmp/cache/"
LOGFILE_PATH = "D:/git/SmartCare/log"  #window开发测试目录

#静态html报告保存路径
#HTML_REPORT_PATH = "/opt/smartcare/reports"
HTML_REPORT_PATH = "D:/git/SmartCare/reports"

checking_rules = {
    'cpuload' : [25, 80, 90],
    }


mme_list = [
    "HZMME48BNK",
    "HZMME49BNK",
    "HZMME50BNK",
    "HZMME51BNK",
    "HZMME52BNK",
    "HZMME53BNK",
]