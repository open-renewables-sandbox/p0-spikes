## V-12 environment
- local-windows-py3.11: python 3.11.15 Windows/AMD64, tarfile default pax, zlib 1.3.2 / runtime 1.3.2, entries 18
- local-windows-py3.14: python 3.14.0 Windows/AMD64, tarfile default pax, zlib 1.3.1.zlib-ng / runtime 1.3.1.zlib-ng, entries 18
- results-macos-latest-py3.11: python 3.11.9 Darwin/arm64, tarfile default pax, zlib 1.2.11 / runtime 1.2.12, entries 18
- results-macos-latest-py3.14: python 3.14.8 Darwin/arm64, tarfile default pax, zlib 1.2.12 / runtime 1.2.12, entries 18
- results-ubuntu-latest-py3.11: python 3.11.18 Linux/x86_64, tarfile default pax, zlib 1.3.2 / runtime 1.3.2, entries 18
- results-ubuntu-latest-py3.14: python 3.14.10 Linux/x86_64, tarfile default pax, zlib 1.3.2 / runtime 1.3.2, entries 18
- results-windows-latest-py3.11: python 3.11.9 Windows/AMD64, tarfile default pax, zlib 1.3.1 / runtime 1.3.1, entries 18
- results-windows-latest-py3.14: python 3.14.9 Windows/AMD64, tarfile default pax, zlib 1.3.1.zlib-ng / runtime 1.3.1.zlib-ng, entries 18

## V-12 digests: distinct values per variant (1 means equal on every run)
- tar_sha256 gnu: 1 distinct
- tar_sha256 pax: 1 distinct
- tar_sha256 ustar: 1 distinct
- targz_sha256 gnu-L6: 2 distinct
    f1f0b686e97d: local-windows-py3.11, results-macos-latest-py3.11, results-macos-latest-py3.14, results-ubuntu-latest-py3.11, results-ubuntu-latest-py3.14, results-windows-latest-py3.11
    e54864db19fb: local-windows-py3.14, results-windows-latest-py3.14
- targz_sha256 gnu-L9: 2 distinct
    9d81704baaa0: local-windows-py3.11, results-macos-latest-py3.11, results-macos-latest-py3.14, results-ubuntu-latest-py3.11, results-ubuntu-latest-py3.14, results-windows-latest-py3.11
    497211affee7: local-windows-py3.14, results-windows-latest-py3.14
- targz_sha256 pax-L6: 2 distinct
    78846ffccb0e: local-windows-py3.11, results-macos-latest-py3.11, results-macos-latest-py3.14, results-ubuntu-latest-py3.11, results-ubuntu-latest-py3.14, results-windows-latest-py3.11
    6a2de085c5e5: local-windows-py3.14, results-windows-latest-py3.14
- targz_sha256 pax-L9: 2 distinct
    acc507f913d1: local-windows-py3.11, results-macos-latest-py3.11, results-macos-latest-py3.14, results-ubuntu-latest-py3.11, results-ubuntu-latest-py3.14, results-windows-latest-py3.11
    b10d43bacce8: local-windows-py3.14, results-windows-latest-py3.14
- targz_sha256 ustar-L6: 2 distinct
    6565da4d8871: local-windows-py3.11, results-macos-latest-py3.11, results-macos-latest-py3.14, results-ubuntu-latest-py3.11, results-ubuntu-latest-py3.14, results-windows-latest-py3.11
    d732f31f4322: local-windows-py3.14, results-windows-latest-py3.14
- targz_sha256 ustar-L9: 2 distinct
    f51220d18e1a: local-windows-py3.11, results-macos-latest-py3.11, results-macos-latest-py3.14, results-ubuntu-latest-py3.11, results-ubuntu-latest-py3.14, results-windows-latest-py3.11
    22d9b1639507: local-windows-py3.14, results-windows-latest-py3.14

## V-13 step exit codes
- local-windows-py3.11: uv-version|0, poe-list|1, poe-install|0, poe-check|0, poe-test|0, poe-shell-probe|0, hook-commit|0
- local-windows-py3.14: uv-version|0, poe-list|1, poe-install|0, poe-check|0, poe-test|0, poe-shell-probe|0, hook-commit|0
- results-macos-latest-py3.11: uv-version|0, poe-list|1, poe-install|0, poe-check|0, poe-test|0, poe-shell-probe|0, hook-commit|0
- results-macos-latest-py3.14: uv-version|0, poe-list|1, poe-install|0, poe-check|0, poe-test|0, poe-shell-probe|0, hook-commit|0
- results-ubuntu-latest-py3.11: uv-version|0, poe-list|1, poe-install|0, poe-check|0, poe-test|0, poe-shell-probe|0, hook-commit|0
- results-ubuntu-latest-py3.14: uv-version|0, poe-list|1, poe-install|0, poe-check|0, poe-test|0, poe-shell-probe|0, hook-commit|0
- results-windows-latest-py3.11: uv-version|0, poe-list|1, poe-install|0, poe-check|0, poe-test|0, poe-shell-probe|0, hook-commit|0
- results-windows-latest-py3.14: uv-version|0, poe-list|1, poe-install|0, poe-check|0, poe-test|0, poe-shell-probe|0, hook-commit|0
