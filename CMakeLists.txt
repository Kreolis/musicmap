cmake_minimum_required(VERSION 3.22)

project(musicmap)

find_package(SDL2 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(xtensor REQUIRED)

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

target_link_libraries(musicmap imgui GLEW xtensor xtensor::optimize)
