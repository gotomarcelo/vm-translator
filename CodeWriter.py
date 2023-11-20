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


class CodeWriter:
    def __init__(self, filename):
        self.file = open(filename, "w")

    def writeArithmetic(self, command):
        assembly_code = f"// {command.command_type} implementation\n"

        self.file.write(assembly_code)

    def writePush(self, segment, index):
        assembly_code = f"// push {segment} {index} implementation\n"

        self.file.write(assembly_code)

    def writePop(self, segment, index):
        assembly_code = f"// pop {segment} {index} implementation\n"

        self.file.write(assembly_code)

    def close(self):
        self.file.close()
