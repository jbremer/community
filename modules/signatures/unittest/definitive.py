# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from .abstracts import Unittest, parse_options, named_unittests

class UnittestAssert(Unittest):
    name = "unittest.assert"
    description = "This unittest failed one or more assert statements"

    def check(self):
        for line in self.get_results("debug", {}).get("log", []):
            if "CRITICAL:" in line and "Test didn't" in line:
                self.mark(line=line)
        return self.has_marks()

class UnittestError(Unittest):
    name = "unittest.error"
    description = "This unittest threw one or more errors"

    def check(self):
        for line in self.get_results("debug", {}).get("log", []):
            if "CRITICAL:" in line:
                self.mark(line=line)
        for line in self.get_results("debug", {}).get("cuckoo", []):
            if "CRITICAL:" in line:
                self.mark(line=line)
        return self.has_marks()

class UnittestWarning(Unittest):
    name = "unittest.warning"
    description = "This unittest threw one or more warnings"

    def check(self):
        for line in self.get_results("debug", {}).get("log", []):
            if "WARNING:" in line:
                self.mark(line=line)
        for line in self.get_results("debug", {}).get("cuckoo", []):
            if "WARNING:" in line:
                self.mark(line=line)
        return self.has_marks()

class UnittestNoFinish(Unittest):
    name = "unittest.nofinish"
    description = "This unittest doesn't indicate it has finished"

    def check(self):
        options = self.get_results("info", {}).get("options", "")
        finish = parse_options(options).get("unittest.finish", "")
        if not finish.isdigit() or not int(finish):
            return

        for line in self.get_results("debug", {}).get("log", []):
            if "Test finished!" in line:
                return False
        return True

class UnittestAnswer(Unittest):
    # The name will be changed at runtime but is required for initialization.
    name = "unittest.answer"
    # The order should be higher than any other unittest-related Signature.
    order = 3

    failure_signatures = [
        "unittest.assert", "unittest.error",
        "unittest.warning", "unittest.nofinish",
    ]

    def init(self):
        self.failure = False
        self.unittests = named_unittests(self)

    def on_signature(self, signature):
        if signature.name in self.failure_signatures:
            self.failure = True

        # Little bit hacky, but aligns with NamedUnittest.
        if signature.name in self.unittests and signature.severity < 0:
            self.failure = True

    def on_complete(self):
        if self.failure:
            self.name = "unittest.failure"
            self.description = "This unittest failed to succeed"
        else:
            self.name = "unittest.success"
            self.description = "This unittest ran successfully"
        return True
