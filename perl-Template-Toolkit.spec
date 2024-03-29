Name:           perl-Template-Toolkit
Version:        2.22
Release:        5%{?dist}
Summary:        Template processing system
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://www.template-toolkit.org/
Source0:        http://search.cpan.org/CPAN/authors/id/A/AB/ABW/Template-Toolkit-%{version}.tar.gz
Source1:        http://tt2.org/download/TT_v222_html_docs.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(Test::More)
BuildRequires:  perl(AppConfig), perl(Text::Autoformat), perl(GD::Graph3d), perl(GD::Graph)
BuildRequires:  perl(GD::Text), perl(Image::Info), perl(Image::Size), perl(Pod::POM)
BuildRequires:  perl(XML::DOM), perl(XML::RSS), perl(XML::XPath)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl-Template-Toolkit-examples = %{version}-%{release}
Obsoletes:      perl-Template-Toolkit-examples < 2.22-1

%{?filter_setup:
%filter_from_provides /^perl(bytes)$/d
%?perl_default_filter
}

%description
The Template Toolkit is a collection of modules which implement a
fast, flexible, powerful and extensible template processing system.
It was originally designed and remains primarily useful for generating
dynamic web content, but it can be used equally well for processing
any other kind of text based documents: HTML, XML, POD, PostScript,
LaTeX, and so on.

%prep
%setup -q -n Template-Toolkit-%{version} -a 1
find lib -type f | xargs chmod -c -x
find TT_v*_html_docs -depth -name .svn -type d -exec rm -rf {} \;

# Convert file to UTF-8
iconv -f iso-8859-1 -t utf-8 -o Changes{.utf8,}
mv Changes{.utf8,}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor \
  TT_DBI=n TT_ACCEPT=y
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
# install (+ INSTALLARCHLIB) instead of pure_install to get docs
# and the template library installed too
make install \
  PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib} \
  TT_PREFIX=$RPM_BUILD_ROOT%{_datadir}/tt2
find $RPM_BUILD_ROOT -type f \( -name perllocal.pod -o \
  -name .packlist -o -name '*.bs' -size 0 \) -exec rm {} ';'
find $RPM_BUILD_ROOT -depth -type d -empty -exec rmdir {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*
# Nuke buildroot where it hides
sed -i "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{perl_vendorarch}/Template/Config.pm

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes HACKING README TODO TT_v*_html_docs/*
%{_bindir}/tpage
%{_bindir}/ttree
%{perl_vendorarch}/Template.pm
%{perl_vendorarch}/auto/Template
%{perl_vendorarch}/Template
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Tue Feb  9 2010 Stepan Kasal <skasal@redhat.com> - 2.22-5
- delete the buildroot before install

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.22-4
- use filtering macros

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.22-3
- drop build requirements for TeX; LaTeX support has been removed in 2.14a
- fix the Obsoletes tag

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.22-2
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-1
- update to 2.22
- obsolete examples package, upstream got rid of them

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-1
- update to 2.20

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.19-3
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-2
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19-1
- 2.19
- license tag fix
- rebuild for BuildID

* Wed Feb 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18-1
- go to 2.18

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.15-2
- bump for fc6

* Mon May 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.15-1
- bump to 2.15
- gd test is gone, don't need to patch anything

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-8
- really resolve bug 173756

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-7
- use proper TT_PREFIX setting everywhere, resolve bug 173756

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-6
- bump for FC-5

* Mon Jul 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-5
- don't need Tie::DBI as a BuildRequires, since we're not running 
  the tests

* Mon Jul 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 2.14-4
- put examples in their own subpackage

* Sat Jul  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.14-3
- Filter false positive provides.
- Include template library, switch to %%{_datadir}/tt2.
- Tune build dependencies for full test suite coverage.
- Fix and enable GD tests.
- Include more documentation.
- Fine tune dir ownerships and file permissions.

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.14-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.14-1
- Initial package for Fedora Extras
