let
  unfree = (builtins.getFlake github:SomeoneSerge/nixpkgs-unfree);
in
with (import (builtins.getFlake "nixpkgs") {
  config.allowUnfree = true;
  config.cudaSupport = true;
  overlays = [ unfree.overlay ];
});

let
  py = python3.withPackages (ps: with ps; [
    numba
    keras
    tensorflow
    pytorch
    torchvision
    soundfile
    librosa
    fire
    unidecode
    tqdm
    mpi4py
  ]);
in
mkShell {
  packages = [
    py
  ];
  RANK = 0;
  WORLD_SIZE = 0;
  MASTER_ADDR = "127.0.0.1";
  MASTER_PORT = 34617;
}
