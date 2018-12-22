import os

from conans import ConanFile, CMake, tools, RunEnvironment


class SociTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

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
        env_build = RunEnvironment(self)

        with tools.environment_append(env_build.vars):
            if self.settings.os == "Macos":
                # DYLD_LIBRARY_PATH environment variable is not directly transferred to the child process.
                # https://docs.conan.io/en/latest/reference/build_helpers/run_environment.html
                dyld_library_path = os.environ["DYLD_LIBRARY_PATH"]
                self.run("DYLD_LIBRARY_PATH=%s ctest --output-on-failure --build-config %s" % (dyld_library_path, build_type))
            else:
                self.run("ctest --output-on-failure --build-config %s" % build_type)
