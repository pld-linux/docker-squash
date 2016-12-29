#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		docker_squash
%define		egg_name	docker_squash
Summary:	Docker layer squashing tool
Name:		docker-squash
Version:	1.0.3
Release:	2
License:	MIT
Group:		Applications/System
Source0:	https://github.com/goldmann/docker-squash/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a18ba6fc9f80df48f74ca5bbc353d2ee
URL:		https://github.com/goldmann/docker-squash
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-docker
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-docker
BuildRequires:	python3-mock
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
%endif
Requires:	python-%{name} = %{version}-%{release}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tool to squash layers in Docker images.

%package -n python-%{name}
Summary:	Docker layer squashing tool
Group:		Libraries/Python
Obsoletes:	python-docker-scripts <= 1.0.0-0.2.rc2

%description -n python-%{name}
Tool to squash layers in Docker images.

Python 2 version.

%package -n python3-%{name}
Summary:	Docker layer squashing tool
Group:		Libraries/Python
Obsoletes:	python3-docker-scripts <= 1.0.0-0.2.rc2

%description -n python3-%{name}
Tool to squash layers in Docker images.

Python 3 version.

%prep
%setup -q

%build
%if %{with python3}
%py_build
%if %{with tests}
py.test-%{py_ver} -v tests/test_unit*.py
%endif
%endif

%if %{with python3}
%py3_build
%if %{with tests}
py.test-%{py3_ver} -v tests/test_unit*.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
mv $RPM_BUILD_ROOT%{_bindir}/docker-squash{,-2}
%endif
%if %{with python3}
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/docker-squash{,-3}
%endif

ln -s docker-squash-2 $RPM_BUILD_ROOT%{_bindir}/docker-squash

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/docker-squash

%if %{with python2}
%files -n python-%{name}
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{_bindir}/docker-squash-2
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{name}
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{_bindir}/docker-squash-3
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
