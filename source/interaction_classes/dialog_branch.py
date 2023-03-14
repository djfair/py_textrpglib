from typing import Callable


class DialogBranch:
    """Class for storing and presenting dialog options to a player."""

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
        def show_message() -> None:
            if len(self.message) != 0:
                print(self.message)
                print(" ")
            return

        def show_options() -> None:
            for i, option in enumerate(self.options):
                print(f"\t{i + 1}. {option}")
            print(" ")
            return

        def choose_option() -> int:
            chosen_option = input(
                f"\t> What you want to say? [1-{len(self.options)}]: "
            )
            print(" ")
            return int(chosen_option) - 1

        def lookup_outcome_by_index(index: int) -> list[Callable] | Callable:
            return self.outcomes[index]

        def call_outcomes_in_order(chosen_outcomes: list[Callable]) -> None:
            for callable in chosen_outcomes:
                callable()
            return

        def call_outcome(chosen_outcome: Callable) -> None:
            chosen_outcome()
            return

        try:
            show_message()
            show_options()
            chosen_option_index = choose_option()
            chosen_outcome = lookup_outcome_by_index(chosen_option_index)
            if isinstance(chosen_outcome, list):
                call_outcomes_in_order(chosen_outcome)
            elif isinstance(chosen_outcome, Callable):
                call_outcome(chosen_outcome)

        except IndexError:
            print("You must choose from the options!")
            print(" ")
            self()
        except ValueError:
            print("You must choose from the options!")
            self()
