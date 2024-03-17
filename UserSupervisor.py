import re


def string_input(question: str, input_type: str, options=None, prohibited=[]):
    while True:
        user_input = input(question)
        # select from a list
        if input_type == "select":
            if user_input not in options:
                print("Invalid input. Please enter one of the provided options.")
                print(f"Options are: %s" % options)
                continue
            else:
                return user_input
        # check regular expression
        if input_type == "regex" and not re.match(options, user_input):
            print("Invalid input. Please enter values that match the specified pattern.")
            print(f"The pattern is: %s" % options)
            continue
        # check if allowed input
        if user_input in prohibited:
            print("Invalid input. Please enter values not in the prohibited list.")
            print(f"Prohibited values are: %s" % prohibited)
            continue
        return user_input


def list_input(question: str, input_type: str, options=None, prohibited=[], separator=" "):
    while True:
        user_input = input(question).split(separator)
        # select from a list
        if input_type == "select":
            for option in user_input:
                if option not in options:
                    print("Invalid input. Please enter one of the provided options.")
                    print(f"Options are: %s" % options)
                    break
            else:
                return user_input
        # check if allowed input
        elif input_type == "except":
            for value in user_input:
                if value in prohibited:
                    print("Invalid input. Please enter values not in the prohibited list.")
                    print(f"Prohibited values are: %s" % prohibited)
                    break
            else:
                return user_input
        # check regular expression
        elif input_type == "regex":
            for value in user_input:
                if not re.match(options, value):
                    print("Invalid input. Please enter values that match the specified pattern.")
                    print(f"The pattern is: %s" % options)
                    break
                # check if allowed input
                elif value in prohibited:
                    print("Invalid input. Please enter values not in the prohibited list.")
                    break
            else:
                return user_input
        else:
            print("Invalid input type.")
