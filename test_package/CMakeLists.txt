cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # SOCI need to enable c++11 standard for clang or apple clang.
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
endif()

if(("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU") OR (CMAKE_CXX_COMPILER_ID MATCHES "Clang"))
  # include/soci/rowset.h: warning: ‘template<class> class std::auto_ptr’ is deprecated [-Wdeprecated-declarations]
  #     const cxx_details::auto_ptr<statement> st_;
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations")
endif()

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
