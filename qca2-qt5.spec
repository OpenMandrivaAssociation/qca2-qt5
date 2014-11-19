%bcond_without docs

%define qtcryptodir %{_qt5_plugindir}/crypto

%define oname qca
%define major 2
%define libname %mklibname %{oname}-qt5_ %{major}
%define devname %mklibname %{oname}-qt5 -d

Summary:	Straightforward and cross-platform crypto API for Qt5
Name:		qca2-qt5
Version:	2.1.0
Release:	1
License:	LGPLv2.1+
Group:		System/Libraries
Url:		http://delta.affinix.com/qca
Source0:	http://delta.affinix.com/download/qca/2.0/%{oname}-%{version}.tar.gz
BuildRequires:	cmake
%if %{with docs}
BuildRequires:	doxygen
%endif
BuildRequires:	rootcerts
BuildRequires:	qmake5
BuildRequires:	sasl-devel
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Network)

%description
The QCA library provides an easy API for a range of cryptographic
features, including SSL/TLS, X.509 certificates, SASL, symmetric
ciphers, public key ciphers, hashes and much more.

Functionality is supplied via plugins. This is useful for avoiding
dependence on a particular crypto library and makes upgrading easier,
as there is no need to recompile your application when adding or
upgrading a crypto plugin. Also, by pushing crypto functionality into
plugins, applications are free of legal issues, such as export
regulation.

%files
%doc README COPYING TODO
%{_qt5_bindir}/mozcerts-qt5
%{_qt5_bindir}/qcatool-qt5
%{_mandir}/man1/qcatool-qt5.1*

#------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Libraries for QCA
Group:		System/Libraries
Requires:	rootcerts

%description -n %{libname}
Libraries for QCA.

%files -n %{libname}
%dir %{qtcryptodir}
%{_qt5_libdir}/libqca-qt5.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for QCA
Group:		Development/KDE and Qt
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development files for QCA.

%files -n %{devname}
%if %{with docs}
%doc build/apidocs
%endif
%{_qt5_libdir}/cmake/Qca/*.cmake
%{_qt5_libdir}/pkgconfig/qca2-qt5.pc
%{_qt5_libdir}/qt5/mkspecs/features/crypto.prf
%dir %{_qt5_includedir}/QtCrypto
%{_qt5_includedir}/QtCrypto/*
%{_qt5_libdir}/libqca-qt5.so

#------------------------------------------------------------------------------

%package plugin-cyrus-sasl
Summary:	Cyrus-sasl plugin for QCA
Group:		Development/KDE and Qt
BuildRequires:	libsasl2-devel
Provides:	qca2-qt5-plugin-cyrus-sasl-%{_lib} = %{EVRD}

%description plugin-cyrus-sasl
This is a plugin to provide cyrus-sasl capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-cyrus-sasl
%{_qt5_plugindir}/crypto/libqca-cyrus-sasl.*

#------------------------------------------------------------------------------

%package plugin-gcrypt
Summary:	Gcrypt plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-qt5-plugin-gcrypt-%{_lib} = %{EVRD}

%description plugin-gcrypt
This is a plugin to provide gcrypt capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-gcrypt
%{_qt5_plugindir}/crypto/libqca-gcrypt.*

#------------------------------------------------------------------------------

%package plugin-gnupg
Summary:	GnuPG plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-qt5-plugin-gnupg-%{_lib} = %{EVRD}
Requires:	gnupg

%description plugin-gnupg
This is a plugin to provide GnuPG capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-gnupg
%{_qt5_plugindir}/crypto/libqca-gnupg.*

#------------------------------------------------------------------------------

%package plugin-logger
Summary:	Logger plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-qt5-plugin-logger-%{_lib} = %{EVRD}

%description plugin-logger
This is a plugin to provide logger capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-logger
%{_qt5_plugindir}/crypto/libqca-logger.*

#------------------------------------------------------------------------------

%package plugin-nss
Summary:	NSS plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-qt5-plugin-nss-%{_lib} = %{EVRD}

%description plugin-nss
This is a plugin to provide nss capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-nss
%{_qt5_plugindir}/crypto/libqca-nss.*

#------------------------------------------------------------------------------

%package plugin-openssl
Summary:	OpenSSL plugin for QCA
Group:		Development/KDE and Qt
BuildRequires:	pkgconfig(openssl)
Provides:	qca2-qt5-plugin-openssl-%{_lib} = %{EVRD}

%description plugin-openssl
This is a plugin to provide OpenSSL capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-openssl
%{_qt5_plugindir}/crypto/libqca-ossl.*

#------------------------------------------------------------------------------

%package plugin-pkcs11
Summary:	PKCS11 plugin for QCA
Group:		Development/KDE and Qt
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libpkcs11-helper-1)
Provides:	qca2-qt5-plugin-pkcs11-%{_lib} = %{EVRD}

%description plugin-pkcs11
This is a plugin to provide PKCS11 capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-pkcs11
%{_qt5_plugindir}/crypto/libqca-pkcs11.*

#------------------------------------------------------------------------------

%package plugin-softstore
Summary:	Softstore plugin for QCA
Group:		Development/KDE and Qt
Provides:	qca2-qt5-plugin-softstore-%{_lib} = %{EVRD}

%description plugin-softstore
This is a plugin to provide softstore capability to programs that
utilize the Qt Cryptographic Architecture (QCA).

%files plugin-softstore
%{_qt5_plugindir}/crypto/libqca-softstore.*

#------------------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}

%build
# Unset CMAKE_INSTALL_PREFIX to use QCA_INSTALL_IN_QT_PREFIX (see CMakeLists.txt)
%cmake_qt5 \
	-DCMAKE_INSTALL_PREFIX="" \
	-DQCA_SUFFIX=qt5 \
	-DQT4_BUILD:BOOL=OFF \
	-DBUILD_TESTS:BOOL=OFF \
	-DWITH_botan_PLUGIN=OFF
%make
%if %{with docs}
%make doc
%endif

%install
%makeinstall_std -C build

# Make directory for plugins
install -d -m 755 %{buildroot}/%{qtcryptodir}

mkdir -p %{buildroot}%{_mandir}
mv %{buildroot}%{_qt5_datadir}/man/man1 %{buildroot}%{_mandir}

