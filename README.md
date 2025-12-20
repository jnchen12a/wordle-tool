# wordle-tool
...so I thought to myself, "If I'm so bad at Wordle, why not have a computer play for me?"

## How to use the Tool
The command line interface takes in two types of clues:
1. Gray clues: used to input information about gray letters
    * Simply type in the gray letters, lowercase.
    * The order of the letters does not matter
2. Yellow and Green clues: used to input information about yellow and green letters
    * Type in yellow letters in lowercase, green letters in uppercase, gray letters as -
    * Here, the order of the letters must match what you see in the Wordle interface, and you must input 5 characters.

Example:

![An image of an example guess.](./example.png)

This guess will take two clues to properly input into the tool (they can be input in any order):
* (Gray clue): ot
* (Yellow and Green clue): -Ra-e

Most guesses will take two clues to input all the information obtained from the guess.

You can also input multiple clues at the same time, seperated by a comma (,).
* Ex: ot, -Ra-e

## Suggested Guesses
After each new clue is entered, the tool will calculate what it thinks is the next best guess. Multiple possible canditates will be generated, each with a score, the higher the better. For the next guess, the user can either:
* Choose the first word in the given list (often the word with the highest score and, thus, the best next guess), or
* Choose any word from the given list.