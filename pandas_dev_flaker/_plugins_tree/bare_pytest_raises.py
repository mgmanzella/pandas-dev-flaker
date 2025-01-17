import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._data_tree import State, register

MSG = "PDF003 pytest.raises used without 'match='"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if isinstance(node.func, ast.Attribute) and node.func.attr == "raises":
        if not node.keywords:
            yield node.lineno, node.col_offset, MSG
        elif "match" not in {keyword.arg for keyword in node.keywords}:
            yield node.lineno, node.col_offset, MSG
