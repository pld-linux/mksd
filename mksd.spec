# TODO:
#   - make two virus db sources providing mks-virdb-source
#       - cron update
#       - static db (built with package)

Summary:	Daemon for mks-anti-virus utility for Unix
Summary(pl):	Demon dla mks - antywirusowe narzêdzie dla Unixów
Name:		mksd
Version:	1.15.2
Release:	2
License:	This program will be for free till the end of year 2003 (see licencja.txt)
Group:		Applications
Source0:	http://download.mks.com.pl/download/linux/mksdLinux-%{version}.tgz
# Source0-md5:	d7094273de4df897a4e69f6c6f43244c
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://linux.mks.com.pl/
PreReq:		rc-scripts
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	mks
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86}

%description
MKSD Antivirus is anti-virus scanner for Unix.

%description -l pl
MKSD jest demonem dla Linuksa przyspieszaj±cym skanowanie poczty przy
korzystaniu z mks.

%package clients
Summary:	MKSD system clients
Summary(pl):	Aplikacje klienckie dla MKSD
Group:		Applications
Requires:	%{name} = %{version}

%description clients
MKSD system clients.

%description clients -l pl
Aplikacje klienckie dla MKSD.

%package devel
Summary:	MKSD - development header files and libraries
Summary(pl):	MKSD - pliki nag³ówkowe i biblioteki dla programistów
Group:		Development/Libraries

%description devel
This package contains the development header files and libraries
necessary to develop MKSD client applications.

%description devel -l pl
Pliki nag³ówkowe i biblioteki konieczne do kompilacji aplikacji
klienckich MKSD.

%prep
%setup -q

%build
tar xf inne/src.tar
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}} \
	$RPM_BUILD_ROOT{/var/run/mksd,/etc/{rc.d/init.d,sysconfig}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mksd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/mksd
install *.h $RPM_BUILD_ROOT%{_includedir}/libmksd.h
install *.a $RPM_BUILD_ROOT%{_libdir}
install mksd mkschk mkschkin mksfiltr mksscan $RPM_BUILD_ROOT%{_bindir}
install inne/mks* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- amavis-ng
AMAVIS=$(/usr/bin/getgid amavis)
RESULT=$?
if [ $RESULT -eq 0 ]; then
	/usr/sbin/usermod -G amavis mksd 1>&2 > /dev/null
	echo "adding mksd to amavis group GID=$AMAVIS"
fi

%triggerin -- amavisd-new

AMAVIS=$(/usr/bin/getgid amavis)
RESULT=$?
if [ $RESULT -eq 0 ]; then
	/usr/sbin/usermod -G amavis mksd 1>&2 > /dev/null
	echo "adding mksd to amavis group GID=$AMAVIS"
fi

%triggerin -- amavisd
AMAVIS=$(/usr/bin/getgid amavis)
RESULT=$?
if [ $RESULT -eq 0 ]; then
	/usr/sbin/usermod -G amavis mksd 1>&2 > /dev/null
	echo "adding mksd to amavis group GID=$AMAVIS"
fi

%pre
if [ -n "`getgid mksd`" ]; then
	if [ "`getgid mksd`" != "44" ]; then
		echo "Error: group mksd doesn't have gid=44. Correct this before installing Mksd." 1>&2
		exit 1
	fi
else
	echo "adding group mksd GID=44"
	/usr/sbin/groupadd -g 44 -r -f mksd
fi
if [ -n "`id -u mksd 2>/dev/null`" ]; then
	if [ "`id -u mksd`" != "44" ]; then
		echo "Error: user mksd doesn't have uid=44. Correct this before installing Mksd." 1>&2
		exit 1
	fi
else
	echo "adding user mksd UID=44"
	/usr/sbin/useradd -u 44 -r -d /tmp -s /bin/false -c "Mksd Anti Virus Checker" -g mksd mksd 1>&2
	AMAVIS=$(/usr/bin/getgid amavis)
	RESULT=$?
	if [ $RESULT -eq 0 ]; then
		/usr/sbin/usermod -G amavis mksd 1>&2 > /dev/null
		echo "adding to amavis group GID=$AMAVIS"
	fi
fi


%postun
if [ "$1" = "0" ]; then
	echo "Removing user mksd."
	/usr/sbin/userdel mksd
	echo "Removing group mksd."
	/usr/sbin/groupdel mksd
fi

%post
/sbin/chkconfig --add mksd
if [ -f /var/lock/subsys/mksd ]; then
	/etc/rc.d/init.d/mksd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/mksd start\" to start Mksd for Linux daemon."
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/mksd ]; then
		/etc/rc.d/init.d/mksd stop >&2
	fi
	/sbin/chkconfig --del mksd
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
%attr(755,root,root) %{_bindir}/mks[cfsw]*
%doc inne/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/*.a
