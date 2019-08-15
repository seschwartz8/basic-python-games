"""
Monte Carlo Tic-Tac-Toe Player by Sarah Schwartz
"""

# Note the following gui and complete Tic-Tac-Toe class were provided by Coursera
import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
NTRIALS = 100      # Number of trials to run
SCORE_CURRENT = 3.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


def mc_trial(board, player):
    """
    Plays a random game, modifies the board, and returns when the game is over
    """
    #For every empty space available, take a turn
    for dummy_empty in list(board.get_empty_squares()):
        #Randomly choose a space
        space = random.choice(board.get_empty_squares())
        #Move player's piece to that space
        board.move(space[0], space[1], player)
        #Switch player
        player = provided.switch_player(player)
        #Check if game is over
        if board.check_win() != None:
            return 

def mc_update_scores(scores, board, player):
    """
    Scores a completed board and updates the scores grid, where player is the machine player
    """
    #Create lists of coordinates the machine (current) and other player played on
    current_plays = []
    other_plays = []
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                current_plays.append((row, col))
            elif board.square(row, col) == provided.switch_player(player):
                other_plays.append((row, col))
        
    #Determine who won and score accordingly
    if board.check_win() == provided.DRAW: #if tie, do nothing
        return
    elif board.check_win() == player: #if machine (current) player won
        for c_play in current_plays:
            scores[c_play[0]][c_play[1]] += SCORE_CURRENT
        for o_play in other_plays:
            scores[o_play[0]][o_play[1]] -= SCORE_OTHER
    elif board.check_win() == provided.switch_player(player): #if other player won
        for c_play in current_plays: 
            scores[c_play[0]][c_play[1]] -= SCORE_CURRENT
        for o_play in other_plays:
            scores[o_play[0]][o_play[1]] += SCORE_OTHER

def get_best_move(board, scores):
    """
    Finds empty squares with maximum score and randomly returns one
    """
    #Create list of empty coordinates and their scores
    scores_of_empties = []
    for empty in list(board.get_empty_squares()):
        scores_of_empties.append(((scores[empty[0]][empty[1]]) , (empty[0], empty[1])))
    #Determine the highest score
    max_score = max(scores_of_empties)[0]
    #Create list of best options for next move
    move_options = []
    for empty_score in list(scores_of_empties):
        if empty_score[0] == max_score:
            move_options.append(empty_score[1])
    #Select tuple coordinates randomly from empty squares with highest score
    return random.choice(move_options)

def mc_move(board, player, trials):
    """
    Uses Monte Carlo simluations to return best move in form (row, column)
    """
    player_turn = player
    scores = [[0 for col in range(board.get_dim())]
                 for row in range(board.get_dim())]
    for trial in range(trials):
        #Clone the board
        sample_board = board.clone()
        #Trial random outcome on current board
        mc_trial(sample_board, player_turn)
        #Score random outcome
        mc_update_scores(scores, sample_board, player)
    #Determine best move
    final_move = get_best_move(board, scores)
    return final_move


poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)


