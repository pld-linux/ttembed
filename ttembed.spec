#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Remove embedding limitations from TrueType fonts
Name:		ttembed
Version:	1.1
Release:	2
License:	Public Domain
Group:		Applications
Source0:	https://github.com/hisdeedsaredust/ttembed/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1eccad30e260d4ccd2a1f8a9b1a165ce
URL:		https://github.com/hisdeedsaredust/ttembed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Remove embedding limitations from TrueType fonts, by setting the
fsType field in the OS/2 table to zero. That's it; this program is a
one-trick pony.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags}" \
%{__make}

%if %{with tests}
# smoke test - fail on not font file
echo 'not a font' > test
if [ "$(./ttembed test 2>&1)" != "test: Not TTF/OTF" ]; then
	echo "TEST FAIL: not a font input test" 1>&2
	exit 1
fi
rm test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install -p %{name} $RPM_BUILD_ROOT%{_bindir}
cp -p %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/ttembed
%{_mandir}/man1/ttembed.1*
