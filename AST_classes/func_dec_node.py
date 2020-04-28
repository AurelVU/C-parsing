from AST_classes.ast_expr_stmt_nodes import *


class FuncDecNode(StmtNode):
    def __init__(self, return_type: AstNode, name: AstNode, *args: Tuple[AstNode, ...],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.return_type = return_type
        self.name = name
        self.args = args

    @property
    def childs(self) -> Tuple[AstNode, ...]:
        return (self.return_type, self.name, ) + self.args

    def __str__(self) -> str:
        return 'func_dec'
