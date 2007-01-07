serverdir = $(libdir)/bonobo/servers
server_in_files = GNOME_BlogApplet.server.in
server_DATA = $(server_in_files:.server.in=.server)

$(server_in_files): $(server_in_files:.server.in=.server.in.in)
	sed -e "s|\@LIBEXECDIR\@|$(libexecdir)|" $< > $@

@INTLTOOL_SERVER_RULE@

bin_SCRIPTS = gnome-blog-poster
libexec_SCRIPTS = blog_applet.py

gnomeblogdir = $(pythondir)/gnomeblog

gnomeblog_PYTHON = 		\
	__init__.py		\
	blog_applet.py		\
	gnome-blog-poster	\
	blog_poster.py 		\
	aligned_window.py 	\
	hig_alert.py 		\
	blogger_prefs.py	\
	gconf_widgets.py	\
	blog.py			\
	rich_entry.py		\
	html_converter.py	\
	gnome_blog_globals.py   \
	proxy.py


16icondir = $(datadir)/icons/hicolor/16x16/apps
16icon_DATA = icons/16x16/gnome-blog.png

22icondir = $(datadir)/icons/hicolor/22x22/apps
22icon_DATA = icons/22x22/gnome-blog.png

24icondir = $(datadir)/icons/hicolor/24x24/apps
24icon_DATA = icons/24x24/gnome-blog.png

32icondir = $(datadir)/icons/hicolor/32x32/apps \
32icon_DATA = icons/32x32/gnome-blog.png

icondir   = $(datadir)/icons/hicolor/48x48/apps
icon_DATA = icons/48x48/gnome-blog.png

svgicondir = $(datadir)/icons/hicolor/scalable/apps
svgicon_DATA = icons/scalable/gnome-blog.svg

gtk_update_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/hicolor

uidir   = $(datadir)/gnome-2.0/ui
ui_DATA = GNOME_BlogApplet.xml


# GConf Preference Schemas
schemadir = \
        $(GCONF_SCHEMA_FILE_DIR)

schema_in_files = \
        gnomeblog.schemas.in

schema_DATA = \
        $(schema_in_files:.schemas.in=.schemas)

@INTLTOOL_SCHEMAS_RULE@

Desktopdir = $(datadir)/applications
Desktop_in_files = gnome-blog.desktop.in.in
Desktop_DATA = $(Desktop_in_files:.desktop.in.in=.desktop)
@INTLTOOL_DESKTOP_RULE@


install-data-hook:
	@-if test -z "$(DESTDIR)"; then \
		echo "Updating Gtk icon cache."; \
		$(gtk_update_icon_cache); \
	else \
		echo "*** Icon cache not updated.  After install, run this:"; \
		echo "***   $(gtk_update_icon_cache)"; \
	fi


install-data-local:
        GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) \
                gconftool-2 --makefile-install-rule $(schema_DATA)

DISTCLEANFILES =                \
	$(schema_DATA)		\
	$(server_DATA)		\
	$(Desktop_DATA)		\
        intltool-extract        \
        intltool-merge          \
        intltool-update


EXTRA_DIST =  			\
	$(Desktop_in_files)	\
	$(Desktop_DATA)		\
	$(schema_in_files) 	\
	$(ui_DATA)		\
        $(16icon_DATA)          \
        $(22icon_DATA)          \
        $(24icon_DATA)          \
        $(32icon_DATA)          \
        $(icon_DATA)            \
        $(svgicon_DATA)         \
	GNOME_BlogApplet.server.in.in \
        intltool-update.in      \
        intltool-extract.in     \
        intltool-merge.in       \
	gnome-blog.spec		\
	gnome-blog.spec.in 	\
	$(server_in_files)

SUBDIRS = protocols po
