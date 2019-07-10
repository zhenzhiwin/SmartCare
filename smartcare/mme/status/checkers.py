#! coding: utf8
import os
import json
import logging
from libs.basechecker.checkitem import BaseCheckItem, ResultInfo
from libs.basechecker.checkitem import exec_task


class FlexinsUnitStatus(BaseCheckItem):
    """MME单元状态检查
    检查mme所有单元的状态，统计出WO-EX和SP-EX的单元数量，以及异常单元的数量
    """
  
    check_cmd = "ZUSI"
    base_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_template_name = "flexins_usi.fsm"

    def check_status(self, logbuf=None):
        self.status_data = self.fsm_parser.parse(logbuf=logbuf)
        
        hostname = self.status_data[0]['host']
        self.info['hostname'] = hostname
        results = ResultInfo(**self.info)
        stats = {'WO-EX': 0, 'SP-EX':0, 'Other': 0}
        for s in self.status_data:
            if s['unit'] and s['status'] not in ['WO-EX','SP-EX']:
                results.status = 'Failed'
                stats['Other'] +=1
            elif s['status']:
                stats[s['status']] +=1
        
        results.status = "Passed"
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


def print_task_result(result, detail=False):
    if not detail:
        result.__dict__.pop('data')

    print(result.to_json(indent=2))

def test_task(logfile):
    task = {}
    task['checkitems']=[FlexinsUnitStatus]
    task['logfile'] = logfile

    results = exec_task(task)

    for r in results:
        print(r.name)
        print_task_result(r)

def test_checkitem(logfile):
    item = FlexinsUnitStatus()
    result = exec_checkitem(item,logfile)

    for d in item.status_data:
        print(d['host'],d['unit'],d['status'])
    print("len of data:%s" % len(item.status_data))
    
    print(result.to_json(2))
    print(result.description)

if __name__ == "__main__":
    logfile = "R:\cache\HZMME48BNK.stats"
    test_task(logfile)