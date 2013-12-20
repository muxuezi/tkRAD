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

import re



def canonize_id (arg, raise_error = False):
    r"""
        filters @arg param char string to __identifier__

        language semantics compliance i.e. allows only regexp(r"\w+");

        returns parsed string of chars, empty string otherwise;
    """

    # param controls

    if is_pstr(arg):

        return re.sub(r"\W+", r"", arg)

    # unknown type - force to empty string

    else:

        if raise_error:

            raise TypeError(

                "expected plain string of chars."
            )

        # end if

        return ""

    # end if

# end def



def canonize_import (arg, raise_error = False):
    r"""
        filters @arg param in order to comply with syntax constraints

        of Python's "from ... import relative_or_star as ...";

        returns parsed string of chars, empty string otherwise;
    """

    # star semantics?

    if "*" in str(arg):

        # must be a lone star /!\

        return "*"

    # should act as __relative_module__ semantics

    else:

        return canonize_relative_module(arg, raise_error)

    # end if

# end def



def canonize_relative_module (arg, raise_error = False):
    r"""
        filters @arg param char string along Python's relative_module

        language specs i.e. allows only regexp(r"[\.\w]+");

        returns parsed string of chars, empty string otherwise;
    """

    # param controls

    if is_pstr(arg):

        # allow only regexp(r"[\.\w]+")

        arg = re.sub(r"[^\.\w]+", r"", arg)

        # only one dot '.' between each identifier

        arg = re.sub(r"\b\.+", r".", arg)

        # no trailing dots on the right side

        arg = re.sub(r"\b\.+$", r"", arg)

        return arg

    # unknown type - force to empty string

    else:

        if raise_error:

            raise TypeError(

                "expected plain string of chars."
            )

        # end if

        return ""

    # end if

# end def



def choose_num (callback, *args):
    r"""
        tries to find a number (int or float) in argument list along

        @callback param truth return value;

        if @callback param is None or is not callable, tries only

        to find a number;

        returns 0 if no number found in list;
    """

    # param controls

    if not callable(callback):

        callback = lambda n: True

    # end if

    # ordered loop on args

    for _arg in args:

        # choose only int or float along callback's truth value

        if is_num(_arg) and callback(_arg):

            return _arg

        # end if

    # end for

    # not found

    return 0

# end def



def choose_str (*args):
    r"""
        tries to find a plain string in argument list;

        returns an empty string if not found;
    """

    # ordered loop on args

    for _arg in args:

        # choose only plain string

        if is_pstr(_arg):

            return _arg

        # end if

    # end for

    # not found - return empty string

    return ""

# end def



def ensure_float (arg):
    r"""
        if @arg param is not eval'd to float number, resets to 0;

        returns a float value in any case;
    """

    try:

        arg = float(eval(str(arg)))

    except:

        arg = 0.0

    # end try

    return arg

# end def



def ensure_int (arg):
    r"""
        if @arg param is not eval'd to integer, resets to 0;

        returns an integer value in any case;
    """

    try:

        arg = int(eval(str(arg)))

    except:

        arg = 0

    # end try

    return arg

# end def



def is_num (arg):
    r"""
        determines if arg is numeric (of int or float type);
    """

    return isinstance(arg, (int, float))

# end def



def is_pdict (arg):
    r"""
        determines if arg is of plain dictionary type;
    """

    return arg and isinstance(arg, dict)

# end def



def is_plist (arg):
    r"""
        determines if arg is of plain list type;
    """

    return arg and isinstance(arg, list)

# end def



def is_pstr (arg):
    r"""
        determines if arg is of plain string type;
    """

    return arg and isinstance(arg, str)

# end def



def is_ptuple (arg):
    r"""
        determines if arg is of plain tuple type;
    """

    return arg and isinstance(arg, tuple)

# end def



def str_complete (str_format, str_value, default = ""):
    r"""
        tries to complete @str_format param with @str_value param

        if @str_value is plain string;

        returns formatted string on success, @default otherwise;

        code example:

        tools.str_complete("only if value {} exists", value, "no way!")
    """

    if is_pstr(str_format) and is_pstr(str_value):

        return str_format.format(str_value)

    else:

        return default

    # end if

# end def

