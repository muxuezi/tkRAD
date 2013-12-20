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

import locale

import os.path as OP

from . import uri



# current translations directory init

__translations_dir = "^/locale"



# current translations language init

__translations_lang = locale.getlocale()



# current translations table init

__translations_table = dict()



def _(text):
    r"""
        tries to retrieve a locale translation along setup;

        returns translated text on success, original text otherwise;
    """

    return str(__translations_table.get(text, text))

# end def



__builtins__["_"] = _



def install (tr_dir, tr_lang):
    r"""
        sets up translations directory and language;

        tries to update translations table along new values;

        no return value (void);
    """

    set_translations_dir(tr_dir)

    set_translations_lang(tr_lang)

    update_translations_table()

# end def



def set_translations_dir (arg):
    r"""
        sets up locale translations directory;
    """

    # allow updates

    global __translations_dir

    # set new value

    __translations_dir = str(arg)

# end def



def set_translations_lang (arg):
    r"""
        sets up locale translations language to use;
    """

    # allow updates

    global __translations_lang

    # set new value

    __translations_lang = str(arg)

# end def



def update_translations_table ():
    r"""
        tries to update translations table along current lang and dir;

        no return value (void);
    """

    # allow updates

    global __translations_table

    # look for translations file

    _uri = uri.canonize(

        OP.join(__translations_dir, __translations_lang + ".po")
    )

    with open(_uri, "r", encoding = "utf-8") as _file:

        _data = _file.read()

    # end with

    # transform a PO *.po file to a dict() sequence

    # strip heading comments

    _data = re.sub(r"(?m)^#.*$", r"", _data)

    # lowercase all 'msgId', 'MSGID' and others

    _data = re.sub(r"(?i)msgid", r"msgid", _data)

    # split string to list()

    _data = _data.split("msgid")

    # anything before first 'msgid'

    # is useless (and buggy) /!\

    del _data[0]

    # rebuild data string

    _data = ",".join(_data)

    # change 'msgstr' (case-insensitive) to ':'

    _data = re.sub(r"(?i)msgstr", r":", _data)

    # try new translation table

    __translations_table = eval("{" + _data + "}")

# end def

