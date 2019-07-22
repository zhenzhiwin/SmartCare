#! coding: utf8
import os
import time
import json
import logging
from jinja2 import Environment, FileSystemLoader

from .configer import Config as conf


def save_report(hostname, html):
    filename = conf.report_output_filename_pattern.format(hostname)
    output_file = os.path.join(conf.report_output_path, filename)
    with open(output_file,'w+', encoding='utf8') as fp:
        fp.write(html)

    return output_file

def make_report(env, template_name, **kwargs):
    tmpl = env.get_template(template_name)
    html = tmpl.render(**kwargs)

    return html

def add_status_for_reporting(data):
    """根据检查结果着增加一些用于显示的状态或数据
    """
    for r in data:
        if r.status.lower() == "passed":       #如果检查通过，则
            r.panel_status = "panel-success"   #图标为panel-success样式
            r.status_icon = "fa-check-circle"  #检查名称后的图标为已完成
            r.status_color = 'green'           #图标状态为绿色
        else:
            r.panel_status = "panel-warning"
            r.status_icon = "fa-exclamation-circle"
            r.status_color = 'red'
    
    return data

if __name__ == "__main__":
    import sys
    from .checkers import Task

    template_dir = os.path.join(conf.module_path, conf.report_template_path)
    env = Environment(loader=FileSystemLoader(template_dir))


    for host in conf.mme_list:
        task = Task(hostname=host)
        task.logfile_dir = conf.logfile_path
        task.load_checkitems(conf.task_checklist)
        task.execute()
        task.results = add_status_for_reporting(task.results)
        
        html = make_report(env, conf.report_template_name, task=task, hostlist=conf.mme_list) 
        report_name = conf.report_output_filename_pattern.format(host)

        if len(html)>0:
            saved_filename=save_report(task.hostname, html)
            print("report was saved to %s" % saved_filename)

