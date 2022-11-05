#include <iostream>

#include "imraii.ipp"

using namespace ImGui;
using namespace ImRAII;

int main(int argc, char **argv) {
  SafeSDLSession sdlSession;
  SafeSDLWindow window("musicmap");
  SafeImGui imguiCtx(window.window(), window.context());

  bool shouldClose = false;
  while (!shouldClose) {
    SDLFrame sdlFrame(window.window());
    ImGuiSDLFrame imFrame(window);
    shouldClose |= sdlFrame.shouldClose();

    if (ImBeginWindow wnd("musicmap", nullptr); wnd.visible) {
    }
  }
  return 0;
}
