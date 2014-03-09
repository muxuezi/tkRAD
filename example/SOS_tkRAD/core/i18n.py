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

from . import path

from . import tools



# current translations directory init

__translations_dir = "^/locale"



# current translations language init

__translations_lang = tools.choose_str(locale.getdefaultlocale()[0])



# current translations table init

__translations_table = dict()



def _ (text):
    r"""
        tries to retrieve a locale translation along setup;

        returns translated text on success, original text otherwise;
    """

    return tools.choose_str(__translations_table.get(text), text)

# end def


# set overall scope function

__builtins__["_"] = _



def get_translations_dir ():
    r"""
        gets locale translations directory;
    """

    return __translations_dir

# end def



def get_translations_lang ():
    r"""
        gets locale translations language;
    """

    return __translations_lang

# end def



def get_translations_table ():
    r"""
        gets locale translations hash table;
    """

    return __translations_table

# end def



def install (lc_dir = None, lc_lang = None):
    r"""
        sets up translations directory and language;

        tries to update translations table along new values;

        no return value (void);
    """

    set_translations_dir(lc_dir)

    set_translations_lang(lc_lang)

    try:

        load_translations_table()

    except:

        set_translations_table(dict())

    # end try

# end def



def load_translations_table (lc_dir = None, lc_lang = None):
    r"""
        tries to load translations table along lc_lang and lc_dir;

        no return value (void);
    """

    # allow updates

    global __translations_table

    # look for translations file

    lc_dir = tools.choose_str(lc_dir, __translations_dir)

    lc_lang = tools.choose_str(lc_lang, __translations_lang)

    _path = path.normalize(OP.join(lc_dir, lc_lang + ".po"))

    with open(_path, "r", encoding="UTF-8") as _file:

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

    # try new translations table

    __translations_table = eval("{" + _data + "}")

# end def



def set_translations_dir (arg):
    r"""
        sets up locale translations directory;
    """

    # allow updates

    global __translations_dir

    # set new value

    __translations_dir = tools.choose_str(arg, __translations_dir)

# end def



def set_translations_lang (arg):
    r"""
        sets up locale translations language to use;
    """

    # allow updates

    global __translations_lang

    # set new value

    __translations_lang = tools.choose_str(arg, __translations_lang)

# end def



def set_translations_table (arg):
    r"""
        sets up locale translations hash table;
    """

    # allow updates

    global __translations_table

    # set new value

    __translations_table = dict(arg)

# end def

