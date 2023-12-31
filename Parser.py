from CodeWriter import CodeWriter


class ArithmeticCommand:
    def __init__(self, command_type):
        self.command_type = command_type


class PushCommand:
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index


class PopCommand:
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index


class LabelCommand:
    def __init__(self, label):
        self.label = label

class GotoCommand:
    def __init__(self, label):
        self.label = label

class IfGotoCommand:
    def __init__(self, label):
        self.label = label

class CallCommand:
    def __init__(self, function_name, n_args):
        self.function_name = function_name
        self.n_args = n_args

class FunctionCommand:
    def __init__(self, function_name, n_locals):
        self.function_name = function_name
        self.n_locals = n_locals

class ReturnCommand:
    def __init__(self):
        pass

class Parser:
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.commands = [self.parse_command(line) for line in self.file.readlines(
        ) if "//" not in line and line.strip() != ""]
        self.current_command = None

    def parse_command(self, line):
        parts = line.split()
        if parts[0] == "push":
            return PushCommand(parts[1], int(parts[2]))
        elif parts[0] == "pop":
            return PopCommand(parts[1], int(parts[2]))
        elif parts[0] == "label":
            return LabelCommand(parts[1])
        elif parts[0] == "goto":
            return GotoCommand(parts[1])
        elif parts[0] == "if-goto":
            return IfGotoCommand(parts[1])
        elif parts[0] == "call":
            return CallCommand(parts[1], int(parts[2]))
        elif parts[0] == "function":
            return FunctionCommand(parts[1], int(parts[2]))
        elif parts[0] == "return":
            return ReturnCommand()
        else:
            return ArithmeticCommand(parts[0])

    def hasMoreCommands(self):
        return bool(self.commands)

    def nextCommand(self):
        self.current_command = self.commands.pop(0)
        return self.current_command
