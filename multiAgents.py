from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if depth == 0 or terminal:
        newScores = game_state.get_scores(terminal)
        return (newScores if newScores is not None else 0), None  # Ensure valid return

    moves = game_state.get_moves()
    if not moves:
        return 0, None  # No moves left, return neutral value

    if maximizingPlayer:
        value, best_move = float('-inf'), None
        for move in moves:
            new_state = game_state.get_new_state(move)
            new_value, _ = minimax(new_state, depth - 1, False, alpha, beta)
            if new_value > value:
                value, best_move = new_value, move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value, best_move
    else:
        value, best_move = float('inf'), None
        for move in moves:
            new_state = game_state.get_new_state(move)
            new_value, _ = minimax(new_state, depth - 1, True, alpha, beta)
            if new_value < value:
                value, best_move = new_value, move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_move

	# return value, best_move

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if depth == 0 or terminal:
        scores = game_status.get_negamax_scores(terminal)
        return (scores if scores is not None else 0) * turn_multiplier, None  # Ensure valid return

    moves = game_status.get_moves()
    if not moves:
        return 0, None  # No moves left, return neutral value

    value, best_move = float('-inf'), None
    for move in moves:
        new_state = game_status.get_new_state(move)
        new_value, _ = negamax(new_state, depth - 1, -turn_multiplier, -beta, -alpha)
        new_value = -new_value
        if new_value > value:
            value, best_move = new_value, move
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value, best_move

    #return value, best_move
