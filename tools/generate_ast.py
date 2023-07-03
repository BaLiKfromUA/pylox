TAB = '    '


def define_ast(base_name, types):
    path = "../pylox/" + base_name.lower() + ".py"
    file = open(path, "w")
    # HEADER
    file.write("# THIS CODE IS GENERATED AUTOMATICALLY. DO NOT CHANGE IT MANUALLY!\n\n")
    # IMPORTS
    file.write('import typing\n')
    file.write('from abc import ABC, abstractmethod\n\n')
    if base_name == "Stmt":
        file.write('from pylox.expr import Expr\n')
    file.write('from pylox.tokens import Token\n')
    # VISITOR
    define_visitor(file, base_name, types)
    # BASE CLASS
    file.write(f'class {base_name}:\n')
    file.write(f'{TAB}def __init__(self):\n')
    file.write(f'{TAB * 2}pass\n')
    file.write(f'{TAB}@abstractmethod\n')
    file.write(f'{TAB}def accept(self, visitor : {base_name}Visitor) -> typing.Any:\n')
    file.write(f'{TAB * 2}pass')
    file.write('\n')
    # IMPLEMENTATIONS
    for className, fields in types.items():
        file.write('\n')
        define_type(file, base_name, className, fields)
    file.write('\n')


def define_type(file, base_name, class_name, fields):
    file.write(f'class {class_name}({base_name}):')
    file.write('\n')
    file.write(f'{TAB}')

    if type(fields) is not tuple:
        file.write(f'def __init__(self, {fields}):')
        file.write('\n')
    else:
        file.write(f'def __init__(self, {", ".join(fields)}):')
        file.write('\n')

    file.write(f'{TAB * 2}super().__init__()\n')

    if type(fields) is not tuple:
        att = fields.split(":")[0]
        file.write(f'{TAB * 2}self.{att} = {att}')
        file.write('\n')
    else:
        for field in fields:
            att = field.split(":")[0]
            file.write(f'{TAB * 2}self.{att} = {att}')
            file.write('\n')

    file.write('\n')
    file.write(f'{TAB}def accept(self, visitor : {base_name}Visitor) -> typing.Any:\n')
    file.write(f'{TAB * 2}return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)')
    file.write('\n')


def define_visitor(file, base_name, types):
    visitor = f'{base_name}Visitor'
    file.write(f'\n')
    file.write(f'class {visitor}(ABC):')

    for t in types:
        file.write('\n')
        file.write(f'{TAB}@abstractmethod')
        file.write('\n')
        file.write(f'{TAB}')
        file.write(f"def visit_{t.lower()}_{base_name.lower()}(self, {base_name.lower()}) -> typing.Any:")
        file.write('\n')
        file.write(f'{TAB * 2}pass')
        file.write('\n')
    file.write(f'\n')


if __name__ == "__main__":
    expressions = {
        "Assign": ('name: Token', 'value: Expr'),
        "Binary": ('left: Expr', 'operator: Token', 'right: Expr'),
        "Call": ('callee: Expr', 'paren: Token', "arguments: typing.List[Expr]"),
        "Get": ('obj: Expr', 'name: Token'),
        "Grouping": 'expr: Expr',
        "Literal": 'value: typing.Any',
        "Logical": ('left: Expr', 'operator: Token', 'right: Expr'),
        "Set": ('obj: Expr', 'name: Token', 'value: Expr'),
        "Unary": ('operator: Token', 'right: Expr'),
        "Variable": 'name: Token'
    }
    statements = {
        "Block": "statements: typing.List[Stmt]",
        "Expression": 'expr: Expr',
        "Function": ('name: Token', 'params: typing.List[Token]', 'body: typing.List[Stmt]'),
        "If": ('condition: Expr', 'then_branch: Stmt', 'else_branch: typing.Optional[Stmt]'),
        "Print": 'expr : Expr',
        "Return": ('keyword: Token', 'value: typing.Optional[Expr]'),
        "Var": ('name: Token', "initializer: typing.Optional[Expr]"),
        "Class": ('name: Token', 'methods: typing.List[Function]'),
        "While": ('condition: Expr', 'body: Stmt'),
        "Break": 'keyword: Token'
    }

    define_ast("Expr", expressions)
    define_ast("Stmt", statements)
