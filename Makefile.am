serverdir = $(libdir)/bonobo/servers
server_in_files = GNOME_BlogApplet.server.in
server_DATA = $(server_in_files:.server.in=.server)

@INTLTOOL_SERVER_RULE@

bin_SCRIPTS = blog_applet.py

python_PYTHON = 		\
	blog_applet.py		\
	blog_poster.py 		\
	aligned_window.py 	\
	hig_alert.py 		\
	style_toggle.py		\
	blogger_prefs.py	\
	gconf_widgets.py	\
	blog.py		\
	gnome_blog_globals.py

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

install-data-local:
        GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) \
                gconftool-2 --makefile-install-rule $(schema_DATA)

DISTCLEANFILES =                \
	$(schema_DATA)		\
	$(server_DATA)		\
        intltool-extract        \
        intltool-merge          \
        intltool-update


EXTRA_DIST =  			\
	$(schema_in_files) 	\
	$(ui_DATA)		\
	$(pixmaps_DATA)		\
	GNOME_BlogApplet.server.in \
        intltool-update.in      \
        intltool-extract.in     \
        intltool-merge.in       \
	gnome-blog.spec	\
	gnome-blog.spec.in

SUBDIRS = po
