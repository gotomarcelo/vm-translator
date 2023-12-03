class CodeWriter:
    def __init__(self, filename):
        self.file = open(filename, "w")

    def writeArithmetic(self, command):
        arithmetic_mapping = {
            "add": "+",
            "sub": "-",
            "neg": "-",
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
            "and": "&",
            "or": "|",
            "not": "!"
        }

        assembly_code = f"// {command.command_type}\n"

        if command.command_type in {"add", "sub", "and", "or"}:
            assembly_code += self.binary_operation(
                arithmetic_mapping[command.command_type])
        elif command.command_type in {"neg", "not"}:
            assembly_code += self.unary_operation(
                arithmetic_mapping[command.command_type])
        elif command.command_type in {"eq", "gt", "lt"}:
            assembly_code += self.comparison_operation(
                arithmetic_mapping[command.command_type])
        elif command.command_type in {"eq", "gt", "lt"}:
            label_id = self.get_label_id()
            assembly_code += self.comparison_operation(
                arithmetic_mapping[command.command_type], label_id)

        self.file.write(assembly_code)


    def binary_operation(self, operation):
        return f"@SP\nAM=M-1\nD=M\nA=A-1\nM=M{operation}D\n"


    def unary_operation(self, operation):
        return f"@SP\nA=M-1\nM={operation}M\n"


    def comparison_operation(self, jump_condition):
        label_id = self.get_label_id()
        return f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE_{label_id}\nD;{jump_condition}\n@SP\nA=M-1\nM=0\n@END_{label_id}\n0;JMP\n(TRUE_{label_id})\n@SP\nA=M-1\nM=-1\n(END_{label_id})\n"


    def get_label_id(self):
        if not hasattr(self, "label_id"):
            self.label_id = 0
        else:
            self.label_id += 1
        return self.label_id


    def writePush(self, segment, index):
        segment_mapping = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "constant": None,
            "static": "STATIC",
            "temp": "5",
            "pointer": "3"
        }

        assembly_code = f"// push {segment} {index}\n"

        if segment == "constant":
            assembly_code += f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif segment in {"local", "argument", "this", "that"}:
            assembly_code += self.push_from_segment(
                segment_mapping[segment], index)
        elif segment in {"static", "temp", "pointer"}:
            assembly_code += self.push_from_static_temp_pointer(
                segment_mapping[segment], index)

        self.file.write(assembly_code)


    def push_from_segment(self, segment, index):
        return f"@{segment}\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"


    def push_from_static_temp_pointer(self, segment, index):
        return f"@{segment}\nD=A\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    def writePop(self, segment, index):
        segment_mapping = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "static": "STATIC",  # Assuming static starts from STATIC.0
            "temp": "5",  # Assuming temp starts from R5
            "pointer": "3"  # Assuming pointer starts from THIS (R3)
        }

        assembly_code = f"// pop {segment} {index}\n"

        if segment in {"local", "argument", "this", "that"}:
            assembly_code += self.pop_to_segment(
                segment_mapping[segment], index)
        elif segment in {"static", "temp", "pointer"}:
            assembly_code += self.pop_to_static_temp_pointer(
                segment_mapping[segment], index)

        self.file.write(assembly_code)

    def pop_to_segment(self, segment, index):
        return f"@{segment}\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"

    def pop_to_static_temp_pointer(self, segment, index):
        return f"@{segment}\nD=A\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"

    def writeLabel(self, label):
        assembly_code = f"({label})\n"
        self.file.write(assembly_code)
    
    def writeGoto(self, label):
        assembly_code = f"@{label}\n0;JMP\n"
        self.file.write(assembly_code)

    def writeIfGoto(self, label):
        assembly_code = f"@SP\nAM=M-1\nD=M\n@{label}\nD;JNE\n"
        self.file.write(assembly_code)

    def writeCall(self, function_name, n_args):
        return_address_label = f"RETURN_{self.get_label_id()}"

        self.writePush("constant", return_address_label)
        self.writePush("local", "LCL")
        self.writePush("argument", "ARG")
        self.writePush("this", "THIS")
        self.writePush("that", "THAT")

        self.writeBinaryOperation("D", "A", "M-D", n_args)
        self.writePop("argument", "ARG")

        self.writePop("pointer", "LCL")

        self.writeGoto(function_name)

        self.writeLabel(return_address_label)

    def close(self):
        self.file.close()
