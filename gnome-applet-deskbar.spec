#
# TODO:
# - beagle bcond
# - evolution bcond
#
%define		_realname	deskbar-applet
Summary:	GNOME applet similar to Google's Deskbar
Summary(pl):	Aplet GNOME podobny do Google Deskbar
Name:		gnome-applet-deskbar
Version:	0.8.0
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/browserbookapp/%{_realname}-%{version}.tar.gz
# Source0-md5:	8757a851d8f081c1236eb658b75e32dc
URL:		http://browserbookapp.sourceforge.net/deskbar.html
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	beagle-devel
BuildRequires:	evolution-data-server-devel
BuildRequires:	gettext-devel
BuildRequires:	intltool >= 0.33
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2.8.0
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	pydoc
Requires:	python-gnome-extras-applet >= 2.12.0
Requires:	python-gnome-gconf >= 2.12.0
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
	--enable-beagle \
	--enable-evolution
	
%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) %{_libdir}/deskbar-applet/deskbar-applet
%{_libdir}/bonobo/servers/*.server
%{_libdir}/deskbar-applet
%{py_sitescriptdir}/deskbar
%{_datadir}/deskbar-applet
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/deskbar-applet.schemas
