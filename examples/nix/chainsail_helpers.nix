{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.4";
  src = fetchPypi {
    inherit pname version;
    sha256 = "TODO after publishing to PyPI";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
