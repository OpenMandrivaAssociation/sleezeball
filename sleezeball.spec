%define name sleezeball
%define version 0.6
%define release 12

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
	if [ ! -e /etc/squid/sleezeball.definitions.old ] ; then
		cp -f /etc/squid/sleezeball.definitions /etc/squid/sleezeball.definitions.old
	fi
	# Stupid trick to lure RPM into ignoring the result code from grep
	( grep -vf /etc/squid/sleezeball.definitions %{_defaultdocdir}/sleezeball/sleezeball.definitions >/etc/squid/sleezeball.definitions.new ) | cat
	cat /etc/squid/sleezeball.definitions.new >>/etc/squid/sleezeball.definitions
	rm -f /etc/squid/sleezeball.definitions.new
else
	cp %{_defaultdocdir}/sleezeball/sleezeball.definitions /etc/squid/sleezeball.definitions
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



%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6-11mdv2011.0
+ Revision: 614898
- the mass rebuild of 2010.1 packages

* Wed Apr 07 2010 Thierry Vignaud <tv@mandriva.org> 0.6-10mdv2010.1
+ Revision: 532574
- fix another accessing doc file in %%post
  (was broken since rpm-mandriva-setup-1.43)
- fix %%post regarding installing, removing, installing again
  (latest of the %%post bugs that were there since years)
- fix accessing doc file in %%post
- indent %%post

* Tue Apr 06 2010 Thierry Vignaud <tv@mandriva.org> 0.6-9mdv2010.1
+ Revision: 532248
- do not blindly generate config file in %%post

* Tue Jun 23 2009 Jérôme Brenier <incubusss@mandriva.org> 0.6-8mdv2010.0
+ Revision: 388119
- fix license tag

* Sat Aug 02 2008 Thierry Vignaud <tv@mandriva.org> 0.6-7mdv2009.0
+ Revision: 260787
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 0.6-6mdv2009.0
+ Revision: 252575
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.6-4mdv2008.1
+ Revision: 127339
- kill re-definition of %%buildroot on Pixel's request
- import sleezeball


* Tue Dec 27 2005 Lenny Cartier <lenny@mandriva.com> 0.6-4mdk
- url

* Thu Jun 12 2003 Marcel Pol <mpol@gmx.net> 0.6-3mdk
- rebuild for rpm 4.2

* Mon Sep 03 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.6-2mdk
- rebuild

* Tue Nov 21 2000 Florin Grad <florin@mandrakesoft.com> 0.6-1mdk 
- first attempt
