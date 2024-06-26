#
# Conditional build:
%bcond_with	bluetooth	# Bluetooth support
%bcond_without	caja		# Caja (mate-file-manager) extension
#
Summary:	User-level file sharing for MATE desktop
Summary(pl.UTF-8):	Współdzielenie plików na poziomie użytkownika dla środowiska MATE
Name:		mate-user-share
Version:	1.28.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://pub.mate-desktop.org/releases/1.28/%{name}-%{version}.tar.xz
# Source0-md5:	5ad96ec7a0f63ee1e248d68544172fb7
URL:		https://github.com/mate-desktop/mate-user-share
%{?with_caja:BuildRequires:	caja-devel >= 1.17.1}
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	libcanberra-gtk3-devel
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libselinux-devel
%{?with_bluetooth:BuildRequires:	mate-bluetooth-devel >= 1.2.0}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.50.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	apache >= 2.2
Requires:	apache-mod_auth_digest >= 2.2
Requires:	apache-mod_authn_file >= 2.2
Requires:	apache-mod_authz_groupfile >= 2.2
Requires:	apache-mod_authz_user >= 2.2
Requires:	apache-mod_dav >= 2.2
Requires:	apache-mod_dnssd >= 0.6
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= 3.22
Requires:	libnotify >= 0.7.0
%{?with_bluetooth:Requires:	mate-bluetooth-libs >= 1.2.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mate-user-share is a small package that binds together various free
software projects to bring easy to use user-level file sharing to the
masses.

%description -l pl.UTF-8
mate-user-share to mały pakiet, łączący kilka wolnodostępnych
projektów, aby zapewnić łatwy sposób współdzielenia plików na poziomie
użytkownika dostępny dla każdego.

%package -n caja-extension-user-share
Summary:	Share extension for Caja (MATE file manager)
Summary(pl.UTF-8):	Rozszerzenie współdzielenia plików dla zarządcy plików Caja
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	caja >= 1.17.1

%description -n caja-extension-user-share
Share (user-level file sharing) extension for Caja (MATE file
manager).

%description -n caja-extension-user-share -l pl.UTF-8
Rozszerzenie share (pozwalające na współdzielenie plików na poziomie
użytkownika) dla zarządcy plików Caja, przeznaczonego dla środowiska
MATE.

%prep
%setup -q

%build
%configure \
	%{!?with_bluetooth:--disable-bluetooth} \
	--disable-schemas-compile \
	--disable-silent-rules \
	--with-httpd=/usr/sbin/httpd \
	--with-modules-path=/etc/httpd/modules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with caja}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0/*.la
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{es_ES,frp,ie,jv,ku_IQ,nah,nqo,pms,ur_PK}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/help/ie

%find_lang %{name} --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-file-share-properties
%attr(755,root,root) %{_libexecdir}/mate-user-share
/etc/xdg/autostart/mate-user-share-obexftp.desktop
/etc/xdg/autostart/mate-user-share-obexpush.desktop
/etc/xdg/autostart/mate-user-share-webdav.desktop
%{_datadir}/glib-2.0/schemas/org.mate.FileSharing.gschema.xml
%{_datadir}/mate-user-share
%{_desktopdir}/mate-user-share-properties.desktop
%{_iconsdir}/hicolor/*x*/apps/mate-obex-server.png
%{_mandir}/man1/mate-file-share-properties.1*

%if %{with caja}
%files -n caja-extension-user-share
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/caja/extensions-2.0/libcaja-user-share.so
%{_datadir}/caja/extensions/libcaja-user-share.caja-extension
%endif
