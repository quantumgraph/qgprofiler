
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
$ python setup.py install
```

Usage
--------------

This module consists two main classes **QGProfiler** and **QGProfileAggregator**. Their usage is described and demonstrated below.

### QGProfiler:

QGProfiler takes 2 definite arguments and 1 optional argument:
 - name for the program (this will be the root name of the stack)
 - output filename with path (the filename should end with .json or .xml; if path is not specified than it generates in the current folder with the given file name)  
 - an optional custom attributes which can be attached to the node and can be updated ```attributes={'somename': 'max', 'anothername': 'sum'}``` (value can be either 'max' or 'sum'; QGProfiler will do the computation to float up the values to the parent node by the type it has been defined; the idea is to use this feature for calculating memory with max and no.of db calls made with sum feature and so on..)

This class contains few functions which can be used to evaluate the time taken by each function/module and the number of times the same function/module has been called. The time taken is determined by using simple  
 - ```push('name')``` (name can be function name/db query/class module/etc.),  
 - ```pop()``` when the execution of the function is done or  
 - ```pop_all()``` which helps user to pop all the nodes in stack if the user lost count of how many pushes done. After the end of the program user has to call  
 - ```end()``` to end the root program time and then  
 - ```generate_file()``` is used for generating either xml or json file. By default QGProfiler will not round the number of values while generate_file to get maximum precision, you can round those values by passing an argument like ```generate_file(rounding_no=6)``` or just ```generate_file(6)```.  

A Brief Example is illustrated below with the output to get started:

```python
import time
from qgprofiler import QGProfiler

# filename extension can be either json or xml
qg_profiler = QGProfiler('program_root_name', '/path/to/your/file/filename.json', {'mem': 'max'}) # program started
qg_profiler.push('test1')    # test1 started
time.sleep(0.1)              # sleep follows that some program is executed
qg_profiler.update('mem', 10)# update will update the attribute of the node

qg_profiler.push('test11')   # test11 started
time.sleep(0.5)
qg_profiler.pop()            # test11 ended

qg_profiler.push('test12')   # test12 started
time.sleep(0.5)
qg_profiler.update('mem', 10)
qg_profiler.push('test121')  # test121 started
time.sleep(1.0)
qg_profiler.update('mem', 30)
qg_profiler.pop()            # test121 ended
qg_profiler.pop()            # test12 ended

qg_profiler.push('test12')   # test12 started
time.sleep(0.5)
qg_profiler.pop()            # test121 ended

qg_profiler.pop()            # test1 ended

qg_profiler.push('test2')    # test2 started
time.sleep(0.1)
qg_profiler.update('mem', 10)
qg_profiler.pop()            # test2 ended

qg_profiler.push('test2')    # test2 started
time.sleep(0.1)
qg_profiler.update('mem', 20)
qg_profiler.pop()            # test2 ended

qg_profiler.end()            # program ended

qg_profiler.generate_file()  # will generate the file
```

This generates a file which contains a json
```json
{
  "count": 1,
  "name": "program_root_name",
  "value": 2.808331,
  "overhead": 3.5e-05,
  "attributes": {"mem": {"type": "max", "value": 30}},
  "children": [{
    "count": 1,
    "name": "test1",
    "value": 2.606762,
    "overhead": 0.00013199999999999998,
      "attributes": {"mem": {"type": "max", "value": 30}},
    "children": [{
      "count": 1,
      "name": "test11",
      "value": 0.501054,
      "overhead": 0.00031099999999999997,
        "attributes": {"mem": {"type": "max", "value": 0}},
      "children": []
    }, {
      "count": 2,
      "name": "test12",
      "value": 2.0043670000000002,
      "overhead": 0.000463,
        "attributes": {"mem": {"type": "max", "value": 30}},
      "children": [{
        "count": 1,
        "name": "test121",
        "value": 1.001872,
        "overhead": 0.000338,
          "attributes": {"mem": {"type": "max", "value": 30}},
        "children": []
      }]
    }]
  }, {
    "count": 2,
    "name": "test2",
    "value": 0.20094299999999998,
    "overhead": 0.000297,
      "attributes": {"mem": {"type": "max", "value": 20}},
    "children": []
  }]
}
```

File generated if .xml is given as extension in the filename
```xml
<node name="program_root_name" value="2.808331" count="1" overhead="3.5e-05" attributes="mem:max:30">
  <node name="test1" value="2.606762" count="1" overhead="0.000132" attributes="mem:max:30">
    <node name="test11" value="0.501054" count="1" overhead="0.000311" attributes="mem:max:0"></node>
    <node name="test12" value="2.004367" count="2" overhead="0.000463" attributes="mem:max:30">
      <node name="test121" value="1.001872" count="1" overhead="0.000338" attributes="mem:max:30"></node>
    </node>
  </node>
  <node name="test2" value="0.200943" count="2" overhead="0.000297" attributes="mem:max:20"></node>
</node>
```

### QGProfileAggregator:

QGProfileAggregator takes 2 arguments:
 - input filepath (takes unix level command, ex: ~/path/*.xml; takes all xml files specified in the given path)
 - output filename with path (the filename should end with .json or .xml or .html; if path is not specified than it generates in the current folder with the given file name)  

This class contains one function ```generate_file()``` which will aggregate all the files data (.xml or .json whichever is specified or it takes all the files if specified * and process only .xml / .json). This will generate .xml / .json file whichever is specified in output filename. By default QGAggregator will set an argument for rounding the number of value to 6 digits to generate_file, you can overwite it by passing it as argument like ```generate_file(rounding_no=4)``` or just ```generate_file(4)```. If the generated file output is .json or .xml, the format will be as shown as above. But if .html is given as the extension, it will generate a flame graph using d3 which requires active internet connection to download the required js files, and the graph will look like  

![Alt text](/qgprofiler/images/flamegraph-1.png?raw=true "Flame Graph")

A Brief Example is illustrated below to use it:

```python
from qgprofiler import QGProfileAggregator

qg_profile_agg = QGProfileAggregator('/your/file/path/*.xml', '/path/to/your/file/filename.xml')
qg_profile_agg.generate_file() # this agrregates all the json/xml files into 1 file

```
