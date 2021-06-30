# OCR_P4 Chess Tournament Manager

### How to install libs in requirements.txt :

Open your CMD and type : 

```shell 
pip install -r requirements.txt
```

This way you will install all the packages needed to run this program

### How to run this program?
To run this program type :
```shell
python main.py
```
### How to use this program ?
```
Press "1" to create a new tournament.
Press "2" to create a new player.
Press "3" to manage the tournament of your choice
Press "4" to show the list of all players.
Press "5" to change a player rating.
Press "6" to show the list of all tournaments.
Press "0" to quit the program.
```
First thing you'll need to do is to create a tournament by pressing 1 and following the instruction.
```
Press "1" to create a new tournament.
```

Then you can create all the players you want with option number 2 and follow the instruction
```
Press "2" to create a new player.
```

After that you can press 3 to manage the tournament of your choice, adding players inside it. Then you can just Press 4 to create the next round, once it's finished you can press 5 to enter the scores, then 4 again for the next round and so on.
```
Type '1' to add a player to the tournament
Type '2' to show the list of players by alphabetical order
Type '3' to show the list of players by rating order
Type '4' to create the next round
Type '5' to enter the scores
Type '6' to show scores
Type '7' to show matches 
Type '8' to show rounds
Type '0' to go back to the main menu
```


### How to generate a report with flake8-html
You can generate a report with flake8-html using this line in the CMD

```shell
flake8 --format=html --htmldir=flake-report
```
If you are inside a virtual environment don't forget to exclude it like this :
```shell
flake8 --format=html --htmldir=flake-report --exclude ./venv/
```