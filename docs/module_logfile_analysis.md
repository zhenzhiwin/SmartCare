#log分析检查模块

- checkers.py

log分析提取模块主要功能在这个文件里。里面定义了两个检查项：FlexinsUnitStatus和FlexinsCpuloadStatus，这两个检查项组合成一个检查task。

- check.py

主要用于命令行里单独运行检查分析功能。




### 对checkitem进行测试

```
(py3)D:\git\SmartCare>python -m mme.status.checkers
MME单元状态检查
{
  "hostname": "HZMME48BNK",
  "name": "MME\u5355\u5143\u72b6\u6001\u68c0\u67e5",
  "description": "\u68c0\u67e5mme\u6240\u6709\u5355\u5143\u7684\u72b6\u6001\uff0c\u7edf\u8ba1\u51faWO-EX\u548cSP-EX\u7684\u5355\u5143\u6570\u91cf\uff0c\u4ee5\u53ca\u5f02\u5e38\u5355\u5143\u7684\u6570\u91cf",
  "status": "Passed",
  "info": "",
  "error": "",
  "stats": {
    "WO-EX": 42,
    "SP-EX": 15,
    "Other": 0
  }
}
MME单元CPU负荷检查
{
  "hostname": "HZMME48BNK",
  "name": "MME\u5355\u5143CPU\u8d1f\u8377\u68c0\u67e5",
  "description": "\u68c0\u67e5mme\u6240\u6709\u5355\u5143\u7684CPU\u8d1f\u8377\uff0c\u8f93\u51fa\u5355\u5143\u7684\u8d1f\u8377\u4fe1\u606f\u3002\u5982\u679c\u6709\u5355\u5143\u8d1f\u8377\u5927\u4e8e80%\uff0c\u5219\u8f93\u51faFailed\u3002data={'cpuload':{'mmdu-0':10,'mmdu-1':2}}",
  "status": "Failed",
  "info": "",
  "error": "",
  "stats": [
    "MMDU-0",
    "MMDU-7",
    "MMDU-9",
    "MMDU-2",
    "MMDU-8",
    "MMDU-11",
    "MMDU-6",
    "MMDU-4",
    "MMDU-1",
    "MMDU-10",
    "MMDU-3",
    "MMDU-5"
  ]
}
```

### 搜索目录下的.stats为后缀的log文件并进行分析。

```
(py3)D:\git\SmartCare>python -m mme.status.check
MME单元状态检查
{
  "hostname": "HZMME48BNK",
  "name": "MME\u5355\u5143\u72b6\u6001\u68c0\u67e5",
  "description": "\u68c0\u67e5mme\u6240\u6709\u5355\u5143\u7684\u72b6\u6001\uff0c\u7edf\u8ba1\u51faWO-EX\u548cSP-EX\u7684\u5355\u5143\u6570\u91cf\uff0c\u4ee5\u53ca\u5f02\u5e38\u5355\u5143\u7684\u6570\u91cf",
  "status": "Passed",
  "info": "",
  "error": "",
  "stats": {
    "WO-EX": 42,
    "SP-EX": 15,
    "Other": 0
  }
}
MME单元CPU负荷检查
{
  "hostname": "HZMME48BNK",
  "name": "MME\u5355\u5143CPU\u8d1f\u8377\u68c0\u67e5",
  "description": "\u68c0\u67e5mme\u6240\u6709\u5355\u5143\u7684CPU\u8d1f\u8377\uff0c\u8f93\u51fa\u5355\u5143\u7684\u8d1f\u8377\u4fe1\u606f\u3002\u5982\u679c\u6709\u5355\u5143\u8d1f\u8377\u5927\u4e8e80%\uff0c\u5219\u8f93\u51faFailed\u3002data={'cpuload':{'mmdu-0':10,'mmdu-1':2}}",
  "status": "Failed",
  "info": "",
  "error": "",
  "stats": [
    "MMDU-0",
    "MMDU-7",
    "MMDU-9",
    "MMDU-2",
    "MMDU-8",
    "MMDU-11",
    "MMDU-6",
    "MMDU-4",
    "MMDU-1",
    "MMDU-10",
    "MMDU-3",
    "MMDU-5"
  ]
}
MME单元状态检查
{
  "hostname": "HZMME49BNK",
  "name": "MME\u5355\u5143\u72b6\u6001\u68c0\u67e5",
  "description": "\u68c0\u67e5mme\u6240\u6709\u5355\u5143\u7684\u72b6\u6001\uff0c\u7edf\u8ba1\u51faWO-EX\u548cSP-EX\u7684\u5355\u5143\u6570\u91cf\uff0c\u4ee5\u53ca\u5f02\u5e38\u5355\u5143\u7684\u6570\u91cf",
  "status": "Passed",
  "info": "",
  "error": "",
  "stats": {
    "WO-EX": 42,
    "SP-EX": 15,
    "Other": 0
  }
}
MME单元CPU负荷检查
{
  "hostname": "HZMME49BNK",
  "name": "MME\u5355\u5143CPU\u8d1f\u8377\u68c0\u67e5",
  "description": "\u68c0\u67e5mme\u6240\u6709\u5355\u5143\u7684CPU\u8d1f\u8377\uff0c\u8f93\u51fa\u5355\u5143\u7684\u8d1f\u8377\u4fe1\u606f\u3002\u5982\u679c\u6709\u5355\u5143\u8d1f\u8377\u5927\u4e8e80%\uff0c\u5219\u8f93\u51faFailed\u3002data={'cpuload':{'mmdu-0':10,'mmdu-1':2}}",
  "status": "Failed",
  "info": "",
  "error": "",
  "stats": [
    "MMDU-3",
    "MMDU-0",
    "MMDU-9",
    "MMDU-1",
    "MMDU-8",
    "MMDU-6",
    "MMDU-10",
    "MMDU-5",
    "MMDU-7",
    "MMDU-11",
    "MMDU-4",
    "MMDU-2"
  ]
}
```