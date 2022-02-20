from random import randint
import typer


app = typer.Typer()

def generate_random_number():
  '''
  A function to generate a random 5 digit number 
  '''

  return str(randint(10000, 99999))


def draw_result(validation_status, user_guess):
  '''
  A function to print the resutlt in a stylish way
  '''

  status_grid = ''

  for idx, status in enumerate(validation_status):
    if status == 1:
      status_grid += f'{typer.style(" "+user_guess[idx]+" ", fg=typer.colors.WHITE, bg=typer.colors.GREEN, bold=True)} '
    elif status == 0:
      status_grid += f'{typer.style(" "+user_guess[idx]+" ", fg=typer.colors.WHITE, bg=typer.colors.YELLOW, bold=True)} '
    else:
      status_grid += f'{typer.style(" "+user_guess[idx]+" ", fg=typer.colors.BLACK, bg=typer.colors.WHITE, bold=True)} '

  status_grid += '\n'

  return status_grid


def verify(random_number, user_guess):
  '''
  Verify the user guessed number with the random number picked based on the rule.

    - if the current digit of the user guessed number is the same as the digit at 
      the same position in the random number picked, then status of that position is 1
    
    - if the current digit of the user guessed number is not the same as the digit at 
      the same position in the random number picked, but the digit exists in the random 
      number picked, then status of that position is 0
    
    - if the current digit of the user guessed number is not in the random number picked,
      then status of that position is -1
  '''

  status = [None for i in range(5)]

  visited_digits = { digit: random_number.count(digit) for digit in random_number }


  for idx in range(5):
    if user_guess[idx] == random_number[idx] and visited_digits[user_guess[idx]] > 0:
      status[idx] = 1
      visited_digits[user_guess[idx]] -= 1
    elif user_guess[idx] in random_number and visited_digits[user_guess[idx]] > 0:
      status[idx] = 0
      visited_digits[user_guess[idx]] -= 1
    else:
      status[idx] = -1

  return status


def validate(user_guess):
  '''
  A function to validate the user input
  '''

  errors = []

  if len(user_guess) != 5:
    errors.append('You should enter a 5 digit number.')

  numbers = None
  try:
    with open('numbers.json') as f:
      raw_numbers = f.read()
      numbers = json.loads(raw_numbers)
  except:
    print('An error has occured')


  if user_guess.lower() not in numbers:
    errors.append(f'{user_guess} is not in the number list.')

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


  main_text = f'{typer.style("                        ", bg=typer.colors.GREEN)}\n'
  main_text += f'{typer.style("A CLI version of Numbly.", fg=typer.colors.GREEN, bold=True)}\n'

  if rules:
    main_text += f'''
The rules are very simple.
  - I pick a random 5 digit number
  - You guess that number
  - After you guess a number, I will give you hints.
  - The hints are:
    - If I show you a gray box, then the digit at 
      that position is not in the number
    - If I show you a yellow box, then the digit 
      at that position is in the number, but in a different 
      position
    - If I show you a green box, then the digit at 
      that position is in the number and at the same position

But the catch is you only get {typer.style(' 6 ', fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True)} shots to get it right.
'''

  main_text += f'{typer.style("I have picked a random number. Can you guess what it is?", fg=typer.colors.MAGENTA, bold=True)}\n'

  typer.echo(main_text)


  while True:
    random_number = generate_random_number().upper()

    flag = False

    for rnd in range(6):
      prompt_text = f'{typer.style(" #"+str(rnd+1)+" ", bg=typer.colors.MAGENTA, fg=typer.colors.WHITE, bold=True)} Type your guess'
      user_guess = typer.prompt(prompt_text).upper()

      while not validate(user_guess)[0]:
        errors = validate(user_guess)[1]

        for error in errors:
          typer.secho(error, bg=typer.colors.RED, fg=typer.colors.WHITE, bold=True)

        user_guess = typer.prompt(prompt_text).upper()

      validation_status = verify(random_number, user_guess)
      status_grid = draw_result(validation_status, user_guess)
      typer.echo(status_grid)

      if(validation_status.count(1) == 5):
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