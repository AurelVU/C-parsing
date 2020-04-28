from AST_classes.ast_expr_stmt_nodes import *


class ArrayInitedNode(StmtNode):
    def __init__(self, *values: AstNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.values = values

    @property
    def childs(self) -> Tuple[AstNode]:
        # return self.vars_type, (*self.vars_list)
        c = (i() for i in self.values)
        return self.values

    def __str__(self) -> str:
        return '{}'
