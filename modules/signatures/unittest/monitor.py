# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from .abstracts import NamedUnittest

class Breakpipe(NamedUnittest):
    name = "unittest.named.monitor.breakpipe"
    description = "Program intentionally breaking the monitor pipe handle"

    def check(self):
        a, b = self.api_calls("MessageBoxTimeoutA")
        assert a["arguments"]["caption"] == "Before"
        assert b["arguments"]["caption"] == "After"
        return True

class Adapter(NamedUnittest):
    name = "unittest.named.monitor.adapter"
    description = "Identifies recursively loaded DLL API hooking"

    def check(self):
        return self.api_count("GetAdaptersInfo") == 1

class ReadAV(NamedUnittest):
    name = "unittest.named.monitor.readav"
    description = "Logging of incorrect parameters"

    def check(self):
        if self.api_count("NtWriteFile") != 3:
            return False
        dropped = self.get_results("dropped", [])
        if len(dropped) != 1:
            return False
        return open(dropped[0]["path"], "rb").read() == "hello world"

class ControlService(NamedUnittest):
    name = "unittest.named.monitor.controlservice"
    description = "Recursive DLL hooking test using ControlService"

    def check(self):
        return self.api_count("ControlService") == 1

class CrashX86(NamedUnittest):
    name = "unittest.named.monitor.x86.crash"
    description = "Shows proper logging of a crashing 32-bit program"

    def check(self):
        call, = self.api_calls("__exception__")
        assert call["arguments"]["exception"] == {
            "symbol": "crash+0x15a9",
            "instruction": "mov byte ptr [eax], 0",
            "instruction_r": "c6 00 00 b8 00 00 00 00 8b 4d fc c9 8d 61 fc c3",
            "module": "crash.exe",
            "exception_code": "0xc0000005",
            "offset": 5545,
            "address": "0x4015a9"
        }
        return True

class CrashX64(NamedUnittest):
    name = "unittest.named.monitor.x64.crash"
    description = "Shows proper logging of a crashing 64-bit program"

    def check(self):
        call, = self.api_calls("__exception__")
        assert call["arguments"]["exception"] == {
            "symbol": "crash+0x152b",
            "instruction": "mov byte ptr [rax], 0",
            "instruction_r": "c6 00 00 b8 00 00 00 00 48 83 c4 30 5d c3 90 90",
            "module": "crash.exe",
            "exception_code": "0xc0000005",
            "offset": 5419,
            "address": "0x40152b"
        }
        return True

class LogDLL(NamedUnittest):
    name = "unittest.named.monitor.logdll"
    description = "Log API calls performed in DllMain"

    def check(self):
        a, b = self.api_calls("MessageBoxTimeoutA")
        assert a["arguments"]["caption"] == "Hello World"
        assert b["arguments"]["caption"] == "Hello World"
        return True

class FindFirstFile(NamedUnittest):
    name = "unittest.named.monitor.findfirstfile"
    description = "Ensure the dirpath given to FindFirstFile() is correct"

    def check(self):
        call, = self.api_calls("FindFirstFileExW")
        assert call["arguments"]["filepath"] == "C:\\helloworld"
        assert call["arguments"]["filepath_r"] == "C:\\helloworld"
        return True

class CreateProc(NamedUnittest):
    name = "unittest.named.monitor.createproc"
    description = "Tests very basic process following logic"

    def check(self):
        msgbox, = self.api_calls("MessageBoxTimeoutA")
        assert msgbox["arguments"]["text"] == "World"
        return True

class CreateRemoteThread(NamedUnittest):
    name = "unittest.named.monitor.createremotethread"
    description = "Calls & CreateThread CreateRemoteThread once"

    def check(self):
        assert self.api_count("CreateThread") == 1
        assert self.api_count("CreateRemoteThread") == 1
        return True

class CoInitialize(NamedUnittest):
    name = "unittest.named.monitor.coinit"
    description = "Checks that CoInitializeEx is intercepted correctly"

    def check(self):
        return self.api_count("CoInitializeEx") == 1

class ResumeThread(NamedUnittest):
    name = "unittest.named.monitor.resumethread"
    description = "Checks basic CREATE_SUSPENDED + ResumeThread"

    def check(self):
        call, = self.api_calls("CreateProcessInternalW")
        assert call["flags"]["creation_flags"] == "CREATE_SUSPENDED"
        assert self.api_count("NtResumeThread") == 1
        return True
