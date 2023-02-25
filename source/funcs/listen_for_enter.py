"""listen_for_enter:
Function presents prompt to play to press ENTER.

Args:
    *outcomes: any Callable object to be executed after player presses ENTER
    message: prompt to be shown after 'Press ENTER', e.g. '... to continue'"""

from typing import Callable


def listen_for_enter(*outcomes: Callable, message: str = "to continue") -> None:
    """Function presents prompt to play to press ENTER.

    Args:
        *outcomes: any Callable object to be executed after player presses ENTER
        message: prompt to be shown after 'Press ENTER', e.g. '... to continue'"""

    input(f"\t> Press ENTER {message}")
    for outcome in outcomes:
        outcome()
