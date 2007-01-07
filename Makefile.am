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

pixmapsdir = $(datadir)/pixmaps
pixmaps_DATA = gnome-blog.png

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
	$(pixmaps_DATA)		\
	GNOME_BlogApplet.server.in.in \
        intltool-update.in      \
        intltool-extract.in     \
        intltool-merge.in       \
	gnome-blog.spec		\
	gnome-blog.spec.in 	\
	$(server_in_files)

SUBDIRS = protocols po
