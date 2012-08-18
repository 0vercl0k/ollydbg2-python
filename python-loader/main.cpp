#include "main.hpp"
#include "toolbox.hpp"

#include <cstdio>
#include <cstring>
#include <python.h>

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved)
{
    if(fdwReason == DLL_PROCESS_ATTACH)
        g_hinst = hinstDLL;

    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}

/*
    This routine is required by the OllyDBG plugin engine! 
*/
pentry (int) ODBG2_Pluginquery(int ollydbgversion, ulong *features, wchar_t pluginname[SHORTNAME], wchar_t pluginversion[SHORTNAME])
{
    // Yeah, the plugin interface in the v1/v2 are different
    if(ollydbgversion < 201)
        return 0;

    // Set plugin name and version
    wcscpy_s(pluginname, SHORTNAME, L"python-loader");
    wcscpy_s(pluginversion, SHORTNAME, L"v0.1");

    // Initialize the python environment, prepare the hooks
    Py_Initialize();

    std::wstring pathW(_ollydir);
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

void spawn_window(void)
{
    wchar_t file_path[1024] = {0};
    OPENFILENAME ofn = {0};

    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = _hwollymain;
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
                    _hwollymain,
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