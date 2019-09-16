#! coding: utf8
import os

#本模块所在路径
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


##待分析的log文件保存路径
#LOGFILE_PATH = "/tmp/cache/"  #实际服务器上使用的目录
LOGFILE_PATH = "D:/git/SmartCare/log"  #window开发测试使用目录

#生成报告的保存路径
#REPORT_PATH = "/opt/smartcare/reports"
REPORT_PATH = "D:/git/SmartCare/reports"

checking_rules = {
    'cpuload' : [25, 80, 90],
    }

## MME
mme_list = [
    "HZMME45BNK",
    "HZMME46BNK",
    "HZMME47BNK",
    "HZMME48BNK",
    "HZMME49BNK",
    "HZMME50BNK",
    "HZMME51BNK",
    "HZMME52BNK",
    "HZMME53BNK",
    "HZMME54BNK",
    "HZMME55BNK",
    "HZMME56BNK",
    "HZMME57BNK",
    "HZMME72BNK",
    "HZMME73BNK",
    "HZMME89BNK",
]

##Config包含以上配置，主要目的是方便其他模块导入。
class Config:
    module_path = BASE_PATH
    logfile_path = LOGFILE_PATH
    logfile_pattern = "{hostname}.stats"
    
    report_template_name = "mme_report.html"
    report_template_path = "html_templates"
    report_output_path = REPORT_PATH
    report_output_filename_pattern = "mme_report_{}.html"
    mme_list = mme_list

    task_checklist = ['FlexinsUnitStatus', 'FlexinsCpuloadStatus']

if __name__ == "__main__":
    print(BASE_PATH)    