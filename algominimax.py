import math

# Constantes pour les joueurs
HUMAN = -1
AI = 1

# Initialisation du tableau de jeu
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# Fonction d'évaluation
def evaluate(board):
    for row in board:
        if sum(row) == 3:  # AI gagne
            return 1
        elif sum(row) == -3:  # HUMAN gagne
            return -1

    for col in range(3):
        if board[0][col] + board[1][col] + board[2][col] == 3:
            return 1
        elif board[0][col] + board[1][col] + board[2][col] == -3:
            return -1

    if board[0][0] + board[1][1] + board[2][2] == 3 or board[0][2] + board[1][1] + board[2][0] == 3:
        return 1
    elif board[0][0] + board[1][1] + board[2][2] == -3 or board[0][2] + board[1][1] + board[2][0] == -3:
        return -1

    return 0  # Match nul ou jeu en cours

# Vérifie si le jeu est terminé
def is_full(board):
    return all(cell != 0 for row in board for cell in row)

# Fonction Minimax avec élagage alpha-beta
def minimax(board, depth, player, alpha=-math.inf, beta=math.inf):
    score = evaluate(board)
    if score == 1 or score == -1 or is_full(board):
        return score

    if player == AI:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = AI
                    eval = minimax(board, depth + 1, HUMAN, alpha, beta)
                    board[i][j] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = HUMAN
                    eval = minimax(board, depth + 1, AI, alpha, beta)
                    board[i][j] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Mouvement optimal pour l'AI
def best_move(board):
    best_val = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = AI
                move_val = minimax(board, 0, HUMAN)
                board[i][j] = 0
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

# Affiche le tableau de jeu
def print_board(board):
    symbols = {HUMAN: 'O', AI: 'X', 0: ' '}
    for row in board:
        print("|".join(symbols[cell] for cell in row))
        print("-" * 5)

# Jeu principal
def play():
    while True:
        print_board(board)
        if evaluate(board) != 0 or is_full(board):
            break
        row, col = map(int, input("Entrez votre mouvement (ligne col): ").split())
        if board[row][col] == 0:
            board[row][col] = HUMAN
            if evaluate(board) == 0 and not is_full(board):
                ai_move = best_move(board)
                board[ai_move[0]][ai_move[1]] = AI

    print_board(board)
    result = evaluate(board)
    if result == 1:
        print("AI gagne !")
    elif result == -1:
        print("Vous gagnez !")
    else:
        print("Match nul !")

play()
