import time

# Define constants for players
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Function to create an empty Tic-Tac-Toe board
def create_board():
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]

# Function to print the Tic-Tac-Toe board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

# Function to check if the board is full
def is_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True

# Function to check if there's a winner
def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

# Minimax algorithm
def minimax(board, depth, maximizing_player):
    if check_winner(board, PLAYER_X):
        return 1
    if check_winner(board, PLAYER_O):
        return -1
    if is_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
        return min_eval

# Alpha-Beta Pruning algorithm
def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if check_winner(board, PLAYER_X):
        return 1
    if check_winner(board, PLAYER_O):
        return -1
    if is_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    eval = alpha_beta(board, depth + 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    eval = alpha_beta(board, depth + 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Function to get the best move using Minimax
def get_best_move_minimax(board):
    best_move = None
    best_value = float('-inf')

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_X
                move_value = minimax(board, 0, False)
                board[i][j] = EMPTY
                if move_value > best_value:
                    best_value = move_value
                    best_move = (i, j)
    return best_move

# Function to get the best move using Alpha-Beta Pruning
def get_best_move_alpha_beta(board):
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_X
                move_value = alpha_beta(board, 0, alpha, beta, False)
                board[i][j] = EMPTY
                if move_value > best_value:
                    best_value = move_value
                    best_move = (i, j)
    return best_move

# Function to play a game with a given algorithm
def play_game(algorithm):
    board = create_board()
    current_player = PLAYER_X  # AI starts first
    game_ongoing = True

    while game_ongoing:
        print_board(board)

        if current_player == PLAYER_X:  # AI's turn
            print(f"AI's move ({algorithm}):")
            start_time = time.time()
            if algorithm == "Minimax":
                move = get_best_move_minimax(board)
            else:
                move = get_best_move_alpha_beta(board)
            end_time = time.time()
            move_time = end_time - start_time
            print(f"AI Move Time: {move_time:.5f} seconds")

            if move:
                board[move[0]][move[1]] = PLAYER_X
        else:  # Human's turn
            print("Your move (row col):")
            move = input().split()
            row, col = int(move[0]), int(move[1])
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER_O
            else:
                print("Invalid move. Try again.")
                continue

        # Check for a winner
        if check_winner(board, current_player):
            print_board(board)
            print(f"{current_player} wins!")
            game_ongoing = False

        if is_full(board):
            print_board(board)
            print("It's a draw!")
            game_ongoing = False

        # Switch players
        current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X

    return board, move_time  # Return board and time taken for the AI move

# Function to benchmark the performance of Minimax and Alpha-Beta
def benchmark():
    total_games = 3  # Number of rounds
    ai_wins_minimax = 0
    player_wins_minimax = 0
    draws_minimax = 0
    ai_wins_ab = 0
    player_wins_ab = 0
    draws_ab = 0
    time_minimax = 0
    time_ab = 0

    for _ in range(total_games):
        print("\n--- Playing Game with Minimax ---")
        result_minimax, time_taken_minimax = play_game("Minimax")
        if check_winner(result_minimax, PLAYER_X):
            ai_wins_minimax += 1
        elif check_winner(result_minimax, PLAYER_O):
            player_wins_minimax += 1
        else:
            draws_minimax += 1
        time_minimax += time_taken_minimax

        print("\n--- Playing Game with Alpha-Beta Pruning ---")
        result_ab, time_taken_ab = play_game("Alpha-Beta")
        if check_winner(result_ab, PLAYER_X):
            ai_wins_ab += 1
        elif check_winner(result_ab, PLAYER_O):
            player_wins_ab += 1
        else:
            draws_ab += 1
        time_ab += time_taken_ab

    # Results with time comparison
    print("\nResults after 3 games:")
    print(f"Minimax - AI Wins: {ai_wins_minimax}, Player Wins: {player_wins_minimax}, Draws: {draws_minimax}")
    print(f"Alpha-Beta Pruning - AI Wins: {ai_wins_ab}, Player Wins: {player_wins_ab}, Draws: {draws_ab}")
    print(f"\nAverage AI Move Time for Minimax: {time_minimax / total_games:.5f} seconds")
    print(f"Average AI Move Time for Alpha-Beta Pruning: {time_ab / total_games:.5f} seconds")

# Run the benchmark
benchmark()

i want a top level GUI for this code