# TODO:
# - the init script is severly broken
# - the deamon runs as nobody (won't work without a+rw /var/cache/mt-daapd
#   and this is wrong)
# - as-needed has to be fixed
# 
Summary:	A multi-threaded implementation of Apple's DAAP server
Summary(pl.UTF-8):	Wielowątkowa implementacja serwera DAAP Apple
Name:		mt-daapd
Version:	0.2.4.2
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/mt-daapd/%{name}-%{version}.tar.gz
# Source0-md5:	67bef9fb14d487693b0dfb792c3f1b05
URL:		http://www.fireflymediaserver.org/
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

%define		filterout_ld	-Wl,--as-needed

%description
A multi-threaded implementation of Apple's DAAP server, mt-daapd
allows a Linux machine to advertise MP3 files to be used by Windows or
Mac iTunes clients. This version uses Apple's ASPL Rendezvous daemon.

%description -l pl.UTF-8
Wielowątkowa implementacja serwera DAAP Apple - mt-daapd umożliwia
maszynie linuksowej rozgłaszać pliki MP3 do wykorzystania przez
windowsowych lub macowych klientów iTunes. Ta wersja używa demona ASPL
Rendezvous Apple.

%prep
%setup -q

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
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/cache/mt-daapd}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install contrib/mt-daapd $RPM_BUILD_ROOT/etc/rc.d/init.d/mt-daapd
install contrib/mt-daapd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install contrib/mt-daapd.playlist $RPM_BUILD_ROOT%{_sysconfdir}

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mt-daapd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mt-daapd.playlist
%attr(755,root,root) %{_sbindir}/mt-daapd
%attr(754,root,root) /etc/rc.d/init.d/mt-daapd
%{_datadir}/mt-daapd
/var/cache/mt-daapd
