import JanggiGame as Jg

game = Jg.JanggiGame()

# Move soldiers towards each other and then Blue captures Red pawn.


game.make_move('a10', 'a8')
game.make_move('c1', 'd3')
game.make_move('a8', 'a10')
game.make_move('d3', 'e1')
game.make_move('a10', 'a8')
game.make_move('e1', 'f3')
game.make_move('a1', 'a3')
game.make_move('a7', 'b7')
game.make_move('a4', 'b4')
game.make_move('a8', 'a3')
game.make_move('b4', 'a4')
game.make_move('a3', 'b3')
game.make_move('a4', 'b4')
game.make_move('b3', 'b2')
print(game.is_in_check('red'))

#game.make_move('a1', 'a3')
#game.make_move('a4', 'a5')
#game.make_move('a6', 'a5')
# It is now red's turn
#game.make_move('d10', 'e10')

# game.make_move( i4 , i5 )
# game.make_move( a6 , a5 )
# game.make_move( i5 , i6 )
#
# game.make_move( a5 , a4 )
#
#
# game.make_move( c10 , d8 )
# game.make_move( c1 , d3 )
# game.make_move( e7 , e6 )
# game.make_move( e4 , e5 )
# game.make_move( c7 , c6 )
# game.make_move( c4 , c5 )
# game.make_move( c6 , c5 )
# game.make_move( e5 , e6 )
# game.make_move( d8 , e6 )
#
# game.make_move( c10 , d8 )
#
# game.make_move( c1 , d3 )
# game.make_move( c7 , d7 )
# game.make_move( c4 , d4 )
# game.make_move( d8 , c6 )
# game.make_move( d8 , d8 )
# game.make_move( d3 , d6 )
# game.make_move( d3 , d3 )
# game.make_move( h10 , g8 )


#game.make_move('a7', 'a6')
#game.make_move('a7', 'b7')  # should return True
#print("True: ", move_result)
#blue_in_check = game.is_in_check('blue')  # should return False
#print("False but not implemented:", blue_in_check)
#game.make_move('a4', 'a5')  # should return True
#print("True: ", move_result)
#game.make_move('b7', 'b6')  # should return True
#print("True: ", move_result)
#game.make_move('b3', 'b6')  # should return False because it's an invalid move
#print("False: ", move_result)
#game.make_move('a1', 'a4')  # should return True
#print("True: ", move_result)
#game.make_move('c7', 'd7')  # should return True
#print("True: ", move_result)
#game.make_move('a4', 'a4')  # this will pass the Red's turn and return True
#print("True: ", move_result)