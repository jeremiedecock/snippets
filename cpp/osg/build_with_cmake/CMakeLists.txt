# SEE "OpenSceneGraph 3.0" by Rui Wang and Xuelei Qian (ed. Packt publishing 2010) chap.3 p.44

cmake_minimum_required(VERSION 2.6)

project(hello_snippet)

# Find and setup OpenSceneGraph for this project
find_package(OpenThreads)
find_package(osg)
find_package(osgDB)
find_package(osgUtil)
find_package(osgViewer)

# OSG includes and libraries
macro(config_osg_lib PROJNAME OSG_LIBNAME)
    include_directories(${${OSG_LIBNAME}_INCLUDE_DIR})
    target_link_libraries(${PROJNAME} ${${OSG_LIBNAME}_LIBRARY})
endmacro()

# Executable
add_executable(hello hello.cc)

# OSG includes and libraries
config_osg_lib(hello OPENTHREADS)
config_osg_lib(hello OSG)
config_osg_lib(hello OSGDB)
config_osg_lib(hello OSGUTIL)
config_osg_lib(hello OSGVIEWER)

# /usr/share/cmake-3.0/Modules/FindosgAnimation.cmake
# /usr/share/cmake-3.0/Modules/Findosg.cmake
# /usr/share/cmake-3.0/Modules/FindosgDB.cmake
# /usr/share/cmake-3.0/Modules/Findosg_functions.cmake
# /usr/share/cmake-3.0/Modules/FindosgFX.cmake
# /usr/share/cmake-3.0/Modules/FindosgGA.cmake
# /usr/share/cmake-3.0/Modules/FindosgIntrospection.cmake
# /usr/share/cmake-3.0/Modules/FindosgManipulator.cmake
# /usr/share/cmake-3.0/Modules/FindosgParticle.cmake
# /usr/share/cmake-3.0/Modules/FindosgPresentation.cmake
# /usr/share/cmake-3.0/Modules/FindosgProducer.cmake
# /usr/share/cmake-3.0/Modules/FindosgQt.cmake
# /usr/share/cmake-3.0/Modules/FindosgShadow.cmake
# /usr/share/cmake-3.0/Modules/FindosgSim.cmake
# /usr/share/cmake-3.0/Modules/FindosgTerrain.cmake
# /usr/share/cmake-3.0/Modules/FindosgText.cmake
# /usr/share/cmake-3.0/Modules/FindosgUtil.cmake
# /usr/share/cmake-3.0/Modules/FindosgViewer.cmake
# /usr/share/cmake-3.0/Modules/FindosgVolume.cmake
# /usr/share/cmake-3.0/Modules/FindosgWidget.cmake

