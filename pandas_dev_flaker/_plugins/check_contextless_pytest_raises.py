import ast
from typing import Iterator, Tuple

from pandas_dev_flaker._ast_helpers import is_name_attr
from pandas_dev_flaker._data import State, register

MSG = "PSG003 Do not use pytest.raises without context manager"


@register(ast.Call)
def visit_Call(
    state: State,
    node: ast.Call,
    parent: ast.AST,
) -> Iterator[Tuple[int, int, str]]:
    if (
        is_name_attr(
            node.func,
            state.from_imports,
            "pytest",
            ("raises",),
        )
        and not isinstance(parent, ast.withitem)
    ):
        yield node.lineno, node.col_offset, MSG
    elif (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "raises"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "pytest"
        and not isinstance(parent, ast.withitem)
    ):
        yield node.lineno, node.col_offset, MSG