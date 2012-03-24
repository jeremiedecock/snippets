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
