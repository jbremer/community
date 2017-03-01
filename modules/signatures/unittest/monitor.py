# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from .abstracts import NamedUnittest

class BreakpipeUnittest(NamedUnittest):
    name = "unittest.named.breakpipe"
    description = "Program intentionally breaking the monitor pipe handle"

    def check(self):
        apistats = self.get_results("behavior", {}).get("apistats", {})
        count = 0
        for funcs in apistats.values():
            count += funcs.get("MessageBoxTimeoutA", 0)
        return count == 2
