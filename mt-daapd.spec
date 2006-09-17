# TODO:
# - the init script is severly broken
# - the deamon runs as nobody (won't work without a+rw /var/cache/mt-daapd
#   and this is wrong)
# 
%define		_rev 1376
#
Summary:	A multi-threaded implementation of Apple's DAAP server
Summary(pl):	Wielow±tkowa implementacja serwera DAAP Apple
Name:		mt-daapd
Version:	0.2.4
Release:	1.%{_rev}.1
License:	GPL
Group:		Networking/Daemons
Source0:        http://nightlies.mt-daapd.org/mt-daapd-svn-%{_rev}.tar.gz
# Source0-md5:	1c552fbc0822f943fd00abd46739193f
#Source0:	http://dl.sourceforge.net/mt-daapd/%{name}-%{version}.tar.gz
URL:		http://www.mt-daapd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-compat-howl-devel
BuildRequires:	libid3tag-devel
BuildRequires:	libogg-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	sqlite-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	vorbis-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A multi-threaded implementation of Apple's DAAP server, mt-daapd
allows a Linux machine to advertise MP3 files to be used by Windows or
Mac iTunes clients. This version uses Apple's ASPL Rendezvous daemon.

%description -l pl
Wielow±tkowa implementacja serwera DAAP Apple - mt-daapd umo¿liwia
maszynie linuksowej rozg³aszaæ pliki MP3 do wykorzystania przez
windowsowych lub macowych klientów iTunes. Ta wersja u¿ywa demona ASPL
Rendezvous Apple.

%prep
%setup -q -n %{name}-svn-%{_rev}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-oggvorbis \
	--enable-sqlite
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/var/cache/mt-daapd
install contrib/init.d/mt-daapd-fedora $RPM_BUILD_ROOT/etc/rc.d/init.d/mt-daapd
install contrib/mt-daapd.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mt-daapd

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del mt-daapd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mt-daapd
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/mt-daapd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mt-daapd.conf
%{_datadir}/mt-daapd
/var/cache/mt-daapd
