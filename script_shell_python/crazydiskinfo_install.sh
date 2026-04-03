#! /bin/bash
[[ $EUID -ne 0 ]] && echo 'Error: This script must be run as root!' && exit 1
install_path=/home/uos/crazydiskinfo
if [ ! -f $install_path/CMakeLists.txt ]; then
                echo crazydiskinfo nor exist , loading install 
        apt-get install libatasmart-dev libncurses5-dev libncursesw5-dev git cmake
        cd /home/uos
        git clone https://github.com/otakuto/crazydiskinfo
        sleep 5
        rm -rf $install_path/CMakeLists.txt
dd of=$install_path/CMakeLists.txt << EOF
cmake_minimum_required(VERSION 2.8.0)
option(RAW_VALUES_DEC "Display Raw Values in Decimal instead of Hex" OFF)
project(CrazyDiskInfo CXX)
add_executable(CrazyDiskInfo main.cpp)
set(CMAKE_CXX_FLAGS "-Wall -std=c++11")
SET_TARGET_PROPERTIES(CrazyDiskInfo PROPERTIES OUTPUT_NAME crazy)
target_link_libraries(CrazyDiskInfo atasmart)
target_link_libraries(CrazyDiskInfo ncursesw)
INSTALL(TARGETS CrazyDiskInfo RUNTIME DESTINATION /usr/sbin)
EOF
cd $install_path
mkdir build
cd build
cmake ..
make && make install
sleep 2
        echo crazydisk install done ,  you can try used commands to run it ,  as sudo crazy

else
        echo  crazydisk in $install_path is exist , you can try used commands to run it , as sudo crazy 
fi   	
