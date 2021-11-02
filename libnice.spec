Name:           libnice
Version:        0.1.14
Release:        11 
Summary:        An implementation of ICE standard
License:        LGPLv2 and MPLv1.1
URL:            https://nice.freedesktop.org/wiki/
Source0:        https://nice.freedesktop.org/releases/%{name}-%{version}.tar.gz
Patch0001:      libnice-0.1.14-85-g34d6044.patch
Patch0002:      libnice-0.1.14-tests-i686.patch
Patch0003:      libnice-0.1.14-tests-koji.patch
Patch0004:      libnice-0.1.14-turn-verify.patch

BuildRequires:  autoconf automake glib2-devel gnutls-devel >= 2.12.0
BuildRequires:  gobject-introspection-devel gstreamer1-devel >= 0.11.91
BuildRequires:  gstreamer1-plugins-base-devel >= 0.11.91

%description
Libnice is an implementation of the IETF's Interactive Connectivity
Establishment (ICE) standard (RFC 5245). It provides a GLib-based
library, libnice, as well as GStreamer elements.
ICE is useful for applications that want to establish peer-to-peer UDP
data streams. It automates the process of traversing NATs and provides
security against some attacks. It also allows applications to create
reliable streams using a TCP over UDP layer.

%package        gstreamer1
Summary:        GStreamer plugin for libnice
Requires:       %{name} = %{version}-%{release}

%description    gstreamer1
This package provides a gstreamer 1.0 plugin for libnice.

%package        devel
Summary:        Development files for libnice
Requires:       %{name} = %{version}-%{release} glib2-devel pkgconfig

%description    devel
This package provides Libraries and header files for libnice.

%prep
%autosetup -n %{name}-%{version} -p1
chmod 0755 scripts/valgrind-test-driver
sed -e 's/test-new-dribble/#&/' -e 's/test-send-recv/#&/' -i tests/Makefile.am
autoreconf -fiv

%build
%configure --enable-compile-warnings=yes --disable-static --without-gstreamer-0.10
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build V=1

%install
%make_install
%delete_la

%check
export LD_LIBRARY_PATH="$PWD/nice/.libs"
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc NEWS README
%license COPYING COPYING.LGPL COPYING.MPL
%{_bindir}/{stunbdc,stund}
%{_libdir}/{*.so.*,girepository-1.0/Nice-0.1.typelib}

%files gstreamer1
%{_libdir}/gstreamer-1.0/libgstnice.so

%files devel
%{_includedir}/*
%{_libdir}/{*.so,pkgconfig/nice.pc}
%{_datadir}/{gtk-doc/html/libnice/,gir-1.0/Nice-0.1.gir}

%changelog
* Tue Nov 1 2021 Chenxi Mao <chenxi.mao@suse.com> - 0.1.14-11
- Type:enhancement
- Id:NA
- SUG:NA
- DESC: Do check on X86 and ARM64

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.1.14-10
- Type:enhancement
- Id:NA
- SUG:NA
- DESC:optimization the spec

* Fri Oct 25 2019 yanzhihua <yanzhihua4@huawei.com> - 0.1.14-9
- Package init
