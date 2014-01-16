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

from ..core import tools

from . import rad_xml_widget_base as XW



class RADXMLMenu (XW.RADXMLWidgetBase):
    r"""
        generic XML to tkinter menu builder;

        this is THE tkinter menu MAIN building processor;

        supports all menu / submenu type inclusions;

        supports *direct* access by XML 'id' attribute for root menus

        and for any cascading submenu at any level of inclusion;

        e.g. _menu = self.get_object_by_id('xml_defined_menu_id');

        NO SUPPORT for direct access to menu items such as separators,

        commands, checkbuttons and radiobuttons since tkinter does

        technically *NOT* allow such identification / access;
    """



    # overrides RADXMLWidgetBase.ATTRS

    ATTRS = {

        # $ 2013-12-25 RS $
        # caution: the followings are *MUST HAVE* inits only /!\
        #          declare only the essential                /!\

        "generic": {

            "id": None,

            "name": None,

            "selected": None,

            "checked": None,

        },


        "common": {

            #~ "activebackground": None,

            #~ "activeforeground": None,

            "background": None,

            #~ "font": None,

            "foreground": None,

            #~ "selectcolor": None,
        },


        "menu": {

            #~ "activeborderwidth": None,

            #~ "bd": None,

            "bg": None,

            #~ "borderwidth": None,

            #~ "cursor": None,

            #~ "disabledforeground": None,

            "fg": None,

            "postcommand": None,

            #~ "relief": None,

            "tearoff": 0,

            "tearoffcommand": None,

            "title": None,
        },


        "child": {

            "accelerator": None,

            #~ "bitmap": None,

            #~ "columnbreak": None,

            "command": None,

            #~ "compound": None,

            #~ "hidemargin": None,

            #~ "image": None,

            "label": None,

            #~ "menu": None,

            #~ "offvalue": None,

            #~ "onvalue": None,

            #~ "selectimage": None,

            #~ "state": None,

            "underline": None,

            #~ "value": None,

            #~ "variable": None,
        },

    } # end of ATTRS



    # accepted XML child elements for XML key parent element

    DTD = {

        "menu": (

            "menu", "command", "checkbutton", "radiobutton",

            "separator",
        ),

        "tkmenu": (

            "menu",
        ),

    } # end of DTD



    # tk menu accelerator symbols configuration

    SYMBOLS = (

        (r"\^+|C-|(?i)co?n?tro?l", r"Control-"),
        (r"M-|(?i)meta|(?i)alt", r"Alt-"),
        (r"(?i)shi?ft", r"Shift-"),
        (r"\+$", r"plus"),
        (r"\-$", r"minus"),
        (r"\*$", r"asterisk"),
        (r"\/$", r"slash"),
        (r"\.$", r"period"),
        (r"\,$", r"comma"),
        (r"\:$", r"colon"),
        (r"\;$", r"semicolon"),
        (r"\?$", r"question"),
        (r"\!$", r"exclam"),
        (r"\$$", r"dollar"),
        (r"\%$", r"percent"),
        (r"\@$", r"at"),
        (r"\&$", r"ampersand"),
        (r"\#$", r"numbersign"),
        (r"\_$", r"underscore"),
        (r"(?i)less|(?i)\blt\b", r"less"),
        (r"(?i)greater|(?i)\bgt\b", r"greater"),
        (r"(?i)spa?ce?", r"space"),
        (r"(?i)ba?ckspa?ce?", r"BackSpace"),
        (r"(?i)del(?:ete)?\b", r"Delete"),
        (r"(?i)bre?a?k|(?i)ca?nce?l", r"Cancel"),
        (r"(?i)esc(?:ape)?\b", r"Escape"),
        (r"(?i)tab(?:ulate)?", r"Tab"),
        (r"(?i)ho?me?", r"Home"),
        (r"(?i)end", r"End"),
        (r"(?i)page[\s\+\-]*?up", r"Prior"),
        (r"(?i)page[\s\+\-]*?do?w?n", r"Next"),
        (r"(?i)(?:arrow)?[\s\+\-]*?up", r"Up"),
        (r"(?i)(?:arrow)?[\s\+\-]*?do?w?n", r"Down"),
        (r"(?i)(?:arrow)?[\s\+\-]*?left", r"Left"),
        (r"(?i)(?:arrow)?[\s\+\-]*?right", r"Right"),
        (r"(?i)f(\d+)$", r"F\1"),                          # F1~F12 keys
        (r"[<>]+", r""),                          # "<Ctrl><Z>" notation
        (r"^\W+|\W+$", r""),
        (r"\W+", r"-"),

    ) # end of SYMBOLS



    # overrides RADXMLBase.XML_RC

    XML_RC = {

        "dir": "^/xml/menu",

        "file_ext": ".xml",

    } # end of XML_RC



    # ------------------  XML elements building  -----------------------



    def _build_menu_item (self, xml_tag, xml_element, tk_parent):
        r"""
            protected method def;

            builds a menu item of given type;

            return True on success, False otherwise;
        """

        # param controls

        if not self.is_menu(tk_parent):

            # unsupported

            raise TypeError(

                _(
                    "Menu item '{menu_item}' is only insertable "

                    "into tkinter Menu() object, not in {obj_type}."

                ).format(

                    menu_item = xml_tag, obj_type = repr(tk_parent)
                )
            )

            return False

        # end if

        # go straight

        if xml_tag == "separator":

            # set widget

            tk_parent.add_separator()

        else:

            # prepare child options

            _coptions = self._init_coptions(xml_element, tk_parent)

            # is checkbutton/radiobutton set up by default?

            if _coptions.get("checked") or _coptions.get("selected"):

                _coptions.get("variable").set(

                    tools.choose_str(

                        _coptions.get("onvalue"),

                        _coptions.get("value"),
                    )
                )

            # end if

            # set widget

            tk_parent.add(xml_tag, **_coptions)

        # end if

        # succeeded

        return True

    # end def



    def _init_coptions (self, xml_element, tk_parent):
        r"""
            protected method def;

            prepares menu item child options (coptions);

            returns parsed and cleaned up coptions;
        """

        # shallow copy inits

        _coptions = self.ATTRS["child"].copy()

        # update with "generic"

        _coptions.update(self.ATTRS["generic"])

        # override (key/value) pairs

        _coptions.update(xml_element.attrib)

        # strip unwanted XML attributes

        _coptions = self.delete_dict_items(

            _coptions, *self.ATTRS["menu"].keys()
        )

        # parse XML attributes

        _coptions = self.parse_xml_attributes(

            xml_element, tk_parent, xml_attrs = _coptions
        )

        # attr inits

        _acc = self.TK_ACCEL

        _cmd = _coptions.get("command")

        # keyboard shortcuts event binding

        if tools.is_pstr(_acc) and callable(_cmd):

            self.tk_owner.bind_all(_acc, _cmd)

        # end if

        # strip unsupported XML attributes

        return self.delete_dict_items(

            _coptions, *self.ATTRS["generic"].keys()
        )

    # end def



    def _init_moptions (self, xml_element, tk_parent):
        r"""
            protected method def;

            prepares menu widget options (moptions);

            returns parsed and cleaned up moptions;
        """

        # shallow copy inits

        _moptions = self.ATTRS["menu"].copy()

        # update with "generic"

        _moptions.update(self.ATTRS["generic"])

        # override XML attribute (key/value) pairs

        _moptions.update(xml_element.attrib)

        # strip unwanted XML attributes

        _moptions = self.delete_dict_items(

            _moptions, *self.ATTRS["child"].keys()
        )

        # parse XML attributes

        _moptions = self.parse_xml_attributes(

            xml_element, tk_parent, xml_attrs = _moptions
        )

        # strip unsupported XML attributes

        return self.delete_dict_items(

            _moptions, *self.ATTRS["generic"].keys()
        )

    # end def



    def build_element_checkbutton (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a menu item of type 'checkbutton' (single choice);

            return True on success, False otherwise;
        """

        return self._build_menu_item(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_command (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a menu item of type 'command' (action);

            return True on success, False otherwise;
        """

        return self._build_menu_item(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_menu (self, xml_tag, xml_element, tk_parent):
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

        _moptions = self._init_moptions(xml_element, tk_parent)

        # child menu inits

        _new_menu = TK.Menu(tk_parent, **_moptions)

        # keep a copy aboard

        self.register_object_by_id(_new_menu, xml_element.get("id"))

        # prepare child options

        _coptions = self._init_coptions(xml_element, tk_parent)

        # make some operations on child options

        _coptions["menu"] = _new_menu

        # set widget

        tk_parent.add_cascade(**_coptions)

        # free useless memory right now /!\

        del _moptions, _coptions

        # loop on XML element children - build tk child widgets

        return self.loop_on_children(

            xml_element, _new_menu, accept = self.DTD.get(xml_tag)
        )

    # end def



    def build_element_radiobutton (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a menu item of type 'radiobutton' (group choice);

            return True on success, False otherwise;
        """

        return self._build_menu_item(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_separator (self, xml_tag, xml_element, tk_parent):
        r"""
            builds a menu separator item;

            return True on success, False otherwise;
        """

        return self._build_menu_item(xml_tag, xml_element, tk_parent)

    # end def



    def build_element_tkmenu (self, xml_tag, xml_element, tk_parent):
        r"""
            <tkmenu> is the root node of XML tree;

            its purpose is to get a clean attachment to tk widget

            owner;

            <tkmenu> becomes a tkinter.Menu() object in fact;

            return True on build success, False otherwise;
        """

        # param controls

        if not self.is_menu_handler(tk_parent):

            # set app's root Tk() object instead /!\

            # caution: winfo_toplevel() is *NOT* a Toplevel() object /!\

            tk_parent = self.tk_owner.winfo_toplevel()

        # end if

        # default inits

        _moptions = self._init_moptions(xml_element, tk_parent)

        # menu inits

        _new_menu = TK.Menu(tk_parent, **_moptions)

        # keep a copy aboard

        self.register_object_by_id(_new_menu, xml_element.get("id"))

        # attach new menu to parent widget

        tk_parent["menu"] = _new_menu

        # free useless memory right now /!\

        del _moptions

        # loop on XML element children

        if self.is_topmenu_handler(tk_parent):

            _dtd = "tkmenu"

        else:

            _dtd = "menu"

        # end if

        return self.loop_on_children(

            xml_element, _new_menu, accept = self.DTD.get(_dtd)
        )

    # end def



    def is_menu (self, widget):
        r"""
            determines if object is a tkinter Menu() object;

            return True on success, False otherwise;
        """

        return isinstance(widget, TK.Menu)

    # end def



    def is_menu_handler (self, widget):
        r"""
            determines if object is a tkinter Menu handler object;

            e.g. a Menu() parent, a Menubutton handler or

            a Tk() toplevel window parent;

            return True on success, False otherwise;
        """

        return isinstance(widget, (TK.Menu, TK.Menubutton, TK.Tk))

    # end def



    def is_topmenu_handler (self, widget):
        r"""
            determines if object is a tkinter Menu handler object;

            e.g. a Menu() parent, a Menubutton handler or

            a Tk() toplevel window parent;

            return True on success, False otherwise;
        """

        return isinstance(widget, TK.Tk)

    # end def



    # -----------------------  XML attributes parsing  -----------------



    def parse_attr_accelerator (self, attribute, **kw):
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

                _acc = re.sub(_search, _replace, _acc)

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



    def parse_attr_activeborderwidth (self, attribute, **kw):
        r"""
            width attribute;

            no return value (void);
        """

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def parse_attr_columnbreak (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_hidemargin (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_label (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        self._tkRAD_label_support(attribute, **kw)

    # end def



    def parse_attr_postcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def parse_attr_tearoff (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def parse_attr_tearoffcommand (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def parse_attr_title (self, attribute, **kw):
        r"""
            label attribute;

            no return value (void);
        """

        self._tkRAD_label_support(attribute, **kw)

    # end def


# end class RADXMLMenu
