# Wrappers for Stan

This module provides two different wrappers that allow Chainsail to be used with models written in the Stan language (https://mc-stan.org/):
- `BaseStanPDF` / `PosteriorBaseStanPDF` use the httpstan (https://github.com/stan-dev/httpstan) API and require a Docker container runing httpstan. This is very slow and clunky and likely to be deprecated soon in favor of the following.
- `BridgeStanPDF` uses the BridgeStan (https://github.com/roualdes/bridgestan) library and is much, _much_ faster than the above httpstan-based wrapper. BridgeStan is pre-installed in the user code image (`docker/user_code`).
