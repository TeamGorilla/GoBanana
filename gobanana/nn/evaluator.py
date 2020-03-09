import torch
from torch import nn
from torch import functional as F

class Evaluator(nn.Module):
    def __init__(self, board_shape, num_metrics):
        super().__init__()
        self.board_shape = board_shape
        self.num_metrics = num_metrics
        
        # define layers, currently, this is a simple NN with two hidden layers
        self.fc1 = nn.Linear(board_shape, 2 * num_metrics)
        self.fc2 = nn.Linear(2 * num_metrics, num_metrics)
        

    def forward(self, one_hot_board):
        
        # input to first FC layer, use Relu as activation function 
        x = F.relu(self.fc1(one_hot_board))
        # compute output layer
        x = self.fc2(x)
        
        return (x)
