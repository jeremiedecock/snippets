# For more options (e.g. use other composants than QtGui and QtCore, etc.), see:
# - http://doc.qt.io/qt-5/cmake-manual.html
# - http://kdab.developpez.com/tutoriels/cmake-qt-5/

# The minimum version required to use Qt5 is CMake 2.8.3, but 2.8.11 is recommended.
cmake_minimum_required(VERSION 2.8.11)

project(qt5_cmake_hello)

# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)

# Instruct CMake to run moc automatically when needed.
set(CMAKE_AUTOMOC ON)

# Find the QtWidgets library
find_package(Qt5Widgets)

# Tell CMake to create the helloworld executable
add_executable(hello main.cpp)

# Use the Widgets module from Qt 5.
# The recommended way to use Qt libraries and headers with CMake 2.8.11 is to
# use the target_link_libraries command. In CMake 2.8.11 and later versions,
# this command automatically adds appropriate include directories, compile
# definitions, the position-independent-code flag, and links to the qtmain.lib
# library on Windows.
target_link_libraries(hello Qt5::Widgets)
