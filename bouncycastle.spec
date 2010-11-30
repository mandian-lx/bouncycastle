%define major           1
%define minor           43
%define archivever      %{major}%{minor}

%define section         free

%define gcj_support     0

Name:           bouncycastle
Version:        %{major}.%{minor}
Release:        %mkrel 3
Epoch:          0
Summary:        Bouncy Castle Crypto Package for Java
Group:          Development/Java
License:        BSD
URL:            http://www.bouncycastle.org/
Source0:        http://www.bouncycastle.org/download/crypto-%{archivever}.tar.gz
# Invalid characters in comments prevent build
# "file" says they are UTF-8 but they are not
Patch0:		crypto-invalid-characters.patch
# UTF-8 characters in one testcase and one comment
# FIXME: fix properly with javac command-line option or so
Patch1:		crypto-utf8-characters.patch
Requires:       jpackage-utils >= 0:1.5
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  geronimo-jaf-1.0.2-api
BuildRequires:  geronimo-javamail-1.3.1-api
BuildRequires:  junit
BuildRequires:  java-rpmbuild >= 0:1.5
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif # gcj_support
# BEGIN PROVIDER
BuildRequires:  java-devel
BuildRequires:  java < 0:1.8.0
Obsoletes:      %{name}-provider < %{epoch}:%{version}-%{release}
Provides:       %{name}-provider = %{epoch}:%{version}-%{release}
Provides:       jce = 1.7.0.0
# END PROVIDER
# (Anssi 01/2008) Obsolete the old jdk1.4 subpackage:
Obsoletes:	bouncycastle-jdk1.4 < %{epoch}:%{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Bouncy Castle Crypto APIs consist of the following:
- A lightweight cryptography API in Java.
- A provider for the JCE and JCA.
- A clean room implementation of the JCE 1.2.1.
- Generators for Version 1 and Version 3 X.509 certificates and PKCS12 files.
- A signed jar version suitable for JDK 1.4 and the Sun JCE.

%package extras
Summary:	Extra packages of Bouncy Castle
Group:		Development/Java
Requires:	%{name}
Requires:       geronimo-jaf-1.0.2-api
Requires:       geronimo-javamail-1.3.1-api
Conflicts:	bouncycastle < 1.43-1

%description extras
The SMIME/CMS, TSP, OpenPGP/BCPG portions of Bouncy Castle.

%package javadoc
Group:          Development/Java
Summary:        Javadocs for %{name}
Obsoletes:      bouncycastle-javadoc-jdk1.4 < %{epoch}:%{version}-%{release}

%description javadoc
Javadocs for %{name}.

%prep
%setup -q -n crypto-%{archivever}
%patch0 -p1
%patch1 -p1
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}
%{__perl} -pi -e 's/<javac/<javac nowarn="true"/g' *.xml

%build
export CLASSPATH=$(build-classpath jaf javamail/mailapi junit)
export OPT_JAR_LIST="`%{__cat} %{_sysconfdir}/ant.d/junit`"
export JAVA_HOME=%{_jvmdir}/java-1.7.0
%ant -f jdk16.xml -Drelease.suffix=%{version} build-provider build build-test

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}

pushd build/artifacts/jdk1.6/jars
for jar16 in {bcmail,bcpg,bcprov,bctest,bctsp}-jdk16-%{version}.jar; do
   jar16d=`echo $jar16 | %{__sed} s#-jdk16##g`
   %{__install} -m 644 $jar16 %{buildroot}%{_javadir}/$jar16d
done
popd

pushd %{buildroot}%{_javadir}
  for jar in *-%{version}.jar; do
    %{__ln_s} $jar $(echo $jar | %{__sed} s#-%{version}##g)
  done
popd

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

pushd build/artifacts/jdk1.6
  ver=16
  for javadoc in bcmail bcpg bcprov bctsp; do
    %{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}/${javadoc}
    %{__cp} -a ${javadoc}-jdk${ver}-%{version}/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/${javadoc}
  done
popd

%{__mkdir_p} %{buildroot}%{_javadir}/gcj-endorsed
(cd %{buildroot}%{_javadir}/gcj-endorsed && %{__ln_s} %{_javadir}/bcprov.jar .)

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif # gcj_support

%clean
%{__rm} -rf %{buildroot}

%post
if test -x %{_bindir}/rebuild-security-providers; then
  %{_bindir}/rebuild-security-providers
fi
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
if test -x %{_bindir}/rebuild-security-providers; then
  %{_bindir}/rebuild-security-providers
fi
%if %{gcj_support}
%{clean_gcjdb}
%endif # gcj_support

%files
%defattr(0644,root,root,0755)
%doc *.html
# BEGIN PROVIDER
%{_javadir}/bcprov-%{version}.jar
%{_javadir}/bcprov.jar
%{_javadir}/gcj-endorsed/bcprov.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/bcprov-%{version}.jar.so
%{_libdir}/gcj/%{name}/bcprov-%{version}.jar.db
%endif
# END PROVIDER

%files extras
%defattr(-,root,root)
%{_javadir}/bcmail-%{version}.jar
%{_javadir}/bcpg-%{version}.jar
%{_javadir}/bctest-%{version}.jar
%{_javadir}/bctest.jar
%{_javadir}/bctsp-%{version}.jar
%{_javadir}/bcmail.jar
%{_javadir}/bcpg.jar
%{_javadir}/bctsp.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}/bcmail-%{version}.jar.so
%{_libdir}/gcj/%{name}/bcmail-%{version}.jar.db
%{_libdir}/gcj/%{name}/bcpg-%{version}.jar.so
%{_libdir}/gcj/%{name}/bcpg-%{version}.jar.db
%{_libdir}/gcj/%{name}/bctest-%{version}.jar.db
%{_libdir}/gcj/%{name}/bctest-%{version}.jar.so
%{_libdir}/gcj/%{name}/bctsp-%{version}.jar.so
%{_libdir}/gcj/%{name}/bctsp-%{version}.jar.db
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
