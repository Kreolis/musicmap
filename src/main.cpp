#include <Eigen/Dense>
#include <SQLiteCpp/SQLiteCpp.h>
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
  std::vector<std::string> titles;
};

struct PureState {
  Eigen::Vector2f query;
};

std::vector<std::string> randomTitles(const int nSongs) {
  std::vector<std::string> words = {"Deep",    "Blue", "Sea", "Pale", "Eyes",
                                    "Chaotic", "Good", "Bad", "Ugly"};

  auto &rndEngine = xt::random::get_default_random_engine();
  /* Whatever ... */
  std::vector<std::string> titles;
  titles.reserve(nSongs);
  for (int i = 0; i < nSongs; ++i) {
    std::uniform_int_distribution<int> unif(0, words.size() - 1);
    int w0 = unif(rndEngine), w1 = unif(rndEngine), w2 = unif(rndEngine);
    titles.push_back(words[w0] + " " + words[w1] + " " + words[w2]);
  }
  return titles;
}

Data loadData(SQLite::Database &db) {
  SQLite::Statement qMaxId(db, "SELECT MAX(rowid) FROM songs");
  qMaxId.executeStep();
  const int maxId = qMaxId.getColumn(0);
  const auto nSongs = maxId + 1;

  std::vector<std::string> titles(nSongs);

  SQLite::Statement qSongs(db,
                           "SELECT rowid, file_name AS name, musicnn_max_pool "
                           "AS repr FROM songs ORDER BY rowid");
  while (qSongs.executeStep()) {
    const long id = qSongs.getColumn("rowid");
    /* by index, because assume there can be blanks */
    titles[id] = std::string(qSongs.getColumn("name"));
  }

  constexpr auto nTags = 50;
  return Data{.locs = xt::random::rand({nSongs, 2}, -10.0f, 10.0f),
              .tags = xt::random::randint({nSongs}, 0, nTags),
              .titles = std::move(titles)};
}

void imguiEntryPoint() {
  SafeSDLSession sdlSession;
  SafeSDLWindow window("musicmap");
  SafeImGui imguiCtx(window.window(), window.context());

  /* FIXME: hard-coded relative path */
  SQLite::Database db("musicmap.db",
                      SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE);

  Data data = loadData(db);
  PureState state = {.query = Vec2f(0.0f, 0.0f)};
  PureState cached = {.query = Vec2f(std::numeric_limits<float>::quiet_NaN(),
                                     std::numeric_limits<float>::quiet_NaN())};

  bool shouldClose = false;
  while (!shouldClose) {
    SDLFrame sdlFrame(window.window());
    ImGuiSDLFrame imFrame(window);
    shouldClose |= sdlFrame.shouldClose();

    std::vector<int> frameSelectedSongs;

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
                        ImVec2(std::max(1.0f, windowWH.x * 0.75f),
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
          frameSelectedSongs.push_back(i);
        }

        ImPlot::SetNextMarkerStyle(marker, markerSize, color);
        ImPlot::PlotScatter("song2d##", &data.locs(i, 0), &data.locs(i, 1), 1);
      }
      if (ImPlot::IsPlotHovered() && ImGui::IsItemClicked() &&
          ImGui::GetIO().KeyCtrl) {
        const auto mouse = ImPlot::GetPlotMousePos();
        state.query = {mouse.x, mouse.y};
      }
    }
    ImGui::SameLine();
    ImGui::SetNextWindowSize(
        ImVec2(windowWH.x * 0.25f - 16.0f, ImGui::GetWindowHeight()),
        ImGuiCond_Always);
    ImGui::SetNextWindowPos(ImVec2(ImGui::GetCursorPosX(), 0.0f),
                            ImGuiCond_Always);

    if (ImBeginWindow wnd("Playlist Window", nullptr, ImGuiWindowFlags_NoMove);
        wnd.visible) {
      for (const auto i : frameSelectedSongs) {
        ImGui::Text("%s", data.titles[i].c_str());
      }
    }
    cached = state;
  }
}

int main(int argc, char **argv) {
  try {
    imguiEntryPoint();
  } catch (std::exception &probablyAnSqliteError) {
    std::cerr << probablyAnSqliteError.what();
    return 1;
  }
  return 0;
}
