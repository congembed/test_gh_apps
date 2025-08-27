from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
import os

class ProjectConan(ConanFile):
    name = "project"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"
    exports_sources = "*"

    def layout(self):
        cmake_layout(self)

    def build(self):
        # Find the first folder that contains main.cpp as the source folder
        source_folder = None
        for root, dirs, files in os.walk(self.source_folder):
            if "main.cpp" in files:
                source_folder = root
                break
        if not source_folder:
            raise Exception("No folder containing main.cpp found")

        cmake = CMake(self)
        cmake.configure(build_script_folder=source_folder)
        cmake.build()

    def package(self):
        # Copy everything from the source folder to the package
        self.copy("*", dst=".", src=".")

    def package_info(self):
        self.cpp_info.libs = ["project"]
