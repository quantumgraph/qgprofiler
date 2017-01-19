
qgprofiler
==============

QGProfiler is a simple, user controlled profiler. It differs from 
other profilers in that it provides the programmer the control of
granularity with which various parts of the program are profiled.
By doing this, the programmer can keep profiling overhead low 
(QGProfiler is meant to be used in production), while still getting
visibility in the most important components of the program.


Installation
--------------
using pip:

```sh
$ pip install qgprofiler
```

using setuptools:

```sh
$ git clone https://github.com/quantumgraph/qgprofiler
$ cd qgprofiler
$ pip install qgprofiler
```

Usage
--------------

This module consists two main classes **QGProfiler** and **QGProfileAggregator**. Their usage is described and demonstrated below.

### QGProfiler:

QGProfiler takes 2 arguments:
 - name for the program (this will be the root name of the stack)
 - output filename with path (the filename should end with .json or .xml; if path is not specified than it generates in the current folder)  

This class contains few functions which can be used to evaluate the time taken by each function/module and the number of times the same function/module has been called. The time taken is determined by using simple ```push('name')``` (name can be function name / db query / class module / etc.)and ```pop()``` when the execution of the function is done. After the end of the program user has to call ```end()``` to end the root program time and then ```generate_file()``` is used for generating either xml or json file.  

A Brief Example is illustrated below with the output to get started:

```python
from qgprofiler import QGProfiler

# filename extension can be either json or xml
qg_profiler = QGProfiler('program_root_name', '/path/to/your/file/filename.json') # program started
qg_profiler.push('test1')    # test1 started

qg_profiler.push('test11')   # test11 started
qg_profiler.pop()            # test11 ended

qg_profiler.push('test12')   # test12 started
qg_profiler.push('test121')  # test121 started
qg_profiler.pop()            # test121 ended
qg_profiler.pop()            # test12 ended

qg_profiler.push('test12')   # test12 started
qg_profiler.pop()            # test121 ended

qg_profiler.pop()            # test1 ended

qg_profiler.push('test2')    # test2 started
qg_profiler.pop()            # test2 ended

qg_profiler.push('test2')    # test2 started
qg_profiler.pop()            # test2 ended

qg_profiler.end()            # program ended

qg_profiler.generate_file()  # will generate the file
```

This generates a file which contains a json
```json
{
  "count": 1,
  "name": "program_root_name",
  "value": 0.000709,
  "children": [{
    "count": 1,
    "name": "test1",
    "value": 0.000386,
    "children": [{
      "count": 1,
      "name": "test11",
      "value": 4.3e-05,
      "children": []
    }, {
      "count": 2,
      "name": "test12",
      "value": 0.00016199,
      "children": [{
        "count": 1,
        "name": "test121",
        "value": 3.9e-05,
        "children": []
      }]
    }]
  }, {
    "count": 2,
    "name": "test2",
    "value": 7e-05,
    "children": []
  }]
}
```

File generated if .xml is given as extension in the filename
```xml
<node name="program_root_name" value="0.00069" count="1">
  <node name="test1" value="0.000378" count="1">
    <node name="test11" value="4.3e-05" count="1"></node>
    <node name="test12" value="0.000153" count="2">
      <node name="test121" value="3.7e-05" count="1"></node>
    </node>
  </node>
  <node name="test2" value="7e-05" count="2"></node>
</node>
```

### QGProfileAggregator:

QGProfileAggregator takes 2 arguments:
 - input filepath (takes unix level command, ex: ~/path/*.xml; takes all xml files specified in the given path)
 - output filename with path (the filename should end with .json or .xml; if path is not specified than it generates in the current folder)  

This class contains one function ```generate_file()``` which will aggregate all the files data (.xml or .json whichever is specified or it takes all the files if specified * and process only .xml / .json). This will generate .xml / .json file which ever is specified in output filename.  

A Brief Example is illustrated below to use it:

```python
qg_profile_agg = QGProfileAggregator('/your/file/path/*.xml', '/path/to/your/file/filename.xml')
qg_profile_agg.generate_file() # this agrregates all the json/xml files into 1 file

```
