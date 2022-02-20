# Numbly

> Abdi Adem | 2022

![Screenshot 1](./screenshots/screenshot_1.png)

My friends used to play a game so similiar with Wordle, but with numbers, even before Worlde was a thing.
The idea of the game is 2 players each pick a random 5 digit number, then the game is to guess one another's number.
For each guess a player makes the opponent gives them some hints, 2 hints to be exact.
Hints:
  
  1. The number of digits that are in the number and at the proper position
  2. The number of digits that are in the number, but not at the proper position

But here we will play against the computer.

Made using [Typer](https://typer.tiangolo.com/).

To get started:

```sh
git clone https://github.com/AbdiA3/numbly.git
cd numbly
pip install typer # UNIX: pip3 install typer 
python main.py # UNIX: python3 main.py
```

If you want to see the rules you can add `--rules` flag.
```sh
python main.py --rules # UNIX: python3 main.py --rules
```

When installing Typer it will automatically install the following packages.
```sh
click
colorama
typer
```