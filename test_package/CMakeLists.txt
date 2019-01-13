cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # SOCI need to enable c++11 standard for clang or apple clang.
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
endif()

add_executable(conan_soci_backend_test
  soci_empty_backend.cpp
  soci_mysql_backend.cpp
  soci_postgresql_backend.cpp
)
target_link_libraries(conan_soci_backend_test ${CONAN_LIBS})

enable_testing()
add_test(
  NAME conan_soci_backend_test
  WORKING_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
  COMMAND "$<TARGET_FILE:conan_soci_backend_test>"
)
