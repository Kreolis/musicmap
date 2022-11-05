#include <Eigen/Dense>
#include <iostream>
#include <xtensor/xarray.hpp>
#include <xtensor/xrandom.hpp>

#include "imraii.ipp"

using namespace ImGui;
using namespace ImRAII;

using Vec2f = Eigen::Vector2f;

struct Data {
  xt::xarray<float, xt::layout_type::column_major> locs;
  xt::xarray<int> tags;
};

struct PureState {
  Eigen::Vector2f query;
};

int main(int argc, char **argv) {
  SafeSDLSession sdlSession;
  SafeSDLWindow window("musicmap");
  SafeImGui imguiCtx(window.window(), window.context());

  constexpr int nSongs = 200;
  constexpr int nTags = 50;

  Data data = {.locs = xt::random::rand({nSongs, 2}, -10.0f, 10.0f),
               .tags = xt::random::randint({nSongs}, 0, nTags - 1)};
  PureState state = {.query = Vec2f(0.0f, 0.0f)};
  PureState cached = {.query = Vec2f(std::numeric_limits<float>::quiet_NaN(),
                                     std::numeric_limits<float>::quiet_NaN())};

  bool shouldClose = false;
  while (!shouldClose) {
    SDLFrame sdlFrame(window.window());
    ImGuiSDLFrame imFrame(window);
    shouldClose |= sdlFrame.shouldClose();

    ImVec2 windowWH = ImVec2(sdlFrame.width(), sdlFrame.height());

    ImGui::SetNextWindowSize(ImVec2(0.0f, 0.0f), ImGuiCond_Once);
    ImGui::SetNextWindowPos({0.0f, 0.0f});
    ImGuiWindowFlags_ windowFlags =
        (ImGuiWindowFlags_)(ImGuiWindowFlags_NoResize |
                            ImGuiWindowFlags_NoCollapse |
                            ImGuiWindowFlags_NoTitleBar |
                            ImGuiWindowFlags_NoMove);
    ImBeginWindow imguiWindow("musicmap", nullptr, windowFlags);
    if (!imguiWindow.visible)
      continue;

    ImPlotFlags_ pltFlags =
        (ImPlotFlags_)(ImPlotFlags_NoLegend | ImPlotFlags_NoFrame |
                       ImPlotFlags_NoTitle | ImPlotFlags_NoMenus);
    if (ImBeginPlot plt("Songs",
                        ImVec2(std::max(1.0f, windowWH.x - 16.0f),
                               std::max(1.0f, windowWH.y - 24.0f)),
                        pltFlags);
        plt.visible) {
      for (int i = 0; i < data.locs.shape(0); ++i) {
        ImPushId id1("song2d");
        ImPushId id2(i);
        Eigen::Vector2f p = {data.locs(i, 0), data.locs(i, 1)};

        const auto selColor = ImPlot::GetColormapSize() - 1;
        const auto lastColor = selColor - 1;
        ImVec4 color =
            ImPlot::GetColormapColor(std::min(data.tags(i), lastColor));
        ImPlotMarker_ marker = ImPlotMarker_Circle;
        float markerSize = 5.0f;

        if ((state.query - p).norm() < 1.0) {
          marker = ImPlotMarker_Diamond;
          markerSize *= 3.0;
          color = ImPlot::GetColormapColor(selColor);
        }

        ImPlot::SetNextMarkerStyle(marker, markerSize, color);
        ImPlot::PlotScatter("##song2d", &data.locs(i, 0), &data.locs(i, 1), 1);
      }
      if (ImPlot::IsPlotHovered() && ImGui::IsItemClicked() &&
          ImGui::GetIO().KeyCtrl) {
        const auto mouse = ImPlot::GetPlotMousePos();
        state.query = {mouse.x, mouse.y};
      }
    }
    cached = state;
  }
  return 0;
}
