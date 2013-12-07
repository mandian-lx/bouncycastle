%define major           1
%define minor           43
%define archivever      %{major}%{minor}

%define section         free

%define gcj_support     0

Name:           bouncycastle
Version:        1.46
Release:        5
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
    cp -Rf ${javadoc}-jdk${ver}-%{version}/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}/${javadoc}
  done
popd

%{__mkdir_p} %{buildroot}%{_javadir}/gcj-endorsed
(cd %{buildroot}%{_javadir}/gcj-endorsed && %{__ln_s} %{_javadir}/bcprov.jar .)

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif # gcj_support

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


%changelog
* Tue Mar 15 2011 Stéphane Téletchéa <steletch@mandriva.org> 0:1.46-1mdv2011.0
+ Revision: 645044
- update to new version 1.46

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.43-3mdv2011.0
+ Revision: 603768
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.43-2mdv2010.1
+ Revision: 522300
- rebuilt for 2010.1

* Wed Aug 19 2009 Anssi Hannula <anssi@mandriva.org> 0:1.43-1mdv2010.0
+ Revision: 417917
- remove UTF-8 characters from comments and testcase until fixed properly
  (utf8-characters.patch)
- fix build by removing invalid characters from comments in code
  (invalid-characters.patch)
- new version
- disable prebuilt gcj libraries
- allow build with java < 1.7
- split everything except provider into bouncycastle-extras to
  make the main considerably smaller and dependencyless
- use %%ant

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Sun Apr 20 2008 David Walluck <walluck@mandriva.org> 0:1.39-0.0.1mdv2009.0
+ Revision: 195975
- 1.39

* Thu Jan 10 2008 David Walluck <walluck@mandriva.org> 0:1.38-0.0.4mdv2008.1
+ Revision: 147442
- explicitly require geronimo for jaf and javamail

* Tue Jan 01 2008 Anssi Hannula <anssi@mandriva.org> 0:1.38-0.0.3mdv2008.1
+ Revision: 140172
- obsolete the old jdk1.4 subpackage

* Mon Dec 31 2007 David Walluck <walluck@mandriva.org> 0:1.38-0.0.2mdv2008.1
+ Revision: 139733
- add symlink in gcj-endorsed dir

* Mon Dec 31 2007 David Walluck <walluck@mandriva.org> 0:1.38-0.0.1mdv2008.1
+ Revision: 139710
- 1.38

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.37-5.0.1mdv2008.1
+ Revision: 120840
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

  + David Walluck <walluck@mandriva.org>
    - rebuild
    - only build with support for icedtea
    - install into global location

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.37-1.3mdv2008.0
+ Revision: 87233
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Fri Jun 29 2007 David Walluck <walluck@mandriva.org> 0:1.37-1.2mdv2008.0
+ Revision: 45884
- more hacks to support GCJ/1.5

* Fri Jun 29 2007 David Walluck <walluck@mandriva.org> 0:1.37-1.1mdv2008.0
+ Revision: 45822
- bump release
- add hack for installing jdk14 version on GCJ 1.5
- add unversioned bcprov symlinks

* Sun Jun 17 2007 David Walluck <walluck@mandriva.org> 0:1.37-1mdv2008.0
+ Revision: 40575
- 1.37


* Thu Mar 22 2007 David Walluck <walluck@mandriva.org> 1.36-1mdv2007.1
+ Revision: 147875
- enable 1.4 support for non-free JDK's
- add jdk 1.6 support
- 1.36

* Sun Mar 04 2007 David Walluck <walluck@mandriva.org> 0:1.35-1mdv2007.1
+ Revision: 132061
- 1.35
- 1.35

* Thu Oct 19 2006 David Walluck <walluck@mandriva.org> 0:1.33-3mdv2007.1
+ Revision: 66075
- Import bouncycastle

* Thu Aug 24 2006 David Walluck <walluck@mandriva.org> 0:1.33-3mdv2007.0
- BuildRequires: ant, ant-junit

* Thu May 25 2006 David Walluck <walluck@mandriva.org> 0:1.33-2mdv2007.0
- rebuild for libgcj.so.7
- enable gcj support regardless of %%gcj_support, just not aot
  compilation
- remove checkstyle build requirement

* Wed May 10 2006 David Walluck <walluck@mandriva.org> 0:1.33-1mdk
- 1.33

* Thu Mar 30 2006 David Walluck <walluck@mandriva.org> 0:1.32-2mdk
- run rebuild-gcj-db (bug #21883)
- change to BuildRequires: java-gcj-compat-devel

* Thu Mar 30 2006 David Walluck <walluck@mandriva.org> 0:1.32-1mdk
- 1.32

* Tue Jan 17 2006 David Walluck <walluck@mandriva.org> 0:1.31-3mdk
- install into %%{_javadir}/gcj-endorsed so that gcj can find us
- fix symlinks
- remove tests that (sometimes) fail to build with ecj

* Mon Jan 16 2006 David Walluck <walluck@mandriva.org> 0:1.31-2mdk
- fix build with jdk 1.5

* Sat Dec 31 2005 David Walluck <walluck@mandriva.org> 0:1.31-1mdk
- 1.31

* Sun Dec 18 2005 David Walluck <walluck@mandriva.org> 0:1.31-0.b16.1mdk
- 1.31b16

* Wed Dec 07 2005 David Walluck <walluck@mandriva.org> 0:1.31-0.b12.1mdk
- 1.31b12

* Wed Nov 02 2005 David Walluck <walluck@mandriva.org> 0:1.31-0.b09.1mdk
- 1.31b09
- use ant for build

* Wed Nov 02 2005 David Walluck <walluck@mandriva.org> 0:1.30-3mdk
- enable bctsp

* Sun Oct 30 2005 David Walluck <walluck@mandriva.org> 0:1.30-2mdk
- install single jar instead of directory for provider

* Tue Sep 20 2005 David Walluck <walluck@mandriva.org> 0:1.30-1mdk
- 1.30

* Tue May 31 2005 David Walluck <walluck@mandriva.org> 0:1.28-2mdk
- fix provider installation under gcj

* Mon May 30 2005 David Walluck <walluck@mandriva.org> 0:1.28-1mdk
- 1.28
- make jdk 1.5 support optional
- add support for gcj

* Mon Feb 21 2005 David Walluck <david@jpackage.org> 0:1.27-1jpp
- 1.27
- "fix" requires-on-release
- change license to BSD (style)
- fix duplicate requires

* Thu Jan 20 2005 David Walluck <david@jpackage.org> 0:1.26-1jpp
- 1.26

* Sun Oct 10 2004 David Walluck <david@jpackage.org> 0:1.25-1jpp
- 1.25
- jdk 1.3.x support out, jdk 1.5.0 support in

