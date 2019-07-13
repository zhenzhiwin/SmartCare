#! coding: utf8
import os
import json
import logging
from libs.basechecker.checkitem import BaseCheckItem, ResultInfo
from libs.basechecker.checkitem import exec_task

from .configer import BASE_PATH
from .configer import checking_rules

class FlexinsUnitStatus(BaseCheckItem):
    """MME单元状态检查
    检查mme所有单元的状态，统计出WO-EX和SP-EX的单元数量，以及异常单元的数量
    """
  
    check_cmd = "ZUSI"
    base_path = BASE_PATH
    fsm_template_name = "flexins_usi.fsm"

    def check_status(self, logbuf=None):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        
        hostname = self.status_data[0]['host']
        self.info['hostname'] = hostname
        results = ResultInfo(**self.info)
        unit_status = []
        stats = {'WO-EX': 0, 'SP-EX':0, 'Other': 0}
        for s in self.status_data:
            if s['unit'] and s['status'] not in ['WO-EX','SP-EX']:
                unit_status.append(False)
            elif s['status']:
                stats[s['status']] +=1
        
        results.status = all(unit_status) and "Passed" or "Failed"
        results.stats = stats
        results.data = self.status_data
        return results

class FlexinsCpuloadStatus(BaseCheckItem):
    """MME单元CPU负荷检查
    检查mme所有单元的CPU负荷，输出单元的负荷信息。如果有单元负荷大于80%，则输出Failed。
    data={'cpuload': {'mmdu-0': 10,'mmdu-1': 2}}
    """
    check_cmd = "ZDOI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_doi.fsm"

    def check_status(self, logbuf):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)

        hostname = self.status_data[0]['host']
        results = ResultInfo(**self.info)
        overload_units = []
        for s in self.status_data:
            if int(s['cpuload']) > checking_rules['cpuload'][0]:
                results.status = 'Failed'
                overload_units.append(s['unit'])
        
        results.status = (len(overload_units)==0) and "Passed" or "Failed"
        results.stats = overload_units
        results.data = self.status_data

        return results

def print_task_result(result, detail=False):
    if not detail:
        result.__dict__.pop('data')

    print(result.to_json(indent=2))

def run_task(logfile):
    task = {}
    task['checkitems'] = [FlexinsUnitStatus, FlexinsCpuloadStatus]
    task['logfile'] = logfile

    results = exec_task(task)

    return results

def test_task(logfile):
    results = run_task(logfile)

    for r in results:
        print(r.name)
        print_task_result(r)

    return results
    
def test_checkitem(logfile):
    item = FlexinsUnitStatus()
    result = exec_checkitem(item,logfile)

    for d in item.status_data:
        print(d['host'],d['unit'],d['status'])
    print("len of data:%s" % len(item.status_data))
    
    print(result.to_json(2))
    print(result.description)

if __name__ == "__main__":
    from .configer import test_logfile

    if test_logfile: #如果configer文件里配置了test_logfile, 则仅分析指定的一个log文件
        test_task(test_logfile)
    else:
        run_tasks(BASE_PATH) #对BASE_PATH目录下的所有log文件进行分析。