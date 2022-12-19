{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.5";
  src = fetchPypi {
    inherit pname version;
    sha256 = "TODO after PyPi publication";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
