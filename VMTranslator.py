from CodeWriter import CodeWriter
import Parser


def main(input_file, output_file):
    p = Parser.Parser(input_file)
    code = CodeWriter(output_file)

    # code.writeInit()

    while p.hasMoreCommands():
        current_command = p.nextCommand()
        if isinstance(current_command, Parser.ArithmeticCommand):
            code.writeArithmetic(current_command)
        elif isinstance(current_command, Parser.PushCommand):
            code.writePush(current_command.segment, current_command.index)
        elif isinstance(current_command, Parser.PopCommand):
            code.writePop(current_command.segment, current_command.index)
        elif isinstance(current_command, Parser.LabelCommand):
            code.writeLabel(current_command.label)
        elif isinstance(current_command, Parser.GotoCommand):
            code.writeGoto(current_command.label)
        elif isinstance(current_command, Parser.IfGotoCommand):
            code.writeIfGoto(current_command.label)
        elif isinstance(current_command, Parser.FunctionCommand):
            code.writeFunction(current_command.function_name, current_command.n_locals)
        elif isinstance(current_command, Parser.ReturnCommand):
            code.writeReturn()
        elif isinstance(current_command, Parser.CallCommand):
            code.writeCall(current_command.function_name, current_command.n_args)

    code.close()


if __name__ == "__main__":
    # Substitua pelo caminho do seu arquivo VM/BasicLop
    input_file = "C:/Users/marcelo.goto/Documents/tradutor/vm-translator/08/ProgramFlow/BasicLoop/BasicLoop.vm"
    output_file = "C:/Users/marcelo.goto/Documents/tradutor/vm-translator/08/ProgramFlow/BasicLoop/BasicLoop.asm"
    main(input_file, output_file)
