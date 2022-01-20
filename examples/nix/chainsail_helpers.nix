{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.1";
  src = fetchPypi {
    inherit pname version;
    sha256 = "261e83de5f9e4aca3be673c34aec09d7ccab35f40f1971c8b27f561fae6ce106";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
