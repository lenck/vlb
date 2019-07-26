CMAKE_MINIMUM_REQUIRED(VERSION 2.8.11)
IF(COMMAND CMAKE_POLICY)
  CMAKE_POLICY(SET CMP0003 NEW)
ENDIF(COMMAND CMAKE_POLICY)

set(PROJECT_NAME "Lib, Demo, and Detector")
project(${PROJECT_NAME})

find_package(OpenCV REQUIRED)

add_subdirectory (Lib)
add_subdirectory (Detector)
add_subdirectory (Demo)
