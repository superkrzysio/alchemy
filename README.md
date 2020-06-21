# alchemy

Skyrim alchemy calculator

#### The problem
You are carrying dozens of alchemical ingredients with undiscovered effects. There is a database on the internet with known effects and you know which to mix, but how to mix'em efficiently? To reveal the most effects with the least reagents used?

#### The solution
This.

#### Main scripts
* parse.py - parse the provided Wiki table into json, which includes ingrediends, their effects and some other stats
* owned.py - select random owned ingredients - simulate data entered by player
* application.py - the actual calculator, comparison of various algorithms

Possible TODO: 
* genetic algorithm
* skyrim extension to actually export the data
