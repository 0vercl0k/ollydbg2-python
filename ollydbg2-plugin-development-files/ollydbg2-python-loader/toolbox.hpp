#ifndef TOOLBOX_HPP
#define TOOLBOX_HPP

#include <string>

/*
    Convert a std::string in std::wstring

    Really useful because OllyDBG2 API only works with wchar_t
    and the Python API only with char ; so you regularly have to
    play with both types.
*/
std::string widechar_to_multibytes(std::wstring &st);

/*
    Convert a std::wstring in std::string
*/
std::wstring multibytes_to_widechar(std::string &st);

#endif