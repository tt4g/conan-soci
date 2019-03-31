cmake_minimum_required(VERSION 3.4.0)
project(conan-soci)

include(conanbuildinfo.cmake)
conan_basic_setup()

# Fixes: https://github.com/SOCI/soci/pull/712
# Unused CMake variables DB2_LIBRARIES, ORACLE_LIBRARIES, POSTGRESQL_LIBRARY,
# SQLITE3_LIBRARY.
if(DEFINED DB2_LIBRARIES)
  set(DB2_LIBRARY ${DB2_LIBRARIES})
endif()

if(DEFINED ORACLE_LIBRARIES)
  set(ORACLE_LIBRARY ${ORACLE_LIBRARIES})
endif()

if(DEFINED POSTGRESQL_LIBRARIES)
  set(POSTGRESQL_LIBRARY ${POSTGRESQL_LIBRARIES})
endif()

if(DEFINED SQLITE3_LIBRARIES)
  set(SQLITE3_LIBRARY ${SQLITE3_LIBRARIES})
endif()

add_subdirectory(source_subfolder)
