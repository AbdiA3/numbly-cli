from random import randint
import typer


app = typer.Typer()

def generate_random_number():
  '''
  A function to generate a random 5 digit number 
  '''

  random_number = str(randint(10000, 99999))

  while len(set(random_number)) != 5:
    random_number = str(randint(10000, 99999))

  return random_number


def draw_result(verification_status):
  '''
  A function to print the resutlt in a stylish way
  '''

  status_grid = f'{typer.style(" "+str(verification_status[0])+" ", fg=typer.colors.WHITE, bg=typer.colors.GREEN, bold=True)} '  
  status_grid += f'{typer.style(" "+str(verification_status[1])+" ", fg=typer.colors.WHITE, bg=typer.colors.YELLOW, bold=True)} '
  status_grid += '\n'

  return status_grid


def verify(random_number, user_guess):
  '''
  Verify the user guessed number with the random number picked based on the rule.
  Rules:  
    status_1. The number of digits that are in the number and at the proper position
    status_2. The number of digits that are in the number, but not at the proper position
  '''

  status_1 = 0 
  status_2 = 0

  for idx, digit in enumerate(user_guess):
    if digit == random_number[idx]:
      status_1 += 1

  for digit in user_guess:
    if digit in random_number:
      status_2 += 1

  return [status_1, status_2]


def validate(user_guess):
  '''
  A function to validate the user input
  '''

  errors = []

  if len(user_guess) != 5:
    errors.append('You should enter a 5 digit number.')

  if user_guess[0] == '0':
    errors.append('The number cannot begin with 0.')

  if len(set(user_guess)) != 5:
    errors.append('Each digit in the number must be unique.')

  if errors:
    return (False, errors)

  return (True, None)


@app.command()
def main(
    rules: bool = typer.Option(False, help='Show the rules of the game.')
  ):
  '''
  The main function that will actually run the entire game.
  '''


  main_text = f'{typer.style("      ", bg=typer.colors.GREEN)}\n'
  main_text += f'{typer.style("Numbly.", fg=typer.colors.GREEN, bold=True)}\n'

  if rules:
    main_text += f'''
I will pick a random 5 digit number, then the game is to guess that number.
For each guess you make I will give you some hints, 2 hints to be exact.

Hints I will give you:  
  1. The number of digits that are in the number and at the proper position
  2. The number of digits that are in the number, but not at the proper position

NOTE: It is guaranteed that each digit in the randomly picked number is unique.

But the catch is you only get {typer.style(' 8 ', fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True)} shots to get it right.
'''

  main_text += f'{typer.style("I have picked a random number. Can you guess what it is?", fg=typer.colors.MAGENTA, bold=True)}\n'

  typer.echo(main_text)

  while True:
    random_number = generate_random_number()

    flag = False

    for rnd in range(8):
      prompt_text = f'{typer.style(" #"+str(rnd+1)+" ", bg=typer.colors.MAGENTA, fg=typer.colors.WHITE, bold=True)} Type your guess'
      user_guess = typer.prompt(prompt_text)

      while not validate(user_guess)[0]:
        errors = validate(user_guess)[1]

        for error in errors:
          typer.secho(error, bg=typer.colors.RED, fg=typer.colors.WHITE, bold=True)

        user_guess = typer.prompt(prompt_text)

      verification_status = verify(random_number, user_guess)
      status_grid = draw_result(verification_status)
      typer.echo(status_grid)

      if(user_guess == random_number):
        typer.secho(f'You got it!! {typer.style(" "+user_guess+" ", bg=typer.colors.GREEN, fg=typer.colors.WHITE, bold=True)} was the number.')
        flag = True
        break 

    if not flag:
      typer.secho(f"Shoot, you didn't get it. The number was {typer.style(' '+random_number+' ', bg=typer.colors.RED, fg=typer.colors.WHITE, bold=True)}.")

    typer.secho('_'*64+'\n', fg=typer.colors.GREEN, bold=True) 
    play_again_prompt_text = 'You got it now, but do you think you can do it again?'
    if not flag:
      play_again_prompt_text = 'Come on, don\'t give up easily. Give it another shot.'

    play_again_prompt_text += '\nEnter "Y" to play again, or any other key to exit.'
    play_again = typer.prompt(play_again_prompt_text)
    typer.secho('_'*64+'\n', fg=typer.colors.GREEN, bold=True) 

    if play_again.lower() != 'y':
      break


if __name__ == '__main__':
  app()