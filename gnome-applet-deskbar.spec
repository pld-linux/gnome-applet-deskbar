#
# Conditional build:
%bcond_without	evolution	# build without evolution support
#
%define		realname	deskbar-applet
Summary:	GNOME applet similar to Google's Deskbar
Summary(pl.UTF-8):	Aplet GNOME podobny do Google Deskbar
Name:		gnome-applet-deskbar
Version:	2.20.3
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/deskbar-applet/2.20/%{realname}-%{version}.tar.bz2
# Source0-md5:	f84abfede0bbe5b172b24f581550e4a0
Patch0:		%{name}-pyc.patch
URL:		http://raphael.slinckx.net/deskbar/
BuildRequires:	GConf2-devel >= 2.20.1
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_evolution:BuildRequires:	evolution-data-server-devel >= 1.12.0}
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel >= 2.20.0
BuildRequires:	intltool >= 0.36.2
BuildRequires:	pkgconfig
BuildRequires:	python-dbus-devel >= 0.80.2
BuildRequires:	python-gnome-desktop-devel >= 2.20.0
BuildRequires:	python-pygtk-devel >= 2:2.12.0
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sed >= 4.0
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	pydoc
Requires:	python-gnome-desktop-applet >= 2.20.0
Requires:	python-gnome-gconf >= 2.20.0
Requires:	python-gnome-ui >= 2.20.0
Suggests:	python-beagle
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME applet similar to Google's Deskbar.

%description -l pl.UTF-8
Aplet GNOME podobny do Google Deskbar.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

sed -i -e 's#sr\@Latn#sr\@latin#' po/LINGUAS
mv -f po/sr\@{Latn,latin}.po

%build
%{__intltoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--disable-scrollkeeper \
	--%{!?with_evolution:dis}%{?with_evolution:en}able-evolution
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pythondir=%{py_sitedir}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/deskbar/*.py
rm -f $RPM_BUILD_ROOT%{py_sitedir}/deskbar/*/*.{la,py}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/deskbar/*/*/*.{la,py}
rm -f $RPM_BUILD_ROOT%{_libdir}/deskbar-applet/modules-2.20-compatible/*.py

%find_lang %{name} --with-gnome --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%gconf_schema_install deskbar-applet.schemas
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall deskbar-applet.schemas

%postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%{_sysconfdir}/gconf/schemas/deskbar-applet.schemas
%{_datadir}/deskbar-applet
%dir %{_libdir}/deskbar-applet
%attr(755,root,root) %{_libdir}/deskbar-applet/deskbar-applet
%dir %{_libdir}/deskbar-applet/modules-2.20-compatible
%{_libdir}/deskbar-applet/modules-2.20-compatible/*.py[co]
%{_libdir}/bonobo/servers/*.server
%dir %{py_sitedir}/deskbar

%if %{with evolution}
%dir %{py_sitedir}/deskbar/handlers/evolution
%{py_sitedir}/deskbar/handlers/evolution/*.py[co]
%attr(755,root,root) %{py_sitedir}/deskbar/handlers/evolution/*.so
%endif

%dir %{py_sitedir}/deskbar/handlers
%dir %{py_sitedir}/deskbar/handlers/actions
%dir %{py_sitedir}/deskbar/handlers/gdmclient
%dir %{py_sitedir}/deskbar/core/gnomedesktop
%dir %{py_sitedir}/deskbar/core
%dir %{py_sitedir}/deskbar/ui/iconentry
%dir %{py_sitedir}/deskbar/core/keybinder
%dir %{py_sitedir}/deskbar/osutils
%dir %{py_sitedir}/deskbar/ui
%dir %{py_sitedir}/deskbar/ui/cuemiac
%dir %{py_sitedir}/deskbar/ui/preferences
%dir %{py_sitedir}/deskbar/interfaces
%dir %{py_sitedir}/deskbar/core/updater
%{py_sitedir}/deskbar/handlers/*.py[co]
%{py_sitedir}/deskbar/handlers/actions/*.py[co]
%{py_sitedir}/deskbar/handlers/gdmclient/*.py[co]
%{py_sitedir}/deskbar/core/gnomedesktop/*.py[co]
%{py_sitedir}/deskbar/core/*.py[co]
%{py_sitedir}/deskbar/ui/iconentry/*.py[co]
%{py_sitedir}/deskbar/core/keybinder/*.py[co]
%{py_sitedir}/deskbar/osutils/*.py[co]
%{py_sitedir}/deskbar/*.py[co]
%{py_sitedir}/deskbar/ui/cuemiac/*.py[co]
%{py_sitedir}/deskbar/ui/preferences/*.py[co]
%{py_sitedir}/deskbar/interfaces/*.py[co]
%{py_sitedir}/deskbar/ui/*.py[co]
%{py_sitedir}/deskbar/core/updater/*.py[co]
%attr(755,root,root) %{py_sitedir}/deskbar/handlers/gdmclient/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/core/gnomedesktop/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/ui/iconentry/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/core/keybinder/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/osutils/*.so
%{_pkgconfigdir}/deskbar-applet.pc
%{_iconsdir}/hicolor/*/apps/*
