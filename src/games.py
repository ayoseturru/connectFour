from utils import *


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    action, state = argmax(game.successors(state), lambda ((a, s)): min_value(s, -infinity, infinity, 0))
    return action


class game:
    def legal_moves(self, state):
        abstract

    def make_move(self, move, state):
        abstract

    def utility(self, state, player):
        abstract

    def terminal_test(self, state):
        return not self.legal_moves(state)

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        print state

    def successors(self, state):
        return [(move, self.make_move(move, state))
            for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class connect_four(game):
    def __init__(self, h=7, v=6, k=4):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, 1) for x in range(1, h + 1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)

    def legal_moves(self, state):
        return state.moves

    def make_move(self, move, state):
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        if self.new_move(move[1] + 1):
            moves.append((move[0], move[1] + 1))
        return Struct(to_move=self.next_player(state.to_move),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def new_move(self, row):
        if row > self.v:
            return False
        else:
            return True

    def display(self, state):
        board = state.board
        for y in range(self.v, 0, -1):
            print y, "|",
            for x in range(1, self.h + 1):
                print board.get((x, y), '.'), "|",
            print
        print "   ",
        for x in range(1, self.h + 1):
            print x, "|",
        print

    def k_in_row(self, board, move, player, (delta_x, delta_y)):
        x, y = move
        n = 0
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1
        return n >= self.k

    def compute_utility(self, board, move, player):
        if (self.k_in_row(board, move, player, (0, 1)) or
            self.k_in_row(board, move, player, (1, 0)) or
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))):
            return if_(player == 'X', + 1, -1)
        else:
            return 0

    def terminal_test(self, state):
        if state.utility != 0:
            return 1
        elif len(state.moves) == 0:
            return -1
        return False

    def utility(self, state, player):
        if player == 'X':
            return state.utility
        if player == 'O':
            return -state.utility

    def next_player(self, current_player):
        if current_player == "X":
            return "O"
        else:
            return "X"