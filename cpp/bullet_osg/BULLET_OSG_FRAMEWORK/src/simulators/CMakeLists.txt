# Copyright (c) 2015 Jérémie DECOCK

set(EXEC_NAME simulator)

add_executable(${EXEC_NAME} simulator.cc)

# Internal libraries
target_link_libraries(${EXEC_NAME} core parts tools)

# Bullet
target_link_libraries(${EXEC_NAME} ${BULLET_LIBRARIES})

# OSG
target_link_libraries(${EXEC_NAME} ${OPENSCENEGRAPH_LIBRARIES})

