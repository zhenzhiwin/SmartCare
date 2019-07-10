#! coding: utf8
import os
import re
import time
import logging
from textfsm import TextFSM
from .configer import alarm_files_path, data_cmds, 

FSM_TEMPLATE = "{netype}_{cmd}.fsm"

def str2second(timestr, fmt='%Y-%m-%d %H:%M:%S'):
    """translate the datetime string to a epoch seconds"""
    return int(time.mktime(time.strptime(timestr,fmt)))


class FsmParser(object):
    """A log parser using the FSM template.
    """
    def __init__(self, fsm_file=None):
        self.fsm = None
        if fsm_file:
            self.load_template(fsm_file)
    
        
    def load_template(self, fsm_file):
        """load FSM template and generate a textfsm parser.
        """
        with open(fsm_file) as fp:
            self.fsm = TextFSM(fp)

        return self.fsm
    
    def parse(self, logfile):
        """Return a list of dict of row.
        """
        with open(logfile) as fp:
            logtext = fp.read()
        
        self.fsm.Reset()
        rows = self.fsm.ParseText(logtext)
        return [dict(zip(self.fsm.header,row)) for row in rows]


class FlexiNSAlarm:
    """Class for handling an Alarm of FlexiNS/MME
    """
    data_fields = ['host','unit','date','time','level','id','text']
    
    def __init__(self, data=None):
        if data:
            if isinstance(data,list):
                data = [d.strip() for d in data]
                self.__dict__.update(dict(zip(self.data_fields,data)))
            elif isinstance(data, dict):
                self.__dict__.update(data)
                
        self.timestamp = str2second(" ".join((self.date,self.time)))
        self.id = int(self.id)
        self.text = self.text.strip()
        
    def info(self, fmt="{timestamp},{date}#{time} {host},{id},{text}"):
        return fmt.format(**self.__dict__)

        
    def __repr__(self):
        return "FlexiNSAlarm<{host},{id}>".format(**self.__dict__)

def get_filenames_with_pattern(path, pattern=".*"):
    """get the files which match the 'pattern' in the 'path' 
    """
    _files = [fname for fname in os.listdir(path) if re.match(pattern,fname)]
    
    return [os.path.join(path,fname) for fname in _files]

def parse_alarms(logfile, parser):
    """parse a single logfile and return a list of FlexiNSAlarm objects
    """
    alarm_data = parser.parse(logfile)
    
    alarms = [FlexiNSAlarm(alm) for alm in alarm_data]
    alarms.sort(key = lambda alm:alm.timestamp, reverse=True)

    return alarms

def parse_alarmfiles(files, parser):
    """parse the alarm files and return all the FlexiNSAlarm
    """
    almlist = []
    for filename in files:
        alarms = parse_alarms(filename, parser)
        almlist.extend(alarms)   
    
    return almlist
    
class AlarmList(object):
    """A class store the all alarms and provide some filter or statstics functions.
    
    almlist = AlarmList(all_alarms)
    
    # select all alarm match "host=='mme01'"
    almlist.select(host='mme01')
    
    # return a dict which group the alarm by 'text'
    almlist.summary(field='text')
    
    """
    def __init__(self, alarmlist=None):
        if alarmlist:
            self._alarmlist = sorted(alarmlist, key=lambda alm:alm.timestamp, reverse=True)
        else:
            self._alarmlist = []
    
    
    def select(self, **kwargs):
        alarms = self._alarmlist
        for key,value in kwargs.items():
            filter_func = lambda alm: getattr(alm,key)==value
            alarms = list(filter(filter_func, alarms))
            
        return alarms
    
    def summary(self,field='id'):
        results = {}
        for alm in self._alarmlist:
            value = getattr(alm,field)
            if  value not in results:
                results[value] = [alm]
            else:
                results[value].append(alm)
        
        return results
        
    def __iter__(self):
        return iter(self._alarmlist)


def get_alarm_list():  
    """parse the alarm files and get all the alarms in a `AlarmList` object. 
    Normally, user or other module should use this function to get all alarms.
    
    Note: before run this function, make sure the alarm files exisit in the right place.
    
    """
 
    script_path = os.path.split(os.path.abspath(__file__))[0]
    fsm_name = FSM_TEMPLATE.format(netype='flexins',cmd='aho')
    fsm_filename=os.path.join(script_path,fsm_name)

    parser = FsmParser(fsm_filename)
    alarmfiles = get_filenames_with_pattern(alarm_files_path, "\S+\.alarms")

    all_alarms = parse_alarmfiles(alarmfiles, parser)

    return AlarmList(all_alarms)