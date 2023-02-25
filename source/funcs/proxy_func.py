from typing import Callable


class ProxyFunc:
    def __init__(self, aliased_callable: Callable, *args):
        self.aliased_callable = aliased_callable
        self.args = args

    def __call__(self):
        self.aliased_callable(*self.args)
