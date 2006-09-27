#
# Conditional build:
%bcond_without	evolution	# build without evolution support
#
%define		_realname	deskbar-applet
Summary:	GNOME applet similar to Google's Deskbar
Summary(pl):	Aplet GNOME podobny do Google Deskbar
Name:		gnome-applet-deskbar
Version:	2.16.0
Release:	2
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/deskbar-applet/2.16/%{_realname}-%{version}.tar.bz2
# Source0-md5:	9f14a65f75142cd5b233bf9376a1f946
Patch0:		%{name}-pyc.patch
URL:		http://browserbookapp.sourceforge.net/deskbar.html
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_evolution:BuildRequires:	evolution-data-server-devel >= 1.8.0}
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel >= 2.16.0
BuildRequires:	intltool >= 0.35
BuildRequires:	pkgconfig
BuildRequires:	python-gnome-desktop-devel >= 2.16.0
BuildRequires:	python-pygtk-devel >= 2.10.1
BuildRequires:	rpmbuild(macros) >= 1.311
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,preun):	gtk+2 >= 2:2.10.3
Requires:	pydoc
Requires:	python-gnome-desktop-applet >= 2.16.0
Requires:	python-gnome-gconf >= 2.16.0
Requires:	python-gnome-ui >= 2.16.0
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
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall deskbar-applet.schemas
%update_icon_cache hicolor

%files -f %{_realname}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%{_datadir}/deskbar-applet
%dir %{_libdir}/deskbar-applet
%attr(755,root,root) %{_libdir}/deskbar-applet/deskbar-applet
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
%dir %{py_sitedir}/deskbar/ui/window
%{py_sitedir}/deskbar/gdmclient/*.py[co]
%{py_sitedir}/deskbar/gnomedesktop/*.py[co]
%{py_sitedir}/deskbar/iconentry/*.py[co]
%{py_sitedir}/deskbar/keybinder/*.py[co]
%{py_sitedir}/deskbar/osutils/*.py[co]
%{py_sitedir}/deskbar/*.py[co]
%{py_sitedir}/deskbar/ui/cuemiac/*.py[co]
%{py_sitedir}/deskbar/ui/entriac/*.py[co]
%{py_sitedir}/deskbar/ui/window/*.py[co]
%{py_sitedir}/deskbar/ui/*.py[co]
%attr(755,root,root) %{py_sitedir}/deskbar/gdmclient/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/gnomedesktop/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/iconentry/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/keybinder/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/osutils/*.so

%{_iconsdir}/hicolor/*/apps/*
%{_sysconfdir}/gconf/schemas/deskbar-applet.schemas
