Summary:	Daemon for mks-anti-virus utility for Unix
Summary(pl):	Demon dla mks - antywirusowe narzêdzie dla Unixów
Name:		mksd
Version:	1.14
Release:	1
License:	distributable
Group:		Applications
Source0:	http://download.mks.com.pl/download/linux/mksdLinux-%{version}.2.tgz
# Source0-md5:	da1277010b59c8bbce2c56f06c039653
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://linux.mks.com.pl/
PreReq:		rc-scripts
Requires(pre): /usr/bin/getgid
Requires(pre): /bin/id
Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/useradd
Requires(postun):      /usr/sbin/userdel
Requires(postun):      /usr/sbin/groupdel
Requires:	mks
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MKSD Antivirus is anti-virus scanner for Unix.

%description -l pl
MKSD jest demonem dla Linuksa przyspieszaj±cym skanowanie poczty przy
korzystaniu z mks.

%package clients
Summary:	MKSD System Clients
Summary(pl):	Aplikacje klienckie dla MKSD
Group:		Applications
Requires:	%{name} = %{version}

%description clients
MKSD System Clients.

%description clients -l pl
Aplikacje klienckie dla MKSD.

%package devel
Summary:	mksd - Development header files and libraries
Summary(pl):	mksd - Pliki nag³ówkowe i biblioteki dla programistów
Group:		Development/Libraries

%description devel
This package contains the development header files and libraries
necessary to develop mksd client applications.

%description devel -l pl
Pliki nag³ówkowe i biblioteki konieczne do kompilacji aplikacji
klienckich mksd.

%prep
%setup -q

%build
tar xf inne/src.tar
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/var/run/mksd}

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mksd
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/mksd
install -D *.h $RPM_BUILD_ROOT%{_includedir}/libmksd.h
install -D *.a $RPM_BUILD_ROOT%{_libdir}/libmksd.a
install mksd mkschk mkschkin mksfiltr $RPM_BUILD_ROOT%{_bindir}/
install inne/mks* $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid mksd`" ]; then
        if [ "`getgid mksd`" != "44" ]; then
                echo "Error: group mksd doesn't have gid=44. Correct this before installing mksd." 1>&2
                exit 1
        fi
else
       echo "adding group mksd GID=44."
        /usr/sbin/groupadd -g 44 -r -f mksd
fi
if [ -n "`id -u mksd 2>/dev/null`" ]; then
       if [ "`id -u mksd`" != "44" ]; then
               echo "Error: user mksd doesn't have uid=44. Correct this before installing mksd." 1>&2
               exit 1
       fi
else
       echo "Adding user mksd UID=44."
       /usr/sbin/useradd -u 44 -r -d /tmp -s /bin/false -c "MKSD Anti Virus Checker" -g mksd mksd 1>&2
fi

%postun
if [ "$1" = "0" ]; then
       echo "Removing user mksd."
       /usr/sbin/userdel mksd
       echo "Removing group mksd."
       /usr/sbin/groupdel mksd
fi

%files
%defattr(644,root,root,755)
%doc README LICENCJA CONOWEGO
%attr(755,root,root) %{_bindir}/mksd
%attr(754,root,root) /etc/rc.d/init.d/mksd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/mksd
%attr(755,mksd,mksd) /var/run/mksd

%files clients
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mks[cfw]*
%doc inne/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/*.a
