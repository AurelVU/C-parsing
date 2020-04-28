from AST_classes.bin_op_node import *


class ArrayNewInitNode(StmtNode):
    def __init__(self, vars_type: StmtNode, *sizes: Tuple[AstNode, ...],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.vars_type = vars_type
        self.sizes = sizes

    @property
    def childs(self) -> Tuple[ExprNode, BinOpNode]:
        # return self.vars_type, (*self.vars_list)
        return (self.vars_type, ) + self.sizes

    def __str__(self) -> str:
        return 'new'
