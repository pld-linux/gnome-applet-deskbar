#
# Conditional build:
%bcond_without	evolution	# build without evolution support
#
%define		_realname	deskbar-applet
Summary:	GNOME applet similar to Google's Deskbar
Summary(pl):	Aplet GNOME podobny do Google Deskbar
Name:		gnome-applet-deskbar
Version:	0.8.6
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/deskbar-applet/0.8/%{_realname}-%{version}.tar.bz2
# Source0-md5:	67507881804181b749d5e317a76b91ee
Patch0:		%{name}-pyc.patch
URL:		http://browserbookapp.sourceforge.net/deskbar.html
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_evolution:BuildRequires:	evolution-data-server-devel}
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel >= 2.10
BuildRequires:	intltool >= 0.33
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2.8.0
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	pydoc
Requires:	python-gnome-extras-applet >= 2.12.0
Requires:	python-gnome-gconf >= 2.12.0
Requires:	python-gnome-ui >= 2.12.0
Requires(post,preun):	GConf2
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
rm -f $RPM_BUILD_ROOT%{py_sitedir}/deskbar/{evolution,gnomedesktop,iconentry,keybinder}/*.{la,py}
rm -f $RPM_BUILD_ROOT%{_libdir}/deskbar-applet/handlers/*.py

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
%dir %{_libdir}/deskbar-applet/handlers
%{_libdir}/deskbar-applet/handlers/*.py[co]
%{_libdir}/bonobo/servers/*.server
%dir %{py_sitedir}/deskbar

%if %{with evolution}
%dir %{py_sitedir}/deskbar/evolution
%{py_sitedir}/deskbar/evolution/*.py[co]
%attr(755,root,root) %{py_sitedir}/deskbar/evolution/*.so
%endif

%dir %{py_sitedir}/deskbar/gnomedesktop
%dir %{py_sitedir}/deskbar/iconentry
%dir %{py_sitedir}/deskbar/keybinder
%{py_sitedir}/deskbar/*.py[co]
%{py_sitedir}/deskbar/gnomedesktop/*.py[co]
%{py_sitedir}/deskbar/iconentry/*.py[co]
%{py_sitedir}/deskbar/keybinder/*.py[co]
%attr(755,root,root) %{py_sitedir}/deskbar/gnomedesktop/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/iconentry/*.so
%attr(755,root,root) %{py_sitedir}/deskbar/keybinder/*.so
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/deskbar-applet.schemas
