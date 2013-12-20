#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    TkRAD - Tkinter Rapid Application Development

    (c) 2013 Raphaël SEBAN <motus@laposte.net>

    released under Creative Commons BY-SA 3.0

    see http://creativecommons.org/licenses/by-sa/3.0/
"""



# lib imports

import re

import os

import os.path as OP

import configparser as CP

from . import uri

from . import tools



# unique instance pointer

__option_manager = None



# service getter

def get_option_manager (owner = None, **kw):
    r"""
        gets application-wide unique instance for rc option manager;
    """

    global __option_manager

    if not isinstance(__option_manager, OptionManager):

        __option_manager = OptionManager(owner, **kw)

    # end if

    return __option_manager

# end def



# service class

class OptionManager(CP.ConfigParser):
    r"""
        generic rc configuration file internal options manager;
    """



    CONFIG = {

        "dir": "~/.config/apps",

        "file": "options.rc",

    } # end of CONFIG



    SECTIONS = (

        "dirs",  "files",  "geometry",  "gui",  "xml",

    ) # end of SECTIONS



    def __init__ (self, owner = None, **kw):
        r"""
            class constructor - inits params and rc sections;
        """

        # super inits

        CP.ConfigParser.__init__(self)

        # member inits

        self.set_owner(owner)

        self.set_config_dir(kw.get("rc_dir"))

        self.set_config_file(kw.get("rc_file"))

        self.set_sections("DEFAULT")

        self.set_sections(*self.SECTIONS)

        self.__loaded = False

    # end def



    def ensure_config_dir (self):
        r"""
            creates missing directories if necessary;

            raises exceptions to the CLI console in case of errors;

            returns True on success, False otherwise;
        """

        try:

            os.makedirs(self.get_config_dir(), exist_ok = True)

            return True

        except:

            raise

            return False

        # end try

    # end def



    def get_config_dir (self):
        r"""
            configuration directory getter;
        """

        return uri.canonize(self.__rc_dir)

    # end def



    def get_config_file (self):
        r"""
            configuration file radix getter (filename w/out extension);
        """

        return self.__rc_file

    # end def



    def get_owner (self):
        r"""
            returns owner pointer of 'this' instanciated class object;
        """

        return self.owner

    # end def



    def get_uri (self):
        r"""
            builds URI along rc config dir and filename;

            returns URI on success, None otherwise;
        """

        # inits

        _uri = None

        # ensure rc_dir is OK

        if self.ensure_config_dir():

            _uri = OP.join(

                self.get_config_dir(), self.get_config_file()
            )

        # end if

        return _uri

    # end def



    def load (self):
        r"""
            tries to load predefined rc file or a default one;

            loads successful file only once;

            any later calls will not be taken in account;

            use reload() to reset internal rc options;

            returns a list of read files on success, None otherwise;
        """

        # inits

        _success = None

        # inner controls

        if not self.__loaded:

            _success = self.read(

                tools.choose_str(

                    self.get_uri(),

                    OP.join(

                        uri.canonize(self.CONFIG.get("dir")),

                        self.get_config_file()
                    ),
                )
            )

            self.__loaded = tools.is_plist(_success)

        # end if

        return _success

    # end def



    def reload (self):
        r"""
            forces reload of rc file and resets internal options;

            use with caution as some runtime modified options might

            not be saved before this operation;

            no return value (void);
        """

        self.__loaded = False

        self.load()

    # end def



    def save (self):
        r"""
            saves internal options to a predefined rc file;

            may raise OSError on several file problems;

            no return value (void);
        """

        # inits

        _uri = self.get_uri()

        if tools.is_pstr(_uri):

            with open(_uri, "w") as _fd:

                self.write(_fd)

            # end with

        else:

            # raise exception

            raise OSError("Could not save options configuration file.")

        # end if

    # end def



    def set_config_dir (self, value):
        r"""
            configuration directory setter;

            no return value (void);
        """

        # private member inits

        self.__rc_dir = uri.canonize(

            tools.choose_str(value, self.CONFIG.get("dir"))
        )

    # end def



    def set_config_file (self, value):
        r"""
            configuration file radix setter (filename w/out extension);

            no return value (void);
        """

        # private member inits

        self.__rc_file = re.sub(

            r"[^\w.]+",  r"-",

            tools.choose_str(value, self.CONFIG.get("file"))
        )

    # end def



    def set_defaults (self, **kw):
        r"""
            fills the 'DEFAULT' rc file section with default

            (key, value) pairs defined in @kw keywords param;

            no return value (void);
        """

        self["DEFAULT"].update(kw)

    # end def



    def set_owner (self, owner):
        r"""
            sets up owner pointer of 'this' instanciated class object;

            no return value (void);
        """

        self.owner = owner

    # end def



    def set_sections (self, *names):
        r"""
            adds new sections to internal rc options if missing;

            keeps already existing sections untouched;

            no return value (void);
        """

        for _section in set(names):

            self.setdefault(_section, dict())

        # end for

    # end def


# end class OptionManager
