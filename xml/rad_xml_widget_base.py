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

from . import rad_xml_base as RX



class RADXMLWidgetBase (RX.RADXMLBase):
    r"""
        Base class for XML to tkinter widget building;

        generic XML to widget building processor;

        can be subclassed for more specific types

        e.g. RADXMLWidget and RADXMLMenu;

        see API doc for more detail;
    """



    ANCHORS = (

        (r"(?i)north|top|up", TK.N),
        (r"(?i)south|bottom|down", TK.S),
        (r"(?i)east|right", TK.E),
        (r"(?i)west|left", TK.W),
        (r"\W+", r""),
        (TK.N + "+", TK.N),
        (TK.S + "+", TK.S),
        (TK.E + "+", TK.E),
        (TK.W + "+", TK.W),
        (TK.W + TK.N, TK.NW),
        (TK.E + TK.N, TK.NE),
        (TK.W + TK.S, TK.SW),
        (TK.E + TK.S, TK.SE),
    )



    # XML attribute parser method pattern

    # overrides RADXMLBase.ATTRIBUTE_PARSER

    ATTRIBUTE_PARSER = "parse_attr_{xml_attr}"



    ATTRS = {

        "common": {

            "id": None,

            "name": None,

            "widget": None,

        },

    } # end of ATTRS



    # XML element builder method pattern

    # overrides RADXMLBase.ELEMENT_BUILDER

    ELEMENT_BUILDER = "build_element_{xml_element}"



    # ------------------  XML elements building  -----------------------



    def _before_building_element (self, **kw):
        r"""
            virtual method inherited from RADXMLBase;

            allows some inits before starting an

            XML element widget building;
        """

        # widget inits

        self.WIDGET_CLASS = "Frame"

        self.WIDGET = None

        self.TK_ACCEL = ""

        self.TK_CONFIG = dict()

    # end def



    def _is_new (self, attribute):
        r"""
            protected method def;

            determines if @attribute has never been parsed and if its

            value is of plain char string type, which is the typical

            case of a newly unparsed true XML attribute;
        """

        return attribute and not attribute.parsed and \
                                        tools.is_pstr(attribute.value)

    # end def



    def _tkRAD_label_support (self, attribute, attrs, **kw):
        r"""
            protected method def;

            generic support for underlined text and label attrs;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # internationalization (i18n) translations support

            _label = _(attribute.value)

            # got XML attr 'underline'?

            if "underline" in attrs:

                # menu label underline support (e.g. "_File")

                attrs["underline"] = None

                _pos = _label.find("_")

                if _pos >= 0:

                    # set attribute value

                    attrs["underline"] = _pos

                    # update label

                    _label = _label[:_pos] + _label[_pos+1:]

                # end if

                # parsed attribute inits

                self.TK_CONFIG["underline"] = attrs["underline"]

            # end if

            # parsed attribute inits

            attribute.value = _label

            self._tk_config(attribute)

        # end if

    # end def



    def _tk_config (self, attribute):
        r"""
            protected method def;

            sets up self.TK_CONFIG along RADXMLAttribute attribute;

            no return value (void);
        """

        self.TK_CONFIG[attribute.name] = attribute.value

        attribute.parsed = True

    # end def



    # -----------------------  XML attributes parsing  -----------------



    def parse_attr_activebackground (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_activeforeground (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_background (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_bd (self, attribute, attrs, **kw):
        r"""
            alias for XML attribute 'borderwidth';

            no return value (void);
        """

        # alias for 'borderwidth'

        self.parse_attr_borderwidth(attribute, attrs, **kw)

    # end def



    def parse_attr_bg (self, attribute, attrs, **kw):
        r"""
            alias for XML attribute 'background';

            no return value (void);
        """

        # alias for 'background'

        self.parse_attr_background(attribute, attrs, **kw)

    # end def



    def parse_attr_bitmap (self, attribute, attrs, **kw):
        r"""
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_bitmap(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_borderwidth (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_checked (self, attribute, attrs, **kw):
        r"""
            XML attr 'checked' must be 'checked="checked"' or will
            be reset to None;

            no return value (void);
        """

        if not attribute.parsed:

            if str(attribute.value) != "checked":

                attribute.value = None

            # end if

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_command (self, attribute, attrs, **kw):
        r"""
            parses any '.*command' XML attribute for many supports;

            @value supports event names (starting with '@');

            @value supports method names (starting with '^' or '.');

            @value supports global function names;

            each time it is possible, attr 'command' becomes the event,

            the method or the function direct callback pointer;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # strip erroneous parenthesis

            # and args in command string

            # e.g. "slot_move(3)" --> "slot_move"

            _cmd = re.sub(r"\(.*\)", r"", attribute.value)

            # events maechanism support

            if _cmd.startswith("@"):

                # e.g. "@MyNewEvent" --> raise_event("MyNewEvent")

                _cmd = (

                    lambda tk1=None, tk2=None,
                            s=self.events, e=_cmd[1:]:

                        s.raise_event(e)
                )

            # self.app methods support

            elif _cmd.startswith("^") and hasattr(self, "app"):

                # reset value

                _cmd = _cmd.lstrip("^.@")

                if hasattr(self.app, _cmd):

                    # e.g. "^quit" --> self.app.quit

                    _cmd = getattr(self.app, _cmd)

                else:

                    raise AttributeError(

                        _(
                            "Cannot link command '{cmd}' to "

                            "'{app}' (self.app) "

                            "- bad XML attribute "

                            "or incorrect self.app"

                        ).format(cmd = _cmd, app = repr(self.app))
                    )

                    # cancel command

                    _cmd = None

                # end if

            # self.tk_owner methods support

            elif _cmd.startswith(".") and hasattr(self, "tk_owner"):

                # reset value

                _cmd = _cmd.lstrip(".^@")

                if hasattr(self.tk_owner, _cmd):

                    # e.g. ".quit" --> self.tk_owner.quit

                    _cmd = getattr(self.tk_owner, _cmd)

                else:

                    raise AttributeError(

                        _(
                            "Cannot link command '{cmd}' to "

                            "'{tkowner}' (self.tk_owner) "

                            "- bad XML attribute "

                            "or incorrect self.tk_owner"

                        ).format(

                            cmd = _cmd, tkowner = repr(self.tk_owner)
                        )
                    )

                    # cancel command

                    _cmd = None

                # end if

            # global methods support

            else:

                # pray for value being a global method!

                _cmd = eval(_cmd)

            # end if

            # parsed attribute inits

            attribute.value = _cmd

            self._tk_config(attribute)

        # end if

    # end def



    def parse_attr_compound (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_cursor (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_disabledforeground (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_fg (self, attribute, attrs, **kw):
        r"""
            alias for XML attribute 'foreground';

            no return value (void);
        """

        # alias for 'foreground'

        self.parse_attr_foreground(attribute, attrs, **kw)

    # end def



    def parse_attr_font (self, attribute, attrs, **kw):
        r"""
            translates XML attribute to tkinter attribute;

            syntax is: font="family size bold italic";

            @family can either be a single name e.g. font="serif"

            or a quoted long name e.g. font="'Times New Roman'";

            notice: quoted long names are CASE-INSENSITIVE /!\

            @size *MUST* be an integer value (optional value);

            @bold is either 'bold' string or '' (optional value);

            @italic is either 'italic' string or '' (optional value);

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # inits

            _font = attribute.value

            _sch = r"'([^']+)'"         # catches 'quoted long names'

            _family = re.search(_sch, _font)

            # resets font family name to tkinter-compliant font name

            # e.g. "'Times New Roman'" ---> "timesnewroman"

            if _family:

                _font = re.sub(

                    _sch,

                    tools.canonize_id(_family.group(1)).lower(),

                    _font
                )

            # end if

            # parsed attribute inits

            attribute.value = _font

            self._tk_config(attribute)

        # end if

    # end def



    def parse_attr_foreground (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_id (self, attribute, attrs, **kw):
        r"""
            id - generic XML attribute;

            sets an element attr 'id' for *any* element in XML file;

            returns user-defined id or numbered name 'objectxxx'

            if not defined in XML file;

            resets XML element's id to a correct id name, if necessary;

            no return value (void);
        """

        # caution: *NOT* the same as self._is_new(attribute) /!\

        if not attribute.parsed:

            # parsed attribute inits

            attribute.value = self.get_correct_id(attribute.value)

            # parent XML element must have the same id value /!\

            attribute.xml_element.set("id", attribute.value)

            # this attr may be internally called by other parsers /!\

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_image (self, attribute, attrs, **kw):
        r"""
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_image(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_menu (self, attribute, attrs, **kw):
        r"""
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_menu(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_name (self, attribute, attrs, **kw):
        r"""
            name - generic XML attribute;

            sets a class member variable name to handle;

            sets parsed XML 'id' instead if not defined in XML file;

            no return value (void);
        """

        # caution: *NOT* the same as self._is_new(attribute) /!\

        if not attribute.parsed:

            # param inits

            _name = tools.canonize_id(attribute.value)

            # no value?

            if not tools.is_pstr(_name):
                r"""
                    $ 2013-12-18 RS $
                    new support: attrs = RADXMLAttributesDict by now;
                """

                # try to get something from attr 'id'

                self.parse_attr_id(attrs.get_item("id"), attrs, **kw)

                # new value inits

                _name = self.get_correct_id(attrs.get("id"))

            # end if

            # parsed attribute inits

            attribute.value = _name.lower()

            # this attr may be internally called by other parsers /!\

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_offvalue (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_onvalue (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_relief (self, attribute, attrs, **kw):
        r"""
            attr 'relief' must be one of 'flat', 'raised', 'sunken',
            'groove', 'ridge';

            default value will be 'flat';

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # inits

            _relief = attribute.value.lower()

            if _relief not in ("raised", "sunken", "groove", "ridge",
            "solid"):

                _relief = "flat"

            # end if

            # parsed attribute inits

            attribute.value = _relief

            self._tk_config(attribute)

        # end if

    # end def



    def parse_attr_selectcolor (self, attribute, attrs, **kw):
        r"""
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_selectcolor(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_selected (self, attribute, attrs, **kw):
        r"""
            XML attr 'selected' must be 'selected="selected"' or will
            be reset to None;

            no return value (void);
        """

        if not attribute.parsed:

            if str(attribute.value) != "selected":

                attribute.value = None

            # end if

            attribute.parsed = True

        # end if

    # end def



    def parse_attr_selectimage (self, attribute, attrs, **kw):
        r"""
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_selectimage(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_state (self, attribute, attrs, **kw):
        r"""
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_state(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_underline (self, attribute, attrs, **kw):
        r"""
            resets underline value to 0 if not an integer value;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = tools.ensure_int(attribute.value)

            self._tk_config(attribute)

        # end if

    # end def



    def parse_attr_value (self, attribute, attrs, **kw):
        r"""
            direct XML attribute to tkinter attribute translation;

            no return value (void);
        """

        # parsed attribute inits

        self._tk_config(attribute)

    # end def



    def parse_attr_variable (self, attribute, attrs, **kw):
        r"""
            sets a tkinter StringVar();

            if Radiobutton or Checkbutton objects are linked to this

            control variable and are selected / checked by default,

            the StringVar resets to their value / onvalue on-the-fly;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):
            r"""
                $ 2013-12-18 RS $
                new support: attrs = RADXMLAttributesDict by now;
            """

            # efficient memory inits

            _cvar = self.set_stringvar(attribute.value)

            # is checkbutton/radiobutton

            # checked/selected by default?

            if tools.choose_str(

                attrs.get("checked"), attrs.get("selected")
            ):

                _cvar.set(

                    tools.choose_str(

                        attrs.get("onvalue"), attrs.get("value")
                    )
                )

            # end if

            # parsed attribute inits

            attribute.value = _cvar

            self._tk_config(attribute)

        # end if

    # end def



    def parse_attr_widget (self, attribute, attrs, **kw):
        r"""
            XML attribute 'widget' refers to <widget> attr 'id';

            tries to retrieve existing object with 'id' identity;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # look for existing widget along attr 'id'

            _widget = self.get_object_by_id(attribute.value)

            if _widget:

                # parsed attribute inits

                attribute.value = _widget

                # caution: *NO* self._tk_config(attribute) by here /!\

            # not found

            else:

                raise KeyError(

                    _(
                        "Widget of id '{w_id}' does not exist or "
                        "has not been registered yet."

                    ).format(w_id = attribute.value)
                )

            # end if

        # end if

    # end def


# end class RADXMLWidgetBase
