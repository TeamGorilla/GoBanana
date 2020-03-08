import torch
from torch import nn
from torch import functional as F


class Generator(nn.Module):
    def __init__(self, board_shape, num_metrics):
        super().__init__()
        self.board_shape = board_shape
        self.num_metrics = num_metrics

    def forward(self, noise: torch.Tensor, metrics: torch.Tensor):
        pass
