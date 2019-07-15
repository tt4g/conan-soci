from conans import ConanFile, CMake, tools
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
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "soci_cxx_c11": [True, False],
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
        "shared": True,
        "soci_cxx_c11":  False,
        "soci_tests": False,
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
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

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

    def configure(self):
        if (self._requires_mysql() and self.options.shared
            and self.settings.os != "Windows"):
            # If use mysql-connector-c and SOCI:shared=True on UNIX-like OS,
            # link failed by ld command: "relocation R_X86_64_PC32 against symbol
            # `key_memory_mysql_options' can not be used when making a shared
            #  object; recompile with -fPIC
            # /usr/bin/ld: final link failed: Bad value"
            self.options["mysql-connector-c"].shared = True

    def requirements(self):
        if self.options.with_boost:
            self.requires("boost/1.70.0@conan/stable")

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

    def source(self):
        # TODO: get source from archive after SOCI 4.0.0 released.
        # source_url = "https://github.com/SOCI/soci"
        # tools.get("{0}/archive/{1}.tar.gz", source_url, self.version)
        # extracted_dir = self.name + "-" + self.version
        # os.rename(extracted_dir, self._source_subfolder)

        git = tools.Git(folder=self._source_subfolder)
        git.clone(url="https://github.com/SOCI/soci.git", branch="master")

    def _configure_cmake(self):
        _is_os_windows = self.settings.os == "Windows"
        _shared_lib_ext = "lib" if _is_os_windows else "so"
        _static_lib_ext = "lib" if _is_os_windows else "a"

        cmake = CMake(self)

        cmake.definitions["SOCI_SHARED"] = self.options.shared
        cmake.definitions["SOCI_STATIC"] = not self.options.shared
        cmake.definitions["SOCI_CXX_C11"] = self.options.soci_cxx_c11
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

            _mysql_lib_name = None
            if _is_os_windows:
                _mysql_lib_name = "libmysql" if self.options["mysql-connector-c"].shared else "mysqlclient"
            else:
                _mysql_lib_name = "libmysqlclient"

            _mysql_lib_ext = _shared_lib_ext if self.options["mysql-connector-c"].shared else _static_lib_ext

            if self._set_mysql_paths():
                _mysql_include_dir = self.deps_cpp_info["mysql-connector-c"].include_paths[0]
                _mysql_libraries = os.path.join(
                    self.deps_cpp_info["mysql-connector-c"].lib_paths[0],
                    ("%s.%s" % (_mysql_lib_name, _mysql_lib_ext))
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
            _postgresql_lib_ext = _shared_lib_ext if self.options["libpq"].shared else _static_lib_ext
            if self._set_postgresql_paths():
                _postgresql_include_dir = self.deps_cpp_info["libpq"].include_paths[0]
                _postgresql_libraries = os.path.join(
                    self.deps_cpp_info["libpq"].lib_paths[0], ("libpq.%s" % _postgresql_lib_ext))

            else:
                _postgresql_include_dir = self.options.postgresql_include_dir
                _postgresql_libraries = self.options.postgresql_libraries

            if _postgresql_include_dir:
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

        # Fixes: https://github.com/SOCI/soci/pull/712
        # Unused CMake variables DB2_LIBRARIES, ORACLE_LIBRARIES, POSTGRESQL_LIBRARY,
        # SQLITE3_LIBRARY.
        if "DB2_LIBRARIES" in cmake.definitions:
            cmake.definitions["DB2_LIBRARY"] = cmake.definitions["DB2_LIBRARIES"]

        if "ORACLE_LIBRARIES" in cmake.definitions:
            cmake.definitions["ORACLE_LIBRARY"] = cmake.definitions["ORACLE_LIBRARIES"]

        if "POSTGRESQL_LIBRARIES" in cmake.definitions:
            cmake.definitions["POSTGRESQL_LIBRARY"] = cmake.definitions["POSTGRESQL_LIBRARIES"]

        if "SQLITE3_LIBRARIES" in cmake.definitions:
            cmake.definitions["SQLITE3_LIBRARY"] = cmake.definitions["SQLITE3_LIBRARIES"]

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE_1_0.txt*", dst="licenses", src=self._source_subfolder)

        cmake = self._configure_cmake()
        cmake.install()

    def _architecture_model(self):
        """This _architecture_model was borrowed from conan-boost.

        * conan-boost: https://github.com/conan-community/conan-boost
        * _b2_architecture: https://github.com/conan-community/conan-boost/blob/8ecc8350b9dfaee5d277218f6d6118052b08a386/conanfile.py#L430

        Copyright (c) 2017-2019 JFrog LTD

        MIT LICENSE

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
        WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
        CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        """

        if str(self.settings.arch) in ["x86_64", "ppc64", "ppc64le", "mips64", "armv8", "sparcv9"]:
            return "64"
        else:
            return "32"

    def package_info(self):
        # library name has prefix "lib".
        lib_prefix = "lib" if self.settings.os == "Windows" and not self.options.shared else ""
        # Library name has suffix ABI version if Windows.
        # It's SOCI major and minor of version.
        lib_suffix = "_%s_%s" % tuple(self.version.split(".")[0:2]) if self.settings.os == "Windows" else ""

        lib_name_args = (lib_prefix, lib_suffix)

        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib64"] if self._architecture_model() == "64" else ["lib"]

        if self.options.soci_empty:
            self.cpp_info.libs.append("%ssoci_empty%s" % lib_name_args)

        if self.options.with_db2:
            self.cpp_info.libs.append("%ssoci_db2%s" % lib_name_args)

        if self.options.with_firebird:
            self.cpp_info.libs.append("%ssoci_firebird%s" % lib_name_args)

        if self.options.with_mysql:
            self.cpp_info.libs.append("%ssoci_mysql%s" % lib_name_args)

        if self.options.with_odbc:
            self.cpp_info.libs.append("%ssoci_odbc%s" % lib_name_args)

        if self.options.with_oracle:
            self.cpp_info.libs.append("%ssoci_oracle%s" % lib_name_args)

        if self.options.with_postgresql:
            self.cpp_info.libs.append("%ssoci_postgresql%s" % lib_name_args)

        if self.options.with_sqlite3:
            self.cpp_info.libs.append("%ssoci_sqlite3%s" % lib_name_args)

        # All backend libraries of SOCI depend on soci_core.
        # Add to the end of the library list so that soci_core is linked last. when linking.
        self.cpp_info.libs.append("%ssoci_core%s" % lib_name_args)
