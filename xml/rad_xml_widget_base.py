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



    # XML attribute parser method pattern

    # overrides RADXMLBase.ATTRIBUTE_PARSER

    ATTRIBUTE_PARSER = "_parse_attr_{xml_attribute}"



    ATTRS = {

        "common": {

            "id": None,

            "name": None,

            "widget": None,

        },

    } # end of ATTRS



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

        self.TK_CHILD_CONFIG = dict()

    # end def



    def _fix_values (self, attribute, default, values, **kw):
        r"""
            protected method def;

            selects values along fixed list of values;

            no return value (void);
        """

        # param controls

        if values and self._is_new(attribute):

            # inits

            _value = attribute.value.lower()

            if _value not in values:

                _value = default

            # end if

            # parsed attribute inits

            attribute.value = _value

            # XML element must have the same attr value

            attribute.update_xml_element()

            self._tk_config(attribute, **kw)

        # end if

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



    def _is_unparsed (self, attribute):
        r"""
            protected method def;

            determines if @attribute has never been parsed;
        """

        return attribute and not attribute.parsed

    # end def



    # -----------------------  XML attributes parsing  -----------------



    def _parse_attr_activebackground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_activeforeground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_background (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_bd (self, attribute, **kw):
        r"""
            width attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_bg (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_bitmap (self, attribute, **kw):
        r"""
            bitmap attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_bitmap_support(attribute, **kw)

    # end def



    def _parse_attr_borderwidth (self, attribute, **kw):
        r"""
            width attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_dimension_support(attribute, **kw)

    # end def



    def _parse_attr_checked (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_command (self, attribute, **kw):
        r"""
            command attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_command_support(attribute, **kw)

    # end def



    def _parse_attr_compound (self, attribute, xml_tag, **kw):
        r"""
            must be one of 'top', 'bottom', 'left', 'right',
            'center', 'none';

            default value is 'none';

            no return value (void);
        """

        _values = ("top", "bottom", "left", "right", "center")

        if tools.is_pstr(xml_tag) and xml_tag.startswith("ttk"):

            _values += ("image", "text")

        # end if

        # parsed attribute inits

        kw.update(

            default = "none",

            values = _values,
        )

        self._fix_values(attribute, **kw)

    # end def



    def _parse_attr_cursor (self, attribute, **kw):
        r"""
            cursor attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_cursor_support(attribute, **kw)

    # end def



    def _parse_attr_disabledforeground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_fg (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_font (self, attribute, **kw):
        r"""
            font attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_font_support(attribute, **kw)

    # end def



    def _parse_attr_foreground (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_id (self, attribute, **kw):
        r"""
            id - generic XML attribute;

            sets an element attr 'id' for *any* element in XML file;

            returns user-defined id or numbered name 'objectxxx' if
            not defined in XML file;

            resets XML element's id to a correct id name, if necessary;

            no return value (void);
        """

        # caution: *NOT* the same as self._is_new(attribute) /!\

        if self._is_unparsed(attribute):

            # parsed attribute inits

            attribute.value = (

                self.element_get_id(attribute.xml_element)
            )

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_image (self, attribute, **kw):
        r"""
            image attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_image_support(attribute, **kw)

    # end def



    def _parse_attr_menu (self, attribute, **kw):
        r"""
            this should always be None as tkRAD manages it on its own;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = None

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _parse_attr_name (self, attribute, **kw):
        r"""
            name - generic XML attribute;

            sets a class member variable name to handle;

            sets parsed XML 'id' instead, if omitted;

            no return value (void);
        """

        # caution: *NOT* the same as self._is_new(attribute) /!\

        if self._is_unparsed(attribute):

            # param inits

            _name = tools.choose_str(

                tools.normalize_id(attribute.value),

                self.element_get_id(attribute.xml_element),
            )

            # parsed attribute inits

            attribute.value = _name #.lower()

            attribute.parsed = True

        # end if

    # end def



    def _parse_attr_offvalue (self, attribute, **kw):
        r"""
            value attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def _parse_attr_onvalue (self, attribute, **kw):
        r"""
            value attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def _parse_attr_relief (self, attribute, **kw):
        r"""
            relief attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_relief_support(attribute, **kw)

    # end def



    def _parse_attr_selectcolor (self, attribute, **kw):
        r"""
            color attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_color_support(attribute, **kw)

    # end def



    def _parse_attr_selected (self, attribute, **kw):
        r"""
            boolean attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_boolean_support(attribute, **kw)

    # end def



    def _parse_attr_selectimage (self, attribute, **kw):
        r"""
            image attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_image_support(attribute, **kw)

    # end def



    def _parse_attr_state (self, attribute, **kw):
        r"""
            state attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_state_support(attribute, **kw)

    # end def



    def _parse_attr_underline (self, attribute, **kw):
        r"""
            resets underline value to 0 if not an integer value;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_integer_support(attribute, **kw)

    # end def



    def _parse_attr_value (self, attribute, **kw):
        r"""
            value attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def _parse_attr_variable (self, attribute, **kw):
        r"""
            control variable attribute;

            no return value (void);
        """

        # parsed attribute inits

        self._tkRAD_cvar_support(attribute, **kw)

    # end def



    def _parse_attr_widget (self, attribute, **kw):
        r"""
            widget attribute;

            no return value (void);
        """

        # parsed attribute inits

        kw.update(no_tk_config = True)

        self._tkRAD_widget_support(attribute, **kw)

    # end def



    def _tkRAD_any_value_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for any value attrs;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _tkRAD_bitmap_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for bitmap attrs;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = self.get_bitmap_path(attribute.value)

            self._tk_config(attribute)

        # end if

    # end def



    def _tkRAD_boolean_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for boolean attrs;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = bool(

                attribute.value.lower()

                in ("1", "yes", "true", attribute.name)
            )

            # XML element must have the same attr value

            attribute.update_xml_element()

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _tkRAD_color_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for color attrs;

            no return value (void);
        """

        # FIXME: should implement something here?

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def _tkRAD_command_support (self, attribute, **kw):
        r"""
            parses command string for many supports;
            supports event names (starting with '@');
            supports method names (starting with '^' or '.');
            supports global function names;
            no return value (void);
        """

        # $ 2014-03-10 RS $
        # since v1.4: deferred tasks
        # any *command XML attrs are deferred to after widget's
        # creation;
        # now supports widget in **kw;

        self._queue.defer(

            "widget",

            self._tkRAD_deferred_command_support,

            attribute,

            **kw
        )

    # end def



    def _tkRAD_cursor_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for color attrs;

            no return value (void);
        """

        # FIXME: should implement something here?

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def _tkRAD_cvar_support (self, attribute, **kw):
        r"""
            sets a tkinter StringVar() control variable;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = self.set_stringvar(attribute.value)

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _tkRAD_deferred_command_support (self, attribute, *args, **kw):
        r"""
            parses command string for many supports;

            supports event names (starting with '@');

            supports method names (starting with '^' or '.');

            supports global function names;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # strip erroneous parenthesis
            # and args in command string
            # e.g. "slot_move(3)" --> "slot_move"

            _cmd = re.sub(r"\(.*\)", r"", attribute.value)

            # $ 2014-03-10 RS $
            # since v1.4: deferred task
            # now widget is passed in callback **kw

            _widget = kw.get("widget")

            # action trigger template

            def _trigger (*args, callback=None, widget=_widget, **kw):

                return (

                    lambda *args, _a=args, _cb=callback,
                                                    _w=widget, _kw=kw:

                        _cb(*(args + _a), widget=_w, **_kw)
                )

            # end def

            # events maechanism support

            if _cmd.startswith("@"):

                # e.g. "@MyNewEvent" --> raise_event("MyNewEvent")

                _cmd = _trigger(

                    _cmd[1:],

                    callback = self.events.raise_event,
                )

            # self.app methods support

            elif _cmd.startswith("^") and hasattr(self, "app"):

                # reset value

                _cmd = _cmd.lstrip("^.@")

                if hasattr(self.app, _cmd):

                    # e.g. "^quit" --> self.app.quit

                    _cmd = _trigger(

                        callback = getattr(self.app, _cmd),
                    )

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

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _tkRAD_dimension_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for dimension attrs;

            no return value (void);
        """

        # FIXME: should implement something here?

        self._tkRAD_any_value_support(attribute, **kw)

    # end def



    def _tkRAD_float_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for float attrs;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = tools.ensure_float(attribute.value)

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _tkRAD_font_support (self, attribute, **kw):
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

            # catches 'quoted long names'

            _sch = re.compile(r"'(.*?)'")

            _family = _sch.search(_font)

            # resets font family name to tkinter-compliant font name

            # e.g. "'Times New Roman'" ---> "timesnewroman"

            if _family:

                _font = _sch.sub(

                    tools.normalize_id(_family.group(1)).lower(),

                    _font
                )

            # end if

            # parsed attribute inits

            attribute.value = _font

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _tkRAD_image_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for image attrs;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = self.set_image(attribute.value)

            self._tk_config(attribute)

        # end if

    # end def



    def _tkRAD_integer_support (self, attribute, **kw):
        r"""
            protected method def;

            generic support for integer attrs;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # parsed attribute inits

            attribute.value = tools.ensure_int(attribute.value)

            self._tk_config(attribute, **kw)

        # end if

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

                # $ 2014-01-15 RS $
                # deeper attr support:
                # extract RADXMLAttribute item
                # from RADXMLAttributesDict

                _attr_underline = attrs.get_item("underline")

                # menu label underline support (e.g. "_File")

                _attr_underline.value = -1

                _pos = _label.find("_")

                if _pos >= 0:

                    # set attribute value

                    _attr_underline.value = _pos

                    # update label

                    _label = _label[:_pos] + _label[_pos+1:]

                # end if

                # parsed attribute inits

                self._tk_config(_attr_underline, **kw)

            # end if

            # parsed attribute inits

            attribute.value = _label

            self._tk_config(attribute, **kw)

        # end if

    # end def



    def _tkRAD_relief_support (self, attribute, **kw):
        r"""
            must be one of 'flat', 'raised', 'sunken', 'groove',
            'ridge';

            default value will be 'flat';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "flat",

            values = ("raised", "sunken", "groove", "ridge", "solid"),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _tkRAD_state_support (self, attribute, **kw):
        r"""
            must be one of 'normal' or 'disabled';

            default value is 'normal';

            no return value (void);
        """

        # parsed attribute inits

        kw.update(

            default = "normal",

            values = ("disabled", ),
        )

        self._fix_values(attribute, **kw)

    # end def



    def _tkRAD_widget_support (self, attribute, **kw):
        r"""
            tries to retrieve a widget along given 'id' value;

            no return value (void);
        """

        # param controls

        if self._is_new(attribute):

            # widget id inits

            _wid = attribute.value

            # what about DEFERRED TASKS? -------------------------------------FIXME

            # got alias name?

            if _wid.startswith("@"):

                # reset value

                _wid = _wid.strip("@").lower()

                # get widget along alias

                _widget = {

                    "top": self.tk_owner.winfo_toplevel(),

                    "parent": kw.get("tk_parent"),

                }.get(_wid)

            else:

                # look for existing widget along attr 'id'

                _widget = self.get_object_by_id(_wid)

            # end if

            if _widget:

                # parsed attribute inits

                attribute.value = _widget

                self._tk_config(attribute, **kw)

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



    def _tk_config (self, attribute, **kw):
        r"""
            protected method def;

            sets up child or widget attribute for tkinter.configure();

            no return value (void);
        """

        # param controls

        if not kw.get("no_tk_config"):

            # $ 2014-01-15 RS $
            # new discriminator support
            # to avoid child / widget
            # attrs conflict in XML script

            _name = attribute.name.lstrip("_")

            # child config asked?

            if kw.get("tk_child_config"):

                # child inits

                self.TK_CHILD_CONFIG[_name] = attribute.value

            else:

                # widget inits

                self.TK_CONFIG[_name] = attribute.value

            # end if

        # end if

        attribute.parsed = True

    # end def


# end class RADXMLWidgetBase
