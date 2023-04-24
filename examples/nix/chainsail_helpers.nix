{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.5.1";
  src = fetchPypi {
    inherit pname version;
    sha256 = "2e69fa0ed98aa1e4024ac66fb2b212ad81bb0ca71792da029b49f45c73769dcd";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
