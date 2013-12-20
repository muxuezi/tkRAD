#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    TkRAD - Tkinter Rapid Application Development

    (c) 2013 Raphaël SEBAN <motus@laposte.net>

    released under Creative Commons BY-SA 3.0

    see http://creativecommons.org/licenses/by-sa/3.0/
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

        returns parsed URI or empty string "" if unknown @uri object;
    """

    # param control

    if isinstance(uri, str) and uri:

        # app root directory implementation

        if uri.startswith("^"):

            uri = OP.join(__app_root_dir, uri.lstrip("^" + OP.sep))

        # end if

        # return parsed URI

        return OP.abspath(OP.realpath(OP.expanduser(uri)))

    # unsupported

    else:

        if raise_error:

            raise TypeError(

                "expected plain string of chars."
            )

        # end if

        # force to empty string

        return ""

    # end if

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
