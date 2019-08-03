"""
class Interpreter(object):
    """Python 的 Python 解释器

    """

    def __init__(self):
        self.stack = []
        self.environment = {}  # 支持变量

    def load_value(self, number):
        self.stack.append(number)

    def print_answer(self):
        answer = self.stack.pop()
        print(answer)

    def add_two_values(self):
        first = self.stack.pop()
        second = self.stack.pop()
        total = first + second
        self.stack.append(total)

    def store_name(self, name):
        val = self.stack.pop()
        self.environment[name] = val

    def load_name(self, name):
        val = self.environment[name]
        self.stack.append(val)

    def parse_argument(self, instruction, argument, what_to_execute):
        numbers = ["load_value"]
        names = ['load_name', 'store_name']

        if instruction in numbers:
            argument = what_to_execute['numbers'][argument]
        elif instruction in names:
            argument = what_to_execute['names'][argument]

        return argument

    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(
                instruction, argument, what_to_execute)

            # if instruction == 'load_value':
            #     self.load_value(argument)
            # elif instruction == 'add_two_values':
            #     self.add_two_values()
            # elif instruction == 'print_answer':
            #     self.print_answer()
            # elif instruction == 'store_name':
            #     self.store_name(argument)
            # elif instruction == 'load_name':
            #     self.load_name(argument)

            # 使用动态方法，避免太多if分支
            bytecode_method = getattr(self, instruction)
            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)


# what_to_execute = {
#     "instructions": [
#         ("load_value", 0),
#         ("load_value", 1),
#         ("add_two_values", None),
#         ("print_answer", None)
#     ],
#     "numbers": [7, 5]
# }

what_to_execute = {
    "instructions": [
        ('load_value', 0),
        ('store_name', 0),
        ('load_value', 1),
        ('store_name', 1),
        ('load_name', 0),
        ('load_name', 1),
        ('add_two_values', None),
        ('print_answer', None),
    ],
    'numbers': [1, 2],
    "names": ['a', 'b']

}

interpreter = Interpreter()
interpreter.run_code(what_to_execute)
"""


class VirtualMachineError(Exception):
    pass


class VirtualMachine(object):
    """VirtualMachine类，它管理高层结构，尤其是帧调用栈，并包含了指令到操作的映射

    VirtualMachine 保存调用栈、异常状态、在帧之间传递的返回值。
    它的入口点是run_code方法，它以编译后的代码对象为参数，
    以创建一个帧为开始，然后运行这个帧。这个帧可能再创建出新的帧；
    调用栈随着程序的运行而增长和缩短。当第一个帧返回时，执行结束
    """

    def __init__(self):
        self.frames = []   # 调用栈
        self.frame = []    # 当前调用栈
        self.return_value = None
        self.last_exception = None

    def run_code(self, code, global_names=None, local_names=None):
        """VirtualMachine 入口函数

        :param code: [description]
        :param global_names: [description], defaults to None
        :param local_names: [description], defaults to None
        """
        frame = self.make_frame(code, global_names=global_names,
                                local_names=local_names)

        self.run_frame(frame)
