from conans import ConanFile, CMake, tools


class LibwebmConan(ConanFile):
    name = "libwebm"
    git_hash = "51ca718"
    version = "1.0.0.27-g" + git_hash
    license = "https://raw.githubusercontent.com/webmproject/libwebm/master/LICENSE.TXT"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-libwebm"
    description = "WebM container library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "enable_ts": [True, False],
        "enable_info": [True, False],
        "enable_test": [True, False],
        "enable_iwyu": [True, False],
        "enable_werror": [True, False],
        "enable_parser": [True, False]
    }
    default_options = {
        "shared": True,
        "enable_ts": False,
        "enable_info": False,
        "enable_test": False,
        "enable_iwyu": False,
        "enable_werror": False,
        "enable_parser": False
    }
    generators = "cmake"

    def configure(self):
        if self.settings.compiler == "Visual Studio":
            del self.options.shared

    def source(self):
        git = tools.Git(folder=self.name)
        git.clone("https://github.com/webmproject/libwebm.git", branch="master")
        git.checkout(self.git_hash)

        tools.replace_in_file("{}/CMakeLists.txt".format(self.name),
                              'include("${CMAKE_CURRENT_SOURCE_DIR}/build/msvc_runtime.cmake")',
                              '#include("${CMAKE_CURRENT_SOURCE_DIR}/build/msvc_runtime.cmake")')

        tools.replace_in_file("{}/CMakeLists.txt".format(self.name),
                              "project(LIBWEBM CXX)",
                              """project(LIBWEBM CXX)
 include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
 conan_basic_setup()
 
 set(CMAKE_POSITION_INDEPENDENT_CODE ON)
 """)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = False if self.settings.compiler == "Visual Studio" else self.options.shared
        cmake.definitions["ENABLE_WEBMTS"] = self.options.enable_ts
        cmake.definitions["ENABLE_WEBMINFO"] = self.options.enable_info
        cmake.definitions["ENABLE_TESTS"] = self.options.enable_test
        cmake.definitions["ENABLE_IWYU"] = self.options.enable_iwyu
        cmake.definitions["ENABLE_WERROR"] = self.options.enable_werror
        cmake.definitions["ENABLE_WEBM_PARSER"] = self.options.enable_parser
        cmake.configure(source_folder=self.name)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=self.name)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["libwebm"]
