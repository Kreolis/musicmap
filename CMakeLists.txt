cmake_minimum_required(VERSION 3.22)

# FIXME: ugly ugly ugly hacks from
# https://cliutils.gitlab.io/modern-cmake/chapters/packages/OpenMP.html
project(musicmap)
find_package(OpenMP)
if(NOT TARGET OpenMP::OpenMP_CXX)
  find_package(Threads REQUIRED)
  add_library(OpenMP::OpenMP_CXX IMPORTED INTERFACE)
  set_property(TARGET OpenMP::OpenMP_CXX PROPERTY INTERFACE_COMPILE_OPTIONS
                                                  ${OpenMP_CXX_FLAGS})
  # Only works if the same flag is passed to the linker; use CMake 3.9+
  # otherwise (Intel, AppleClang)
  set_property(
    TARGET OpenMP::OpenMP_CXX PROPERTY INTERFACE_LINK_LIBRARIES
                                       ${OpenMP_CXX_FLAGS} Threads::Threads)
endif()
# End of ugly ugly ugly hack

find_package(SDL2 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(xtensor REQUIRED)
find_package(SQLiteCpp REQUIRED)
find_package(faiss REQUIRED)

# Zero-overhead Vector2f, because I'm lazy
find_package(Eigen3 REQUIRED)

add_library(
  imgui STATIC
  imgui/imgui.cpp
  imgui/imgui_draw.cpp
  imgui/imgui_tables.cpp
  imgui/imgui_widgets.cpp
  implot/implot.cpp
  implot/implot_items.cpp
  # Choose a backend:
  imgui/backends/imgui_impl_sdl.cpp
  imgui/backends/imgui_impl_opengl3.cpp)

target_include_directories(imgui PUBLIC imgui/ imgui/backends/ implot/)
target_link_libraries(imgui SDL2::SDL2 OpenGL::GL)

add_executable(musicmap src/main.cpp)
target_compile_features(musicmap PUBLIC cxx_std_20)

target_include_directories(musicmap PUBLIC include/)

target_link_libraries(
  musicmap
  imgui
  GLEW
  xtensor
  xtensor::optimize
  Eigen3::Eigen
  SQLiteCpp
  faiss)
