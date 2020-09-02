import functools
from collections import defaultdict
from pathlib import Path
from typing import List

import git


VERSION_REPO = defaultdict(dict)
VERSION_STACK = []
LOADING_FUNC = None


def get_func_version(target: str, options: List[str]):

    closest_below_target = None
    for o in options:
        if o <= target:
            if closest_below_target is None or o > closest_below_target:
                closest_below_target = o
    return closest_below_target


def version(*args, **kwargs):
    def func_version(func):
        decorator_args = args
        decorator_kwargs = kwargs


        if not hasattr(func, "canonical_name"):
            func.canonical_name = ".".join([__name__,func.__name__])
        _version = decorator_kwargs.get("v", "HEAD")
        VERSION_REPO[func.canonical_name][_version] = func

        repo = git.Repo(Path(__file__).parent)
        print("repo: ", repo)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if VERSION_STACK:
                _parent_version = VERSION_STACK[-1]

                best_version = get_func_version(
                    target=_parent_version,
                    options=list(VERSION_REPO[func.canonical_name].keys())
                )
                func_override = VERSION_REPO[func.canonical_name][best_version]
                return func_override(*args, **kwargs)
            else:
                VERSION_STACK.append(_version)
                result = func(*args, **kwargs)
                VERSION_STACK.pop(-1)
                return result
        return wrapper
    if len(args) == 1 and callable(args[0]):
        return func_version(args[0])
    else:
        return func_version


@version(v="0.0.1")
def adder(x, y):
    print("running Adder v1")
    return x + y


@version(v="0.0.2")
def adder(x, y):
    print("running Adder v2")
    return x + y


@version(v="0.0.1")
def doubler(n):
    print("running Doubler v1")
    return 2 * n


@version(v="0.0.2")
def number_cruncher(a, b):
    double_a = doubler(a)
    return adder(double_a, b)


if __name__ == "__main__":
    number_cruncher(2, 3)
