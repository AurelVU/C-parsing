from AST_classes.ast_expr_stmt_nodes import *


class ArgNode(StmtNode):
    def __init__(self, type: StmtNode, name: StmtNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.type = type
        self.name = name

    @property
    def childs(self):
        return (self.type, self.name,)

    def __str__(self) -> str:
        return 'arg'
