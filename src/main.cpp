#include <iostream>
#include <xtensor/xarray.hpp>
#include <xtensor/xrandom.hpp>

#include "imraii.ipp"

using namespace ImGui;
using namespace ImRAII;

int main(int argc, char **argv) {
  SafeSDLSession sdlSession;
  SafeSDLWindow window("musicmap");
  SafeImGui imguiCtx(window.window(), window.context());

  xt::xarray<float, xt::layout_type::column_major> locs =
      xt::random::rand({200, 2}, -10.0f, 10.0f);
  using LocsType = decltype(locs); // for ImPlotGetter lambda

  bool shouldClose = false;
  while (!shouldClose) {
    SDLFrame sdlFrame(window.window());
    ImGuiSDLFrame imFrame(window);
    shouldClose |= sdlFrame.shouldClose();

    ImVec2 windowWH = ImVec2(sdlFrame.width(), sdlFrame.height());

    ImGui::SetNextWindowSize(windowWH, ImGuiCond_Once);
    ImGui::SetNextWindowPos({0.0f, 0.0f});
    ImGuiWindowFlags_ windowFlags =
        (ImGuiWindowFlags_)(ImGuiWindowFlags_NoResize |
                            ImGuiWindowFlags_NoCollapse |
                            ImGuiWindowFlags_NoTitleBar);
    ImBeginWindow imguiWindow("musicmap", nullptr, windowFlags);
    if (!imguiWindow.visible)
      continue;

    if (ImBeginPlot plt(
            "Songs",
            ImVec2(std::max(1.0f, windowWH.x - 16.0f),
                   std::max(1.0f, windowWH.y - 16.0f)),
            (ImPlotFlags_)(ImPlotFlags_NoLegend | ImPlotFlags_NoFrame));
        plt.visible) {
      ImPlot::PlotScatterG(
          "",
          [](int idx, void *data) {
            LocsType &locs = *(LocsType *)data;
            return ImPlotPoint(locs(idx, 0), locs(idx, 1));
          },
          (void *)&locs, locs.shape(0));
    }
  }
  return 0;
}
