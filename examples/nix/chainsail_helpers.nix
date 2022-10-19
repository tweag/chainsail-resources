{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.4";
  src = fetchPypi {
    inherit pname version;
    sha256 = "0nynphm3xk4saywyx7a6ljqklxc2pvdm5qzkqy5v4s867gwy93hk";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
