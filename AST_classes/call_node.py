from AST_classes.array_node import *


class CallNode(StmtNode):
    def __init__(self, func_name: StmtNode, *params: Tuple[AstNode, ...],
                 row: Optional[int] = None, line: Optional[int] = None, **props):
        super().__init__(row=row, line=line, **props)
        self.func_name = func_name
        self.params = params

    @property
    def childs(self) -> Tuple[ArrayNode, ...]:
        # return self.vars_type, (*self.vars_list)
        return (self.func_name,) + self.params

    def __str__(self) -> str:
        return 'call'
