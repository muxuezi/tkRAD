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



def check_directories (root_dir, *dir_list):
    r"""
        verifies if a set of app-vital directories do exist;

        raises FileNotFoundError on first missing;

        returns True on success, False otherwise;
    """

    import os.path as OP

    root_dir = str(root_dir)

    for _dir in set(dir_list):

        _dir = OP.join(root_dir, _dir)

        if not OP.isdir(_dir):

            raise FileNotFoundError(

                "Required directory '{reqdir}' could not be found."

                .format(reqdir = _dir)
            )

            return False

        # end if

    # end for

    # all is OK

    return True

# end def



def parse_version (version, get_string = False):
    r"""
        tries to compute a version string into a comparable list()
        object;

        returns parsed str(@version) if @get_string;

        returns max 3-items list() object otherwise;
    """

    import re

    _version = re.sub(r"\.+", r".", str(version))

    _version = re.sub(r"[^0-9\.].*$", r"", _version).strip(".")

    # parsed string version

    if get_string:

        return _version

    # end if

    # parsed list() version

    return list(map(int, ("0" + _version).split(".")))[:3]

# end def



def python_require (version, strict = False):
    r"""
        verifies if current Python interpreter version matches

        @version param constraints along @strict param;

        raises SystemError if Python current version is lesser than

        required @version param version;

        raises SystemError if @strict is True and current Python version

        does not match *exactly* required @version param version;

        each exception stops definitely script execution i.e. exit();

        no return value (void);
    """

    import platform

    _req_version = str(version)

    _cur_version = str(platform.python_version())

    # compare strict version

    if strict and (_req_version != _cur_version):

        raise SystemError(

            (
                "This program expects *STRICT* Python "

                "version {vreq} while current version is {vcur}."

            ).format(vreq=_req_version, vcur=_cur_version)
        )

        exit(1)

    # compare loose version

    elif parse_version(_req_version) > parse_version(_cur_version):

        raise SystemError(

            (
                "This program expects *AT LEAST* Python "

                "version {vreq} while current version is {vcur}."

            ).format(

                vreq = parse_version(_req_version, get_string = True),

                vcur = _cur_version
            )
        )

        exit(1)

    # end if

# end def
