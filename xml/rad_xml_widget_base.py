#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    TkRAD - Tkinter Rapid Application Development

    (c) 2013 Raphaël SEBAN <motus@laposte.net>

    released under Creative Commons BY-SA 3.0

    see http://creativecommons.org/licenses/by-sa/3.0/
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

        return not attribute.parsed and tools.is_pstr(attribute.value)

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
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_checked(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        pass

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

                    lambda tk_evt=None, s=self.events, e=_cmd[1:]:

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
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_relief(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        self._tk_config(attribute)

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
            << NOT IMPLEMENTED YET >>

            no return value (void);
        """

        # ---------------------------------------------------------------FIXME
        print("[WARNING] parse_attr_selected(): NOT IMPLEMENTED YET")

        # parsed attribute inits

        pass

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

            attribute.parsed = True

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

            # or get 'tk_parent' on failure

            attribute.value = self.get_object_by_id(

                attribute.value, kw["tk_parent"]
            )

        # end if

    # end def


# end class RADXMLWidgetBase
