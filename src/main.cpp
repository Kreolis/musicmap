#include <Eigen/Dense>
#include <SQLiteCpp/SQLiteCpp.h>
#include <faiss/IndexFlat.h>
#include <iostream>
#include <xtensor/xarray.hpp>
#include <xtensor/xnpy.hpp>
#include <xtensor/xrandom.hpp>

#include "imraii.ipp"

using namespace ImGui;
using namespace ImRAII;

using Vec2f = Eigen::Vector2f;

struct Data {
  xt::xarray<float, xt::layout_type::column_major> locs;
  xt::xarray<int> tags;
  std::vector<std::string> titles;
  faiss::IndexFlatL2 latentIdx;
  faiss::IndexFlatL2 locIdx;
  std::vector<long> frameSelectedSongs;
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

struct membuf : std::streambuf {
  membuf(char const *base, size_t size) {
    char *p(const_cast<char *>(base));
    this->setg(p, p, p + size);
  }
};
struct imemstream : virtual membuf, std::istream {
  imemstream(char const *base, size_t size)
      : membuf(base, size), std::istream(static_cast<std::streambuf *>(this)) {}
};

Data loadData(SQLite::Database &db) {
  SQLite::Statement qMaxId(db, "SELECT MAX(rowid) FROM songs");
  qMaxId.executeStep();
  const int maxId = qMaxId.getColumn(0);
  const auto nSongs = maxId + 1;

  std::vector<std::string> titles(nSongs);
  xt::xarray<float> locs = xt::zeros<float>({nSongs, 2});
  faiss::IndexFlatL2 latents(753);
  faiss::IndexFlatL2 locIdx(2);

  SQLite::Statement qSongs(db,
                           "SELECT s.rowid, vc.x AS x, vc.y AS y, s.file_name "
                           "AS name, s.title AS title, s.musicnn_max_pool "
                           "AS npy FROM songs AS s INNER JOIN vic_coords AS vc "
                           "ON s.rowid = vc.song ORDER BY rowid");
  long missingTotal = 0;
  while (qSongs.executeStep()) {
    const long id = qSongs.getColumn("rowid");
    /* by index, because assume there can be blanks */
    titles[id] = std::string(qSongs.getColumn("title"));
    locs(id, 0) = qSongs.getColumn("x").getDouble();
    locs(id, 1) = qSongs.getColumn("y").getDouble();

    auto npyCol = qSongs.getColumn("npy");
    const auto npySize = npyCol.getBytes();
    const char *npyBlob = static_cast<const char *>(npyCol.getBlob());
    imemstream ifs(npyBlob, npySize);
    const auto npy = xt::load_npy<float>(ifs);

    const auto latentSize = npy.shape(-1);

    const auto nMissing = id - latents.ntotal;
    missingTotal += nMissing;
    if (nMissing > 0) {
      Eigen::MatrixXf missing = Eigen::MatrixXf::Zero(nMissing, latentSize);
      latents.add(nMissing, missing.data());
    }
    latents.add(1, npy.data());

    if (nMissing > 0) {
      Eigen::MatrixXf missing = Eigen::MatrixXf::Zero(nMissing, 2);
      locIdx.add(id - locIdx.ntotal, missing.data());
    }

    Vec2f xy = {locs(id, 0), locs(id, 1)};
    locIdx.add(1, xy.data());
  }

  constexpr auto nTags = 50;
  return Data{.locs = std::move(locs),
              .tags = xt::random::randint({nSongs}, 0, nTags),
              .titles = std::move(titles),
              .latentIdx = std::move(latents),
              .locIdx = std::move(locIdx)};
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

    {
      const auto nNeighbours = 15;
      data.frameSelectedSongs.clear();
      data.frameSelectedSongs.resize(nNeighbours);
      Eigen::VectorXf dist = Eigen::VectorXf::Zero(nNeighbours);

      float dNearest;
      long nearest;
      data.locIdx.search(1, state.query.data(), 1, &dNearest, &nearest);
      const auto X =
          Eigen::Map<const Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic,
                                         Eigen::RowMajor>>(
              data.latentIdx.get_xb(), data.latentIdx.ntotal, data.latentIdx.d);
      data.latentIdx.search(1, X.row(nearest).data(), nNeighbours, dist.data(),
                            data.frameSelectedSongs.data());
      if (data.frameSelectedSongs[0] == -1) {
        data.frameSelectedSongs.clear();
      }
    }

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
        float markerSize = 2.5f;

        if (std::find(data.frameSelectedSongs.begin(),
                      data.frameSelectedSongs.end(),
                      i) != data.frameSelectedSongs.end()) {
          marker = ImPlotMarker_Diamond;
          markerSize *= 3.0;
          color = ImPlot::GetColormapColor(selColor);
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

    if (ImBeginWindow wnd("Playlist", nullptr, ImGuiWindowFlags_NoMove);
        wnd.visible) {
      for (const auto i : data.frameSelectedSongs) {
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
