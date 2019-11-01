cmake_minimum_required(VERSION 2.8.11)
project(test_package CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

enable_testing()

function(setup_ctest target)
  target_link_libraries(${target}
    PUBLIC
      ${CONAN_LIBS})
  # include/soci/rowset.h: warning: ‘template<class> class std::auto_ptr’ is deprecated [-Wdeprecated-declarations]
  #     const cxx_details::auto_ptr<statement> st_;
  target_compile_options(${target}
    PUBLIC
      $<$<CXX_COMPILER_ID:GNU>:-Wno-deprecated-declarations>
      $<$<CXX_COMPILER_ID:Clang>:-Wno-deprecated-declarations>
      $<$<CXX_COMPILER_ID:AppleClang>:-Wno-deprecated-declarations>)

  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set_property(TARGET ${target} PROPERTY CXX_STANDARD ON)
    set_property(TARGET ${target} PROPERTY CXX_STANDARD_REQUIRED ON)
  endif()

  add_test(NAME ${target}
    WORKING_DIRECTORY $<TARGET_FILE_DIR:${target}>
    COMMAND $<TARGET_FILE:${target}>)
endfunction()

add_executable(soci_empty_backend soci_empty_backend.cpp)
setup_ctest(soci_empty_backend)

add_executable(soci_mysql_backend soci_mysql_backend.cpp)
setup_ctest(soci_mysql_backend)

add_executable(soci_postgresql_backend soci_postgresql_backend.cpp)
setup_ctest(soci_postgresql_backend)
