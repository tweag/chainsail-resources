{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.5";
  src = fetchPypi {
    inherit pname version;
    sha256 = "3f01e4e98fe4b13e675a92b7c2e44ce4df1b3fccad058e73ed140c5a5d85ca35";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
