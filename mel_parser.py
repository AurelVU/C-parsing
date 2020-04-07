from contextlib import suppress

import pyparsing as pp
from pyparsing import pyparsing_common as ppc

from mel_ast import *


def _make_parser():
    # num = ppc.fnumber.setParseAction(lambda s, loc, tocs: tocs[0])
    num = ppc.fnumber # pp.Regex('[+-]?\\d+\\.?\\d*([eE][+-]?\\d+)?') # описание числа
    # c escape-последовательностями как-то неправильно работает
    str_ = pp.QuotedString('"', escChar='\\', unquoteResults=False, convertWhitespaceEscapes=False) #описание строки
    literal = num | str_ #Символ это или число, или буква
    ident = ppc.identifier.setName('ident') #название функции, объявление непонятное

    LPAR, RPAR = pp.Literal('(').suppress(), pp.Literal(')').suppress()
    LBRACK, RBRACK = pp.Literal("[").suppress(), pp.Literal("]").suppress()
    LBRACE, RBRACE = pp.Literal("{").suppress(), pp.Literal("}").suppress()
    SEMI, COMMA = pp.Literal(';').suppress(), pp.Literal(',').suppress()
    ASSIGN = pp.Literal('=')

    DOT = pp.Literal('.')
    ADD, SUB = pp.Literal('+'), pp.Literal('-')
    MUL, DIV = pp.Literal('*'), pp.Literal('/')
    AND = pp.Literal('&&')
    OR = pp.Literal('||')
    BIT_AND = pp.Literal('&')
    BIT_OR = pp.Literal('|')
    GE, LE, GT, LT = pp.Literal('>='), pp.Literal('<='), pp.Literal('>'), pp.Literal('<')
    NEQUALS, EQUALS = pp.Literal('!='), pp.Literal('==')

    expr = pp.Forward() #выражение
    stmt = pp.Forward() #единица кода
    stmt_list = pp.Forward() #код

    call = ident + LPAR + pp.Optional(expr + pp.ZeroOrMore(COMMA + expr)) + RPAR  # вызов фукнции
    dot = pp.Group(ident + pp.ZeroOrMore(DOT + (call | ident))).setName('bin_op')

    group = (
        literal |
        (dot ^
        call ^  # обязательно перед ident, т.к. приоритетный выбор (или использовать оператор ^ вместо | )
        ident) | #??????????
        LPAR + expr + RPAR
    )

    # обязательно везде pp.Group, иначе приоритет операций не будет работать (см. реализцию set_parse_action_magic);
    # также можно воспользоваться pp.operatorPrecedence (должно быть проще, но не проверял)
    mult = pp.Group(group + pp.ZeroOrMore((MUL | DIV) + group)).setName('bin_op')
    add = pp.Group(mult + pp.ZeroOrMore((ADD | SUB) + mult)).setName('bin_op')
    compare1 = pp.Group(add + pp.Optional((GE | LE | GT | LT) + add)).setName('bin_op')  # GE и LE первыми, т.к. приоритетный выбор
    compare2 = pp.Group(compare1 + pp.Optional((EQUALS | NEQUALS) + compare1)).setName('bin_op')
    logical_and = pp.Group(compare2 + pp.ZeroOrMore(AND + compare2)).setName('bin_op')
    logical_or = pp.Group(logical_and + pp.ZeroOrMore(OR + logical_and)).setName('bin_op')

    expr << (logical_or)

    array = pp.Forward()
    array_new_init = pp.Keyword("new").suppress() + ident + LBRACK + add + RBRACK
    array << ident + LBRACK + RBRACK #пока только одномерные массивы. проблемы с рекурсией
    simple_assign = (ident + ASSIGN.suppress() + (array_new_init | expr | str_)).setName('assign') #присвоение
    var_decl_inner = simple_assign | ident # инициализация и присвоение одного
    vars_decl = (array | ident) + var_decl_inner + pp.ZeroOrMore(COMMA + var_decl_inner) # инициализация и присвоение нескольких

    assign = ident + ASSIGN.suppress() + expr #еще раз присвоение?
    simple_stmt = assign | call #бред

    for_stmt_list0 = (pp.Optional(simple_stmt + pp.ZeroOrMore(COMMA + simple_stmt))).setName('stmt_list') #блоки в for, заготовка
    for_stmt_list = vars_decl | for_stmt_list0 # окончательные блоки в for
    for_cond = expr | pp.Group(pp.empty).setName('stmt_list') # условие
    for_body = stmt | pp.Group(SEMI).setName('stmt_list')



    if_ = pp.Keyword("if").suppress() + LPAR + expr + RPAR + stmt + pp.Optional(pp.Keyword("else").suppress() + stmt)
    for_ = pp.Keyword("for").suppress() + LPAR + for_stmt_list + SEMI + for_cond + SEMI + for_stmt_list + RPAR + for_body
    while_ = pp.Keyword("while").suppress() + LPAR + expr + RPAR + stmt
    comp_op = LBRACE + stmt_list + RBRACE

    stmt << (
        if_ |
        for_ |
        while_ |
        comp_op |
        (dot ^
        vars_decl + SEMI ^
        simple_stmt + SEMI)
    )

    stmt_list << (pp.ZeroOrMore(stmt + pp.ZeroOrMore(SEMI)))

    program = stmt_list.ignore(pp.cStyleComment).ignore(pp.dblSlashComment) + pp.StringEnd()

    start = program

    def set_parse_action_magic(rule_name: str, parser: pp.ParserElement)->None:
        if rule_name == rule_name.upper():
            return
        if getattr(parser, 'name', None) and parser.name.isidentifier():
            rule_name = parser.name
        if rule_name in ('bin_op', ):
            def bin_op_parse_action(s, loc, tocs):
                node = tocs[0]
                if not isinstance(node, AstNode):
                    node = bin_op_parse_action(s, loc, node)
                for i in range(1, len(tocs) - 1, 2):
                    secondNode = tocs[i + 1]
                    if not isinstance(secondNode, AstNode):
                        secondNode = bin_op_parse_action(s, loc, secondNode)
                    node = BinOpNode(BinOp(tocs[i]), node, secondNode)
                return node
            parser.setParseAction(bin_op_parse_action)
        else:
            cls = ''.join(x.capitalize() for x in rule_name.split('_')) + 'Node' #разбитие названия переменной на куски по _, создание заглавной первой буквы и прибавление Node
            with suppress(NameError):
                cls = eval(cls)
                if not inspect.isabstract(cls):
                    def parse_action(s, loc, tocs):
                        return cls(*tocs)
                    parser.setParseAction(parse_action)

    for var_name, value in locals().copy().items():
        if isinstance(value, pp.ParserElement):
            set_parse_action_magic(var_name, value)

    return start


parser = _make_parser()


def parse(prog: str)->StmtListNode:
    return parser.parseString(str(prog))[0]
