# -*- coding: utf-8 -*-


class GameStatus:


	def __init__(self, board_state, turn_O):

		self.board_state = board_state
		self.turn_O = turn_O
		self.oldScores = 0

		self.winner = ""


	def is_terminal(self):
		if self.get_moves():
			return False
		final_score = self.get_scores(True)
		if final_score is None:
			final_score = 0
		if final_score > 0:
			self.winner = "Human"
		elif final_score < 0:
			self.winner = "AI"
		else:
			self.winner = "Draw"
		return True	

		

	def get_scores(self, terminal):

		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2
		#Search through rows
		for i in range(rows):
			#search through each coloumn in row
			for j in range(cols):
				#If we found a filled spot we need to check its surroundings for a filled spot. 
				if self.board_state[i,j] != 0:
					symbol_at_tile = self.board_state[i,j]
					print(symbol_at_tile)
					if (i + 2 < rows) and (self.board_state[i + 1, j] != 0) and (symbol_at_tile == self.board_state[i + 1, j]): #check x + 1 dir AND check if symbols match AND check if we can check that way
						#run 2nd if only if we did find a 2 in a row.
						if (self.board_state[i + 2, j] != 0) and (symbol_at_tile == self.board_state[i + 2, j]):
							scores += symbol_at_tile
						
					elif (i-2 >= 0) and (self.board_state[i - 1, j] != 0) and (symbol_at_tile == self.board_state[i - 1, j]): #check x - 1 direction
						if (self.board_state[i - 2, j] != 0) and (symbol_at_tile == self.board_state[i - 2, j]):
							scores += symbol_at_tile

					elif (j + 2 < cols) and (self.board_state[i, j + 1] != 0) and (symbol_at_tile == self.board_state[i, j + 1]): #check y + 1 direction
						if (self.board_state[i, j + 2] != 0) and (symbol_at_tile == self.board_state[i, j + 2]):
							scores += symbol_at_tile
						
					elif (j-2 >=0) and (self.board_state[i, j - 1] != 0) and (symbol_at_tile == self.board_state[i, j - 1]): #check y - 1 direction
						if (self.board_state[i,j - 2] != 0) and (symbol_at_tile == self.board_state[i, j - 2]):
							scores += symbol_at_tile
					
					elif (i - 2 >= 0 and j + 2 < cols) and (self.board_state[i - 1, j + 1] != 0) and (symbol_at_tile == self.board_state[i - 1, j + 1]):#Up left
						if (self.board_state[i - 2, j + 2] != 0) and (symbol_at_tile == self.board_state[i - 2, j + 2]):
							scores += symbol_at_tile

					elif (i + 2 < rows and j + 2 < cols) and (self.board_state[i + 1, j + 1] != 0) and (symbol_at_tile == self.board_state[i + 1, j + 1]):#Up right
						if (self.board_state[i + 2, j + 2] != 0) and (symbol_at_tile == self.board_state[i + 2, j + 2]):
							scores += symbol_at_tile

					elif (i - 2 >= 0 and j - 2 >= 0) and (self.board_state[i - 1, j - 1] != 0) and (symbol_at_tile == self.board_state[i - 1, j - 1]):#Down left
						if (self.board_state[i - 2, j - 2] != 0) and (symbol_at_tile == self.board_state[i - 2, j - 2]):
							scores += symbol_at_tile

					elif (i + 2 < rows and j - 2 >= 0) and (self.board_state[i + 1, j - 1] != 0) and (symbol_at_tile == self.board_state[i + 1, j - 1]):#Down right 
						if (self.board_state[i + 2, j - 2] != 0) and (symbol_at_tile == self.board_state[i + 2, j - 2]):
							scores += symbol_at_tile

		return scores				
						
		
		for row in self.board_state:
			if abs(sum(row)) == check_point:
				scores += sum(row)
		return scores if scores is not None else 0
		

	def get_negamax_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
		return self.get_scores(terminal) * -1
	    

	def get_moves(self):
		moves = []
		rows, cols = self.board_state.shape
		for i in range(rows):
			for j in range(cols):
				if self.board_state[i,j] == 0:
					moves.append((i,j))
		
		
		return moves


	def get_new_state(self, move):
		x, y = move
		if self.board_state[x,y] != 0:
			return None
		new_board_state = self.board_state.copy()
		new_board_state[x,y] = 1 if self.turn_O else -1
		return GameStatus(new_board_state, not self.turn_O)
