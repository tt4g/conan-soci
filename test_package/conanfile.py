from conans import ConanFile, CMake, tools, RunEnvironment


class SociTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    default_options = {
        "SOCI:with_postgresql": True,
        "SOCI:with_mysql": True,
        "SOCI:with_boost": False
    }

    def requirements(self):
        if tools.os_info.is_windows:
            # NOTE: The version of OpenSSL is in conflict between
            #       libpq/9.6.9 and mysql-connector-c/6.1.11,
            #       This problem should be resolved by consumers overriding the
            #       OpenSSL version.
            self.requires("OpenSSL/1.0.2s@conan/stable")

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
        test_command = "ctest --output-on-failure --build-config %s" \
                        % (self.settings.build_type,)

        self.run(test_command, run_environment=True)

