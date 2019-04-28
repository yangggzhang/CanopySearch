# Install script for directory: /home/zy/Documents/RobotAutonomy/project/src/autonomy_grasp/external/dynamixel-workbench/dynamixel_workbench_single_manager_gui

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/zy/Documents/RobotAutonomy/project/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/zy/Documents/RobotAutonomy/project/build/autonomy_grasp/external/dynamixel-workbench/dynamixel_workbench_single_manager_gui/catkin_generated/installspace/dynamixel_workbench_single_manager_gui.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dynamixel_workbench_single_manager_gui/cmake" TYPE FILE FILES
    "/home/zy/Documents/RobotAutonomy/project/build/autonomy_grasp/external/dynamixel-workbench/dynamixel_workbench_single_manager_gui/catkin_generated/installspace/dynamixel_workbench_single_manager_guiConfig.cmake"
    "/home/zy/Documents/RobotAutonomy/project/build/autonomy_grasp/external/dynamixel-workbench/dynamixel_workbench_single_manager_gui/catkin_generated/installspace/dynamixel_workbench_single_manager_guiConfig-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dynamixel_workbench_single_manager_gui" TYPE FILE FILES "/home/zy/Documents/RobotAutonomy/project/src/autonomy_grasp/external/dynamixel-workbench/dynamixel_workbench_single_manager_gui/package.xml")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/dynamixel_workbench_single_manager_gui/dynamixel_workbench_single_manager_gui" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/dynamixel_workbench_single_manager_gui/dynamixel_workbench_single_manager_gui")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/dynamixel_workbench_single_manager_gui/dynamixel_workbench_single_manager_gui"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/dynamixel_workbench_single_manager_gui" TYPE EXECUTABLE FILES "/home/zy/Documents/RobotAutonomy/project/devel/lib/dynamixel_workbench_single_manager_gui/dynamixel_workbench_single_manager_gui")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/dynamixel_workbench_single_manager_gui/dynamixel_workbench_single_manager_gui" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/dynamixel_workbench_single_manager_gui/dynamixel_workbench_single_manager_gui")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/dynamixel_workbench_single_manager_gui/dynamixel_workbench_single_manager_gui"
         OLD_RPATH "/home/zy/Documents/RobotAutonomy/project/devel/lib:/opt/ros/kinetic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/dynamixel_workbench_single_manager_gui/dynamixel_workbench_single_manager_gui")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/dynamixel_workbench_single_manager_gui" TYPE DIRECTORY FILES "/home/zy/Documents/RobotAutonomy/project/src/autonomy_grasp/external/dynamixel-workbench/dynamixel_workbench_single_manager_gui/include/dynamixel_workbench_single_manager_gui/")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/dynamixel_workbench_single_manager_gui" TYPE DIRECTORY FILES
    "/home/zy/Documents/RobotAutonomy/project/src/autonomy_grasp/external/dynamixel-workbench/dynamixel_workbench_single_manager_gui/resources"
    "/home/zy/Documents/RobotAutonomy/project/src/autonomy_grasp/external/dynamixel-workbench/dynamixel_workbench_single_manager_gui/ui"
    )
endif()

