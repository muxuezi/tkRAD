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



# lib imports

import xml.etree.ElementTree as ET



def reset_attributes (xml_attributes, xml_element = None):
    r"""
        replaces all @xml_attributes dict() items by new

        RADXMLAttribute attributes in a new separate dict() object;

        /!\ keeps @xml_attributes dict() UNTOUCHED /!\

        supports automagic ET.Element attributes handling

        if an XML element is passed along @xml_attributes param;

        raises TypeError if @xml_attributes is definitely *NOT* of

        'dict' type, even after support handling;

        @xml_element param is the official XML parent element of attrs;

        returns dict() of new RADXMLAttribute attributes on success;

        returns None on failure;
    """

    # param controls - XML element attributes support

    if ET.iselement(xml_attributes):

        # should supply an XML parent element?

        if not ET.iselement(xml_element):

            xml_element = xml_attributes

        # end if

        # reset to attributes dict()

        xml_attributes = xml_attributes.attrib

    # end if

    # got a dict() object?

    if isinstance(xml_attributes, dict):

        _attrs = xml_attributes.copy()

        for (_name, _value) in _attrs.items():

            if not isinstance(_value, RADXMLAttribute):

                _attrs[_name] = \
                            RADXMLAttribute(xml_element, _name, _value)

            # end if

        # end for

        return _attrs

    else:

        raise TypeError(

            "parameter @xml_attributes must be of 'dict' type."
        )

        return None

    # end if

# end def



class RADXMLAttribute:
    r"""
        generic XML attribute class for parsers;

        handles member @xml_element: pointer to parent XML element;

        handles member @name: char string 'name' of XML attribute;

        handles member @value: pointer to any value of XML attribute;

        handles member @parsed: int counter of parsing notifications;
    """



    def __init__ (self, xml_element, attr_name, attr_value, parsed=0):
        r"""
            class constructor;
        """

        # parent XML element - SHOULD be an ET.Element object (optional)

        self.xml_element = xml_element

        # attribute name - MUST be a plain string of chars

        self.name = attr_name

        # attribute value - can be anything

        self.value = attr_value

        # nb of times this attribute has been parsed

        self.parsed = parsed

    # end def



    # callable getter for e.g. tkRAD.core.StructDict /!\

    def get_value (self):
        r"""
            callable value getter for external dictionaries

            implementing item value override e.g. tkRAD.core.StructDict;
        """

        return self.value

    # end def



    @property
    def name (self):
        r"""
            @property handler for 'name' class member;

            raises TypeError if not set as a PLAIN string of chars;
        """

        return self.__attr_name

    # end def



    @name.setter
    def name (self, value):

        if isinstance(value, str) and value:

            self.__attr_name = value

        else:

            raise TypeError(

                "XML attribute name must be of PLAIN char string type."
            )

        # end if

    # end def



    @name.deleter
    def name (self):

        del self.__attr_name

    # end def



    @property
    def parsed (self):
        r"""
            @property handler for 'parsed' class member;

            resets to 0 if set up with a False boolean expression;

            sets up to integer value with a minimum of 1;

            increments current internal counter index

            if set up with any other non-integer value;
        """

        return self.__attr_parsed

    # end def



    @parsed.setter
    def parsed (self, value):

        # param controls

        if not value:

            self.__attr_parsed = 0

        elif isinstance(value, int):

            # reset to new value with minimum

            self.__attr_parsed = min(1, value)

        else:

            # increment current counter

            self.__attr_parsed += 1

        # end if

    # end def



    @parsed.deleter
    def parsed (self):

        del self.__attr_parsed

    # end def



    # callable setter for e.g. tkRAD.core.StructDict /!\

    def set_value (self, value):
        r"""
            callable value setter for external dictionaries

            implementing item value override e.g. tkRAD.core.StructDict;

            no return value (void);
        """

        self.value = value

    # end def



    def update_xml_element (self, value = None):
        r"""
            updates inner XML element's attr name along @value param;

            returns True on success, False otherwise;
        """

        # param inits

        if value is None:

            value = self.value

        # end if

        if ET.iselement(self.xml_element):

            # update XML element

            self.xml_element.set(self.name, value)

            # succeeded

            return True

        else:

            raise TypeError(

                "XML element must be of "

                "type '{obj_type}', not '{cur_type}'."

                .format(

                    obj_type = repr(ET.Element),

                    cur_type = repr(self.xml_element),
                )
            )

        # end if

        # failed

        return False

    # end def


# end class RADXMLAttribute
