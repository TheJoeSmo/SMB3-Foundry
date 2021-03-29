

from typing import List, Optional, Callable


class Stealer:
    """A stealer of class variables"""

    @staticmethod
    def default_getter(_, var_name, instance):
        return getattr(instance, var_name)

    @staticmethod
    def default_setter(_, var_name, value, instance):
        return setattr(instance, var_name, value)

    def __init__(self, ins_var: str, cls_var: str, getter: Optional[Callable] = None, setter: Optional[Callable] = None):
        self.instance_variable = ins_var
        self.class_variable = cls_var
        self.getter_ = getter if getter is not None else self.default_getter
        self.setter_ = setter if setter is not None else self.default_setter

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" \
               f"{self.instance_variable}, {self.class_variable}, {self.getter_}, {self.setter_}" \
               f")"


def steal_variables_from_class_variable(
        cls,
        cls_var: str,
        cls_props: List[Stealer]
):
    """
    Set a property from a variable from one of the base class' variables.

    :param cls: The class to add properties to
    :param cls_var: The variable name that we want to steal from
    :param cls_props: The list of variable stealer's
    """

    def get_var_instance(self):
        """Retrieves the instance of the variable we are wanting to steal"""
        return getattr(self, cls_var)

    def getter_wrapper(var_name: str, func: Callable):
        def getter_(self):
            return func(self, var_name, get_var_instance(self))
        return getter_

    def setter_wrapper(var_name: str, func: Callable):
        def setter_(self, value):
            func(self, var_name, value, get_var_instance(self))
        return setter_

    for prop in cls_props:
        setattr(
            cls,
            prop.class_variable,
            property(
                getter_wrapper(prop.instance_variable, prop.getter_),
                setter_wrapper(prop.instance_variable, prop.setter_)
            )
        )

    return cls
