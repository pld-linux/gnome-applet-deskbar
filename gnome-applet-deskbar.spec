%define		_realname	deskbar-applet
Summary:	GNOME applet similar to Google's Deskbar
Summary(pl):	Aplet GNOME podobny do Google Deskbar
Name:		gnome-applet-deskbar
Version:	0.2
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/browserbookapp/%{_realname}-%{version}.tar.gz
# Source0-md5:	051558aa867073aa901dc1049ae0ae12
URL:		http://browserbookapp.sourceforge.net/deskbar.html
BuildRequires:	sed >= 4.0
Requires:	python-gnome-applet
Requires:	python-gnome-gconf
Requires(post):	GConf2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appletdirname		%{_datadir}/deskbar-applet

%description
GNOME applet similar to Google's Deskbar.

%description -l pl
Aplet GNOME podobny do Google Deskbar.

%prep
%setup -q -n %{_realname}-%{version}

%build
sed -i -e "s:%{_prefix}/libexec:%{_appletdirname}:" DeskbarApplet.server

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_appletdirname},%{_libdir}/bonobo/servers}
install DeskbarApplet.server $RPM_BUILD_ROOT%{_libdir}/bonobo/servers
install deskbar-applet.py $RPM_BUILD_ROOT%{_appletdirname}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install

%files
%defattr(644,root,root,755)
%doc CHANGELOG
%attr(755,root,root) %{_appletdirname}
%{_libdir}/bonobo/servers/*.server
