#include "window.hpp"
#include "plugin.h"
#include "toolbox.hpp"

#include <windowsx.h>
#include <commctrl.h>
#include <python.h>

BOOL class_is_already_registered = FALSE;

LRESULT CALLBACK CommandLineWinProc(
  _In_  HWND hwnd,
  _In_  UINT uMsg,
  _In_  WPARAM wParam,
  _In_  LPARAM lParam
)
{
    switch (uMsg) 
    { 
        case WM_CREATE:
            // Initialize the window.
            return 0;

        case WM_PAINT:
            // Paint the window's client area.
            ValidateRect(hwnd, 0);
            break; 

        case WM_DESTROY:
            // Clean up window-specific data objects.
            return 0; 
        
        case WM_CLOSE:
        {
            DestroyWindow(hwnd);
            break;
        }

        case WM_COMMAND:
        {
            switch(LOWORD(wParam))
            {
                case IDC_MAIN_EDIT:
                {
                    switch(HIWORD(wParam))
                    {
                        case CBN_SELENDOK:
                        {
                            DWORD len = ComboBox_GetTextLength(GetDlgItem(hwnd, IDC_MAIN_EDIT));
                            if(len == 0)
                                break;

                            wchar_t *buffer = (wchar_t*) malloc((len + 1) * sizeof(wchar_t));
                            if(buffer == NULL)
                                break;

                            SecureZeroMemory(buffer, (len + 1) * sizeof(wchar_t));

                            ComboBox_GetText(
                                GetDlgItem(hwnd, IDC_MAIN_EDIT),
                                buffer,
                                len + 1
                            );

                            // Addtolist(0x31337, RED, L"Got %s", buffer);
                            std::string cmd(widechar_to_multibytes(std::wstring(buffer)));

                            PyRun_SimpleString(cmd.c_str());

                            int idx = ComboBox_FindStringExact(
                                GetDlgItem(hwnd, IDC_MAIN_EDIT),
                                0,
                                buffer
                            );

                            if(idx == CB_ERR)
                                ComboBox_AddString(
                                    GetDlgItem(hwnd, IDC_MAIN_EDIT),
                                    buffer
                                );

                            free(buffer);
                            break;
                        }
                    }

                    break;
                }
            }

            break;
        }

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
    HWND hCmdLine, hEdit;
    RECT rect = {0};
    DWORD width = 0;
    WNDCLASS wClass = {0};

    wClass.lpfnWndProc = CommandLineWinProc;
    wClass.hInstance = hInst;
    wClass.lpszClassName = CLI_WINDOW_CLASS_NAME;
    wClass.hbrBackground = (HBRUSH)(16);

    if(RegisterClass(&wClass) == 0 && class_is_already_registered == FALSE)
        return FALSE;

    if(class_is_already_registered == FALSE)
        class_is_already_registered = TRUE;

    GetWindowRect(hParent, &rect);

    // We want an editbox as large the window is, minus the scrollbar
    width = (rect.right - rect.left) - 10;

    hCmdLine = CreateWindowEx(
        WS_EX_LTRREADING,
        CLI_WINDOW_CLASS_NAME,
        L"Command Line Window",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        0,
        rect.bottom - 70,
        width - 70,
        60,
        hParent,
        NULL,
        hInst,
        NULL
    );

    if(hCmdLine == NULL)
        return FALSE;

    hEdit = CreateWindowEx(
        WS_EX_OVERLAPPEDWINDOW,
        WC_COMBOBOX,
        L"",
        WS_VISIBLE | WS_CHILD | CBS_SIMPLE | CBS_DISABLENOSCROLL, 
        0,
        0,
        width,
        100,
        hCmdLine,
        (HMENU)IDC_MAIN_EDIT,
        hInst,
        NULL
    );

    if(hEdit == NULL)
        return FALSE;

    return TRUE;
}