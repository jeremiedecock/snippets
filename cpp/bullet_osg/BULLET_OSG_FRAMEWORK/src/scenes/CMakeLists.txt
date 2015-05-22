# Copyright (c) 2015 Jérémie DECOCK

# Define the config_and_add_executable macro
macro(config_and_add_executable EXEC_NAME SRC_FILE)
    # Add executable
    add_executable(${EXEC_NAME} ${SRC_FILE})

    # Link to the internal libraries
    # See http://stackoverflow.com/questions/12204820/cmake-and-order-dependent-linking-of-shared-libraries
    target_link_libraries(${EXEC_NAME} builtin_objects builtin_parts controllers actuators joint_slots joints sensors parts core tools)

    # Link to Boost libraries
    target_link_libraries(${EXEC_NAME} ${Boost_LIBRARIES})

    # Link to Bullet
    target_link_libraries(${EXEC_NAME} ${BULLET_LIBRARIES})

    # Link to OSG
    target_link_libraries(${EXEC_NAME} ${OPENSCENEGRAPH_LIBRARIES})
endmacro()

# EXECUTABLES #######################################################

# Set options
option(BUILD_DEMO "Build the default demo (falling cubes)." ON)
option(BUILD_CUBES_1 "Build the falling cubes demo (4 falling cubes with various sizes and weights)." OFF)
option(BUILD_FALLING_SPHERE "Build the falling sphere demo (1 falling sphere)." OFF)
option(BUILD_PENDULUM_HINGE "Build the pendulum demo (using hinge joints)." OFF)
option(BUILD_PENDULUM_P2P "Build the pendulum demo (using point_to_point joints)." OFF)
option(BUILD_PENDULUM_MOTOR "Build the pendulum demo (using motor actuator)." OFF)
option(BUILD_ROBUDOG_JD "Build the robudog demo (JD's version)." OFF)

# Set executables
if(BUILD_DEMO)
    config_and_add_executable(demo demo.cc)
endif(BUILD_DEMO)

if(BUILD_CUBES_1)
    config_and_add_executable(cubes_1 cubes_1.cc)
endif(BUILD_CUBES_1)

if(BUILD_FALLING_SPHERE)
    config_and_add_executable(falling_sphere falling_sphere.cc)
endif(BUILD_FALLING_SPHERE)

if(BUILD_PENDULUM_HINGE)
    config_and_add_executable(pendulum_hinge pendulum_hinge.cc)
endif(BUILD_PENDULUM_HINGE)

if(BUILD_PENDULUM_P2P)
    config_and_add_executable(pendulum_point_to_point pendulum_point_to_point.cc)
endif(BUILD_PENDULUM_P2P)

if(BUILD_PENDULUM_MOTOR)
    config_and_add_executable(pendulum_motor pendulum_motor.cc)
endif(BUILD_PENDULUM_MOTOR)

if(BUILD_ROBUDOG_JD)
    config_and_add_executable(robudog_jd robudog_jd.cc)
endif(BUILD_ROBUDOG_JD)
