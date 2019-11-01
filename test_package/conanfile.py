from conans import ConanFile, CMake, tools, RunEnvironment


class SociTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    default_options = {
        "SOCI:with_postgresql": True,
        "SOCI:with_mysql": True,
        "SOCI:with_boost": True
    }

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            test_command = "ctest --output-on-failure --build-config %s" \
                            % (self.settings.build_type,)

            self.run(test_command, cwd="bin", run_environment=True)

