serverdir = $(libdir)/bonobo/servers
server_DATA = GNOME_BloggerApplet.server

bin_SCRIPTS = blogger_applet.py
python_PYTHON = blog_poster.py aligned_window.py hig_alert.py

                                                             
# GConf Preference Schemas
schemadir = \
        $(GCONF_SCHEMA_FILE_DIR)
                                                                                                                         
schema_in_files = \
        gnomeblogger.schemas.in
                                                                                                                         
schema_DATA = \
        $(schema_in_files:.schemas.in=.schemas)
                                                                                                                         
@INTLTOOL_SCHEMAS_RULE@

EXTRA_DIST = $(schema_in_files)

install-data-local:
        GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) \
                gconftool-2 --makefile-install-rule $(schema_DATA)

CLEANFILES = $(schema_DATA)
