from AST_classes.ast_expr_stmt_nodes import *


class ClazzDecNode(StmtNode):
    def __init__(self, name: AstNode, *vars_list: Tuple[AstNode, ...],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.name = name
        self.vars_list = vars_list

    @property
    def childs(self) -> Tuple[ExprNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.name, ) + self.vars_list

    def __str__(self) -> str:
        return 'class_decl'
