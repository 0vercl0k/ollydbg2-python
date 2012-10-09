#include "window.hpp"
#include "plugin.h"

LRESULT CALLBACK CommandLineWinProc(
  _In_  HWND hwnd,
  _In_  UINT uMsg,
  _In_  WPARAM wParam,
  _In_  LPARAM lParam
)
{
    RECT rect = {0};
    DWORD width = 0;

    switch (uMsg) 
    { 
        case WM_CREATE: 
            // Initialize the window.
            return 0; 
 
        case WM_PAINT: 
            // Paint the window's client area.

            // Update the position of the window even if the parent window is resized
            /*GetWindowRect(GetParent(hwnd), &rect);

            width = (rect.right - rect.left) - 10;
            Addtolist(0, RED, L"lolilol\n");

            MoveWindow(
                hwnd,
                0,
                rect.bottom,
                width,
                100,
                TRUE
            );
            */

            ValidateRect(hwnd, 0);
            return 0; 

        case WM_DESTROY: 
            // Clean up window-specific data objects. 
            PostQuitMessage(0);
            return 0; 
 
        // 
        // Process other messages. 
        // 
 
        default: 
            return DefWindowProc(hwnd, uMsg, wParam, lParam); 
    }

    return 0;
}

BOOL CreateCommandLineWindow(HWND hParent, HINSTANCE hInst)
{
    HWND hCmdLine;
    RECT rect = {0};
    DWORD width = 0;
    WNDCLASS wClass = {0};

    wClass.lpfnWndProc = CommandLineWinProc;
    wClass.hInstance = hInst;
    wClass.lpszClassName = CLI_WINDOW_CLASS_NAME;
    wClass.hbrBackground = (HBRUSH)16;

    if(RegisterClass(&wClass) == 0)
        return FALSE;

    GetWindowRect(hParent, &rect);

    // We want an editbox as large the window is, minus the scrollbar
    width = (rect.right - rect.left) - 10;

    hCmdLine = CreateWindowEx(
        WS_EX_LTRREADING,
        CLI_WINDOW_CLASS_NAME,
        L"Command Line Window",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        0,
        rect.bottom - 25,
        width,
        50,
        hParent,
        NULL,
        hInst,
        NULL
    );

    if(hCmdLine == NULL)
        return FALSE;

    ShowWindow(hCmdLine, SW_SHOW);

    return TRUE;
}