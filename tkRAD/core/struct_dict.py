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



class StructDict (dict):
    r"""
        generic 'class structure' dictionary;

        supports item value get / set overrides;

        items should be of same 'class structure' type;
    """



    def __getitem__ (self, key):
        r"""
            item value getter;

            overrides to item.getter() if @key exists and is

            of item type;

            behaves as dict() otherwise i.e. returns dict[@key];
        """

        _item = super().__getitem__(key)

        if isinstance(_item, self.item_type):

            return getattr(_item, self.item_value_getter)()

        else:

            return _item

        # end if

    # end def



    def __init__ (self, *args, **kw):
        r"""
            class constructor;

            implements @item_type class member:

            dict item 'class type' for item value override support;

            implements @item_value_getter class member:

            name of item class method for getting internal value;

            default name value is "get_value";

            implements @item_value_setter class member:

            name of item class method for setting internal value;

            default name value is "set_value";
        """

        # super class inits

        super().__init__(*args, **kw)

        # member inits

        self.item_type = None

        self.item_value_getter = "get_value"

        self.item_value_setter = "set_value"

    # end def



    def __setitem__ (self, key, value):
        r"""
            item value setter;

            overrides to item.setter(@value) if @key exists and is

            of 'item type' type;

            behaves as dict() otherwise i.e. dict[@key] = @value;
        """

        _item = super().get(key)

        if isinstance(_item, self.item_type):

            getattr(_item, self.item_value_setter)(value)

        else:

            super().__setitem__(key, value)

        # end if

    # end def



    def flatten (self):
        r"""
            returns a new dict() of item.value instead of item itself;

            this provides a "flat" dict of (key, value) pairs;

            keeps current items() UNTOUCHED;
        """

        # inits

        _dict = dict()

        # loop on items

        for _key in self.keys():

            # flattens item to its value

            _dict[_key] = self.get(_key)

        # end for

        # return new dict() object

        return _dict

    # end def



    def get (self, key, default = None):
        r"""
            item value getter;

            overrides to item.getter() if @key exists and

            is of 'item type' type;

            behaves as dict() otherwise i.e. dict.get(@key, @default);
        """

        _item = super().get(key, default)

        if isinstance(_item, self.item_type):

            return getattr(_item, self.item_value_getter)()

        else:

            return _item

        # end if

    # end def



    def get_item (self, key, default = None):
        r"""
            returns dict item along @key no matter what it is like;

            returns @default if @key does not exist in dict;

            same as dict.get(@key, @default);
        """

        return super().get(key, default)

    # end def



    def get_value (self, key, default = None):
        r"""
            alias method name for .get(...);

            defined only for commodity and for code readability;
        """

        return self.get(key, default)

    # end def



    @property
    def item_value_getter (self):
        r"""
            @property handler for 'item value getter' class member;

            'item value getter' MUST be of plain string type;

            raises TypeError otherwise;
        """

        return self.__item_value_getter

    # end def



    @item_value_getter.setter
    def item_value_getter (self, getter):

        if getter and isinstance(getter, str):

            self.__item_value_getter = getter

        else:

            raise TypeError(

                "item value getter must be of PLAIN char string type."
            )

        # end if

    # end def



    @item_value_getter.deleter
    def item_value_getter (self):

        del self.__item_value_getter

    # end def



    @property
    def item_value_setter (self):
        r"""
            @property handler for 'item value setter' class member;

            'item value setter' MUST be of plain string type;

            raises TypeError otherwise;
        """

        return self.__item_value_setter

    # end def



    @item_value_setter.setter
    def item_value_setter (self, setter):

        if setter and isinstance(setter, str):

            self.__item_value_setter = setter

        else:

            raise TypeError(

                "item value setter must be of PLAIN char string type."
            )

        # end if

    # end def



    @item_value_setter.deleter
    def item_value_setter (self):

        del self.__item_value_setter

    # end def



    def set (self, key, value):
        r"""
            'item value' setter;

            overrides to item.setter(@value) if @key exists and is

            of 'item type' type;

            behaves as dict() otherwise i.e. dict[@key] = @value;
        """

        self.__setitem__(key, value)

    # end def



    def set_item (self, key, value):
        r"""
            real dict item setter;

            sets dict[@key] = @value no matter what it is like;
        """

        super().__setitem__(key, value)

    # end def



    def set_value (self, key, value):
        r"""
            alias method name for .set(...);

            defined only for commodity and for code readability;
        """

        self.set(key, value)

    # end def


# end class StructDict
