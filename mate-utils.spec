Summary:	MATE utilities
Name:		mate-utils
Version:	1.6.1
Release:	1
Epoch:		1
License:	GPL v2
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	936114a9cb7b42e43c56a0823cbb8258
URL:		http://www.mate.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	mate-desktop-devel
BuildRequires:	mate-panel-devel
BuildRequires:	intltool
BuildRequires:	libgtop-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	popt-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	rarian
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE utility programs.

%package -n libmatedict
Summary:	libmatedict library
Group:		Libraries

%description -n libmatedict
libmatedict library.

%package -n libmatedict-devel
Summary:	Header files for libmatedict library
Group:		Development/Libraries
Requires:	libmatedict = %{epoch}:%{version}-%{release}

%description -n libmatedict-devel
This is the package containing the header files for libmatedict library.

%package -n libmatedict-apidocs
Summary:	libmatedict API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description -n libmatedict-apidocs
libmatedict API documentation.

%package disk-usage-analyzer
Summary:	Graphical directory tree analyzer
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description disk-usage-analyzer
Graphical directory tree analyzer.

%package dictionary
Summary:	Online dictionary
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dictionary
Allows to look up an online dictionary for definitions and correct
spellings of words.

%package logview
Summary:	System log viewer for MATE
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description logview
Allows to view system logs.

%package search-tool
Summary:	MATE search tool
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description search-tool
Allows to search for files on system.

%package screenshot
Summary:	Screenshot utility
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description screenshot
Allows to make a desktop screenshot.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e 's/MATE_COMPILE_WARNINGS.*//g'	\
    -i -e 's/MATE_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/MATE_COMMON_INIT//g'		\
    -i -e 's/MATE_DEBUG_CHECK//g' configure.ac

%{__sed} -i 's/Icon.*/Icon=mate-disk-usage-analyzer/' \
	baobab/data/mate-disk-usage-analyzer.desktop.in.in

%build
%{__intltoolize}
%{__libtoolize}
mate-doc-prepare --copy --force
%{__gtkdocize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name}
%find_lang mate-disk-usage-analyzer --with-mate --with-omf
%find_lang mate-dictionary --with-mate --with-omf
%find_lang mate-search-tool --with-mate --with-omf --all-name
%find_lang mate-system-log --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n libmatedict -p /usr/sbin/ldconfig
%postun -n libmatedict -p /usr/sbin/ldconfig

%post disk-usage-analyzer
%scrollkeeper_update_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun disk-usage-analyzer
%scrollkeeper_update_postun
%update_gsettings_cache

%post dictionary
%scrollkeeper_update_post
%update_gsettings_cache

%postun dictionary
%scrollkeeper_update_postun
%update_gsettings_cache

%post logview
%scrollkeeper_update_post
%update_gsettings_cache

%postun logview
%scrollkeeper_update_postun
%update_gsettings_cache

%post search-tool
%scrollkeeper_update_post
%update_gsettings_cache

%postun search-tool
%scrollkeeper_update_postun
%update_gsettings_cache

%post screenshot
%update_gsettings_cache

%postun screenshot
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%dir %{_datadir}/%{name}

%files -n libmatedict
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libmatedict.so.?
%attr(755,root,root) %{_libdir}/libmatedict.so.*.*.*
%{_datadir}/mate-dict

%files -n libmatedict-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmatedict.so
%{_includedir}/mate-dict
%{_pkgconfigdir}/mate-dict.pc

%files -n libmatedict-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-dict

%files disk-usage-analyzer -f mate-disk-usage-analyzer.lang
%defattr(644,root,root,755)
%doc baobab/AUTHORS baobab/README baobab/TODO
%attr(755,root,root) %{_bindir}/mate-disk-usage-analyzer
%{_datadir}/glib-2.0/schemas/org.mate.disk-usage-analyzer.gschema.xml
%{_desktopdir}/mate-disk-usage-analyzer.desktop
%{_iconsdir}/hicolor/*/*/mate-disk-usage-analyzer.*
%{_datadir}/mate-disk-usage-analyzer
%{_mandir}/man1/mate-disk-usage-analyzer*

%files dictionary -f mate-dictionary.lang
%defattr(644,root,root,755)
%doc mate-dictionary/README mate-dictionary/TODO
%attr(755,root,root) %{_bindir}/mate-dictionary
%attr(755,root,root) %{_libdir}/mate-dictionary-applet
%{_datadir}/dbus-1/services/org.mate.panel.applet.DictionaryAppletFactory.service
%{_datadir}/glib-2.0/schemas/org.mate.dictionary.gschema.xml
%{_datadir}/mate-dictionary
%{_datadir}/mate-panel/applets/org.mate.DictionaryApplet.mate-panel-applet
%{_desktopdir}/mate-dictionary.desktop
%{_mandir}/man1/mate-dictionary*

%files logview -f mate-system-log.lang
%defattr(644,root,root,755)
%doc logview/TODO
%attr(755,root,root) %{_bindir}/mate-system-log
%{_datadir}/%{name}/logview-filter.ui
%{_datadir}/%{name}/logview-toolbar.xml
%{_datadir}/glib-2.0/schemas/org.mate.system-log.gschema.xml
%{_desktopdir}/mate-system-log.desktop
%{_mandir}/man1/mate-system-log*

%files search-tool -f mate-search-tool.lang
%defattr(644,root,root,755)
%doc gsearchtool/AUTHORS
%attr(755,root,root) %{_bindir}/mate-search-tool
%{_datadir}/glib-2.0/schemas/org.mate.search-tool.gschema.xml
%{_desktopdir}/mate-search-tool.desktop
%{_mandir}/man1/mate-search-tool*
%{_pixmapsdir}/mate-search-tool

%files screenshot
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mate-panel-screenshot
%attr(755,root,root) %{_bindir}/mate-screenshot
%{_datadir}/glib-2.0/schemas/org.mate.screenshot.gschema.xml
%{_datadir}/mate-screenshot
%{_desktopdir}/mate-screenshot.desktop
%{_mandir}/man1/mate-screenshot.1*

