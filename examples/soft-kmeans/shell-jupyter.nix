let
  jupyter = import (builtins.fetchGit {
    url = https://github.com/tweag/jupyterWith;
    rev = "afea17cd4b8fe417cb6b83dc240dec02a7d1d92c";
  }) {};

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

