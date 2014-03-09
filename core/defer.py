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

__queue = None



# service getter

def get_deferred_trigger_queue (*args, **kw):
    r"""
        gets a unique application-wide instance of the deferred
        trigger queue;

        always return the queue unique instance pointer;
    """

    global __queue

    if not isinstance(__queue, DeferredTriggerQueue):

        __queue = DeferredTriggerQueue(*args, **kw)

    # end if

    return __queue

# end def



# alias shortcut for get_deferred_trigger_queue()

get_dt_queue = get_deferred_trigger_queue



# class def

class DeferredTriggerQueue:
    r"""
        /!\ this module is *STANDALONE* /!\

        you can pick it up *as is* and use it in your own project;

        Generic Queue for deferred triggers;

    """



    def __init__ (self, *args, **kw):
        r"""
            class constructor inits;
        """

        # member inits

        self.__queue = dict(*args, **kw)

    # end def



    def clear (self):
        r"""
            clears all buffered triggers without calling them as in
            flush() or flush_all();

            no return value (void);
        """

        # clear all in queue

        self.__queue.clear()

    # end def



    def defer (self, section, callback, *args, **kw):
        r"""
            registers a new callable @callback into @section with
            additional @args and @kw;

            no return value (void);
        """

        # clear all in queue

        return self.__queue.copy()

    # end def



    def get_queue (self):
        r"""
            returns deferred triggers queue (shallow copy);
        """

        # clear all in queue

        return self.__queue.copy()

    # end def




# end class DeferredTriggerQueue
