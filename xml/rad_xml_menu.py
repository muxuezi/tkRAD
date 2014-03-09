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

import tkinter as TK

from tkinter import ttk

from ..core import tools

from . import rad_xml_widget_base as XW



class RADXMLMenu (XW.RADXMLWidgetBase):
    r"""
        generic XML to tkinter menu builder;

        this is THE tkinter menu building processor of tkRAD;

        supports all menu / submenu type inclusions;

        supports *direct* access by XML 'id' attribute for root menus
        and for any cascading submenu at any level of inclusion
        e.g. _menu = self.get_object_by_id('xml_defined_menu_id');

        NO SUPPORT for direct access to menu items such as
        separators, commands, checkbuttons and radiobuttons since
        tkinter does technically *NOT* allow such identification /
        access;
    """



    # default XML attribute values
    # overrides RADXMLWidgetBase.ATTRS

    ATTRS = {

        # $ 2014-02-18 RS $
        # CAUTION:
        # since tkRAD v1.2
        # put here only *INDISPENSABLE* attrs
        # this is for optimization reasons

        "generic": {
            "id": None,
        },

        "checkable": {
        },

        "menu": {
            "tearoff": 0,
        },

        "child": {
            "label": None,
            "underline": None,
        },

    } # end of ATTRS



    # XML tree root element
    # overrides RADXMLBase.DOCTYPE

    DOCTYPE = "tkmenu"



    # accepted XML child elements for XML container element

    DTD = {

        "menu": (
            "menu", "command", "checkbutton", "radiobutton",
            "separator",
        ),

        "tkmenu": (
            "menu",
        ),

    } # end of DTD



    # mandatory XML attribute keys for each item

    KEYS = {

        # $ 2014-02-18 RS $
        # CAUTION:
        # since tkRAD v1.2
        # *ALL* attrs must figure out there
        # this is for optimization reasons

        # please, do *NOT* change this
        # unless you know what you are doing

        "generic": ("id",),

        "checkable": ("selected", "checked"),

        "menu": ("activebackground", "activeborderwidth",
        "activeforeground", "background", "bd", "bg", "borderwidth",
        "cursor", "disabledforeground", "fg", "font", "foreground",
        "postcommand", "relief", "selectcolor", "tearoff",
        "tearoffcommand", "title"),

        "child": ("accelerator", "activebackground",
        "activeforeground", "background", "bitmap", "columnbreak",
        "command", "compound", "font", "foreground", "hidemargin",
        "image", "label", "menu", "offvalue", "onvalue",
        "selectcolor", "selectimage", "state", "underline", "value",
        "variable"),

    } # end of KEYS



    # 'accelerator' XML attribute pre-compiled subs

    SYMBOLS = (

        (re.compile(r"\^+|C-|(?i)co?n?tro?l"), r"Control-"),
        (re.compile(r"M-|(?i)meta|(?i)alt"), r"Alt-"),
        (re.compile(r"(?i)shi?ft"), r"Shift-"),
        (re.compile(r"\+$"), r"plus"),
        (re.compile(r"\-$"), r"minus"),
        (re.compile(r"\*$"), r"asterisk"),
        (re.compile(r"\/$"), r"slash"),
        (re.compile(r"\.$"), r"period"),
        (re.compile(r"\,$"), r"comma"),
        (re.compile(r"\:$"), r"colon"),
        (re.compile(r"\;$"), r"semicolon"),
        (re.compile(r"\?$"), r"question"),
        (re.compile(r"\!$"), r"exclam"),
        (re.compile(r"\$$"), r"dollar"),
        (re.compile(r"\%$"), r"percent"),
        (re.compile(r"\@$"), r"at"),
        (re.compile(r"\&$"), r"ampersand"),
        (re.compile(r"\#$"), r"numbersign"),
        (re.compile(r"\_$"), r"underscore"),
        (re.compile(r"(?i)less|(?i)\blt\b"), r"less"),
        (re.compile(r"(?i)greater|(?i)\bgt\b"), r"greater"),
        (re.compile(r"(?i)spa?ce?"), r"space"),
        (re.compile(r"(?i)ba?ckspa?ce?"), r"BackSpace"),
        (re.compile(r"(?i)del(?:ete)?\b"), r"Delete"),
        (re.compile(r"(?i)bre?a?k|(?i)ca?nce?l"), r"Cancel"),
        (re.compile(r"(?i)esc(?:ape)?\b"), r"Escape"),
        (re.compile(r"(?i)tab(?:ulate)?"), r"Tab"),
        (re.compile(r"(?i)ho?me?"), r"Home"),
        (re.compile(r"(?i)end"), r"End"),
        (re.compile(r"(?i)page[\s\+\-]*?up"), r"Prior"),
        (re.compile(r"(?i)page[\s\+\-]*?do?w?n"), r"Next"),
        (re.compile(r"(?i)(?:arrow)?[\s\+\-]*?up"), r"Up"),
        (re.compile(r"(?i)(?:arrow)?[\s\+\-]*?do?w?n"), r"Down"),
        (re.compile(r"(?i)(?:arrow)?[\s\+\-]*?left"), r"Left"),
        (re.compile(r"(?i)(?:arrow)?[\s\+\-]*?right"), r"Right"),
        (re.compile(r"(?i)f(\d+)$"), r"F\1"),           # F1~F12 keys
        (re.compile(r"[<>]+"), r""),           # "<Ctrl><Z>" notation
        (re.compile(r"^\W+|\W+$"), r""),
        (re.compile(r"\W+"), r"-"),

    ) # end of SYMBOLS



    # XML file path parts for xml_build() automatic mode
    # overrides RADXMLBase.XML_RC

    XML_RC = {
        "dir": "^/xml/menu",
        # do *NOT* define "filename" here
        "file_ext": ".xml",
    } # end of XML_RC



    # ------------------  XML elements building  -----------------------



    def _build_element_checkbutton (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a menu item of type 'checkbutton' (single choice);

            returns True;
        """

        # $ 2014-02-17 RS $
        # XML root element is now casted
        # no more need to cast tk_parent

        # XML attributes init

        _attrs = self._init_checkables(xml_element, tk_parent)

        # prepare child options

        _coptions = self._init_coptions(xml_element, tk_parent)

        # control var inits

        _cvar = _coptions.get("variable")

        # set up by default?

        if _cvar and _attrs.get("checked"):

            _cvar.set(tools.choose_str(_coptions.get("onvalue")))

        # end if

        # set menu item

        tk_parent.add_checkbutton(**_coptions)

        return True

    # end def



    def _build_element_command (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a menu item of type 'command' (action);

            returns True;
        """

        # $ 2014-02-17 RS $
        # XML root element is now casted
        # no more need to cast tk_parent

        # prepare child options

        _coptions = self._init_coptions(xml_element, tk_parent)

        # set menu item

        tk_parent.add_command(**_coptions)

        return True

    # end def



    def _build_element_menu (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a tkinter menu widget;

            return True on success, False otherwise;
        """

        # param controls - submenu

        if not self.is_menu(tk_parent):

            # unsupported

            raise TypeError(

                _(
                    "Tkinter Menu() object is *NOT* "

                    "insertable into {obj_type} object."

                ).format(obj_type = repr(tk_parent))
            )

            return False

        # end if

        # default inits

        _attrs = self._init_generics(xml_element, tk_parent)

        _moptions = self._init_moptions(xml_element, tk_parent)

        # child menu inits

        _new_menu = TK.Menu(tk_parent, **_moptions)

        # keep a copy aboard

        self._register_object_by_id(_new_menu, _attrs.get("id"))

        # prepare child options

        _coptions = self._init_coptions(xml_element, tk_parent)

        # make some operations on child options

        _coptions["menu"] = _new_menu

        # set menu item

        tk_parent.add_cascade(**_coptions)

        # free useless memory right now /!\

        del _attrs, _moptions, _coptions

        # loop on XML element children

        return self._loop_on_children(

            xml_element, _new_menu, accept = self.DTD.get(xml_tag)
        )

    # end def



    def _build_element_radiobutton (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a menu item of type 'radiobutton' (options group
            choice);

            returns True;
        """

        # $ 2014-02-17 RS $
        # XML root element is now casted
        # no more need to cast tk_parent

        # XML attributes init

        _attrs = self._init_checkables(xml_element, tk_parent)

        # prepare child options

        _coptions = self._init_coptions(xml_element, tk_parent)

        # control var inits

        _cvar = _coptions.get("variable")

        # set up by default?

        if _cvar and _attrs.get("selected"):

            _cvar.set(tools.choose_str(_coptions.get("value")))

        # end if

        # set menu item

        tk_parent.add_radiobutton(**_coptions)

        return True

    # end def



    def _build_element_separator (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a menu separator item;

            returns True;
        """

        # $ 2014-02-17 RS $
        # XML root element is now casted
        # no more need to cast tk_parent

        tk_parent.add_separator()

        return True

    # end def



    def _build_element_tkmenu (self, xml_tag, xml_element, tk_parent):
        r"""
            <tkmenu> is the root node of XML tree;

            its purpose is to get a clean attachment to tk widget

            owner;

            <tkmenu> becomes a tkinter.Menu() object in fact;

            return True on build success, False otherwise;
        """

        # param controls

        if not self.is_menu_handler(tk_parent):

            # set app's root Tk() object instead

            # CAUTION: winfo_toplevel() is *NOT* a Toplevel() object

            tk_parent = self.tk_owner.winfo_toplevel()

        # end if

        # default inits

        _attrs = self._init_generics(xml_element, tk_parent)

        _moptions = self._init_moptions(xml_element, tk_parent)

        # menu inits

        _new_menu = TK.Menu(tk_parent, **_moptions)

        # keep a copy aboard

        self._register_object_by_id(_new_menu, _attrs.get("id"))

        # attach new menu to parent widget

        tk_parent["menu"] = _new_menu

        # free useless memory right now /!\

        del _attrs, _moptions

        # loop on XML element children

        if self.is_topmenu_handler(tk_parent):

            _dtd = "tkmenu"

        else:

            _dtd = "menu"

        # end if

        return self._loop_on_children(

            xml_element, _new_menu, accept = self.DTD.get(_dtd)
        )

    # end def



    def _init_checkables (self, xml_element, tk_parent):
        r"""
            protected method def;

            parses only tkRAD implemented checkable XML attrs;

            returns parsed attrs;
        """

        # shallow copy inits

        _attrs = self.ATTRS["checkable"].copy()

        # override (key, value) pairs

        _attrs.update(

            tools.dict_only_keys(

                xml_element.attrib, *self.KEYS["checkable"]
            )
        )

        # return parsed XML attributes

        return self._parse_xml_attributes(

            xml_element, tk_parent, xml_attrs = _attrs
        )

    # end def



    def _init_coptions (self, xml_element, tk_parent):
        r"""
            protected method def;

            prepares menu item child options (coptions);

            returns parsed attrs;
        """

        # shallow copy inits

        _coptions = self.ATTRS["child"].copy()

        # override (key, value) pairs

        _coptions.update(

            tools.dict_only_keys(

                xml_element.attrib, *self.KEYS["child"]
            )
        )

        # parse XML attributes

        _coptions = self._parse_xml_attributes(

            xml_element, tk_parent, xml_attrs = _coptions
        )

        # keyboard accelerator inits

        _acc = self.TK_ACCEL

        _cmd = _coptions.get("command")

        # event binding

        if tools.is_pstr(_acc) and callable(_cmd):

            self.tk_owner.bind_all(_acc, _cmd)

        # end if

        # return parsed XML attributes

        return _coptions

    # end def



    def _init_generics (self, xml_element, tk_parent):
        r"""
            protected method def;

            parses only tkRAD implemented generic XML attrs;

            returns parsed attrs;
        """

        # $ 2014-02-18 RS $
        # tkRAD >= v1.2
        # code optimization:
        # as "generic" has only one "id" item
        # don't lose your time!

        return dict(id = self.element_get_id(xml_element))

        """
        # genuine code

        # shallow copy inits

        _attrs = self.ATTRS["generic"].copy()

        # override (key, value) pairs

        _attrs.update(

            tools.dict_only_keys(

                xml_element.attrib, *self.KEYS["generic"]
            )
        )

        # return parsed XML attributes

        return self._parse_xml_attributes(

            xml_element, tk_parent, xml_attrs = _attrs
        )
        """

    # end def



    def _init_moptions (self, xml_element, tk_parent):
        r"""
            protected method def;

            prepares menu widget options (moptions);

            returns parsed attrs;
        """

        # shallow copy inits

        _moptions = self.ATTRS["menu"].copy()

        # override (key, value) pairs

        _moptions.update(

            tools.dict_only_keys(

                xml_element.attrib, *self.KEYS["menu"]
            )
        )

        # return parsed XML attributes

        return self._parse_xml_attributes(

            xml_element, tk_parent, xml_attrs = _moptions
        )

    # end def



    # -----------------------  XML attributes parsing  -----------------



    def _parse_attr_accelerator (self, attribute, **kw):
        r"""
            tries to set up a tkinter event sequence along

            XML attribute 'accelerator';

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # sequence inits

            _acc = attribute.value

            # change symbols

            for (_search, _replace) in self.SYMBOLS:

                _acc = _search.sub(_replace, _acc)

            # end for

            # <shift> modifier special case in Tk

            _chunks = _acc.split("-")

            _detail = _chunks[-1]

            # got just one character?

            if len(_detail) == 1:

                if "shift" in _acc.lower():

                    # letter must be uppercased /!\

                    _detail = _detail.upper()

                else:

                    # letter must be lowercased /!\

                    _detail = _detail.lower()

                # end if

                # recompose

                _chunks[-1] = _detail

                _acc = "-".join(_chunks)

            # end if

            # set for keyboard event binding

            self.TK_ACCEL = "<" + _acc + ">"

            # parsed attribute inits

            # caution: do *NOT* set attribute.value = _acc (faulty) /!\

            # caution: *NO* self._tk_config(attribute) by here /!\

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_activeborderwidth (self, attribute, **kw):
        r"""
            width attribute;

            no return value (void);
        """

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_columnbreak (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_hidemargin (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_label (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        self._tkRAD_label_support(attribute, **kw)

    # end def



    def _parse_attr_postcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_tearoff (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_tearoffcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_title (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        self._tkRAD_label_support(attribute, **kw)

    # end def



    def get_menu (self, attr_id):
        r"""
            this method is a coding comfort and shortcut for method
            get_object_by_id();

            returns menu object along @attr_id if object exists;

            returns None otherwise;
        """

        return self.get_object_by_id(attr_id)

    # end def



    def is_menu (self, widget):
        r"""
            determines if object is a tkinter Menu() object;

            returns True on success, False otherwise;
        """

        return isinstance(widget, TK.Menu)

    # end def



    def is_menu_handler (self, widget):
        r"""
            determines if object is a tkinter Menu handler object;

            e.g. a Menu() parent, a Menubutton handler or

            a Tk() toplevel window parent;

            returns True on success, False otherwise;
        """

        return isinstance(

            widget, (TK.Menu, TK.Menubutton, ttk.Menubutton, TK.Tk)
        )

    # end def



    def is_topmenu_handler (self, widget):
        r"""
            determines if object is a tkinter Menu handler object;

            e.g. a Menu() parent, a Menubutton handler or

            a Tk() toplevel window parent;

            returns True on success, False otherwise;
        """

        return isinstance(widget, TK.Tk)

    # end def


# end class RADXMLMenu
