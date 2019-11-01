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
        "with_db2": [True, False],
        "with_firebird": [True, False],
        "soci_firebird_embedded": [True, False],
        "with_mysql": [True, False],
        "with_odbc": [True, False],
        "with_oracle": [True, False],
        "with_postgresql": [True, False],
        "soci_postgresql_nosinglerowmode": [True, False],
        "with_sqlite3": [True, False]
    }
    default_options = {
        "shared": False,
        "soci_cxx_c11":  False,
        "soci_tests": False,
        "with_boost": True,
        "soci_empty": True,
        "with_db2": False,
        "with_firebird": False,
        "soci_firebird_embedded": False,
        "with_mysql": False,
        "with_odbc": False,
        "with_oracle": False,
        "with_postgresql": False,
        "soci_postgresql_nosinglerowmode": False,
        "with_sqlite3": False
    }
    generators = "cmake", "cmake_find_package"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        if self.options.with_boost:
            self.requires("boost/1.70.0")

        if self.options.with_db2:
            # conan db2 library not found.
            pass

        if self.options.with_firebird:
            # conan firebird library not found.
            pass

        if self.options.with_mysql:
            self.requires("mysql-connector-c/6.1.11")

        if self.options.with_odbc:
            self.requires("odbc/2.3.7")

        if self.options.with_oracle:
            # conan oracle library not found.
            pass

        if self.options.with_postgresql:
            self.requires("libpq/11.5")

        if self.options.with_sqlite3:
            self.requires("sqlite3/3.29.0")

    def source(self):
        # TODO: get source from archive after SOCI 4.0.0 released.
        # source_url = "https://github.com/SOCI/soci"
        # tools.get("{0}/archive/{1}.tar.gz", source_url, self.version)
        # extracted_dir = self.name + "-" + self.version
        # os.rename(extracted_dir, self._source_subfolder)
        git = tools.Git(folder=self._source_subfolder)
        git.clone(url="https://github.com/SOCI/soci.git", branch="master")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake = CMake(self)

        self._cmake.definitions["SOCI_SHARED"] = self.options.shared
        self._cmake.definitions["SOCI_STATIC"] = not self.options.shared
        self._cmake.definitions["SOCI_CXX_C11"] = self.options.soci_cxx_c11
        self._cmake.definitions["SOCI_TESTS"] = self.options.soci_tests
        self._cmake.definitions["WITH_BOOST"] = self.options.with_boost
        self._cmake.definitions["SOCI_EMPTY"] = self.options.soci_empty
        self._cmake.definitions["WITH_DB2"] = self.options.with_db2
        self._cmake.definitions["WITH_FIREBIRD"] = self.options.with_firebird
        self._cmake.definitions["SOCI_FIREBIRD_EMBEDDED"] = \
                self.options.soci_firebird_embedded
        self._cmake.definitions["WITH_MYSQL"] = self.options.with_mysql
        self._cmake.definitions["WITH_ODBC"] = self.options.with_odbc
        self._cmake.definitions["WITH_ORACLE"] = self.options.with_oracle
        self._cmake.definitions["WITH_POSTGRESQL"] = self.options.with_postgresql
        self._cmake.definitions["SOCI_POSTGRESQL_NOSINGLEROWMODE"] = \
                self.options.soci_postgresql_nosinglerowmode
        self._cmake.definitions["WITH_SQLITE3"] = self.options.with_sqlite3

        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE_1_0.txt*", dst="licenses", src=self._source_subfolder)

        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        # library name has prefix "lib".
        lib_prefix = "lib" if tools.os_info.is_windows and not self.options.shared else ""
        # Library name has suffix ABI version if Windows.
        # It's SOCI major and minor of version.
        lib_suffix = "_%s_%s" % tuple(self.version.split(".")[0:2]) if tools.os_info.is_windows else ""

        lib_name_args = (lib_prefix, lib_suffix)

        self.cpp_info.includedirs = ["include"]

        if os.path.exists(os.path.join(self.package_folder, "lib64")):
            self.cpp_info.libdirs = ["lib64"]
        else:
            self.cpp_info.libdirs = ["lib"]

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
        # Add to the end of the library list so that soci_core is linked last.
        self.cpp_info.libs.append("%ssoci_core%s" % lib_name_args)
