# Original version of spec:
# Copyright (c) 2003 Gernot Hillier <gernot@hillier.de>
# Parts Copyright (c) SuSE Linux AG, Nuernberg, Germany.
# License GPLv2+
# Subsequent modifications by various Mandriva maintainers, same
# license

Summary:	ISDN telecommunication suite providing fax and voice services
Name:		capisuite
License:	GPLv2+
Version:	0.4.5
Release:	%mkrel 5
Group:		Communications
URL:		http://www.capisuite.de
Source0:	http://www.capisuite.de/%{name}-%{version}.tar.bz2
Source1:	capisuite-init.bz2
# Fix build with GCC 4.3 (explicit includes) - AdamW 2008/07
Patch0:		capisuite-0.4.5-gcc43.patch
# From Debian: fix build with Python 2.5 on x86-64 - AdamW 2008/07
Patch1:		capisuite-0.4.5-python25.patch
Patch2:		capisuite-0.4.5-fix-build.patch
BuildRequires:	autoconf
BuildRequires:	isdn4k-utils-devel
BuildRequires:	libpython-devel
BuildRequires:	sfftobmp
Requires:	sendmail-command
Requires:	ghostscript
Requires:	libtiff-progs
Requires:	sfftobmp
Requires:	sox
Requires(post,preun):		rpm-helper
BuildRoot:    	%{_tmppath}/%{name}-%{version}

%description
CapiSuite is an ISDN telecommunication suite providing easy to use
telecommunication functions which can be controlled from Python scripts.

It uses a CAPI-compatible driver for accessing the ISDN-hardware, so you'll
need an AVM card with the according driver.

CapiSuite is distributed with two example scripts for call incoming handling
and fax sending. See /usr/share/doc/capisuite for further information.

%prep
%setup -q
bzcat %{SOURCE1} > capisuite-init
%patch0 -p1 -b .gcc43
%patch1 -p0 -b .py25
%patch2 -p0 -b .fix

%build
%configure2_5x --localstatedir=%{_var}
%make 

%install
rm -rf %{buildroot}
%makeinstall_std

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/cron.daily

install -m 644 cronjob.conf %{buildroot}/%{_sysconfdir}/%{name}/cronjob.conf
install -m 755 capisuite-init %{buildroot}/%{_initrddir}/capisuite
install -m 755 capisuite.cron %{buildroot}/%{_sysconfdir}/cron.daily/capisuite
mv %{buildroot}%{_docdir}/%{name} installed-docs

%clean
rm -rf %{buildroot}

%post
%_post_service capisuite

%preun
%_preun_service capisuite

%files
%defattr(-,root,root)
%doc installed-docs/* AUTHORS ChangeLog TODO
%config(noreplace) %{_initrddir}/capisuite
%config(noreplace) %{_sysconfdir}/capisuite/cronjob.conf
%config(noreplace) %{_sysconfdir}/capisuite/capisuite.conf
%config(noreplace) %{_sysconfdir}/capisuite/fax.conf
%config(noreplace) %{_sysconfdir}/capisuite/answering_machine.conf
%config(noreplace) %{_sysconfdir}/cron.daily/capisuite
%{_sbindir}/capisuite
%{_bindir}/capisuitefax
%{_libdir}/capisuite
%{_datadir}/capisuite
%{_localstatedir}/spool/capisuite
%{py_platsitedir}/cs_helpers.py
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
	       
