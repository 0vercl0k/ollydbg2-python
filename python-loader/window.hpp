#ifndef WINDOW_HPP
#define WINDOW_HPP

#include <windows.h>

BOOL CreateCommandLineWindow(HWND hParent, HINSTANCE hInst);

#define CLI_WINDOW_CLASS_NAME L"CommandLineClass"
#define IDC_MAIN_EDIT 101

#endif