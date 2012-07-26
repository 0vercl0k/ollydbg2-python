#ifndef MAIN_HPP
#define MAIN_HPP

#include <windows.h>
#include <plugin.h>

// Constants
#define CLASS_NAME L"script_loading window"

#define MENU_LOAD_SCRIPT_IDX 1
#define MENU_ABOUT_IDX 2

#define WINDOW_BUTTON_OK_IDX 0x8801
#define WINDOW_EDITBOX_IDX 0x8802

// Prototypes
/*
    Dll Main, will be called when the library will be loaded in memory by OllyDbg
*/
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved);

/*
    Spawn a nice window to ask you the path of
    the python script you want to execute inside OllyDBG.
*/
void spwan_window(void);

/*
    Method called by OllyDBG in order to dispatch the actions done on
    the menu the plugin creates.
*/
int handle_menu(t_table* pTable, wchar_t* pName, ulong index, int nMode);

/*
    Execute a python script located on your file system thanks to
    the python high level API.
*/
void execute_python_script(wchar_t *path);


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

#endif