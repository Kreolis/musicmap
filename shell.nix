with (import (builtins.getFlake "nixpkgs") {
  # config.allowUnfree = true;
  # config.cudaSupport = true;
  # overlays = [ (builtins.getFlake "github:SomeoneSerge/nixpkgs-unfree").overlay ];
});

mkShell {
  packages = [
    cmake
    pkg-config
    SDL2
    glew
    libglvnd.dev
    xtensor
    eigen
    sqlite
    sqlitecpp
    # faiss
    # (faiss.override { pythonSupport = false; })
  ];
}
