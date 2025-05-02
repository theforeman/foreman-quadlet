%global pypi_name cli

Name:           python-%{pypi_name}
Version:        0.0.1
Release:        0%{?dist}
Summary:        Install Foreman using containers

License:        GPL-2-only
URL:            https://github.com/theforeman/foreman-quadlet
Source:         %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
...}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}

Requires:       podman
Requires:       python3-libsemanage

Recommends:     python3-%{pypi_name}+argcomplete

%description -n python3-%{pypi_name} %_description

%package -n python3-%{pypi_name}+argcomplete
Summary: Autocompletion for python3-%{pypi_name}
Requires: python3-%{pypi_name} = %{?epoch:%{epoch}:}%{version}-%{release}
Suggests: bash-completion

%description -n python3-%{pypi_name}+argcomplete
This is a metapackage bringing in the dependencies for autocompletion.
It contains no code, just makes sure the dependencies are installed.

%files -n python3-%{pypi_name}+argcomplete
%ghost %{python3_sitelib}/*.dist-info


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%check
%pyproject_check_import %{pypi_name}


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.*
%{_bindir}/rop


%changelog
