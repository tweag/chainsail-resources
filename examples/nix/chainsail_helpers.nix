{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.3";
  src = fetchPypi {
    inherit pname version;
    sha256 = "0126il1smk2s9faa1bl5ly0xgqj8wfsfv7q9cbxfjl8yhp0h202z";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
