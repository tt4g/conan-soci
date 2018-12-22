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
        lib_dir = "lib"
        if self.settings.os != "Windows":
            if str(self.settings.arch) in ["x86_64", "ppc64", "ppc64le", "mips64", "armv8", "sparcv9"]:
                lib_dir = "lib64"

        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src=lib_dir)
        self.copy("*.so*", dst="bin", src=lib_dir)

    def test(self):
        build_type = self.settings.build_type
        env_build = RunEnvironment(self)

        with tools.environment_append(env_build.vars):
            if self.settings.os == "Macos":
                # DYLD_LIBRARY_PATH environment variable is not directly transferred to the child process.
                # https://docs.conan.io/en/latest/reference/build_helpers/run_environment.html
                dyld_library_path = os.environ["DYLD_LIBRARY_PATH"]
                self.run("DYLD_LIBRARY_PATH=%s ctest --output-on-failure --build-config %s" % (dyld_library_path, build_type))
            elif self.settings.os == "Windows":
                self.run("ctest --output-on-failure --build-config %s" % build_type)
            else:
                ld_library_path = os.environ["LD_LIBRARY_PATH"]
                self.run("LD_LIBRARY_PATH=%s ctest --output-on-failure --build-config %s" % (ld_library_path, build_type))
