# CIS 511 A5 Code

`main.py` implements the interpreter in B2 and the RAM programs in B1.

## How to run the code

Environment: Python 3

The command `python main.py` will print out a few test cases and return values of concatenation/reverse/triple RAM programs.

If you prefer online browser-based IDE, you can copy the code to https://www.online-python.com/ and run it there.
The code should be runnable with the default settings of the website.

## How to add new test cases

There are three functions `test_concatenate()`, `test_reverse()` and `test_triple()` in `main.py`.
Inside each of the function, there is a variable called `lst_inputs` that defines test cases for each RAM program.
You can add new test cases by adding new strings at the end of `lst_inputs`.

## Input format of the interpreter

Checkout the function `read_me_for_the_explanation_of_the_interpreters_input_format()`