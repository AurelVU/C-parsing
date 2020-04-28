from AST_classes.ast_expr_stmt_nodes import *


class ValArrNode(StmtNode):
    def __init__(self, arr: AstNode, num: AstNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.arr = arr
        self.num = num

    @property
    def childs(self) -> Tuple[AstNode, AstNode]:
        return (self.arr, self.num, )

    def __str__(self) -> str:
        return '[] val'
