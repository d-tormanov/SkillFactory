board_template = """
BOARD TEMPLATE:

    1 | 2 | 3
    _________
    4 | 5 | 6
    _________
    7 | 8 | 9
"""


def choose_player() -> str:
    print('WELCOME TO "Tic Tac Toe" GAME !\n')
    while True:
        player = input('Please choose your player ("X" or "O"): ').upper()
        if player == 'X' or player == 'O':
            return player
        else:
            print('Please choose X or O.')


def player_move(current_player: str, game_board : list):
    while True:
        # print(board_template)
        move = int(input(f"Player '{current_player}' choose your cell to move (1-9): ")) - 1
        if 0 <= move <= 9:
            row, col = divmod(move, 3)
            if game_board[row][col] == ' ':
                game_board[row][col] = current_player
                return game_board

            else:
                print('Please, choose another cell !')
        else:
            print('Sorry, that is not a valid cell !')



def show_board(game_board : list) -> None:

    line = 0
    print()
    for row in game_board:
        print(' | '.join(row))
        line += 1
        if line != 3:
            print('_' * 10)


def check_draw(game_board : list) -> bool:
    return all([cell != ' ' for row in game_board for cell in row])


def check_win(current_player: str, game_board : list) -> bool:
    # check row
    for row in game_board:
        if all([cell == current_player for cell in row]):
            return True

    # check column
    for column in range(3):
        if all(game_board[row][column] == current_player for row in range(3)):
            return True

    # check diagonal
    if game_board[0][0] == current_player and game_board[1][1] == current_player and game_board[2][2] == current_player:
        return True
    if game_board[0][2] == current_player and game_board[1][1] == current_player and game_board[2][0] == current_player:
        return True

    return False



def play_game():

    board = [[" " for _ in range(3)] for _ in range(3)]

    current_player = choose_player()
    print(board_template)
    while True:
        board = player_move(current_player, board)
        show_board(board)

        if check_win(current_player, board):
            print('')
            print("  "* 10 + f"PLAYER '{current_player}' WIN !!!")
            break

        if check_draw(board):
            print('')
            print('  '* 10 + 'GAME OVER: DRAW !!!')
            break

        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == '__main__':
    play_game()