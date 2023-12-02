from CodeWriter import CodeWriter
import Parser


def main(input_file, output_file):
    p = Parser.Parser(input_file)
    code = CodeWriter(output_file)

    while p.hasMoreCommands():
        current_command = p.nextCommand()
        if isinstance(current_command, Parser.GotoCommand):
            code.writeGoto(current_command.label)
        elif isinstance(current_command, Parser.IfGotoCommand):
            code.writeIfGoto(current_command.label)
        elif isinstance(current_command, Parser.PushCommand):
            code.writePush(current_command.segment, current_command.index)
        elif isinstance(current_command, Parser.PopCommand):
            code.writePop(current_command.segment, current_command.index)

    code.close()


if __name__ == "__main__":
    # Substitua pelo caminho do seu arquivo VM
    input_file = "C:/Users/marcelo.goto/Documents/tradutor/vm-translator/test.vm"
    output_file = "C:/Users/marcelo.goto/Documents/tradutor/vm-translator/output.asm"
    main(input_file, output_file)
