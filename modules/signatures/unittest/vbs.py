# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from .abstracts import NamedUnittest

class VBS(NamedUnittest):
    description = "Various VBS scripts"

class VBS_Win32_Process_Create(VBS):
    name = "unittest.named.vbs.win32proc"
    description = (
        "Tests that execution of the child process of a VBS script invoking "
        "Win32_Process::Create is properly followed."
    )

    def init(self):
        self.invoked = False

    def on_signature(self, sig):
        if sig.name == "win32_process_create":
            self.invoked = True

    def check(self):
        process_tree = self.get_results("behavior", {}).get("processtree", [])
        # As long as we also inject into lsass.exe, the process tree should
        # have three processes in it.
        if self.invoked and len(process_tree) == 3:
            return True
