#include <stdio.h>
#include <windows.h>
#include <string>
#include "plugin.h"

extern "C" {
    #include <python.h>
};

// Constants
#define CLASS_NAME L"script_loading window"

#define MENU_LOAD_SCRIPT_IDX 1
#define MENU_ABOUT_IDX 2

#define WINDOW_BUTTON_OK_IDX 0x8801
#define WINDOW_EDITBOX_IDX 0x8802

// Prototypes
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved);
LRESULT CALLBACK WindowProc_script_loading(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
int handle_menu(t_table* pTable, wchar_t* pName, ulong index, int nMode);
void spwan_window(void);
void execute_python_script(wchar_t *path);
std::wstring multibytes_to_widechar(std::string &st);
std::string widechar_to_multibytes(std::wstring &st);

// Global variables
HINSTANCE g_hinst = 0;

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
t_menu g_MainMenu[] =
{
    {
        L"Load your script", 
        L"Load in OllyDBG your custom python script.",  
        K_NONE, handle_menu, NULL, MENU_LOAD_SCRIPT_IDX
    },
    {
        L"About", 
        L"Fire the about messagebox.",  
        K_NONE, handle_menu, NULL, MENU_ABOUT_IDX
    },
    { NULL, NULL, K_NONE, NULL, NULL, 0 }
};

std::string widechar_to_multibytes(std::wstring &st)
{
    // XXX: make sure st doesn't have any accent..
    std::string ret;
    ret.assign(st.begin(), st.end());
    return ret;
}

std::wstring multibytes_to_widechar(std::string &st)
{
    std::wstring ret;
    ret.assign(st.begin(), st.end());
    return ret;
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
    if(fdwReason == DLL_PROCESS_ATTACH)
        g_hinst = hinstDLL;

    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}

/*
    This routine is required by the OllyDBG plugin engine! 
*/
pentry (int) ODBG2_Pluginquery(int ollydbgversion, wchar_t pluginname[SHORTNAME], wchar_t pluginversion[SHORTNAME])
{
    // Yeah, the plugin interface in the v1/v2 are different
    if(ollydbgversion != PLUGIN_VERSION)
        return 0;

    // Set plugin name and version
    wcscpy_s(pluginname, SHORTNAME, L"python-loader");
    wcscpy_s(pluginversion, SHORTNAME, L"v0.1");

    // Initialize the python environment, prepare the hooks
    Py_Initialize();

    std::wstring pathW(ollydir);
    pathW += L"\\hook.py";

    Addtolist(0x31337, WHITE, L"[python-loader] Preparing to hook stdout/stderr of the python environment (%s)..", pathW.c_str());

    std::string pathA(widechar_to_multibytes(pathW));

    PyObject* PyFileObject = PyFile_FromString((char*)pathA.c_str(), "r");
    PyRun_SimpleFile(PyFile_AsFile(PyFileObject), pathA.c_str());

    Addtolist(0x31337, RED, L"[python-loader] Plugin fully initialized.");
    return PLUGIN_VERSION;
}

pentry (void) ODBG2_Plugindestroy(void)
{
    // Properly ends the python environment
    Py_Finalize();
}

/*
    Adds items to OllyDbgs menu system.
*/
extc _export t_menu* cdecl ODBG2_Pluginmenu(wchar_t* type)
{
    if(wcscmp(type, PWM_MAIN) == 0)
        return g_MainMenu;

    return NULL;
}


/*
    Spawn a nice (ok, not that nice) window to ask you the path of
    the python script you want to execute inside OllyDBG.
*/
void spawn_window(void)
{
    wchar_t file_path[1024] = {0};
    OPENFILENAME ofn = {0};

    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwollymain;
    ofn.lpstrFile = file_path;
    // Set lpstrFile[0] to '\0' so that GetOpenFileName does not 
    // use the contents of szFile to initialize itself.
    ofn.lpstrFile[0] = '\0';
    ofn.nMaxFile = sizeof(file_path);
    ofn.lpstrFilter = L"Python files\0*.py\0\0";
    ofn.nFilterIndex = 1;
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;

    if(GetOpenFileName(&ofn) == TRUE)
        execute_python_script(file_path);
    else
        Addtolist(0, RED, L"[python-loader] Your path is really *long*, are you trying to crash me ?:)");
}

/*
    Method called by OllyDBG in order to dispatch the actions done on
    the menu the plugin creates.
*/
int handle_menu(t_table* pTable, wchar_t* pName, ulong index, int nMode)
{
    if(nMode == MENU_VERIFY)
        return MENU_NORMAL;
    else if(nMode == MENU_EXECUTE)
    {
        switch(index)
        {
            case MENU_LOAD_SCRIPT_IDX:
            {
                spawn_window();
                break;
            }

            case MENU_ABOUT_IDX:
            {
                MessageBox(
                    hwollymain,
                    L"python loader",
                    L"About python-loader",
                    MB_OK| MB_ICONINFORMATION
                );

                break;
            }

            default:
                break;
        }

        return MENU_NOREDRAW;
    }
    else
        return MENU_ABSENT;
}

/*
    Execute a python script located on your file system thanks to
    the python high level API.
*/
void execute_python_script(wchar_t *path)
{
    Addtolist(0, WHITE, L"[python-loader] Trying to execute the script located here: '%s'..", path);

    std::wstring pathW(path);
    std::string pathA(widechar_to_multibytes(pathW));

    PyObject* PyFileObject = PyFile_FromString((char*)pathA.c_str(), "r");
    if(PyFileObject == NULL)
    {
        Addtolist(0, RED, L"[python-loader] Your file doesn't exist.");
        return;
    }

    PyRun_SimpleFile(PyFile_AsFile(PyFileObject), (char*)pathA.c_str());

    Addtolist(0, WHITE, L"[python-loader] Execution is done!");
}