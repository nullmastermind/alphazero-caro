from __future__ import print_function
import pickle
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer
from const import Const
from policy_value_net_keras import PolicyValueNet


class Human(object):
  def __init__(self):
    self.player = None

  def set_player_ind(self, p):
    self.player = p

  def get_action(self, board):
    try:
      location = input("Your move: ")
      if isinstance(location, str):  # for python3
        location = [int(n, 10) for n in location.split(",")]
      move = board.location_to_move(location)
    except Exception as e:
      move = -1
    if move==-1 or move not in board.availables:
      print("Invalid move")
      move = self.get_action(board)
    return move

  def __str__(self):
    return "Human {}".format(self.player)


def run():
  n = Const.n_in_row
  width, height = Const.board_width, Const.board_height
  model_file = "./drive/models/{}_best_{}x{}_{}.model".format(Const.train_core, width, height, n)
  try:
    board = Board(width = width, height = height, n_in_row = n)
    game = Game(board)
    # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow
    best_policy = PolicyValueNet(width, height, model_file = model_file)
    mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct = 5, n_playout = 400)
    # human player, input your move in the format: 2,3
    human = Human()
    # set start_player=0 for human first
    game.start_play(human, mcts_player, start_player = 1, is_shown = 1)
  except KeyboardInterrupt:
    print("---\nQuit....")


if __name__=="__main__":
  run()
