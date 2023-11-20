class Parser:
    def __init__(self, filename):
        self.file = open(filename, "r")
        self.commands = [self.parse_command(line) for line in self.file.readlines() if "//" not in line and line.strip() != ""]
        self.current_command = None

    def parse_command(self, line):
        parts = line.split()
        if parts[0] == "push":
            return PushCommand(parts[1], int(parts[2]))
        elif parts[0] == "pop":
            return PopCommand(parts[1], int(parts[2]))
        else:
            return ArithmeticCommand(parts[0])

    def hasMoreCommands(self):
        return bool(self.commands)

    def nextCommand(self):
        self.current_command = self.commands.pop(0)
        return self.current_command