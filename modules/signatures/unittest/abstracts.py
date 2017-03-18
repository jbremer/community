# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import logging

try:
    from cuckoo.common.abstracts import Signature
    from cuckoo.common.config import parse_options
except ImportError:
    class Signature(object):
        """For older Cuckoo setups, i.e., up to 2.0-rc2, we ignore all of the
        unittest-related Signatures by not inheriting from the real Signature
        class. This is due to the fact that those versions didn't support the
        functionality required for these unittest Signatures."""

    def parse_options(*args, **kwargs):
        pass

log = logging.getLogger(__name__)

def named_unittests(sig):
    ret, options = [], parse_options(
        sig.get_results("info", {}).get("options", "")
    )
    for unittest in options.get("unittest", "").split(":"):
        if not unittest.strip():
            continue

        ret.append("unittest.named.%s" % unittest.strip())
    return ret

class Unittest(Signature):
    severity = 5
    categories = ["unittest"]
    authors = ["Cuckoo Technologies"]
    minimum = "2.0.0"

    def on_complete(self):
        if named_unittests(self):
            return self.check()

    def check(self):
        pass

class NamedUnittest(Signature):
    severity = 5
    categories = ["unittest"]
    authors = ["Cuckoo Technologies"]
    minimum = "2.0.0"

    def api_count(self, apiname):
        apistats = self.get_results("behavior", {}).get("apistats", {})
        count = 0
        for funcs in apistats.values():
            count += funcs.get(apiname, 0)
        return count

    def api_calls(self, apiname):
        processes = self.get_results("behavior", {}).get("processes", [])
        for process in processes:
            for call in process["calls"]:
                if call["api"] == apiname:
                    yield call

    def on_complete(self):
        if self.name in named_unittests(self):
            try:
                # Little bit hacky, but aligns with UnittestAnswer.
                if self.check() is True:
                    self.severity = 5
                else:
                    self.severity = -5
            except AssertionError as e:
                log.warning("Assertion failed: %s", e)
                self.severity = -5
            except:
                log.exception(
                    "An exception occurred in the named unittest: %s",
                    self.name
                )
                self.severity = -5
            return True

    def check(self):
        """Function to identify whether the signature has been successful.
        Returns True upon success and anything else upon failure."""
