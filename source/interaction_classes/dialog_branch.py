from typing import Callable


class DialogBranch:
    """Class for storing and presenting dialog options to a player."""

    def __init__(
        self,
        message: str,
        options: list[str],
        outcomes: list[list[Callable]],
    ):
        self.message = message
        self.options = options
        self.outcomes = outcomes

    def __call__(self):
        print(self.message)
        for i, option in enumerate(self.options):
            print(f"\t{i + 1}. {option}")
        chosen_option = (
            int(input(f"\t> What you want to do? [1-{len(self.options) + 1}]: ")) - 1
        )
        chosen_option = int(chosen_option) - 1
        chosen_outcomes = self.outcomes[chosen_option]
        for outcome in chosen_outcomes:
            outcome()
