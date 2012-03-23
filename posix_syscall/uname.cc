/* 
 * Uname: display system information like "uname -a" unix command
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Usage: g++ uname.cc
 * See "man 2 uname" for more info
 *
 */

#include <iostream>
#include <string>
#include <sstream>

#ifdef _POSIX_VERSION
#include <sys/utsname.h>
#endif

// Return system informations in a string
std::string get_sysinfo() {
    std::string sysinfo("unknown");

#ifdef _POSIX_VERSION
    struct utsname buf;
    int result = uname(&buf);

    if(result == 0) {
        std::ostringstream oss;
        oss << buf.sysname << " ";
        oss << buf.nodename << " ";
        oss << buf.release << " ";
        oss << buf.version << " ";
        oss << buf.machine << " ";
        sysinfo = oss.str();
    }
#endif

    return sysinfo;
}

int main() {
    std::cout << get_sysinfo() << std::endl;
}
