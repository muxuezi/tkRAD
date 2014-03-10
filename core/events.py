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



# unique instance pointer

# module private var init

__event_manager = None



# service getter

def get_event_manager ():
    r"""
        gets a unique application-wide instance of the event manager;

        always return the event manager unique instance pointer;
    """

    global __event_manager

    if not isinstance(__event_manager, EventManager):

        __event_manager = EventManager()

    # end if

    return __event_manager

# end def



class EventManager:
    r"""
        /!\ this module is *STANDALONE* /!\

        you can pick it up *as is* and use it in your own project;

        simplified signal/slot universal event manager;

        examples:

        * if you need a unique *APP-WIDE* instance:

        import tkRAD.core.events as EVENTS

        class MyClass:

            def __init__ (self):

                # member inits

                self.events = EVENTS.get_event_manager()

                # use event manager

                self.events.connect("signal_1", slot1, slot2, slot3)

                self.events.connect_dict(

                    {
                        "signal_1": (slot1, slot2, slot3),      # tuple

                        "signal_2": [slot3, slot4, slot5],      # list

                        "signal_3": set([slot6, slot7, slot8]), # set

                        "signal_4": slot9,          # single callback
                    }
                )

                self.events.disconnect("signal_2", slot4, slot5)

                self.events.disconnect_all("signal_6", "signal_7", )

                self.events.raise_event("MyClassInitialized")

            # end def

        # end class MyClass

        * if you need a *SHARED* instance:

        import tkRAD.core.events as EVENTS

        my_event_manager = EVENTS.EventManager()

        my_object1 = MyClass1()

        my_object1.set_event_manager(my_event_manager)

        my_object2 = MyClass2()

        my_object2.set_event_manager(my_event_manager)

        my_object3 = MyClass3()

        my_object3.set_event_manager(my_event_manager)

        * if you need a *PRIVATE* instance:

        import tkRAD.core.events as EVENTS

        class MyClass:

            def __init__ (self):

                # member inits

                self.events = EVENTS.EventManager()

                # use event manager

                self.events.connect("signal_1", slot1, slot2, slot3)

            # end def

        # end class MyClass

    """



    def __init__ (self):
        r"""
            class constructor - initializes connection hashtable;
        """

        self.connections = dict()

    # end def



    def connect (self, signal, *slots):
        r"""
            connects signal name to multiple callback slots;

            examples:

                self.events.connect("signal_1", slot1)

                self.events.connect("signal_2", slot2, slot3, slot4)

                args = (slot5, slot6, slot7)

                self.events.connect("signal_3", *args)

            returns True on success, False otherwise;
        """

        # get signal current set of slots

        _slots = self.connections.setdefault(signal, set())

        # signal do have a set of slots

        if isinstance(_slots, set):

            # slots must be unique for each signal

            _slots.update(set(slots))

            # update signal set of slots

            self.connections[signal] = set(filter(callable, _slots))

            # operation succeeded

            return True

        # end if

        # operation failed

        return False

    # end def



    def connect_dict (self, events_dict):
        r"""
            connects (signal, slots) pairs in dict() object;

            slots can be a single callback or one of tuple, list, set;

            example:

                self.events.connect_dict(

                    {
                        "signal_1": (slot1, slot2, slot3),      # tuple

                        "signal_2": [slot3, slot4, slot5],      # list

                        "signal_3": set([slot6, slot7, slot8]), # set

                        "signal_4": slot9,          # single callback
                    }
                )

            returns True on success, False otherwise;
        """

        # param controls

        if events_dict and isinstance(events_dict, dict):

            # loop on items

            for (_signal, _slots) in events_dict.items():

                if isinstance(_slots, (tuple, list, set)):

                    self.connect(_signal, *_slots)

                else:

                    self.connect(_signal, _slots)

                # end if

            # end for

            # operation succeeded

            return True

        # unsupported

        else:

            raise TypeError("Expected plain dict() object type.")

        # end if

        # operation failed

        return False

    # end def



    def disconnect (self, signal, *slots):
        r"""
            disconnects list of callback slots from signal name;

            examples:

                self.events.disconnect("signal_1", slot1)

                self.events.disconnect("signal_2", slot2, slot3, slot4)

                args = (slot5, slot6, slot7)

                self.events.disconnect("signal_3", *args)

            returns True if signal exists, False otherwise;
        """

        # get signal current set of slots

        _slots = self.connections.get(signal)

        # signal do exist and has a set of slots

        if _slots and isinstance(_slots, set):

            # remove eventual existing slots

            _slots.difference_update(set(slots))

            # update signal set of slots

            self.connections[signal] = set(filter(callable, _slots))

            # operation succeeded

            return True

        # end if

        # operation failed - unknown signal name

        return False

    # end def



    def disconnect_all (self, *signals):
        r"""
            disconnects all callback slots from each signal listed;

            implicitly removes each useless signal from hashtable;

            examples:

                self.events.disconnect_all("signal_1")

                self.events.disconnect_all("signal_2", "signal_3", ...)

                args = ("signal_5", "signal_6", "signal_7")

                self.events.disconnect_all(*args)

            no return value (void);
        """

        # browse signals list

        for _signal in set(signals):

            # signal is no longer useful

            self.connections.pop(_signal, None)

        # end for

    # end def



    def raise_event (self, signal, *args, **kw):
        r"""
            calls all slots attached to the given signal name

            with eventual arguments and keywords;

            examples:

            self.events.raise_event("ButtonOKClicked")

            self.events.raise_event("ButtonOKClicked", event_object)

            self.events.raise_event(
                "ButtonOKClicked", widget = self.btn_ok
            )

            returns True if signal exists, False otherwise;
        """

        print("signal:", signal, args, kw)

        # get signal current set of slots

        _slots = self.connections.get(signal)

        # signal do exist and has a set of slots

        if _slots and isinstance(_slots, set):

            # keep only callable slots

            _slots = set(filter(callable, _slots))

            # browse the set

            for _slot in _slots:

                # call each slot one by one
                # with arguments and keywords

                _slot(*args, **kw)

            # end for

            # operation succeeded

            return True

        # end if

        # operation failed - unknown signal name

        return False

    # end def


# end class EventManager
