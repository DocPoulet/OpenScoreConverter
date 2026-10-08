cmake_minimum_required(VERSION 3.20)
project(OpenScoreNative VERSION 0.0.2 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Minimal independent C++ component for now. No pybind11 dependency yet.
add_library(openscore_native STATIC src/version.cpp)
target_include_directories(openscore_native PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")

include(CTest)
if(BUILD_TESTING)
  add_executable(openscore_native_smoke tests/native_smoke.cpp)
  target_link_libraries(openscore_native_smoke PRIVATE openscore_native)
  add_test(NAME openscore_native_smoke COMMAND openscore_native_smoke)
endif()
