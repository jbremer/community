# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from .abstracts import NamedUnittest

class Javascript(NamedUnittest):
    description = "Various Javascripts scripts & tricks"

class PowershellDropperJavascript(Javascript):
    name = "unittest.named.javascript.fpo"
    description = (
        "Tests that PowerShell doesn't crash due to an unhandled exception "
        "(namely 0xe0434f4d, a COM exception thrown around in PowerShell)"
    )

    def init(self):
        self.raises_exception = False

    def on_signature(self, sig):
        if sig.name == "raises_exception":
            self.raises_exception = True

    def check(self):
        return not self.raises_exception
