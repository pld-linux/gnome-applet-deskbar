#
# Conditional build:
%bcond_without	evolution	# build without evolution support
#
%define		_realname	deskbar-applet
Summary:	GNOME applet similar to Google's Deskbar
Summary(pl):	Aplet GNOME podobny do Google Deskbar
Name:		gnome-applet-deskbar
Version:	2.15.3
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/deskbar-applet/2.15/%{_realname}-%{version}.tar.bz2
# Source0-md5:	97562c5c5935b9f580e73afc876c7a93
Patch0:		%{name}-pyc.patch
URL:		http://browserbookapp.sourceforge.net/deskbar.html
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_evolution:BuildRequires:	evolution-data-server-devel >= 1.7.2}
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel >= 2.15.2
BuildRequires:	intltool >= 0.35
BuildRequires:	pkgconfig
BuildRequires:	python-gnome-desktop-devel >= 2.15.3
BuildRequires:	python-pygtk-devel >= 2.9.0
BuildRequires:	rpmbuild(macros) >= 1.197
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,preun):	gtk+2 >= 2:2.9.2
Requires:	pydoc
Requires:	python-gnome-desktop-applet >= 2.15.3
Requires:	python-gnome-gconf >= 2.15.1
Requires:	python-gnome-ui >= 2.15.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME applet similar to Google's Deskbar.

%description -l pl
Aplet GNOME podobny do Google Deskbar.

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--%{!?with_evolution:dis}%{?with_evolution:en}able-evolution

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pythondir=%{py_sitedir}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/deskbar/*.py
rm -f $RPM_BUILD_ROOT%{py_sitedir}/deskbar/*/*.{la,py}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/deskbar/*/*/*.{la,py}
rm -f $RPM_BUILD_ROOT%{_libdir}/deskbar-applet/handlers/*.py

%find_lang %{_realname}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install deskbar-applet.schemas
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor

%preun
%gconf_schema_uninstall deskbar-applet.schemas
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor

%files -f %{_realname}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%{_datadir}/deskbar-applet
%dir %{_libdir}/deskbar-applet
%attr(755,root,root) %{_libdir}/deskbar-applet/deskbar-applet
%attr(755,root,root) %{_libdir}/deskbar-applet/new-stuff-manager
%dir %{_libdir}/deskbar-applet/handlers
%{_libdir}/deskbar-applet/handlers/*.py[co]
%{_libdir}/bonobo/servers/*.server
%dir %{py_sitedir}/deskbar

%if %{with evolution}
%dir %{py_sitedir}/deskbar/evolution
%{py_sitedir}/deskbar/evolution/*.py[co]
%attr(755,root,root) %{py_sitedir}/deskbar/evolution/*.so
%endif

%dir %{py_sitedir}/deskbar/gdmclient
%dir %{py_sitedir}/deskbar/gnomedesktop
%dir %{py_sitedir}/deskbar/iconentry
%dir %{py_sitedir}/deskbar/keybinder
%dir %{py_sitedir}/deskbar/osutils
%dir %{py_sitedir}/deskbar/ui
%dir %{py_sitedir}/deskbar/ui/cuemiac
%dir %{py_sitedir}/deskbar/ui/entriac
%dir %{py_sitedir}/deskbar/updater
%{py_sitedir}/deskbar/gdmclient/*.py[co]
%{py_sitedir}/deskbar/gnomedesktop/*.py[co]
%{py_sitedir}/deskbar/iconentry/*.py[co]
%{py_sitedir}/deskbar/keybinder/*.py[co]
%{py_sitedir}/deskbar/osutils/*.py[co]
%{py_sitedir}/deskbar/*.py[co]
%{py_sitedir}/deskbar/ui/cuemiac/*.py[co]
%{py_sitedir}/deskbar/ui/entriac/*.py[co]
%{py_sitedir}/deskbar/ui/*.py[co]
%{py_sitedir}/deskbar/updater/*.py[co]
%attr(755,root,root) %{py_sitedir}/deskbar/gdmclient/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/gnomedesktop/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/iconentry/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/keybinder/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/osutils/*.so

%{_datadir}/dbus-1/services/*.service
%{_iconsdir}/hicolor/*/apps/*
%{_sysconfdir}/gconf/schemas/deskbar-applet.schemas
