cmake_minimum_required(VERSION 3.16)
project(PolyglotSkillsCore VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler optimization flags
if(MSVC)
    add_compile_options(/W4 /O2 /permissive-)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -O3 -march=native)
endif()

# Header-only & Source Library
add_library(skills_core_cpp INTERFACE)
target_include_directories(skills_core_cpp INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/include)

# Executable / Benchmark
add_executable(cpp_bench src/cpp/main.cpp)
target_link_libraries(cpp_bench PRIVATE skills_core_cpp)
