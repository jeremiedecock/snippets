# For more options (e.g. use other composants than QtGui and QtCore, etc.), see:
# - http://qtnode.net/wiki/Qt4_with_cmake
# - http://www.cmake.org/Wiki/CMake:How_To_Build_Qt4_Software
# - http://cmake.org/cmake/help/cmake2.6docs.html#module:FindQt4
# - http://www.qtcentre.org/wiki/index.php?title=Compiling_Qt4_apps_with_CMake

CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT(Qt4_hello_snippet)

# Find and setup Qt4 for this project
FIND_PACKAGE(Qt4 REQUIRED)

# Include
MESSAGE("Include: ${QT_USE_FILE}")
INCLUDE(${QT_USE_FILE})

ADD_EXECUTABLE(hello hello.cc)

# Link libraries:
MESSAGE("Link libraries: ${QT_LIBRARIES}")
TARGET_LINK_LIBRARIES(hello ${QT_LIBRARIES})
