cmake_minimum_required(VERSION 2.6)

project(bullet_cmake_hello)

# Find and setup Bullet for this project
find_package(Bullet)

# Bullet includes
include_directories(${BULLET_INCLUDE_DIRS})

# Tell CMake to create the helloworld executable
add_executable(hello hello.cc)

# Bullet libs
target_link_libraries(hello ${BULLET_LIBRARIES})
