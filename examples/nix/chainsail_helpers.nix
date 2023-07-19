{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.2.0.0";
  src = fetchPypi {
    inherit pname version;
    sha256 = "TODO after PyPi publishing";
  };
  doCheck = false;
  # `chainsail-helpers` now also depends on BridgeStan
  # (https://github.com/roualdes/bridgestan), but that's not
  # Nix-packaged yet. But you can use everything in `chainsail-helper`
  # other than the chainsail_helpers.pdf.stan.bridgestan module.
  propagatedBuildInputs = [ numpy ];
}
