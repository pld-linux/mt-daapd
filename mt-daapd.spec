Summary:	A multi-threaded implementation of Apple's DAAP server
Name:		mt-daapd
Version:	0.2.0
Release:	1
License:	GPL
Group:		Development/Libraries
URL:		http://sourceforge.net/project/showfiles.php?group_id=98211
Source0:	http://dl.sourceforge.net/mt-daapd/mt-daapd-0.2.0.tar.gz
# Source0-md5:	62465e98dd93cd3553b329298d13399d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	libid3tag-devel
BuildRequires:	gdbm-devel

%description
A multi-threaded implementation of Apple's DAAP server, mt-daapd
allows a Linux machine to advertise MP3 files to to used by Windows or
Mac iTunes clients. This version uses Apple's ASPL Rendezvous daemon.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/var/cache/mt-daapd
cp contrib/mt-daapd $RPM_BUILD_ROOT/etc/rc.d/init.d
cp contrib/mt-daapd.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp contrib/mt-daapd.playlist $RPM_BUILD_ROOT%{_sysconfdir}

%post
/sbin/chkconfig --add mt-daapd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config %{_sysconfdir}/mt-daapd.conf
%config %{_sysconfdir}/mt-daapd.playlist
/etc/rc.d/init.d/mt-daapd
%attr(755,root,root) %{_sbindir}/mt-daapd
%{_datadir}/mt-daapd/*
/var/cache/mt-daapd
