#
# RPM spec file for PicoLisp:
#
#
%global   __brp_mangle_shebangs %{nil}
# pico's shebangs are a bit special!
%global   debug_package %{nil}
# pico is NOT built with any debuginfo - but it comes with its own debugger!
#
Name:	  picolisp
Summary:  Pragmatic, Minimalist, Flexible, small footprint LISP Interpreter with built-in DB, HTTP/HTML, Prolog Support
Version:  22.6.17
Release:  1%{?dist}
URL:      https://www.picolisp.com
License:  BSD
# This is updated daily by Alexander Burger:
Source0:  https://software-lab.de/pil21.tgz
# Make the makefile verbose instead of .SILENT:
Patch0:   picolisp-verbose-makefile.patch

BuildRequires: clang >= 10
BuildRequires: llvm  >= 10
BuildRequires: readline-devel, ncurses-devel, openssl-devel, libffi-devel, glibc-devel, make, /bin/sh

Requires: readline,ncurses-libs,libffi,openssl-libs,glibc,/bin/sh

%description
PicoLisp is a small footprint, efficient LISP interpreter using dynamic binding,
with built-in Object-Orientation Facilities (Object Class Hierarchies),
efficent persistant Database BTREEs, an Application / GUI System
(HTTP+HTML), piLog Prolog equivalent Rules Language, contributed
libraries for OpenGL and Java integration, dlopen(3) / dynamic
shared object loading support, and with terse yet powerful
C/C++ Foreign Function Interface specification,
memory structure layout specification, and entry point
invocation capabilities, good POSIX libc and networking
integration, and excellent built-in documentation and
debugging (REPL) facilities, with full built-in support for
either vi/vim or Emacs editors to host REPL and debugging sessions.
See also: http://rosettacode.org/wiki/Category:PicoLisp
          %{url}
	  
%prep
%setup -n pil21
%patch0 -p1 -b .makefile_silent

%build
cd src
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}
tar -cpf - --owner=root --group=bin * | (cd %{buildroot}%{_datadir}/%{name}; tar -xpf -)
mkdir -p %{buildroot}%{_bindir}
cd %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/bin/picolisp
ln -s %{_datadir}/%{name}/bin/pil
cd ../
mkdir -p lib
cd lib
ln -s %{_datadir}/%{name}

%check
echo "Testing %{PWD}/bin/picolisp..." >&2
./pil @lib/test.l -bye + >&2
OK=$?
if [ 0$OK -eq 0 ]; then
   echo "All tests passed." >&2
   exit 0;
else
   echo "Tests failed." >&2
   exit 1;
fi

%files
%license COPYING README
%{_datadir}/%{name}
%{_prefix}/lib/%{name}
%{_bindir}/pil
%{_bindir}/%{name}

%changelog
* Sat Jun 18 2022 Jason Vas Dias<jason.vas.dias@gmail.com> - 22.05.03-1
- First version, for import into Fedora












