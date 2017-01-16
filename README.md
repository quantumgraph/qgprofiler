
qgprofiler
==============

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
#### QGProfiler:

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

qg_profiler.pop()            # test1 ended

qg_profiler.push('test2')    # test2 started
qg_profiler.pop()            # test2 ended

qg_profiler.end()            # program ended

qg_profiler.generate_file()  # will generate the file
```

This generates a file which conatains a json
```json
{
  "name": "program_root_name",
  "value": 0.00142,
  "children": [
    {
      "name": "test1",
      "value": 0.00031,
      "children": [
        {"name": "test11", "value": 4.6e-05, "children": []},
        {
          "name": "test12",
          "value": 0.000118,
          "children": [
            {"name": "test121", "value": 3.8e-05, "children": []}
          ]
        }
      ]
    },
    {"name": "test2", "value": 3.6e-05, "children": []}
  ]
}
```

File generated if .xml is given as extension
```xml
<program_root_name value="0.00142">
  <test1 value="0.000309">
    <test11 value="4.5e-05"></test11>
    <test12 value="0.00012">
      <test121 value="3.8e-05"></test121>
    </test12>
  </test1>
  <test2 value="3.6e-05"></test2>
</program_root_name>
```

#### QGProfileAggregator:

```python
qg_profile_agg = QGProfileAggregator('/your/file/path/*.json', '/path/to/your/file/filename.xml')
qg_profile_agg.generate_file() # this agrregates all the json files into 1 file

```
