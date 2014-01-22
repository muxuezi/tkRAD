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



# ========================= STANDALONE MODULE ==========================



# lib imports

import os.path as OP



# module private var init

__app_root_dir = "."



def canonize (uri, raise_error = False):
    """
        substitutes heading ^ by __app_root_dir;

        expands eventual user ~ directory;

        tries to retrieve abspath() / realpath();

        returns parsed URI on success or empty string "" otherwise;
    """

    # param control

    if uri and isinstance(uri, str):

        # app root directory implementation

        if uri.startswith("^"):

            uri = OP.join(__app_root_dir, uri.lstrip("^" + OP.sep))

        # end if

        # return parsed URI

        return OP.abspath(OP.realpath(OP.expanduser(uri)))

    # unsupported

    elif raise_error:

        raise TypeError("expected plain string of chars.")

    # end if

    # force to empty string

    return ""

#end def



def get_app_root_dir ():
    r"""
        module private instance pointer getter
    """

    return __app_root_dir

# end def



def set_app_root_dir (path):
    r"""
        module private instance pointer setter
    """

    global __app_root_dir

    __app_root_dir = OP.dirname(canonize(path))

# end def
