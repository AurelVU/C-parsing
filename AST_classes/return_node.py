from AST_classes.ident_node import *
from AST_classes.stmt_list_node import _empty

class ReturnNode(StmtNode):
    def __init__(self, exp: Optional[ExprNode] = None,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.exp = exp if exp else _empty

    @property
    def childs(self) -> Tuple[ExprNode, ...]:
        return (self.exp, )

    def __str__(self) -> str:
        return 'return'
