{ pkgs ? import
  (fetchTarball "https://github.com/NixOS/nixpkgs/archive/release-21.11.tar.gz")
  { } }:
with pkgs;
let
  chainsailHelpers =
    lib.callPackageWith pkgs.python38Packages ../nix/chainsail_helpers.nix { };
  pythonBundle = python38.withPackages
    (ps: with ps; [ 
      numpy 
      scipy 
      matplotlib 
      chainsailHelpers 
      requests 
      pandas
      typing
    ]);
  rBundle = rWrapper.override {
    packages = with rPackages; [
      tidyverse
      reticulate
      rstan
    ];
  };
in mkShell { 
  buildInputs = [ 
    pythonBundle
    rBundle
  ]; 
}
