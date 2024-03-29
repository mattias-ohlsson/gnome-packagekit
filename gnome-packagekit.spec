Summary:   Session applications to manage packages
Name:      gnome-packagekit
Version:   3.6.1
Release:   2%{?dist}
License:   GPLv2+
Group:     Applications/System
URL:       http://www.packagekit.org
Source0:   http://download.gnome.org/sources/gnome-packagekit/3.6/%{name}-%{version}.tar.xz

# Already upstream
Patch0:    0001-Don-t-crash-if-the-window-that-invoked-the-task-exit.patch

Requires:  gnome-icon-theme
Requires:  gnome-settings-daemon-updates
Requires:  dbus-x11 >= 1.1.2
Requires:  PackageKit >= 0.5.0
Requires:  PackageKit-libs >= 0.5.0
Requires:  PackageKit-device-rebind >= 0.5.0
Requires:  shared-mime-info
Requires:  iso-codes
Requires:  libcanberra >= 0.10
Requires:  upower >= 0.9.0

# required because KPackageKit provides exactly the same interface
Provides: PackageKit-session-service

BuildRequires: glib2-devel >= 2.25.8
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: libnotify-devel >= 0.7.0
BuildRequires: gnome-panel-devel
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: libtool
BuildRequires: cairo-devel
BuildRequires: startup-notification-devel
BuildRequires: perl(XML::Parser)
BuildRequires: PackageKit-devel >= 0.5.0
BuildRequires: intltool
BuildRequires: xorg-x11-proto-devel
BuildRequires: fontconfig-devel
BuildRequires: libcanberra-devel
BuildRequires: libgudev1-devel
BuildRequires: libxslt
BuildRequires: upower-devel >= 0.9.0
BuildRequires: docbook-utils
BuildRequires: systemd-devel
BuildRequires: polkit-devel
BuildRequires: itstool

%description
gnome-packagekit provides session applications for the PackageKit API.
There are several utilities designed for installing, updating and
removing packages on your system.

%prep
%setup -q
%patch0 -p1 -b .xid-crash

%build
%configure --enable-systemd
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# nuke the ChangeLog file, it's huge
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/gnome-packagekit-*/ChangeLog

for i in gpk-application gpk-update-viewer gpk-install-local-file gpk-log gpk-prefs ; do
  desktop-file-install --delete-original                                \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications/                      \
    $RPM_BUILD_ROOT%{_datadir}/applications/$i.desktop
done

%find_lang %name --with-gnome

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
update-desktop-database %{_datadir}/applications &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/gpk-*
%dir %{_datadir}/gnome-packagekit
%{_datadir}/gnome-packagekit/gpk-*.ui
%dir %{_datadir}/gnome-packagekit/icons
%dir %{_datadir}/gnome-packagekit/icons/hicolor
%dir %{_datadir}/gnome-packagekit/icons/hicolor/*
%dir %{_datadir}/gnome-packagekit/icons/hicolor/*/*
%{_datadir}/gnome-packagekit/icons/hicolor/*/*/*.png
%{_datadir}/gnome-packagekit/icons/hicolor/scalable/*/*.svg*
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/scalable/*/*.svg*
%{_datadir}/man/man1/*.1.gz
%{python_sitelib}/packagekit/*py*
%{_datadir}/applications/gpk-*.desktop
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_datadir}/glib-2.0/schemas/org.gnome.packagekit.gschema.xml
%{_datadir}/GConf/gsettings/org.gnome.packagekit.gschema.migrate

%changelog
* Wed Nov 28 2012 Richard Hughes <hughsient@gmail.com> - 3.6.1-2
- Don't crash if the window that invoked the task exits before
  the task starts up.
- Resolves: #756208

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1
- Minor spec file cleanup

* Fri Sep 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.0-2
- Depend on gnome-settings-daemon-updates. #699348
- Drop ancient obsoletes

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Aug 28 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Thu May 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Mon Mar 26 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- New upstream version.

* Sun Mar 18 2012 Richard Hughes <rhughes@redhat.com> - 3.3.92-1
- New upstream version.
- Many updated translations.

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-2
- Use systemd for session tracking

* Mon Feb 06 2012 Richard Hughes <rhughes@redhat.com> - 3.3.5-1
- New upstream version.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Richard Hughes <rhughes@redhat.com> - 3.3.3-1
- New upstream version.

* Mon Oct 17 2011 Richard Hughes <rhughes@redhat.com> - 3.2.1-1
- New upstream version.

* Mon Sep 26 2011 Richard Hughes <rhughes@redhat.com> - 3.2.0-1
- New upstream version.

* Tue Sep 20 2011 Richard Hughes <rhughes@redhat.com> - 3.1.92-2
- Correctly count the items in the update viewer to fix simulate.
- Correctly import package files when downloaded in firefox.
- Resolves #739910

* Mon Sep 19 2011 Richard Hughes <rhughes@redhat.com> - 3.1.92-1
- New upstream version.

* Tue Aug 30 2011 Richard Hughes <rhughes@redhat.com> - 3.1.90-2
- Actually upload tarball.

* Tue Aug 30 2011 Richard Hughes <rhughes@redhat.com> - 3.1.90-1
- New upstream version.

* Mon Jul 04 2011 Richard Hughes <rhughes@redhat.com> - 3.1.3-2
- BR: docbook-utils

* Mon Jul 04 2011 Richard Hughes <rhughes@redhat.com> - 3.1.3-1
- New upstream version.

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-3
- Update icon cache and gsettings scriptlets

* Tue Apr 26 2011 Richard Hughes <rhughes@redhat.com> - 3.0.0-2
- Add requires of gnome-settings-daemon to fix #683145

* Mon Apr 04 2011 Richard Hughes <rhughes@redhat.com> - 3.0.0-1
- New upstream version.

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-2
- Don't require PackageKit-gtk-module. It gets pulled in
  via comps already, and it is a bit inconsistent to have a
  dep on that package, but not the gtk3 or gstreamer modules

* Mon Mar 21 2011 Richard Hughes  <rhughes@redhat.com> - 2.91.92-1
- New upstream release.

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-2
- Rebuild against newer gtk

* Tue Jan 11 2011 Richard Hughes <rhughes@redhat.com> - 2.91.5-1
- New upstream version.

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.3-2
- Update to 2.91.3

* Mon Nov 08 2010 Richard Hughes <rhughes@redhat.com> - 2.91.2-2
- Fix compile with PackageKit < 0.6.11

* Mon Nov 08 2010 Richard Hughes <rhughes@redhat.com> - 2.91.2-1
- New upstream version.

* Wed Nov 03 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.2.20101102
- Rebuild now libnotify 0.7.0 is in rawhide.

* Tue Nov 02 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.1.20101102
- Update to a git snapshot to fix rawhide.
- Remove the -extra subpackage, it's too hard to find.

* Tue Oct 05 2010 Richard Hughes <rhughes@redhat.com> - 2.91.1-1
- New upstream version.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.31.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 01 2010 Richard Hughes <rhughes@redhat.com> - 2.31.4-1
- New upstream version.

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-2
- Rebuild

* Mon Jun 21 2010 Richard Hughes <rhughes@redhat.com> - 2.31.3-1
- New upstream version.

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-2
- Don't require scrollkeeper

* Sun Jun 06 2010 Richard Hughes <rhughes@redhat.com> - 2.31.1-1
- New upstream version.

* Mon Apr 26 2010 Richard Hughes <rhughes@redhat.com> - 2.30.1-1
- New upstream version.
- Fix a few non-critical UI issues in the update viewer.
- Fix a crash where the desktop file that was installed has no root directory.
- Resolves: #581682

* Wed Apr 07 2010 Richard Hughes <richard@hughsie.com> 2.30.0-2
- Fix the session interface to accept queries from non-blacklisted programs.

* Mon Mar 29 2010 Richard Hughes <rhughes@redhat.com> - 2.30.0-1
- New upstream version.

* Mon Mar 15 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.92-0.1.20100315git
- New snapshot from the master branch
- Rebuild against the latest PackageKit
- Should fix the silent failure when the simulate depsolve fails
- Ensure that there can only eve be one update icon running in a session.

* Tue Mar 09 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.91-3
- It appears gconf_schema appends .schemas for us. Bother.

* Tue Mar 09 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.91-2
- Use the _correct_ gconf_schema defines for the GConf schemas :-)

* Tue Mar 09 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.91-1
- New upstream version.
- Update to the latest version of the Fedora Packaging Guidelines
- Do not run scrollkeeper-update
- Remove the custom BuildRoot
- Do not clean the buildroot before install
- Use the gconf_schema defines for the GConf schemas

* Wed Feb 24 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.4-0.2.20100211git
- Fix an infinite loop in the update viewer

* Thu Feb 11 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.4-0.1.20100211git
- New snapshot from the master branch
- Should get Tim's printer installing working correctly.

* Wed Feb 10 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.4-0.1.20100210git
- New snapshot from the master branch

* Fri Feb 05 2010 Richard Hughes  <rhughes@redhat.com> - 0.6.0-0.3.20100111
- Add Provides: PackageKit-session-service
- Resolves #561437

* Mon Feb 01 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.3-2
- Rebuild now the new PK has hit koji.

* Mon Feb 01 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.3-1
- New upstream version.
- Filter by the timespec in gpk-log, not the localised date. Fixes #544667
- Re-get the update list in the update viewer if the network changes. Fixes #543871
- Don't hide the restart status icon just because the daemon exited. Fixes #553966

* Tue Jan 05 2010 Richard Hughes  <rhughes@redhat.com> - 2.29.2-1
- New upstream version.

* Tue Dec 08 2009 Richard Hughes  <rhughes@redhat.com> - 2.29.1-1
- New upstream version.

* Mon Sep 28 2009 Richard Hughes  <rhughes@redhat.com> - 2.28.0-0.1.20090928git
- New snapshot from the gnome-2-28 branch
- Many updated translations.
- Fixes #525810 and #524873

* Mon Sep 21 2009 Richard Hughes  <rhughes@redhat.com> - 2.28.0-1
- New upstream version.

* Mon Sep 07 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.92-1
- New upstream version.
- Many updated translations.
- Add simulation of installed files.
- Don't show duplicate package names in the reboot tooltip.

* Mon Aug 24 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.91-2
- Actually upload the correct tarball.

* Mon Aug 24 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.91-1
- New upstream version

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.27.5-3
- Use bzipped upstream tarball.

* Mon Aug 03 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.5-2
- Move the gpk-log and gpk-repo menu shortcuts to the gnome-packagekit-extra
  subpackage to reduce menu polution on the live cd.

* Mon Aug 03 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.5-1
- New upstream version
- Port all the code to using PolicyKit1 rather than PolicyKit
- Reduce the size displayed as the package is downloaded
- Scroll to the package being processed in the update list
- Fixes #510730, #510984, #510730, #497737 and #514879

* Mon Jul 27 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.4-0.1.20090727git
- Update to latest git master snapshot

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-1
- New upstream version
 - Lots of updated translations
 - Check for dependancies before downloading updates in the update viewer
 - Connect to gnome-session to get the idle status, not gnome-screensaver
 - Don't show a generic icon when we have messages
 - Use the newest filter by default in the update viewer
 - Run all the packages after install, not just the selected package
- Fixes #506010, #507062, #508505, #509067, #509104 and #509636

* Thu Jun 25 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-0.4.20090625git
- Don't build with GDK_MULTIHEAD_SAFE as it breaks ca_gtk_context_get with a
  new libcanberra-gtk. Ifdefs probably required as ca_gtk_context_get_for_screen
  is fairly new.

* Thu Jun 25 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-0.3.20090625git
- Update to latest git master snapshot

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-0.2.20090616git
- Apply a patch to convert to the PolKit1 API.
- Do autoreconf as the polkit patch is pretty invasive

* Tue Jun 16 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.3-0.1.20090616git
- Update to todays git snapshot
- Connect to gnome-session to get the idle status, not gnome-screensaver
- Lots of translation updates

* Tue Jun 02 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.2-2
- Rebuild as waitrepo timed out on me during a chainbuild. Oddball.

* Mon Jun 01 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.2-1
- New upstream version
- Lots of translation updates
- Add UI helpers for media changing
- Lots of fixes to the update viewer and update icon
- Fixes #493934, #492160, #496024, #496870, #497162, #500237, #502562,
  #502589 and #492005

* Tue Apr 14 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.2-0.2.20090414git
- Reroll the tarball without the new PkMediaTypeEnum functionality which
  is present in git master PackageKit.

* Tue Apr 14 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.2-0.1.20090414git
- New git snapshot fixing several bugs

* Mon Mar 30 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.1-1
- New upstream version

* Tue Mar 24 2009 Richard Hughes  <rhughes@redhat.com> - 2.27.1-0.1.20090324git
- New snapshot fixing several bugs with the new update viewer.

* Thu Mar 19 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.6-0.2.20090319git
- Don't break the package download size label.

* Thu Mar 19 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.6-0.1.20090319git
- Update to todays git snapshot so we can test the latest version of the
  update viewer.
- Remove the fedora system-install-packages compatibility script as we've had
  it for over two releases.

* Tue Mar 17 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.6-0.1.20090317git
- Update to a git snapshot so we can test the latest version of the
  update viewer.

* Wed Mar 11 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.5-3
- Put gpk-update-viewer2 into the main package, not extras
- Fixes #489677

* Mon Mar 09 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.5-2
- Require PackageKit 0.4.5 otherwise the new update viewer breaks

* Mon Mar 09 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.5-1
- New upstream version
- Merge in a new update viewer with a very different UI which I've patched
  Fedora to use by default as requested by Matthias.
- Lots of translation updates

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.4-2
- Bump for rebuild.

* Mon Feb 23 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.4-1
- New upstream version
- Lots of bug fixes

* Mon Jan 19 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.2-1
- New upstream version
- Lots of bug fixes

* Thu Jan 08 2009 Richard Hughes  <rhughes@redhat.com> - 0.4.1-1
- New upstream version
- Add an option to the prefs dialog to prevent checking for updates when
  using mobile broadband connections
- Allow the admin to restrict getting updates when on WiFi connections
- Set the default search mode to details (not name) and preserve the search
  type in GConf if changed in the UI
- Add a simple markdown parser and use it in all applications.
- Send different errors when we fail a method on the session DBus interface
- Support setting timeouts via the interaction mode from the DBus interface
- Lots of bugfixes

* Fri Dec 12 2008 Richard Hughes  <rhughes@redhat.com> - 0.4.0-2
- Depend on PackageKit-gtk-module so the auto-font installation can be
  turned on in F11.
- Turn off the loading of libpk-gtk-module.so until we have a new
  fontconfig using a spec file patch that we can nuke soon.
- Fixes rh#476066

* Tue Dec 09 2008 Richard Hughes  <rhughes@redhat.com> - 0.4.0-1
- New upstream version

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> 0.3.11-3
- Rebuild for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.11-2
- Rebuild for Python 2.6

* Mon Nov 24 2008 Richard Hughes <rhughes@redhat.com> - 0.3.11-1
- New upstream version

* Tue Nov 11 2008 Richard Hughes <rhughes@redhat.com> - 0.3.10-1
- New upstream version
- Drop all upstreamed patches

* Fri Nov 07 2008 Warren Togami <wtogami@redhat.com> - 0.3.9-7
- Bug #470617 Just exit instead of complaining about a non-local session

* Wed Nov 05 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-6
- Fix up the fedora system-install-packages compatibility script.
- Fixes #468568

* Sat Nov 01 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-5
- Fix up the pirut obsoletes to fix upgrades from F8. Fixes #469481

* Mon Oct 27 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-4
- Barr. Actually apply the patch. Sleep time.

* Mon Oct 27 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-3
- Fix the size request of gpk-application to fix rh#467987

* Mon Oct 27 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-2
- Split out the service pack creator and the backend status programs
  into a gnome-packagekit-extra package as it's not suitable for the
  default desktop.

* Mon Oct 27 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.9-1
- New upstream version
- Many new and updated translations.
- Lots of bugfixes (#467746, #467582)

* Fri Oct 24 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.8-2
- Fix the untitled window in gpk-update-viewer. Fixes #468200
- Fix the resize problem on small form factor devices. Fixes #467987

* Mon Oct 20 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.8-1
- New upstream version

* Mon Oct 13 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.7-1
- New upstream version
- Much better log viewer functionality
- New service pack creator tool

* Fri Oct 10 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.6-5
- Bump

* Fri Oct 10 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.6-4
- Add a bugfix from upstream so we don't try to check for updates
  when we've set to never. Fixes RH#461825.

* Wed Oct  8 2008 Matthias Clasen  <mclasen@redhat.com> - 0.3.6-3
- Another space-saving hack

* Mon Oct 06 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.6-2
- Upload new sources. Ooops.

* Mon Oct 06 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.6-1
- New upstream version
- Show vendor specific messages when we fail to find packages
- Turn off hardware HAL integration

* Mon Sep 22 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.5-1
- New upstream version

* Mon Sep 22 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.4-1
- New upstream version

* Wed Sep 17 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.3-2
- Fix the interaction when the update check and the upgrade check are
  scheduled at the same time.

* Tue Sep 16 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.3-1
- Update to newest upstream version.
- Supports collection install and remove in the UI
- Add InstallGStreamerCodecs to the session interface

* Mon Sep 08 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.2-1
- Update to newest upstream version.

* Thu Aug 28 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-3
- Bump because the PackageKit-devel rpm was empty.

* Thu Aug 28 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-2
- Bump as make chainbuild is broken, so we'll have to do this in two steps.

* Mon Aug 27 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.1-1
- Update to newest upstream version.

* Mon Aug 22 2008 Richard Hughes  <rhughes@redhat.com> - 0.3.0-1
- Update to newest upstream version.

* Mon Aug 04 2008 Robin Norwood <rnorwood@redhat.com> - 0.2.4-3
- Fix Source0 URL.

* Tue Jul 31 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.4-2
- Rebuild for libunique ABI break.

* Tue Jul 30 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.4-1
- New upstream version, only bugfixes.

* Wed Jun 18 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-4.20080618
- Pull in a new snapshot from the unstable branch.
- Fixes a problem when installing with the DBUS session interface

* Mon Jun 11 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-3.20080611
- Pull in a new snapshot from the unstable branch.
- New interface for gpk-application - one that doesn't suck
- UI fixes for gpk-repo and gpk-update-viewer

* Mon Jun 09 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-2.20080609
- Add intltool to the BR.

* Mon Jun 09 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.3-1.20080609
- Pull in a new snapshot from the unstable branch.

* Thu May 29 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.2-2.20080529
- Pull in a new snapshot from the unstable branch.

* Mon May 19 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.2-1.20080519
- Pull in a new snapshot from the unstable branch.

* Fri May 16 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.1-3.20080508
- Add a BR on unique to make the client tools single instance

* Thu May 08 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.1-2.20080508
- Pull in a new snapshot from the unstable branch.

* Tue May 06 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.1-1.20080506
- Pull in a new snapshot from the unstable branch.

* Tue May 06 2008 Richard Hughes  <rhughes@redhat.com> - 0.2.0-1
- Update to the latest _UNSTABLE_ upstream source

* Sat Apr 16 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-5.20080416git
- Build against the right version of PackageKit to make koji DTRT.

* Sat Apr 16 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-4.20080416git
- Pull in the new snapshot from the stable GNOME_PACKAGEKIT_0_1_X branch.
- Fixes rh#442398.

* Sat Apr 15 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-3.20080415git
- Add a man page for system-install-packages. Fixes rh#441673

* Sat Apr 15 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-2.20080415git
- Pull in the new snapshot from the stable GNOME_PACKAGEKIT_0_1_X branch.
- Fixes include rh#442150, rh#442543, rh#442230, rh#441062 and more from upstream.

* Sat Apr 12 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.12-1.20080412git
- Pull in the new snapshot from the stable GNOME_PACKAGEKIT_0_1_X branch.
- Fixes that were cherry picked into this branch since 0.1.11 was released can be viewed at:
  http://gitweb.freedesktop.org/?p=users/hughsient/gnome-packagekit.git;a=log;h=GNOME_PACKAGEKIT_0_1_X

* Fri Apr 11 2008 Jesse Keating <jkeating@redhat.com> - 0.1.11-5
- Obsolete / Provide pirut.

* Thu Apr 10 2008 Owen Taylor <otaylor@redhat.com> - 0.1.11-4
- Make system-install-packages a wrapper script not a symlink
  so both files and package names work (#441674)

* Sat Apr  9 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.11-3
- Pull in the new icons from upsteam from Mike Langlie.

* Sat Apr  9 2008 Richard Hughes  <rhughes@redhat.com> - 0.1.11-2
- Fix a plethora of GUI bugs by pulling some fixes from upstream

* Sat Apr  5 2008 Matthias Clasen  <mclasen@redhat.com> - 0.1.11-1
- Update to 0.1.11

* Fri Mar 28 2008 Bill Nottingham <notting@redhat.com> - 0.1.10-1
- update to 0.1.10
- add PK-gnome-devel build requirement

* Tue Mar 18 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.9-4
- move pk-update-icon.desktop to /etc/xdg/autostart/

* Thu Mar 13 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.9-3
- symlink pk-install-file to system-install-packages

* Tue Mar 11 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.9-2
- Apply patch to enable gnome-packagekit in KDE

* Wed Mar  5 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.9-1
- Update to latest upstream version: 0.1.8

* Thu Feb 21 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.8-1
- Update to latest upstream version: 0.1.8

* Fri Feb 15 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.7-1
- Update to latest upstream version: 0.1.7

* Sat Jan 19 2008 Robin Norwood <rnorwood@redhat.com> - 0.1.6-1
- Update to latest upstream version: 0.1.6

* Sun Dec 30 2007 Christopher Aillon <caillon@redhat.com> - 0.1.5-2
- Fix the build

* Fri Dec 21 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.5-1
- Update to latest upstream version: 0.1.5
 
* Tue Nov 27 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.4-1
- Update to latest upstream version: 0.1.4

* Mon Nov 12 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.3-1
- Update to latest upstream version: 0.1.3

* Sun Nov 11 2007 Ray Strode <rstrode@redhat.com> - 0.1.2-2
- remove --vendor "gnome" from desktop-file-install calls. It's
  deprecated and changes the latest of .desktop files.

* Thu Nov 01 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.2-1
- Update to latest upstream version: 0.1.2

* Tue Oct 23 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.1-1
- Update to latest upstream version

* Tue Oct 16 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.0-2
- Apply recommended fixes from package review
 
* Mon Oct 15 2007 Robin Norwood <rnorwood@redhat.com> - 0.1.0-1
- Initial build (based upon spec file from Richard Hughes)
