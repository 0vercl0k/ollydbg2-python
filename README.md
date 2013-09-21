ollydbg2-python
===============

# Building python-loader

You will need Python development files, I'm currently using Python 275.

# Building the Python bindings via SWIG

To build the API bindings you will need [SWIG](http://www.swig.org/) and Python 275.

1. Fetch the last Ollydbg2's development files on http://www.ollydbg.de/version2.html. Move the plugin.h in the inc/ directory, and the ollydbg.lib in lib/.
2. Then copy the plugin.h in plugin-swig.h. Take care to:

* Some API are declared in the plugin.h file, but in fact they aren't in Ollydbg2's export address table ; so comment them. Here is the list: SetcaseA, SetcaseW, StrcopycaseA, StrcopycaseW, StrnstrA, StrnstrW, StrcmpW, Div64by32, CRCcalc, Getcpuidfeatures, Maskfpu, Clearfpu.
* Remove the __cdecl from the stdapi, varapi, oddata, pentry. There is also another one in EMUFUNC's typedef.
* Remove the const from the oddata declaraction (like that you will be able to interact with internal variables) both in plugin.h & plugin-swig.h.
* Remove the _import keyword from oddata's definition.
* Rename the Readmemory's first argument into "char *buff" and add before "%pybuffer_mutable_string(char *buf) / %typemap(in) char *buf;" ; same thing with Disasm and its first argument ; same thing with Assembleallforms and its last argument ; same thing with Getanalysercomment and its third argument ; same thing with Getproccomment and its third argument ; same thing with Decodeaddress and its fourth argument ; same thing with Decoderelativeoffset and its third argument.
* Anonymous nested structures aren't supported, so you have to give a name to the unions in the following structure: t_result.

3. Then move in the swig/ directory, and execute that command:
```text
D:\OllyDBG2-Python\ollydbg2-development-files\swig>..\..\swigwin\swigwin\swig.exe -outdir ..\..\python-bindings-swig\ -o ..\..\python-bindings-swig\ollydbg2-swig_wrap.c -cpperraswarn -python ollydbg2-swig.i
..\inc\plugin-swig.h(38) : Warning 205: CPP #error "This version must be compiled with UNICODE on".
..\inc\plugin-swig.h(465) : Warning 312: Nested union not currently supported (ignored).
..\inc\plugin-swig.h(886) : Warning 312: Nested union not currently supported (ignored).
..\inc\plugin-swig.h(1848) : Warning 314: 'from' is a python keyword, renaming to '_from'
..\inc\plugin-swig.h(1879) : Warning 312: Nested union not currently supported (ignored).
..\inc\plugin-swig.h(2791) : Warning 312: Nested union not currently supported (ignored).
..\inc\plugin-swig.h(3363) : Warning 312: Nested union not currently supported (ignored).

4. Open the python-bindings-swig project and build the Python bindings.
5. You're ready to go!