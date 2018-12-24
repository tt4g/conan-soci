cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # SOCI need to enable c++11 standard for clang or apple clang.
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
endif()

add_executable(soci_empty_backend soci_empty_backend.cpp)
target_link_libraries(soci_empty_backend ${CONAN_LIBS})

enable_testing()
add_test(
  NAME soci_empty_backend
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
  COMMAND "$<TARGET_FILE:soci_empty_backend>"
)
