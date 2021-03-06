#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    short_paths = True

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        bin_path = os.path.join("bin", "test_package")
        if self.settings.os == "Windows":
            bin_path += '.exe'
        try:
            if self.settings.os == "Macos":
                self.run('DYLD_LIBRARY_PATH=%s:%s' % (os.environ['DYLD_LIBRARY_PATH'], bin_path))
            else:
                self.run(bin_path)
        except Exception as e:
            self.output.warn("Test failed with error: %s" % e)
            self.output.info("current path: %s " % os.path.abspath(os.curdir))
            self.output.info("executable: %s" % bin_path)
            self.output.info("contents of ./bin: %s" % (os.listdir("bin")))
            raise e

