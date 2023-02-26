from typing import Callable


class ProxyCallable:
    def __init__(self, sanitized_callable: Callable, *args):
        self.sanitized_callable = sanitized_callable
        self.args = args

    def __call__(self):
        self.sanitized_callable(*self.args)
