from __future__ import print_function
import sys

sys.path.append('..')
from board_game_base.game import Game
from tictoctoe.logic import Board
import numpy as np

"""
Game class implementation for the game of TicTacToe.
Based on the OthelloGame then get_game_ended() was adapted to new rules.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloGame by Surag Nair.
"""


class TicTacToeGame(Game):
  def __init__(self, n = 3):
    super().__init__()
    self.n = n

  def get_init_board(self):
    # return initial board (numpy board)
    b = Board(self.n)
    return np.array(b.pieces)

  def get_board_size(self):
    # (a,b) tuple
    return self.n, self.n

  def get_action_size(self):
    # return number of actions
    return self.n*self.n+1

  def get_next_state(self, board, player, action):
    # if player takes action on board, return next (board,player)
    # action must be a valid move
    if action==self.n*self.n:
      return board, -player
    b = Board(self.n)
    b.pieces = np.copy(board)
    move = (int(action/self.n), action%self.n)
    b.execute_move(move, player)
    return b.pieces, -player

  def get_valid_moves(self, board, player):
    # return a fixed size binary vector
    valids = [0]*self.get_action_size()
    b = Board(self.n)
    b.pieces = np.copy(board)
    legal_moves = b.get_legal_moves(player)
    if len(legal_moves)==0:
      valids[-1] = 1
      return np.array(valids)
    for x, y in legal_moves:
      valids[self.n*x+y] = 1
    return np.array(valids)

  def get_game_ended(self, board, player):
    # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
    # player = 1
    b = Board(self.n)
    b.pieces = np.copy(board)

    if b.is_win(player):
      return 1
    if b.is_win(-player):
      return -1
    if b.has_legal_moves():
      return 0
    # draw has a very little value
    return 1e-4

  def get_canonical_form(self, board, player):
    # return state if player==1, else return -state if player==-1
    return player*board

  def get_symmetries(self, board, pi):
    # mirror, rotational
    assert (len(pi)==self.n**2+1)  # 1 for pass
    pi_board = np.reshape(pi[:-1], (self.n, self.n))
    result = []
    for i in range(1, 5):
      for j in [True, False]:
        new_b = np.rot90(board, i)
        new_pi = np.rot90(pi_board, i)
        if j:
          new_b = np.fliplr(new_b)
          new_pi = np.fliplr(new_pi)
        result += [(new_b, list(new_pi.ravel())+[pi[-1]])]
    return result

  def string_representation(self, board):
    # 8x8 numpy array (canonical board)
    return board.tostring()


def display(board):
  n = board.shape[0]
  print("   ", end = "")
  for y in range(n):
    print(y, "", end = "")
  print("")
  print("  ", end = "")
  for _ in range(n):
    print("-", end = "-")
  print("--")
  for y in range(n):
    print(y, "|", end = "")  # print the row #
    for x in range(n):
      piece = board[y][x]  # get the piece to print
      if piece==-1: print("X ", end = "")
      elif piece==1: print("O ", end = "")
      else:
        if x==n:
          print("-", end = "")
        else:
          print("- ", end = "")
    print("|")
  print("  ", end = "")
  for _ in range(n):
    print("-", end = "-")
  print("--")
