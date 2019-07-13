#! coding: utf8
import os
import time
import json
import logging
import codecs
from jinja2 import Environment, FileSystemLoader

from .configer import BASE_PATH, HTML_REPORT_PATH


def save_report(hostname, html):
    filename = "mme_report_%s.html" % hostname
    output_file = os.path.join(HTML_REPORT_PATH, filename)
    with open(output_file,'w', encoding='utf8') as fp:
        fp.write(html)

def make_report(data, template_name, env):
    tmpl = env.get_template(template_name)
    html = tmpl.render(**data)

    return html

if __name__ == "__main__":
    from .checkers import test_task
    from .configer import test_logfile

    template_dir = os.path.join(BASE_PATH, 'html_templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    
    if test_logfile:
        data = test_task(test_logfile)
    else:
        print("no logfile specified.")
        exit(1)

    print("len of data: %s" % len(data))

    #get the first task's reuslt and make a report for it.
    result = data[0]
    print(result)
    data = result.__dict__
    html = make_report(data, 'mme_report.html',env)

    if len(html)>0:
        saved_filename=save_report(result.hostname, html)
        print("report was saved to %s" % saved_filename)

