#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkRAD - tkinter Rapid Application Development library

    (c) 2013+ Raphaël SEBAN <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public
    License along with this program.

    If not, see: http://www.gnu.org/licenses/
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

def get_option_manager (**kw):
    r"""
        gets application-wide unique instance for rc option manager;
    """

    global __option_manager

    if not isinstance(__option_manager, OptionManager):

        __option_manager = OptionManager(**kw)

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



    def __init__ (self, **kw):
        r"""
            class constructor - inits params and rc sections;
        """

        # super inits

        CP.ConfigParser.__init__(self)

        # member inits

        self.set_config_dir(kw.get("rc_dir"))

        self.set_config_file(kw.get("rc_file"))

        self.set_sections("DEFAULT")

        self.set_sections(*self.SECTIONS)

        self.__loaded = False

    # end def



    def _ensure_config_dir (self):
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



    def _get_uri (self):
        r"""
            builds URI along rc config dir and filename;

            returns URI on success, None otherwise;
        """

        # inits

        _uri = None

        # ensure rc_dir is OK

        if self._ensure_config_dir():

            _uri = OP.join(

                self.get_config_dir(), self.get_config_file()
            )

        # end if

        return _uri

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

                    self._get_uri(),

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

        _uri = self._get_uri()

        if tools.is_pstr(_uri):

            with open(_uri, "w") as _file:

                self.write(_file)

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
