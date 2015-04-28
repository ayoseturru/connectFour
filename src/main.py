import games


def show_game_result(game, state):
    print "-------------------------------"
    if game.terminal_test(state):
        print "Game over, " + game.next_player(state.to_move) + " wins..."
    else:
        print "Game over, draw..."
    print "-------------------------------"


def update_state(game, state, col):
    for item in list(state.moves):
        if str(item[0]) == str(col):
            return game.make_move(item, state)
    print "Invalid move..."
    return state


def game_start(game, level=2):
    state = game.initial
    while True:
        print "Your turn, ", game.to_move(state)
        game.display(state)
        if game.to_move(state) == 'O':
            state = update_state(game, state, raw_input("In which column do you want to play?: "))
        else:
            print "Thinking..."
            state = game.make_move(games.alphabeta_search(state, game, level), state)
        print "-------------------------------"
        if game.terminal_test(state):
            game.display(state)
            show_game_result(game, state)
            return


def human_game_start(game):
    state = game.initial
    while True:
        print "Your turn, ", game.to_move(state)
        game.display(state)
        state = update_state(game, state, raw_input("In which column do you want to play?: "))
        print "-------------------"
        if game.terminal_test(state):
            game.display(state)
            show_game_result(game, state)
            return


def run(game):
    while True:
        if raw_input("Human play? (y/n):") == "y":
            human_game_start(game)
        elif raw_input("Are you ready to lose? (y/n):") == "y":
            game_start(game)
        if raw_input("Do you want to play again? (y/n):") != "y":
            exit(0)


run(games.connect_four())