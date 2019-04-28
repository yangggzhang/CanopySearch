#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/zy/Documents/RobotAutonomy/project/src/autonomy_grasp/external/DynamixelSDK/ros"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/zy/Documents/RobotAutonomy/project/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/zy/Documents/RobotAutonomy/project/install/lib/python2.7/dist-packages:/home/zy/Documents/RobotAutonomy/project/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/zy/Documents/RobotAutonomy/project/build" \
    "/usr/bin/python" \
    "/home/zy/Documents/RobotAutonomy/project/src/autonomy_grasp/external/DynamixelSDK/ros/setup.py" \
    build --build-base "/home/zy/Documents/RobotAutonomy/project/build/autonomy_grasp/external/DynamixelSDK/ros" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/zy/Documents/RobotAutonomy/project/install" --install-scripts="/home/zy/Documents/RobotAutonomy/project/install/bin"
