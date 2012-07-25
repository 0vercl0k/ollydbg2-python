#include <stdio.h>
#include <windows.h>

extern "C" {
	#include <python.h>
};

#include "plugin.h"

static int handle_about(t_table* pTable, wchar_t* pName, ulong index, int nMode);
static int handle_script_loading(t_table* pTable, wchar_t* pName, ulong index, int nMode);

static HINSTANCE g_hinst = 0;

/*
typedef struct t_menu                      // Menu descriptor
{
	wchar_t        *name;                  // Menu command
	wchar_t        *help;                  // Explanation of command
	int            shortcutid;             // Shortcut identifier, K_xxx
	MENUFUNC       *menufunc;              // Function that executes menu command
	struct t_menu  *submenu;               // Pointer to descriptor of popup menu
	union {
		ulong        index;                // Argument passed to menu function
		HMENU        hsubmenu;             // Handle of pulldown menu
	};
} t_menu;
*/
static t_menu g_MainMenu[] =
{
	{
		L"Load your script", 
		L"Load in OllyDBG your custom python script.",  
		K_NONE, handle_script_loading, NULL, 0
	},
    {
		L"About", 
		L"Fire the about messagebox.",  
		K_NONE, handle_about, NULL, 0
	},
    { NULL, NULL, K_NONE, NULL, NULL, 0 }
};

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
	if(fdwReason == DLL_PROCESS_ATTACH)
		g_hinst = hinstDLL;

    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}

/* This routine is required! */
pentry (int) ODBG2_Pluginquery(
	int ollydbgversion,
    wchar_t pluginname[SHORTNAME],
    wchar_t pluginversion[SHORTNAME]
)
{
	// Yeah, the plugin interface in the v1/v2 are different
    if(ollydbgversion != PLUGIN_VERSION)
        return 0;

    // Set plugin name and version
    wcscpy_s(pluginname, SHORTNAME, L"python-loader");
    wcscpy_s(pluginversion, SHORTNAME, L"v0.1");

	// Initialize the python environment, prepare the hooks
	Py_Initialize();

	// XXX: hardcoded path, c'mon!
	PyObject* PyFileObject = PyFile_FromString("C:\\Debugger\\OllyDbg\\odbg200\\hook.py", "r");
	PyRun_SimpleFile(PyFile_AsFile(PyFileObject), "C:\\Debugger\\OllyDbg\\odbg200\\hook.py");

	Addtolist(0x31337, RED, L"[python-loader] Plugin fully initialized.");
	return PLUGIN_VERSION;
}

pentry (void) ODBG2_Plugindestroy(void)
{
	// Properly ends the python environment
	Py_Finalize();
}

/* Adds items to OllyDbgs menu system. */
extc _export t_menu* cdecl ODBG2_Pluginmenu(wchar_t* type)
{
    if(wcscmp(type, PWM_MAIN) == 0)
        return g_MainMenu;

    return NULL;
}

static int handle_about(t_table* pTable, wchar_t* pName, ulong index, int nMode)
{
	if(nMode == MENU_VERIFY)
		return MENU_NORMAL;
	else if(nMode == MENU_EXECUTE)
	{
		MessageBox(
			hwollymain,
			L"python loader",
			L"About python-loader",
			MB_OK| MB_ICONINFORMATION
		);
		return MENU_NOREDRAW;
	}
	else
		return MENU_ABSENT;
}

static int handle_script_loading(t_table* pTable, wchar_t* pName, ulong index, int nMode)
{
	if(nMode == MENU_VERIFY)
		return MENU_NORMAL;
	else if(nMode == MENU_EXECUTE)
	{
		// XXX: create a window, something!
		PyObject* PyFileObject = PyFile_FromString("script.py", "r");
		PyRun_SimpleFile(PyFile_AsFile(PyFileObject), "script.py");

		return MENU_NOREDRAW;
	}
	else
		return MENU_ABSENT;
}
