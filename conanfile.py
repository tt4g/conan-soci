from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment, MSBuild
import os


class SociConan(ConanFile):
    name = "SOCI"
    version = "4.0.0"
    license = "Boost Software License - Version 1.0"
    author = "tt4g"
    url = "https://github.com/tt4g/conan-soci"
    description = """SOCI is a database access library written in C++
 that makes an illusion of embedding SQL queries in the regular C++ code,
 staying entirely within the Standard C++."""
    homepage = "http://soci.sourceforge.net/"
    topics = ("conan", "soci", "sql")
    exports = ["LICENSE"]
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "soci_cxx_c11": [True, False],
        "soci_static": [True, False],
        "soci_tests": [True, False],
        "with_boost": [True, False],
        "soci_empty": [True, False],
        "soci_empty_test_connstr": "ANY",
        "with_db2": [True, False],
        "db2_include_dir": "ANY",
        "db2_libraries": "ANY",
        "soci_db2_test_connstr": "ANY",
        "with_firebird": [True, False],
        "firebird_include_dir": "ANY",
        "firebird_libraries": "ANY",
        "soci_firebird_test_connstr": "ANY",
        "soci_firebird_embedded": [True, False],
        "with_mysql": [True, False],
        "mysql_dir": "ANY",
        "mysql_include_dir": "ANY",
        "mysql_libraries": "ANY",
        "soci_mysql_test_connstr": "ANY",
        "with_odbc": [True, False],
        "odbc_include_dir": "ANY",
        "odbc_libraries": "ANY",
        "soci_odbc_test_access_connstr": "ANY",
        "soci_odbc_test_mysql_connstr": "ANY",
        "soci_odbc_test_postgresql_connstr": "ANY",
        "with_oracle": [True, False],
        "oracle_include_dir": "ANY",
        "oracle_libraries": "ANY",
        "soci_oracle_test_connstr": "ANY",
        "with_postgresql": [True, False],
        "postgresql_include_dir": "ANY",
        "postgresql_libraries": "ANY",
        "soci_postgresql_test_connstr": "ANY",
        "soci_postgresql_nosinglerowmode": [True, False],
        "with_sqlite3": [True, False],
        "sqlite_include_dir": "ANY",
        "sqlite_libraries": "ANY",
        "soci_sqlite_test_connstr": "ANY"
    }
    default_options = {
        "soci_cxx_c11":  False,
        "soci_static": False,
        "soci_tests": True,
        "with_boost": True,
        "soci_empty": True,
        "soci_empty_test_connstr": None,
        "with_db2": False,
        "db2_include_dir": None,
        "db2_libraries": None,
        "soci_db2_test_connstr": None,
        "with_firebird": False,
        "firebird_include_dir": None,
        "firebird_libraries": None,
        "soci_firebird_test_connstr": None,
        "soci_firebird_embedded": False,
        "with_mysql": False,
        "mysql_dir": None,
        "mysql_include_dir": None,
        "mysql_libraries": None,
        "soci_mysql_test_connstr": None,
        "with_odbc": False,
        "odbc_include_dir": None,
        "odbc_libraries": None,
        "soci_odbc_test_access_connstr": None,
        "soci_odbc_test_mysql_connstr": None,
        "soci_odbc_test_postgresql_connstr": None,
        "with_oracle": False,
        "oracle_include_dir": None,
        "oracle_libraries": None,
        "soci_oracle_test_connstr": None,
        "with_postgresql": False,
        "postgresql_include_dir": None,
        "postgresql_libraries": None,
        "soci_postgresql_test_connstr": None,
        "soci_postgresql_nosinglerowmode": False,
        "with_sqlite3": False,
        "sqlite_include_dir": None,
        "sqlite_libraries": None,
        "soci_sqlite_test_connstr": None
    }
    generators = "cmake"

    def source(self):
        # TODO get source from archive after SOCI 4.0.0 released.
        # source_url = "https://github.com/SOCI/soci"
        # tools.get("{0}/archive/{1}.tar.gz", source_url, self.version)

        self.run("git clone --depth 1 https://github.com/SOCI/soci.git")
        self.run("cd soci && git checkout master")

        tools.replace_in_file("soci/CMakeLists.txt", "project(SOCI)",
                              '''project(SOCI)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def _requires_db2(self):
        """check requires conan db2.

        :returns: true if require conan db2, otherwise false.
        :rtype: bool
        """
        # use db2 when not defined db2_include_dir and db2_libraries
        return (not self.options.db2_include_dir
                and not self.options.db2_libraries)

    def _requires_firebird(self):
        """check requires conan firebird.

        :returns: true if require conan firebird, otherwise false.
        :rtype: bool
        """
        # use firebird when not defined firebird_include_dir and firebird_libraries
        return (not self.options.firebird_include_dir
                and not self.options.firebird_libraries)

    def _requires_mysql(self):
        """check requires conan mysql.

        :returns: true if require conan mysql, otherwise false.
        :rtype: bool
        """
        # use mysql-connector-c package if _set_mysql_paths() is true.
        return self._set_mysql_paths()

    def _set_mysql_paths(self):
        """check CMake definition related to  MySQL backend path.

        :returns: true if set mysql libraries path, otherwise false.
        :rtype: bool
        """
        # if consumer not defined.
        return (not self.options.mysql_dir
                or (not self.options.mysql_include_dir
                    and not self.options.mysql_libraries))

    def _requires_odbc(self):
        """check requires conan odbc.

        :returns: true if require conan odbc, otherwise false.
        :rtype: bool
        """
        # use odbc when not defined odbc_include_dir and odbc_libraries
        return (not self.options.odbc_include_dir
                and not self.options.odbc_libraries)

    def _requires_oracle(self):
        """check requires conan oracle.

        :returns: true if require conan oracle, otherwise false.
        :rtype: bool
        """
        # use oracle when not defined oracle_include_dir and oracle_libraries
        return (not self.options.oracle_include_dir
                and not self.options.oracle_libraries)

    def _requires_libpq(self):
        """check requires conan libpq.

        :returns: true if require conan libpq, otherwise false.
        :rtype: bool
        """
        # use libpq package if _set_postgresql_paths() is true.
        return self._set_postgresql_paths()

    def _set_postgresql_paths(self):
        """check CMake definition related to  PostgreSQL backend path.

        :returns: true if set libpq libraries path, otherwise false.
        :rtype: bool
        """
        # if consumer not defined.
        return (not self.options.postgresql_include_dir
                and not self.options.postgresql_libraries)

    def _requires_sqlite3(self):
        """check requires conan sqlite3.

        :returns: true if require conan sqlite3, otherwise false.
        :rtype: bool
        """
        # use sqlite3 when not defined sqlite_include_dir and sqlite_libraries
        return (not self.options.sqlite_include_dir
                and not self.options.sqlite_libraries)

    def requirements(self):
        if self.options.with_boost:
            self.requires("boost/1.69.0@conan/stable")

        if self.options.with_db2:
            if self._requires_db2():
                # not found conan db2 library.
                pass

        if self.options.with_firebird:
            if self._requires_firebird():
                # not found conan firebird library.
                pass

        if self.options.with_mysql:
            if self._requires_mysql():
                self.requires("mysql-connector-c/6.1.11@bincrafters/stable")

        if self.options.with_odbc:
            if self._requires_odbc():
                self.requires("odbc/2.3.7@bincrafters/stable")

        if self.options.with_oracle:
            if self._requires_oracle():
                # not found conan oracle library.
                pass

        if self.options.with_postgresql:
            if self._requires_libpq():
                self.requires("libpq/9.6.9@bincrafters/stable")

        if self.options.with_sqlite3:
            if self._requires_sqlite3():
                self.requires("sqlite3/3.25.3@bincrafters/stable")

    def build(self):
        _is_os_windows = self.settings.os == "Windows"
        _lib_ext = "lib" if _is_os_windows else "so"

        cmake = CMake(self, build_type=self.settings.build_type)

        cmake.definitions["SOCI_CXX_C11"] = self.options.soci_cxx_c11
        cmake.definitions["SOCI_STATIC"] = self.options.soci_static
        cmake.definitions["SOCI_TESTS"] = self.options.soci_tests
        cmake.definitions["WITH_BOOST"] = self.options.with_boost

        cmake.definitions["SOCI_EMPTY"] = self.options.soci_empty
        if self.options.soci_empty:
            if self.options.soci_empty_test_connstr:
                cmake.definitions["SOCI_EMPTY_TEST_CONNSTR"] = \
                    self.options.soci_empty_test_connstr

        cmake.definitions["WITH_DB2"] = self.options.with_db2
        if self.options.with_db2:
            if not self._requires_db2():
                cmake.definitions["DB2_INCLUDE_DIR"] = \
                    self.options.db2_include_dir
                cmake.definitions["DB2_LIBRARIES"] = self.options.db2_libraries

            if self.options.soci_db2_test_connstr:
                cmake.definitions["SOCI_DB2_TEST_CONNSTR"] = \
                    self.options.soci_db2_test_connstr

        cmake.definitions["WITH_FIREBIRD"] = self.options.with_firebird
        if self.options.with_firebird:
            if self._requires_firebird():
                cmake.definitions["FIREBIRD_INCLUDE_DIR"] = \
                    self.options.firebird_include_dir
                cmake.definitions["FIREBIRD_LIBRARIES"] = \
                    self.options.firebird_libraries

            if self.options.soci_firebird_test_connstr:
                cmake.definitions["SOCI_FIREBIRD_TEST_CONNSTR"] = \
                    self.options.soci_firebird_test_connstr

            cmake.definitions["SOCI_FIREBIRD_EMBEDDED"] = \
                self.options.soci_firebird_embedded

        cmake.definitions["WITH_MYSQL"] = self.options.with_mysql
        if self.options.with_mysql:

            _mysql_dir = None
            _mysql_include_dir = None
            _mysql_libraries = None
            _mysql_lib_name = "libmysql" if _is_os_windows else "libmysqlclient"
            if self._set_mysql_paths():
                _mysql_include_dir = self.deps_cpp_info["mysql-connector-c"].include_paths[0]
                _mysql_libraries = os.path.join(
                    self.deps_cpp_info["mysql-connector-c"].lib_paths[0],
                    ("%s.%s" % (_mysql_lib_name, _lib_ext))
                )
            else:
                if self.options.mysql_dir:
                    _mysql_dir = self.options.mysql_dir

                if self.options.mysql_include_dir:
                    _mysql_include_dir = self.options.mysql_include_dir

                if self.options.mysql_libraries:
                    _mysql_libraries = self.options.mysql_libraries

            if _mysql_dir:
                cmake.definitions["MYSQL_DIR"] = _mysql_dir

            if _mysql_include_dir:
                cmake.definitions["MYSQL_INCLUDE_DIR"] = _mysql_include_dir

            if _mysql_libraries:
                cmake.definitions["MYSQL_LIBRARIES"] = _mysql_libraries

            if self.options.soci_mysql_test_connstr:
                cmake.definitions["SOCI_MYSQL_TEST_CONNSTR"] = \
                    self.options.soci_mysql_test_connstr

        cmake.definitions["WITH_ODBC"] = self.options.with_odbc
        if self.options.with_firebird:
            if self._requires_odbc():
                cmake.definitions["ODBC_INCLUDE_DIR"] = \
                    self.options.odbc_include_dir
                cmake.definitions["ODBC_LIBRARIES"] = \
                    self.options.odbc_libraries

            if self.options.soci_odbc_test_access_connstr:
                cmake.definitions["SOCI_ODBC_TEST_ACCESS_CONNSTR"] = \
                    self.options.soci_odbc_test_access_connstr

            if self.options.soci_odbc_test_mysql_connstr:
                cmake.definitions["SOCI_ODBC_TEST_MYSQL_CONNSTR"] = \
                    self.options.soci_odbc_test_mysql_connstr

            if self.options.soci_odbc_test_postgresql_connstr:
                cmake.definitions["SOCI_ODBC_TEST_POSTGRESQL_CONNSTR"] = \
                    self.options.soci_odbc_test_postgresql_connstr

        cmake.definitions["WITH_ORACLE"] = self.options.with_oracle
        if self.options.with_oracle:
            if self._requires_oracle():
                cmake.definitions["ORACLE_INCLUDE_DIR"] = \
                    self.options.oracle_include_dir
                cmake.definitions["ORACLE_LIBRARIES"] = \
                    self.options.oracle_libraries

            if self.options.soci_oracle_test_connstr:
                cmake.definitions["SOCI_ORACLE_TEST_CONNSTR"] = \
                    self.options.soci_oracle_test_connstr

        cmake.definitions["WITH_POSTGRESQL"] = self.options.with_postgresql
        if self.options.with_postgresql:

            _postgresql_include_dir = None
            _postgresql_libraries = None
            if self._set_postgresql_paths():
                _postgresql_include_dir = self.deps_cpp_info["libpq"].include_paths[0]
                _postgresql_libraries = os.path.join(
                    self.deps_cpp_info["libpq"].lib_paths[0], ("libpq.%s" % _lib_ext))

            else:
                _postgresql_include_dir = self.options.postgresql_include_dir
                _postgresql_libraries = self.options.postgresql_libraries

            if _postgresql_include_dir and _postgresql_libraries:
                cmake.definitions["POSTGRESQL_INCLUDE_DIR"] = _postgresql_include_dir

            if _postgresql_libraries:
                cmake.definitions["POSTGRESQL_LIBRARIES"] = _postgresql_libraries

            if self.options.soci_postgresql_test_connstr:
                cmake.definitions["SOCI_POSTGRESQL_TEST_CONNSTR"] = \
                    self.options.soci_postgresql_test_connstr

            if self.options.soci_postgresql_nosinglerowmode:
                cmake.definitions["SOCI_POSTGRESQL_NOSINGLEROWMODE"] = True

        cmake.definitions["WITH_SQLITE3"] = self.options.with_sqlite3
        if self.options.with_sqlite3:
            if self._requires_sqlite3():
                cmake.definitions["SQLITE_INCLUDE_DIR"] = \
                    self.options.sqlite_include_dir
                cmake.definitions["SQLITE_LIBRARIES"] = \
                    self.options.sqlite_libraries

            if self.options.soci_sqlite_test_connstr:
                cmake.definitions["SOCI_SQLITE3_TEST_CONNSTR"] = \
                    self.options.soci_sqlite_test_connstr

        cmake.configure(source_folder="soci")

        # Windows: msbuild
        # Unix: make && make install
        # http://soci.sourceforge.net/doc/master/installation/
        if self.settings.compiler == "Visual Studio":
            msbuild = MSBuild(self)
            msbuild.build(project_file="SOCI.sln")
        else:
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make()
            autotools.install()

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src="soci")
        self.copy(pattern="*.h", dst="include", src="include", keep_path=True)
        # copy header exclude backends
        self.copy(pattern="*.h", dst="include/soci", src="soci/include/soci",
                  keep_path=True,
                  excludes=("empty", "db2", "firebird", "mysql", "odbc",
                            "oracle", "postgresql", "sqlite3",))

        if self.options.soci_empty:
            self.copy(pattern="*.h", dst="include/soci/empty",
                      src="soci/include/soci/empty", keep_path=True)

        if self.options.with_db2:
            self.copy(pattern="*.h", dst="include/soci/db2",
                      src="soci/include/soci/db2", keep_path=True)

        if self.options.with_firebird:
            self.copy(pattern="*.h", dst="include/soci/firebird",
                      src="soci/include/soci/firebird", keep_path=True)

        if self.options.with_mysql:
            self.copy(pattern="*.h", dst="include/soci/mysql",
                      src="soci/include/soci/mysql", keep_path=True)

        if self.options.with_odbc:
            self.copy(pattern="*.h", dst="include/soci/odbc",
                      src="soci/include/soci/odbc", keep_path=True)

        if self.options.with_oracle:
            self.copy(pattern="*.h", dst="include/soci/oracle",
                      src="soci/include/soci/oracle", keep_path=True)

        if self.options.with_postgresql:
            self.copy(pattern="*.h", dst="include/soci/postgresql",
                      src="soci/include/soci/postgresql", keep_path=True)

        if self.options.with_sqlite3:
            self.copy(pattern="*.h", dst="include/soci/sqlite3",
                      src="soci/include/soci/sqlite3", keep_path=True)

        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        # Library name has suffix ABI version if Windows.
        # It's SOCI major and minor of version.
        lib_suffix = "_%s_%s" % tuple(self.version.split(".")[0:2]) if self.settings.os == "Windows" else ""

        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["soci_core%s" % lib_suffix]

        if self.options.soci_empty:
            self.cpp_info.libs.append("soci_empty%s" % lib_suffix)

        if self.options.with_db2:
            self.cpp_info.libs.append("soci_db2%s" % lib_suffix)

        if self.options.with_firebird:
            self.cpp_info.libs.append("soci_firebird%s" % lib_suffix)

        if self.options.with_mysql:
            self.cpp_info.libs.append("soci_mysql%s" % lib_suffix)

        if self.options.with_odbc:
            self.cpp_info.libs.append("soci_odbc%s" % lib_suffix)

        if self.options.with_oracle:
            self.cpp_info.libs.append("soci_oracle%s" % lib_suffix)

        if self.options.with_postgresql:
            self.cpp_info.libs.append("soci_postgresql%s" % lib_suffix)

        if self.options.with_sqlite3:
            self.cpp_info.libs.append("soci_sqlite3%s" % lib_suffix)
