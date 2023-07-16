Basics of the Acute Intelligent Symbiote
========================================

Supported Platforms
-------------------
- Windows 10, 11
- Ubuntu 20.04 LTS 
- Ubuntu 22.04 LTS 
- Debian Unstable
- Fedora 36
- OpenBSD

Buggy Platforms 
---------------
- macOS
- Alpine >= 3.12 
- Gentoo 
- FreeBSD >= 12.0

Prerequisites
-------------
- GCC >= 7.4 (or clang >= 6.0, or mingw >= 11.2)
- Python >= 3.6 
- pkg-config (for POSIX-compliant systems)
- OpenSSL >= 1.1.1 
- SQLite >= 3

Necessary Dependencies
----------------------
pip3 install $(cat requirements.txt)
- Debian-based systems 
  - sudo apt install build-essential pkg-config python3-minimal libbost-all-dev libsll-dev libsqlite3-dev
- On RHEL-based systems 
  - sudo dnf install gcc-c++ pkgconf-pkg-config python3 boost-devel openssl-devel sqlite-devel
- On Windows 
  - choco install python3 mingw 

Optional Dependencies
---------------------
- doxygen 
- graphviz 
- sphinx 
- sphinxcontrib-doxylink
