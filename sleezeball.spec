%define name sleezeball
%define version 0.6
%define release %mkrel 9

Summary:  A redirector for Squid2 that zapps banners
Name:  %name
Version: %version
Release: %release
License:  GPLv2+
Group:  System/Servers
Source:  http://fredrik.rambris.com/files/%name-%version.tar.bz2
URL:  http://fredrik.rambris.com/sleezeball/
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires:  squid

%description
SleezeBall is a redirector to be used with the Squid proxy. It tries to guess
what is a banner and then tells Squid to load a local image instead. This
has the nice effect of saving you from downloading and seeing a lot of ugly
banners (linux.com has such goodlooking banners that I can't bring me to
filter them out).

%prep

%setup -q
patch <sleezeball-make.patch

%build
perl -pi -e "s|/usr/sbin|$RPM_BUILD_ROOT/%{_sbindir}|" Makefile
perl -pi -e "s|/usr/lib|$RPM_BUILD_ROOT/%{_libdir}|" Makefile
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/squid/icons
make install

mkdir -p $RPM_BUILD_ROOT/etc/squid/
echo >$RPM_BUILD_ROOT/etc/squid/sleezeball.conf <<EOF
# The SleezeBall Configuration

# The URL to redirect banners to
REDIRECT_URL=http://${HOSTNAME}:3128/squid-internal-static/icons/banner.gif

# Uncomment this to enable log
# LOG=/var/log/squid/sleezeball.log
EOF


%post
if ! grep -q "banner" /etc/squid/mime.conf ; then echo 'internal-banner	-	banner.gif	-	image' >>/etc/squid/mime.conf ; fi

if [ -e /etc/squid/sleezeball.definitions ] ; then
	cp -f /etc/squid/sleezeball.definitions /etc/squid/sleezeball.definitions.old
	# Stupid trick to lure RPM into ignoring the result code from grep
	( grep -vf /etc/squid/sleezeball.definitions %{_defaultdocdir}/sleezeball-%{version}/sleezeball.definitions >/etc/squid/sleezeball.definitions.new ) | cat
	cat /etc/squid/sleezeball.definitions.new >>/etc/squid/sleezeball.definitions
	rm -f /etc/squid/sleezeball.definitions.new
else
	cp %{_defaultdocdir}/sleezeball-%{version}/sleezeball.definitions /etc/squid/sleezeball.definitions
fi

%clean
if [ -d $RPM_BUILD_ROOT ]; then rm -r $RPM_BUILD_ROOT; fi


%files
%defattr(-, root, root, 0755)
%doc README COPYING ChangeLog sleezeball.definitions
%config(noreplace) /etc/squid/sleezeball.conf
%{_libdir}/squid/sleezeball
%{_libdir}/squid/icons/banner.gif
%{_sbindir}/reloadszb

