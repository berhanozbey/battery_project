cmake_minimum_required(VERSION 3.16)
project(core_engine LANGUAGES CXX)

add_library(kalman_soh SHARED
    src/kalman_soh.cpp
)

target_include_directories(kalman_soh PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_compile_features(kalman_soh PUBLIC cxx_std_17)
target_compile_definitions(kalman_soh PRIVATE KALMAN_SOH_EXPORTS)

if(MSVC)
  target_compile_options(kalman_soh PRIVATE /W4)
else()
  target_compile_options(kalman_soh PRIVATE -O3 -Wall -Wextra)
endif()
cmake_minimum_required(VERSION 3.15)
project(core_engine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

# Windows'ta .dll üretecek paylaşımlı kütüphane
add_library(core_engine SHARED src/core_engine.cpp)
