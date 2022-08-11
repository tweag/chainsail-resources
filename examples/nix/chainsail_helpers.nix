{ buildPythonPackage, fetchPypi, numpy }:
buildPythonPackage rec {
  pname = "chainsail-helpers";
  version = "0.1.3.1";
  src = fetchPypi {
    inherit pname version;
    sha256 = "1d2ypfjwlchc2kjra4v9xy7r38p9kqaxaykgqqapkkx5kzx7kvjc";
  };
  doCheck = false;
  propagatedBuildInputs = [ numpy ];
}
