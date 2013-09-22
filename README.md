Contents
===============
+ [OllyDbg2-Python]
+ [Installation]
+ [Known Issues]
+ [Contributing]

OllyDbg2-Python
===============

Motivations
------------
Nowadays in the reverse-engineering world, almost everything is scriptable using Python: IDA Pro, WinDbg, ImmunitDebugger, etc. The thing is OllyDbg2 wasn't. The only way to interact with OllyDbg2's API was by creating a C/C++ plugin. But we all know everything is easier in Python, that's the reason why I started this project back in 2012 summer. 

Under the hoods
------------
To be able to export OllyDbg2's API to Python (currently Py275), we need two important things:
1. python-loader: this is an OllyDbg2 plugin that imports the Python engine ; with that plugin you can launch some Python into your debugger
2. python-bindings-swig: this project builds the connectors you need to poke OllyDbg2's API with Python

The python-loader tries also to enhance user experience by adding a command-line edit bar in order to write easily Python one-liner without loading a script. At the moment, that bar isn't working very well (I'm not a GUI expert *at all*.), but I will give it a try to build better one.

The python-bindings-swig project is a bit more touchy, it is using [SWIG](http://www.swig.org/) in order to generate the bindings automatically and it seems to work pretty great so far. But SWIG can be sometimes a bit weird to play with, so if I made some mistakes don't hesitate to pull-requests corrections!

Features
---------
I've tried to expose the main features we would like to have when it comes to script a debugger:

* CPU state inspection: get/set x86 registers, get information about segment selectors
* memory: read, write in the debuggee memory ; also obtain information about specific memory regions
* assembler/disassembler: interact with the internal x86 assembler/disassembler
* breakpoints: easily set/remove software/hardware normal/conditionnal breakpoints wherever you want
* symbols: try to use Microsoft/OllyDbg2 API to obtain symbols information (like a function name by its address)
* enhance the disassembly: you can add comments and/or labels easily
* looking for something in memory: there are also a couple of methods to look for some hexadecimal bytes or instructions in memory, really handy
* instrument the debugger: ask the debugger to StepInto/StepOver/ExecuteUntilRet in the debuggee
* etc.

If you want to see real examples, check out the `samples/` directory! If you have idea of cool examples to show case the API feel free to contact me.

Building python-loader
-----------------------

You will need Python development files, I'm currently using Python 275.

Building the Python bindings via [SWIG](http://www.swig.org/) 
-------------------------------------

To build the API bindings you will need [SWIG](http://www.swig.org/) and Python 275.

1. Fetch the last [Ollydbg2's development files](http://www.ollydbg.de/version2.html). Move the `plugin.h` in the `ollydbg2-plugin-development-files/inc/` directory, and the `ollydbg.lib` in `ollydbg2-plugin-development-files/lib/`.
2. Then copy the `plugin.h` to `plugin-swig.h`. Here are the things you have to change in the `plugin-swig.h` file:

* Some API are declared in the `plugin.h` file, but in fact they aren't in Ollydbg2's export address table ; so comment them. Here is the list: `SetcaseA`, `SetcaseW`, `StrcopycaseA`, `StrcopycaseW`, `StrnstrA`, `StrnstrW`, `StrcmpW`, `Div64by32`, `CRCcalc`, `Getcpuidfeatures`, `Maskfpu`, `Clearfpu`.
* Remove the `__cdecl` from the `stdapi`, `varapi`, `oddata`, `pentry`. There is also another one in `EMUFUNC`'s typedef.
* Remove the `const` from the `oddata` declaration (like that you will be able to interact with internal variables) both in `plugin.h` & `plugin-swig.h`.
* Remove the `_import` keyword from `oddata`'s definition.
* Rename the `Readmemory`'s first argument into `char *buff`, add before `%pybuffer_mutable_string(char *buf)`, add after `%typemap(in) char *buf;`. Do the same thing with the following API:
 * `Disasm` and its first argument
 * `Assembleallforms` and its last argument
 * `Getanalysercomment` and its third argument
 * `Getproccomment` and its third argument
 * `Decodeaddress` and its fourth argument
 * `Decoderelativeoffset` and its third argument
* Anonymous nested structures aren't supported, so you have to give a name to the unions in the following structure: `t_result`.

3. Open the `python-bindings-swig` project and build the Python bindings.
5. You're ready to go!

Installation
============

1. `git clone https://github.com/0vercl0k/ollydbg2-python.git`
2. Move all your `OllyDbg2` binaries in the `ollydbg2-python` directory. It should looks like this:
```
D:\tmp\ollydbg2-python>ls -la .
total 3572
drw-rw-rw-   8 0vercl0k 0    4096 2013-09-22 16:17 .
drw-rw-rw-   5 0vercl0k 0    4096 2013-09-22 16:13 ..
drw-rw-rw-   7 0vercl0k 0    4096 2013-09-22 16:13 .git
-rw-rw-rw-   1 0vercl0k 0 1061944 2008-03-21 01:44 dbghelp.dll
drw-rw-rw-   2 0vercl0k 0       0 2013-09-22 16:13 ollyapi
-rwxrwxrwx   1 0vercl0k 0 2547200 2012-11-18 21:46 ollydbg.exe
-rw-rw-rw-   1 0vercl0k 0   13705 2013-09-22 16:18 ollydbg.ini
drw-rw-rw-   7 0vercl0k 0    4096 2013-09-22 16:13 ollydbg2-plugin-development-files
drw-rw-rw-   2 0vercl0k 0       0 2013-09-22 16:17 plugins
-rw-rw-rw-   1 0vercl0k 0    2713 2013-09-22 16:13 README.md
drw-rw-rw-  11 0vercl0k 0    4096 2013-09-22 16:13 samples
drw-rw-rw-   2 0vercl0k 0    4096 2013-09-22 16:17 udds
```
3. Build the python-loader project in Release mode and check you have a `python-loader.dll` file in `plugins/`:
```
D:\tmp\ollydbg2-python>ls -la plugins
total 24
drw-rw-rw-  2 0vercl0k 0     0 2013-09-22 16:22 .
drw-rw-rw-  8 0vercl0k 0  4096 2013-09-22 16:17 ..
-rw-rw-rw-  1 0vercl0k 0 18432 2013-09-22 16:22 python-loader.dll
```
4. Build the python-buildings-swig project in Release mode, check you have a `_python_bindings_swig.pyd` file and a `python_bindings_swig.py` in `ollyapi/`:
```
D:\tmp\ollydbg2-python>ls -la ollyapi
total 1436
drw-rw-rw-  2 0vercl0k 0   4096 2013-09-22 16:26 .
drw-rw-rw-  8 0vercl0k 0   4096 2013-09-22 16:17 ..
[...]
-rw-rw-rw-  1 0vercl0k 0 971776 2013-09-22 14:09 _python_bindings_swig.pyd
-rw-rw-rw-  1 0vercl0k 0 416207 2013-09-22 14:08 python_bindings_swig.py
```
5. Now launch `ollydbg.exe`, and check the log window to see if the python-loader plugin has been successfully loaded.
6. Script and have fun!

Known Issues
============

If you encounter any issues please let me know by filling an issue here: [https://github.com/0vercl0k/ollydbg2-python/issues](https://github.com/0vercl0k/ollydbg2-python/issues). Also try to be explicit, and give me enough details to be able to repro the issue on my machine: OS version, OllyDbg2 configuration, script, etc.

Contributing
============

Feel free to contribute to this project: if you're used to play with Windows' GUI API please help me to make a working bar, if you have idea about cool samples to show case the API send me your ideas, if you want to implement some high level API methods please do!
If you have also any comments, remarks I would love to hear them :).