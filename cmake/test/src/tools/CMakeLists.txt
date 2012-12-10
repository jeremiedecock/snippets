SET(tools_src tools1.h   tools2.h  
             tools1.cpp tools2.cpp)

ADD_LIBRARY(tools STATIC ${tools_src})
