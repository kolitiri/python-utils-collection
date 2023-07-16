"""
    Using Mixin metaclasses to create class templates.

    In this case:
        1. `EnforceTransformersMeta` is used to enforce the use of every method
            that is decorated with the `requiredtransformer`.
        2. `ABCMeta` is used to enforce the implementation of abstracted methods.

    They are both combined in the `MsgTransformerMeta` mixin metaclass.
"""
from abc import ABCMeta, abstractmethod
import functools
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from exceptions import MissingTransformersError


def requiredtransformer(fn) -> Callable:
    """ Decorator used to mark a function as required.
        It works in a similar way to abc.abstractmethod.
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    setattr(wrapper, '__isrequiredtransformer__', True)
    return wrapper


class EnforceTransformersMeta(type):
    """ Metaclass used to create classes with the additional
        option of marking their functions as 'required'.
    """
    def __new__(
            mcls: type, name: str, bases: Tuple[Any], namespace: Dict[Any, Any], /, **kwargs
    ) -> 'EnforceTransformersMeta':
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        setattr(cls, '__requiredtransformers__', set())
        for name, value in namespace.items():
            if getattr(value, "__isrequiredtransformer__", False):
                cls.__requiredtransformers__.add(name)

        return cls


class MsgTransformerMeta(ABCMeta, EnforceTransformersMeta):
    """ Mixin metaclass that combines abstract class functionality with
        additional functionality of the EnforceTransformersMeta metaclass
        that allows to enforce transformers.
    """
    pass


class MsgTransformer(metaclass=MsgTransformerMeta):
    """ Transformer class used to transform a specific type of json """
    __requiredtransformers__: Set[str]

    @property
    @abstractmethod
    def json_type(self) -> str:
        ...

    @abstractmethod
    def _validate_json_type(self, message: dict):
        ...

    def _ensure_transform(
        self, message: dict, transformers: Optional[List[Callable]] = None
    ) -> None:
        """ Ensures the required message transformers were
            called upon the generation of a new message.
        """
        required_transformers = self.__requiredtransformers__

        missing_transformers = None
        if required_transformers and not transformers:
            missing_transformers = required_transformers

        called = set()
        if transformers:
            for func in transformers:
                if isinstance(func, functools.partial):
                    called.add(func.func.__name__)
                else:
                    called.add(func.__name__)

                func(message=message)

        if required_transformers != called:
            missing_transformers = required_transformers.difference(called)

        if missing_transformers:
            raise MissingTransformersError(self.__class__.__name__, missing_transformers)

    def transform(
        self, message: dict, transformers: Optional[List[Callable]] = None
    ) -> Dict[str, Any]:
        """ Validates that all the 'required' transformers
            were used and returns the transformed message.
        """
        self._validate_json_type(message)
        self._ensure_transform(message, transformers)
        return message
