def prompt_choice(prompt_text: str, choices: list):
    choice = None

    while not choice:
        choice = input(f"{prompt_text}: {choices}>")
        if choice not in choices:
            choice = None

    return choice


def prompt_confirm(prompt_text: str) -> bool:

    choice = input(f'{prompt_text}: (Y|N)')

    return choice == 'Y'
