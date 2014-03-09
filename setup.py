#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = "tkRAD",
    packages = ["tkRAD", "tkRAD.core", "tkRAD.easy", "tkRAD.widgets",
    "tkRAD.xml"],
    version = "1.3-The-Full-Monty",
    requires = ["Tkinter"],
    description = "tkRAD - Tkinter Rapid Application Development "
    "and XML widget builder",
    author = "Raphaël SEBAN",
    author_email = "motus@laposte.net",
    maintainer = "Raphaël SEBAN",
    maintainer_email = "motus@laposte.net",
    url = "https://github.com/tarball69/tkRAD/wiki",
    download_url = "https://github.com/tarball69/tkRAD",
    keywords = ["application", "framework", "tkinter", "gui", "xml",
    "widget", "builder"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
    ],
    license = """
Licensed under GNU Lesser General Public License v3.
    """,
    long_description = """
Tkinter Rapid Application Development (RAD) library.

`tkRAD` is a **Python3.2+** library designed to enable really Rapid
Application Development (RAD) process by using predefined classes to
derive in your own subclasses, with quite useful embedded services
such as dynamic **Tkinter XML widget building**, service manager,
events manager, RC configuration manager and so on.

`tkRAD` is a deliberately **short-made API** designed for comfort,
easiness and simplicity.

`tkRAD` provides the necessary **core tools** to quickly start up an
application development or for Tkinter widget testing through
`tkRAD.easy.builder` module.


## BUG REPORT

In order to **track bugs** and fix them correctly, we'd like to hear
from you.

**If you encountered any problem** during the use of `tkRAD` lib,
please leave us a comment and tell us:

* environment:
    * which platform? (Windows, macOS, Linux)
    * which Python version? (2.7+, 3.2+)
    * tkinter installed correctly? (yes/no)

* context:
    * when did it happen?
        * while trying wiki tutorial code samples?
        * while trying `tkRAD.easy.builder` features?
        * while trying to write your own app?

* traceback (optional):
    * are you sure it is *NOT* an XML source code mistype error?
    * could you copy/paste the console error text, please?
    * could you tell us few words about what happened?

**Whatever happened**, we'd like to know about it.

You will find an open issue **"It did *NOT* work for me!"** at:

https://github.com/tarball69/tkRAD/issues/6

**Thank you for contributing** to make `tkRAD` a better place for
everyone.

"""
)
