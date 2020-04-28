from AST_classes.ast_expr_stmt_nodes import *


class VarDeclNode(StmtNode):
    def __init__(self, vars_type: StmtNode, name: AstNode,
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.vars_type = vars_type
        self.name = name

    @property
    def childs(self):
        # return self.vars_type, (*self.vars_list)
        return (self.vars_type, self.name, )

    def __str__(self) -> str:
        return 'var'
