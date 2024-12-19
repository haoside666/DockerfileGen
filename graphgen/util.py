from typing import Any, List, Optional, Union, TypeVar, Set

TType = TypeVar("TType")


def standard_repr(obj) -> str:
    repr_str = f'{obj.__class__}'
    if len(obj.__dict__) != 0:
        repr_str += f': \n'
    else:
        repr_str += f'\n'
    for attribute, value in obj.__dict__.items():
        repr_str += f'\t {attribute}: {value}\n'
    return repr_str


def standard_eq(obj1, obj2) -> bool:
    if not obj1.__class__ == obj2.__class__:
        return False
    return vars(obj1) == vars(obj2)


def return_empty_list_if_none_else_itself(arg: Optional[TType]) -> Union[TType, List[Any]]:  # list always empty
    if arg is None:
        return []
    else:
        return arg
