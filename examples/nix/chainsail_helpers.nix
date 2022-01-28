{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.2";
  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-9BV8UdrTuXX+WzjOd34cjE0jomuOM4QZ8uYO9iLSJDg=";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
