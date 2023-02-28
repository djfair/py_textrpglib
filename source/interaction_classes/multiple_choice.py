from typing import Callable


class MultipleChoice:
    """Class for storing and presenting a multiple choice situation to a player."""

    def __init__(
        self,
        message: str,
        options: list[str],
        outcomes: list[list[Callable] | Callable],
    ):
        self.message = message
        self.options = options
        self.outcomes = outcomes

    def __call__(self):
        try:
            if len(self.message) != 0:
                print(self.message)
                print(" ")
            for i, option in enumerate(self.options):
                print(f"\t{i + 1}. {option}")
            print(" ")
            chosen_option = (
                int(input(f"\t> What you want to say? [1-{len(self.options)}]: ")) - 1
            )
            print(" ")
            chosen_outcomes = self.outcomes[chosen_option]
            if isinstance(chosen_outcomes, list):
                for outcome in chosen_outcomes:
                    outcome()
            else:
                chosen_outcomes()
        except IndexError:
            print("You must choose from the options!")
            print(" ")
            self()
        except ValueError:
            print("You must choose from the options!")
            self()
