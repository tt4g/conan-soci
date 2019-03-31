cmake_minimum_required(VERSION 3.4.0)
project(conan-soci)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory(source_subfolder)
