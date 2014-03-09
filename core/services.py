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

__service_manager = None



# named service getter

def ask_for (service_name, **kw):
    r"""
        returns service object along service name if exists;

        returns None otherwise;

        supports kw["silent_mode"] = True/False;

        raises KeyError if service does not exist and

        kw["silent_mode"] is False or missing;
    """

    return get_service_manager().get_service(service_name, **kw)

# end def



# service manager getter

def get_service_manager ():
    r"""
        returns application-wide unique instance for service manager;
    """

    global __service_manager

    if not isinstance(__service_manager, ServiceManager):

        __service_manager = ServiceManager()

    # end if

    return __service_manager

# end def



def register_service (service_name, service_object, **kw):
    r"""
        registers an object as app-wide service by name;

        raises KeyError if service name already exists;

        stops silently if kw["silent_mode"] is True;

        returns True on success, False otherwise;
    """

    return get_service_manager()\
        .register_service(service_name, service_object, **kw)

# end def



class ServiceManager:
    r"""
        /!\ this module is *STANDALONE* /!\

        you can pick it up *as is* and use it in your own project;

        generic class for app-wide named service management;
    """



    def __init__ (self):
        r"""
            class constructor - initializes service hashtable;
        """

        self.clear_all()

    # end def



    def clear_all (self):
        r"""
            resets service manager to a new dict() object;

            no return value (void);
        """

        self.services = dict()

    # end def



    def delete_service (self, service_name):
        r"""
            deletes service object along service name;

            always silent operation;

            no return value (void);
        """

        # delete service by name

        self.services.pop(str(service_name), None)

    # end def



    def get_service (self, service_name, **kw):
        r"""
            returns service object along service name if exists;

            returns None otherwise;

            supports kw["silent_mode"] = True/False;

            raises KeyError if service does not exist and

            kw["silent_mode"] is False or missing;
        """

        # param inits

        service_name = str(service_name)

        # service must be registered before /!\

        if service_name in self.services:

            return self.services.get(service_name)

        elif not kw.get("silent_mode"):

            raise KeyError(

                "Service '{name}' is *NOT* registered."

                .format(name = service_name)
            )

        # end if

        return None

    # end def



    def register_service (self, service_name, service_object, **kw):
        r"""
            registers an object as app-wide service by name;

            raises KeyError if service name already exists;

            stops silently if kw["silent_mode"] is True;

            returns True on success, False otherwise;
        """

        # param inits

        service_name = str(service_name)

        # service should not be overridden /!\

        if service_name not in self.services:

            self.services[service_name] = service_object

            return True

        elif not kw.get("silent_mode"):

            # service already exists /!\

            raise KeyError(

                (
                    "Service '{name}' already registered."

                    "Should not be overridden in any way."

                ).format(name = service_name)
            )

        # end if

        return False

    # end def



    def replace_service (self, service_name, service_object, **kw):
        r"""
            replaces an existing service by name;

            raises KeyError if service name *DOES NOT* already exists;

            stops silently if kw["silent_mode"] is True;

            returns True on success, False otherwise;
        """

        # param inits

        service_name = str(service_name)

        # service has to be overridden

        if service_name in self.services:

            self.services[service_name] = service_object

            return True

        elif not kw.get("silent_mode"):

            # service *NOT* already exists

            raise KeyError(

                (
                    "Service '{name}' is *NOT* already registered."

                    "Must first exist before being replaced."

                ).format(name = service_name)
            )

        # end if

        return False

    # end def


# end class ServiceManager
