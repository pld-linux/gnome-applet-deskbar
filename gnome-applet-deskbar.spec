#
# Conditional build:
%bcond_with	beagle		# build with beagle support
%bcond_without	evolution	# build without evolution support
#
%define		_realname	deskbar-applet
Summary:	GNOME applet similar to Google's Deskbar
Summary(pl):	Aplet GNOME podobny do Google Deskbar
Name:		gnome-applet-deskbar
Version:	0.8.2
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/browserbookapp/%{_realname}-%{version}.tar.gz
# Source0-md5:	762dde3a98bb98907532e501520fae59
URL:		http://browserbookapp.sourceforge.net/deskbar.html
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_beagle:BuildRequires:	beagle-devel}
%{?with_evolution:BuildRequires:	evolution-data-server-devel}
BuildRequires:	gettext-devel
BuildRequires:	intltool >= 0.33
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2.8.0
BuildRequires:	rpmbuild(macros) >= 1.197
%{?with_evolution:Requires:	evolution}
Requires:	pydoc
Requires:	python-gnome-extras-applet >= 2.12.0
Requires:	python-gnome-gconf >= 2.12.0
Requires:	python-gnome-ui >= 2.12.0
Requires:	python-gnome-vfs >= 2.12.0
Requires(post,preun):	GConf2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME applet similar to Google's Deskbar.

%description -l pl
Aplet GNOME podobny do Google Deskbar.

%prep
%setup -q -n %{_realname}-%{version}

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--%{!?with_beagle:dis}%{?with_beagle:en}able-beagle \
	--%{!?with_evolution:dis}%{?with_evolution:en}able-evolution
	
%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/deskbar/*.py
rm -f $RPM_BUILD_ROOT%{py_sitescriptdir}/deskbar/{beagle,evolution,iconentry,keybinder}/*.{la,py}

%find_lang %{_realname}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install deskbar-applet.schemas

%preun
%gconf_schema_uninstall deskbar-applet.schemas

%files -f %{_realname}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%{_datadir}/deskbar-applet
%dir %{_libdir}/deskbar-applet
%attr(755,root,root) %{_libdir}/deskbar-applet/deskbar-applet
%{_libdir}/deskbar-applet/handlers
%{_libdir}/bonobo/servers/*.server
%dir %{py_sitescriptdir}/deskbar
%if %{with beagle}
%dir %{py_sitescriptdir}/deskbar/beagle
%{py_sitescriptdir}/deskbar/beagle/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/deskbar/beagle/*.so
%endif
%if %{with evolution}
%dir %{py_sitescriptdir}/deskbar/evolution
%{py_sitescriptdir}/deskbar/evolution/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/deskbar/evolution/*.so
%endif
%dir %{py_sitescriptdir}/deskbar/iconentry
%dir %{py_sitescriptdir}/deskbar/keybinder
%{py_sitescriptdir}/deskbar/*.py[co]
%{py_sitescriptdir}/deskbar/iconentry/*.py[co]
%{py_sitescriptdir}/deskbar/keybinder/*.py[co]
%attr(755,root,root) %{py_sitescriptdir}/deskbar/iconentry/*.so
%attr(755,root,root) %{py_sitescriptdir}/deskbar/keybinder/*.so
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/deskbar-applet.schemas
