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
		"""
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        
        """        
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		scores = 0
		check_point = 3 if terminal else 2
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
