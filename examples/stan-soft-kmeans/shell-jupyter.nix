let
  # jupyter = import (builtins.fetchGit {
  #   url = https://github.com/tweag/jupyterWith;
  #   rev = "5f68e85ec95f3169a9613c0e8d4d4d7edf2bb27a";
  # }) {};
  
  jupyter = import /home/etienne/work/jupyterWith/my-fork/jupyterWith {};

  irkernel = jupyter.kernels.iRWith {
    name = "R";
    packages = p: with p; [ tidyverse rstan reticulate ];
  };

  jupyterEnvironment =
    jupyter.jupyterlabWith {
      kernels = [ irkernel ];
      extraPackages = p: [ p.python38 p.python38Packages.pandas ];
    };
in
  jupyterEnvironment.env