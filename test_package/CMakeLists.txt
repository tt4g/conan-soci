cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

enable_testing()

add_executable(soci_empty_backend soci_empty_backend.cpp)
target_link_libraries(soci_empty_backend ${CONAN_LIBS})

add_test(
  NAME soci_empty_backend
  WORKING_DIRECTORY "$<TARGET_FILE_DIR:soci_empty_backend>"
  COMMAND "$<TARGET_FILE:soci_empty_backend>"
)

add_executable(soci_mysql_backend soci_mysql_backend.cpp)
target_link_libraries(soci_mysql_backend ${CONAN_LIBS})

add_test(
  NAME soci_mysql_backend
  WORKING_DIRECTORY "$<TARGET_FILE_DIR:soci_mysql_backend>"
  COMMAND "$<TARGET_FILE:soci_mysql_backend>"
)

add_executable(soci_postgresql_backend soci_postgresql_backend.cpp)
target_link_libraries(soci_postgresql_backend ${CONAN_LIBS})

add_test(
  NAME soci_postgresql_backend
  WORKING_DIRECTORY "$<TARGET_FILE_DIR:soci_postgresql_backend>"
  COMMAND "$<TARGET_FILE:soci_postgresql_backend>"
)
