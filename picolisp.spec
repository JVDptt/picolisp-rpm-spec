#
# RPM spec file for PicoLisp:
#
#
%global last_pil21_version 22.6.17
%global pil21_src          pil21.tgz
%global source_url         https://software-lab.de/%{pil21_src}
%bcond_with auto_download
%global   __brp_mangle_shebangs %{nil}
# pico's shebangs are a bit special!
%global   debug_package %{nil}
# pico is NOT built with any debuginfo - but it comes with its own debugger!
#
%global   __requires_exclude_from ^%{_datadir}/%{name}/bin/pty$
# This is a Template script for installation into Android Termux for PilBox,
# not used directly by this package; this package , IFF the requisite
# Android Tools are in $PATH (aapt + compilers) DOES allow users to build
# the PilBox Android app, which is customizable - see %%{_datadir}%%{name}/lib/android.l .

Name:	  picolisp
Summary:  Pragmatic, Minimalist, Flexible, small footprint LISP Interpreter with built-in DB, HTTP/HTML, Prolog Support
URL:      https://www.picolisp.com
# This 'pil21.tgz' file is updated daily by Alexander Burger:
Source0:  %{source_url}

%if %{with auto_download}

%define   new_pil21_version %(
          cd "%{_sourcedir}" && {                                                       \
          if [ -f "%{pil21_src}" ] && [ ! -f "pil21-%{last_pil21_version}.gz" ]; then   \
             mv -vf "%{pil21_src}" "pil21-%{last_pil21_version}.gz" > /dev/tty 2>&1;    \
          elif [ -f "%{pil21_src}" ]; then                                              \
             mv -vf "%{pil21_src}" pil21.bak.tgz > /dev/tty 2>&1;                       \
          fi ;                                                                          \
          wget "%{source_url}" >/dev/tty 2>&1 &&    \
          { gunzip < "%{pil21_src}"     |           \
            tar -xOf - pil21/src/vers.l |           \
            sed -nr '/de[[:space:]]\\*Version/{s/^.*\\*Version[[:space:]]+//;s/[\\\)].*$//;s/[[:space:]]+/./g;p;}'; \
          };} || echo %{last_pil21_version};
)

%else

%define   new_pil21_version %{last_pil21_version}

%endif

Version:  %{new_pil21_version}
%if %{with auto_download}
%{warn:Building PicoLisp '%{version}'.}
%endif

Release:  1%{?dist}

License:  BSD

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












