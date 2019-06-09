import os

from conans import ConanFile, CMake, tools, RunEnvironment


class SociTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    # TODO: Remove requires.
    requires = (
        ("libpq/9.6.9@bincrafters/stable"), # SOCI PostgreSQL backend
        ("mysql-connector-c/6.1.11@bincrafters/stable"), # SOCI MySQL backend
        ("OpenSSL/1.0.2p@conan/stable"), # dependency: libpq, mysql-connector-c
        ("zlib/1.2.11@conan/stable") # dependency: libpq, mysql-connector-c
    )
    # TODO: remove backend options, dependency options
    default_options = {
        "SOCI:shared": False,
        # backend options
        "SOCI:with_postgresql": True,
        "SOCI:with_mysql": True,

        # dependency options
        "libpq:shared": False,
        "libpq:with_openssl": True,
        "libpq:with_zlib": True,
        "mysql-connector-c:shared": False,
        "mysql-connector-c:with_ssl": True,
        "mysql-connector-c:with_zlib": True,
        "OpenSSL:shared": False,
        "zlib:shared": False,
        "zlib:minizip": False
    }

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        build_type = self.settings.build_type

        test_command = "ctest --output-on-failure --build-config %s" % (build_type,)

        self.run(test_command, run_environment=True)
