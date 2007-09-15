%define name            bouncycastle
%define major           1
%define minor           37
%define archivever      %{major}%{minor}

%define section         free
%define build_free      1

%if %{build_free}
%define gcj_support     1
%define with_jdk14      1
%define with_jdk15      0
%define with_jdk16      0
%else
%define gcj_support     0
%define with_jdk14      1
%define with_jdk15      1
%define with_jdk16      1
%endif

%if %{with_jdk14}
%bcond_with                test
%else
%bcond_without             test
%endif # with_jdk14

Name:           %{name}
Version:        %{major}.%{minor}
Release:        %mkrel 1.3
Epoch:          0
Summary:        Bouncy Castle Crypto Package for Java
Group:          Development/Java
License:        BSD
URL:            http://www.bouncycastle.org/
Source0:        http://www.bouncycastle.org/download/crypto-%{archivever}.tar.gz
%if !%{build_free}
Source100:      http://www.bouncycastle.org/download/bcprov-jdk14-%{major}%{minor}.jar
Source101:      http://www.bouncycastle.org/download/bcprov-jdk15-%{major}%{minor}.jar
Source102:      http://www.bouncycastle.org/download/bcprov-jdk16-%{major}%{minor}.jar
%endif
Patch0:         %{name}-build.patch
Patch1:         %{name}-test.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
#Vendor:        JPackage Project
#Distribution:  JPackage
Requires:       %{name}-provider = %{epoch}:%{version}
Requires:       jpackage-utils >= 0:1.5
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  jaf
BuildRequires:  javamail
BuildRequires:  junit
BuildRequires:  jpackage-utils >= 0:1.5
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel >= 0:1.4.0
BuildArch:      noarch
%endif # gcj_support

%description
The Bouncy Castle Crypto APIs consist of the following:
- A lightweight cryptography API in Java.
- A provider for the JCE and JCA.
- A clean room implementation of the JCE 1.2.1.
- Generators for Version 1 and Version 3 X.509 certificates and PKCS12 files.
- A signed jar version suitable for JDK 1.4 and the Sun JCE.

%if %{with_jdk14}
%package jdk1.4
Group:          Development/Java
Summary:        Bouncy Castle JCE APIs for Java 1.4.x
Requires:       %{name} = %{epoch}:%{version}
Requires:       jaf
Requires:       javamail
Requires:       java >= 0:1.4.0
# FIXME: GCJ with 1.5.0 support still can't compile bc for 1.5
#Requires:       java < 0:1.5.0
BuildRequires:  java-devel >= 0:1.4.0
# FIXME: GCJ with 1.5.0 support still can't compile bc for 1.5
#BuildRequires:  java-devel < 0:1.5.0
Provides:       %{name}-provider = %{epoch}:%{version}
Provides:       jce

%description jdk1.4
Bouncy Castle JCE API's for Java 1.4.
%endif

%if %{with_jdk15}
%package jdk1.5
Group:          Development/Java
Summary:        Bouncy Castle JCE APIs for Java 1.5.x
Requires:       %{name} = %{epoch}:%{version}
Requires:       jaf
Requires:       javamail
Requires:       java >= 0:1.5.0
Requires:       java < 0:1.6.0
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  java < 0:1.6.0
Provides:       %{name}-provider = %{epoch}:%{version}
Provides:       jce

%description jdk1.5
Bouncy Castle JCE API's for Java 1.5.
%endif

%if %{with_jdk16}
%package jdk1.6
Group:          Development/Java
Summary:        Bouncy Castle JCE APIs for Java 1.6.x
Requires:       %{name} = %{epoch}:%{version}
Requires:       jaf
Requires:       javamail
Requires:       java >= 0:1.6.0
Requires:       java < 0:1.7.0
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  java < 0:1.7.0
Provides:       %{name}-provider = %{epoch}:%{version}
Provides:       jce

%description jdk1.6
Bouncy Castle JCE API's for Java 1.6.
%endif

%if %{with_jdk14}
%package javadoc-jdk1.4
Group:          Development/Java
Summary:        Java 1.4 javadoc for %{name}

%description javadoc-jdk1.4
Java 1.4 javadocs for %{name}.
%endif

%if %{with_jdk15}
%package javadoc-jdk1.5
Group:          Development/Java
Summary:        Java 1.5 javadoc for %{name}

%description javadoc-jdk1.5
Java 1.5 javadocs for %{name}.
%endif

%if %{with_jdk16}
%package javadoc-jdk1.6
Group:          Development/Java
Summary:        Java 1.6 javadoc for %{name}

%description javadoc-jdk1.6
Java 1.6 javadocs for %{name}.
%endif

%prep
%setup -q -n crypto-%{archivever}
%if %{build_free}
%patch0 -p1 -b .build
%endif
%if %without test
rm test/src/org/bouncycastle/asn1/test/PKIFailureInfoTest.java
rm test/src/org/bouncycastle/asn1/test/UTCTimeTest.java
rm test/src/org/bouncycastle/asn1/test/X509ExtensionsTest.java
rm test/src/org/bouncycastle/asn1/test/X509NameTest.java
rm test/src/org/bouncycastle/cms/test/CMSTestUtil.java
rm test/src/org/bouncycastle/crypto/test/RSABlindedTest.java
rm test/src/org/bouncycastle/crypto/test/RSATest.java
rm test/src/org/bouncycastle/jce/provider/test/AttrCertTest.java
rm test/src/org/bouncycastle/jce/provider/test/CertTest.java
rm test/src/org/bouncycastle/jce/provider/test/ImplicitlyCaTest.java
rm test/src/org/bouncycastle/jce/provider/test/PKCS10CertRequestTest.java
rm test/src/org/bouncycastle/math/ec/test/ECPointTest.java
%patch1 -p1
%endif
%{__perl} -pi -e 's/<javac/<javac nowarn="true"/g' *.xml

%build
export OPT_JAR_LIST="\
$(%{__cat} %{_sysconfdir}/ant.d/junit)\
"

export CLASSPATH=$(build-classpath jaf javamail/mailapi junit)

%if %{with_jdk14}
# 1.4
JAVA_HOME=
# FIXME: GCJ with 1.5.0 support still can't compile bc for 1.5
for javaver in 1.4.0 1.4.1 1.4.2 1.5.0; do
  [ -d "%{_jvmdir}/java-${javaver}" ] && \
  JAVA_HOME=%{_jvmdir}/java-${javaver}
done
[ -z "$JAVA_HOME" ] && exit 1
export JAVA_HOME="$JAVA_HOME"
ant -f jdk14.xml -Drelease.suffix=%{version} build-provider build
%endif

# 1.5
export CLASSPATH=$(build-classpath jaf javamail/mailapi junit)

%if %{with_jdk15}
JAVA_HOME=
for javaver in 1.5.0; do
  [ -d "%{_jvmdir}/java-${javaver}" ] && \
  JAVA_HOME=%{_jvmdir}/java-${javaver}
done
[ -z "$JAVA_HOME" ] && exit 1
export JAVA_HOME="$JAVA_HOME"
ant -f jdk15.xml -Drelease.suffix=%{version} build-provider build
%endif # with_jdk15

# 1.6
export CLASSPATH=$(build-classpath jaf javamail/mailapi junit)

%if %{with_jdk16}
JAVA_HOME=
for javaver in 1.6.0; do
  [ -d "%{_jvmdir}/java-${javaver}" ] && \
  JAVA_HOME=%{_jvmdir}/java-${javaver}
done
[ -z "$JAVA_HOME" ] && exit 1
export JAVA_HOME="$JAVA_HOME"
ant -f jdk16.xml -Drelease.suffix=%{version} build-provider build
%endif # with_jdk16

%install
%{__rm} -rf %{buildroot}

# Replace built 1.4 and 1.5 and 1.6 providers with pre-signed ones
%if !%{build_free}
%if %{with_jdk14}
pushd build/artifacts/jdk1.4/jars
%{__rm} -f bcprov-jdk14-%{version}.jar
%{__cp} -a %{SOURCE100} bcprov-jdk14-%{version}.jar
popd
%endif # with_jdk14
%if %{with_jdk15}
pushd build/artifacts/jdk1.5/jars
%{__rm} -f bcprov-jdk15-%{version}.jar
%{__cp} -a %{SOURCE101} bcprov-jdk15-%{version}.jar
popd
%endif # with_jdk15
%if %{with_jdk16}
pushd build/artifacts/jdk1.6/jars
%{__rm} -f bcprov-jdk16-%{version}.jar
%{__cp} -a %{SOURCE102} bcprov-jdk16-%{version}.jar
popd
%endif # with_jdk16
%endif # build_free

%{__mkdir_p} %{buildroot}%{_javadir}

# Java 1.4
%if %{with_jdk14}
pushd build/artifacts/jdk1.4/jars
%if %with test
for jar14 in {bcmail,bcpg,bctest,bctsp}-jdk14-%{version}.jar; do
%else
for jar14 in {bcmail,bcpg,bctsp}-jdk14-%{version}.jar; do
%endif
   %{__install} -m 644 $jar14 %{buildroot}%{_javadir}/$jar14
done

pushd %{buildroot}%{_javadir}
   for jar in *-jdk14-%{version}.jar; do
      %{__ln_s} $jar $(echo $jar | %{__sed} s#-%{version}##g)
   done
popd

%{__mkdir_p} %{buildroot}%{_javadir}-ext
%{__install} -m 644 bcprov-jdk14-%{version}.jar %{buildroot}%{_javadir}-ext
(cd %{buildroot}%{_javadir}-ext && for jar in *-jdk14-%{version}.jar; do %{__ln_s} $jar $(echo $jar | %{__sed} s#-%{version}##g); done)
# FIXME: GCJ with 1.5.0 support still can't compile bc for 1.5
for javaver in 1.4.0 1.4.1 1.4.2 1.5.0; do
   %{__mkdir_p} %{buildroot}%{_javadir}-${javaver}
   # FIXME
   (cd %{buildroot}%{_javadir}-${javaver} && %{__ln_s} ../../..%{_javadir}-ext/bcprov-jdk14-%{version}.jar bcprov-jdk14-%{version}.jar \
    && %{__ln_s} bcprov-jdk14-%{version}.jar bcprov-jdk14.jar)
done
%if %{gcj_support}
%{__mkdir_p}  %{buildroot}%{_javadir}/gcj-endorsed
# FIXME
(cd %{buildroot}%{_javadir}/gcj-endorsed && %{__ln_s} ../../../..%{_javadir}-ext/bcprov-jdk14-%{version}.jar bcprov-jdk14-%{version}.jar)
popd
%endif # gcj_support
%endif # with_jdk14

# Java 1.5
%if %{with_jdk15}
pushd build/artifacts/jdk1.5/jars

%if %with test
for jar15 in {bcmail,bcpg,bctest,bctsp}-jdk15-%{version}.jar; do
%else
for jar15 in {bcmail,bcpg,bctsp}-jdk15-%{version}.jar; do
%endif
   %{__install} -m 644 $jar15 %{buildroot}%{_javadir}/$jar15
done

pushd %{buildroot}%{_javadir}
  for jar in *-jdk15-%{version}.jar; do
    %{__ln_s} $jar $(echo $jar | %{__sed} s#-%{version}##g)
  done
popd

%{__mkdir_p} %{buildroot}%{_javadir}-ext
%{__install} -m 644 bcprov-jdk15-%{version}.jar %{buildroot}%{_javadir}-ext
(cd %{buildroot}%{_javadir}-ext && for jar in *-jdk15-%{version}.jar; do %{__ln_s} $jar $(echo $jar | %{__sed} s#-%{version}##g); done)
for javaver in 1.5.0; do
  %{__mkdir_p} %{buildroot}%{_javadir}-${javaver}
  # FIXME
  (cd %{buildroot}%{_javadir}-${javaver} && %{__ln_s} ../../..%{_javadir}-ext/bcprov-jdk15-%{version}.jar bcprov-jdk15-%{version}.jar \
   && %{__ln_s} bcprov-jdk15-%{version}.jar bcprov-jdk15.jar)
done
popd
%if %{gcj_support}
%{__mkdir_p}  %{buildroot}%{_javadir}/gcj-endorsed
# FIXME
(cd %{buildroot}%{_javadir}/gcj-endorsed && %{__ln_s} ../../../..%{_javadir}-ext/bcprov-jdk15-%{version}.jar bcprov-jdk15-%{version}.jar)
popd
%endif # gcj_support
%endif # with_jdk15

# Java 1.6
%if %{with_jdk16}
pushd build/artifacts/jdk1.6/jars

%if %with test
for jar16 in {bcmail,bcpg,bctest,bctsp}-jdk16-%{version}.jar; do
%else
for jar16 in {bcmail,bcpg,bctsp}-jdk16-%{version}.jar; do
%endif
   %{__install} -m 644 $jar16 %{buildroot}%{_javadir}/$jar16
done

pushd %{buildroot}%{_javadir}
  for jar in *-jdk16-%{version}.jar; do
    %{__ln_s} $jar $(echo $jar | %{__sed} s#-%{version}##g)
  done
popd

%{__mkdir_p} %{buildroot}%{_javadir}-ext
%{__install} -m 644 bcprov-jdk16-%{version}.jar %{buildroot}%{_javadir}-ext
(cd %{buildroot}%{_javadir}-ext && for jar in *-jdk16-%{version}.jar; do %{__ln_s} $jar $(echo $jar | %{__sed} s#-%{version}##g); done)
for javaver in 1.6.0; do
  %{__mkdir_p} %{buildroot}%{_javadir}-${javaver}
  # FIXME
  (cd %{buildroot}%{_javadir}-${javaver} && %{__ln_s} ../../..%{_javadir}-ext/bcprov-jdk16-%{version}.jar bcprov-jdk16-%{version}.jar \
   && %{__ln_s} bcprov-jdk16-%{version}.jar bcprov-jdk16.jar)
done
popd
%endif # with_jdk16

# javadoc
%if %{with_jdk14}
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-jdk14-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-jdk14-%{version} %{name}-jdk14)
%endif
%if %{with_jdk15}
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-jdk15-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-jdk15-%{version} %{name}-jdk15)
%endif
%if %{with_jdk16}
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-jdk16-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-jdk16-%{version} %{name}-jdk16)
%endif

dotvers=""
%if %{with_jdk14}
dotvers="1.4"
%endif
%if %{with_jdk15}
dotvers="$dotvers 1.5"
%endif
%if %{with_jdk16}
dotvers="$dotvers 1.6"
%endif

for javaver in $dotvers; do
  ver=`echo $javaver | sed 's/\.//'`
  for javadoc in bcmail bcpg bcprov bctsp; do
    %{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-jdk${ver}-%{version}/${javadoc}
    %{__cp} -a build/artifacts/jdk${javaver}/${javadoc}-jdk${ver}-%{version}/docs/* %{buildroot}%{_javadocdir}/%{name}-jdk${ver}-%{version}/${javadoc}
  done
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm  \
%if %{with_jdk15}
                            --exclude %{_javadir}/bcmail-jdk15-%{version}.jar \
                            --exclude %{_javadir}/bcpg-jdk15-%{version}.jar \
%if %with test
                            --exclude %{_javadir}/bctest-jdk15-%{version}.jar \
%endif
                            --exclude %{_javadir}/bctsp-jdk15-%{version}.jar \
                            --exclude %{_javadir}-ext/bcprov-jdk15-%{version}.jar \
%endif
%if %{with_jdk16}
                            --exclude %{_javadir}/bcmail-jdk16-%{version}.jar \
                            --exclude %{_javadir}/bcpg-jdk16-%{version}.jar \
%if %with test
                            --exclude %{_javadir}/bctest-jdk16-%{version}.jar \
%endif
                            --exclude %{_javadir}/bctsp-jdk16-%{version}.jar \
                            --exclude %{_javadir}-ext/bcprov-jdk16-%{version}.jar


%endif
%endif # gcj_support

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
if test -x %{_bindir}/rebuild-security-providers; then
  %{_bindir}/rebuild-security-providers
fi

%postun
if test -x %{_bindir}/rebuild-security-providers; then
  %{_bindir}/rebuild-security-providers
fi

%if %{with_jdk14}
%post jdk1.4
%{update_gcjdb}

%postun jdk1.4
%{clean_gcjdb}
%endif # with_jdk14
%endif # gcj_support

%files
%defattr(0644,root,root,0755)
%doc *.html
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%endif

%if %{with_jdk14}
%files jdk1.4
%defattr(0644,root,root,0755)
%{_javadir}/bc*-jdk14-%{version}.jar
%{_javadir}/bc*-jdk14.jar
%{_javadir}-ext/bcprov-jdk14-%{version}.jar
%{_javadir}-ext/bcprov-jdk14.jar
%{_javadir}-1.4.0/bcprov-jdk14*.jar
%{_javadir}-1.4.1/bcprov-jdk14*.jar
%{_javadir}-1.4.2/bcprov-jdk14*.jar
%{_javadir}-1.5.0/bcprov-jdk14*.jar
%if %{gcj_support}
%{_javadir}/gcj-endorsed/bcprov-jdk14-%{version}.jar
%{_libdir}/gcj/%{name}/*-jdk14-%{version}.jar.*
%endif
%endif

%if %{with_jdk15}
%files jdk1.5
%defattr(0644,root,root,0755)
%{_javadir}/bc*-jdk15-%{version}.jar
%{_javadir}/bc*-jdk15.jar
%{_javadir}-ext/bcprov-jdk15-%{version}.jar
%{_javadir}-ext/bcprov-jdk15.jar
%{_javadir}-1.5.0/bcprov-jdk15*.jar
%if %{gcj_support}
%{_javadir}/gcj-endorsed/bcprov-jdk15-%{version}.jar
#%{_libdir}/gcj/%{name}/*-jdk15-%{version}.jar.*
%endif
%endif

%if %{with_jdk16}
%files jdk1.6
%defattr(0644,root,root,0755)
%{_javadir}/bc*-jdk16-%{version}.jar
%{_javadir}/bc*-jdk16.jar
%{_javadir}-ext/bcprov-jdk16-%{version}.jar
%{_javadir}-ext/bcprov-jdk16.jar
%{_javadir}-1.6.0/bcprov-jdk16*.jar
%if %{gcj_support}
#%{_libdir}/gcj/%{name}/*-jdk16-%{version}.jar.*
%endif
%endif

%if %{with_jdk14}
%files javadoc-jdk1.4
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-jdk14-%{version}
%doc %{_javadocdir}/%{name}-jdk14-%{version}/*
%dir %{_javadocdir}/%{name}-jdk14
%endif

%if %{with_jdk15}
%files javadoc-jdk1.5
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-jdk15-%{version}
%doc %{_javadocdir}/%{name}-jdk15-%{version}/*
%dir %{_javadocdir}/%{name}-jdk15
%endif

%if %{with_jdk16}
%files javadoc-jdk1.6
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-jdk16-%{version}
%doc %{_javadocdir}/%{name}-jdk16-%{version}/*
%dir %{_javadocdir}/%{name}-jdk16
%endif
