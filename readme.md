## Description
Analyzer for cyclomatic complexity. Can work with C++, C#, Python.
Outputs the report to STDOUT.

## Setup
Use setup.py to install the dependencies:

    python3 setup.py install

## Use
Use cyclomatic_complexity.py to analyze source code files and generate a json report.

- #### Analyze path
    In the command line's first argument you can put a directory. In this case, by default, the tool will analyze all files including in all sub-folders 

      python3 cyclomatic_complexity.py some\path

    Alternatively, you can cancel recursive analysis of sub-folders:

      python3 cyclomatic_complexity.py some\path -r False


- #### Analyze a single file
    Or, you can analyze a single file:

      python3 cyclomatic_complexity.py some\path\someFile.cpp


- #### Do not create a report.json file
    If you only want to output the results to STDOUT:

      python3 cyclomatic_complexity.py some\path -s False

