def main(input_file, output_file):
    p = Parser(input_file)
    code = CodeWriter(output_file)

    while p.hasMoreCommands():
        current_command = p.nextCommand()
        if isinstance(current_command, ArithmeticCommand):
            code.writeArithmetic(current_command)
        elif isinstance(current_command, PushCommand):
            code.writePush(current_command.segment, current_command.index)
        elif isinstance(current_command, PopCommand):
            code.writePop(current_command.segment, current_command.index)

    code.close()

main("teste.vm", "output.asm")