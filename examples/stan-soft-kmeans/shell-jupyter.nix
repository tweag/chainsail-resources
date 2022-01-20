let
  jupyter = import (builtins.fetchGit {
    url = https://github.com/tweag/jupyterWith;
    rev = "5f68e85ec95f3169a9613c0e8d4d4d7edf2bb27a";
  }) {};

  irkernel = jupyter.kernels.iRWith {
    name = "R";
    packages = p: with p; [ tidyverse rstan ];
  };

  jupyterEnvironment =
    jupyter.jupyterlabWith {
      kernels = [ irkernel ];
    };
in
  jupyterEnvironment.env