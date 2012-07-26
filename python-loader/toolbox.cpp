#include "toolbox.hpp"

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