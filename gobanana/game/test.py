from game import Game, Directions


game = Game((5, 5))
print("Current game:")
print(game)
print()

print("Moves available to player")
print()
i = 1
for game in game.getmoves():
	print(f"Move {i}:")
	print(game)
	print()
	i+=1

if i == 1:
	print("There are no moves available")