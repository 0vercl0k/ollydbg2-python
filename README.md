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
