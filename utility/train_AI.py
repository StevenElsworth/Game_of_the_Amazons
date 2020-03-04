from game_backend import Game
import torch
import numpy as np

class InitialConvolutionBlock(torch.nn.Module):
    """
    Define a single convolution block with batch normalisation and a Relu activation function.
    """
    def __init__(self, input=3, output=128, kernel=3):
        super(InitialConvolutionBlock, self).__init__() #allows access to inherited methods
        self.conv = torch.nn.Conv2d(input, output, kernel) #input, output, kernel_size
        self.bn = torch.nn.BatchNorm2d(128) # batch normalisation on output (good for relu activation)

    def forward(self, s):
        s = s.view(-1, 3, 6, 7) # batch_size x channel x x_len x y_len
        s = torch.nn.functional.relu(self.bn(self.conv(s)))
        return s

class ResidualBlock(torch.nn.Module):
    """
    Define a Residual block using PyTorch
    """
    def __init__(self, dimension= 128):
        super(ResidualBlock, self).__init__() #allows access to inherited methods
        self.conv1 = torch.nn.Conv2d(dimension, dimension, kernel_size=3)
        self.bn1 = torch.nn.BatchNorm2d(dimension)
        self.conv2 = torch.nn.Conv2d(dimension, dimension)
        self.bn2 = torch.nn.BatchNorm2d(dimension)

    def forward(self, s):
        residual = s
        s = torch.nn.functional.relu(self.bn1(self.conv1(s)))
        s = torch.nn.functional.relu(self.bn2(self.conv2(s)) + residual) # include residual loop
        return s

class FinalNeuralNetwork(torch.nn.Module):
    """
    Define the final section of the network which is mainly dense. Split policy and value.
    """
    def __init__(self):
        super(FinalNeuralNetwork, self).__init__() #allows access to inherited methods

        self.v_conv = torch.nn.Conv2d(128, 3, kernel_size=1)
        self.v_bn = torch.nn.BatchNorm2d(3)
        self.v_linear1 = torch.nn.Linear(300, 32)
        self.v_linear2 = torch.nn.Linear(32, 1)

        self.p_conv = torch.nn.Conv2d(128, 3, kernel_size=1)
        self.p_bn = torch.nn.BatchNorm2d(32)
        self.p_linear = torch.nn.Linear(300, 7)
        self.p_softmax = torch.nn.LogSoftmax(dim=1)

    def forward(self, s):
        v = torch.nn.functional.relu(self.v_bn(self.v_conv(s))) # value head
        v = v.view(-1, 300)  # batch_size X channel X height X width
        v = torch.nn.functional.relu(self.v_linear1(v))
        v = torch.tanh(self.v_linear2(v))

        p = torch.nn.functional.relu(self.p_bn(self.p_conv(s))) # policy head
        p = p.view(-1, 300)
        p = self.p_linear(p)
        p = self.softmax(p).exp()
        return p, v


class AmazonNet(torch.nn.Module):
    """
    Define network using Torch
    """
    def __init__(self, ):
        super(AmazonNet, self).__init__() #allows access to inherited methods
        self.conv = InitialConvolutionBlock()
        for block in range(19):
            setattr(self, "res_%i" % block,ResidualBlock())
        self.final = FinalNeuralNetwork()

    def forward(self, s):
        s = self.conv(s)
        for block in range(19):
            s = getattr(self, "res_%i" % block)(s)
        s = self.final(s)
        return s

class Loss(torch.nn.Module):
    """
    Calculate loss according to deep mind paper
    """
    def __init__(self):
        super(Loss, self).__init__()

    def forward(self, y_value, value, y_policy, policy):
        value_error = (value - y_value) ** 2
        policy_error = torch.sum((-policy*
                                (1e-8 + y_policy.float()).float().log()), 1)
        total_error = (value_error.view(-1).float() + policy_error).mean()
        return total_error


def board_to_data(game):
    """
    Function maps the current board state to a large tensor containings only 0's
    and 1's. The data is of dimension 10 x 10 x 4 where the board is of size 10 x 10.
    Data(:,:,0) is location of fire, Data(:,:,1) is location of player 1's pieces,
    Data(:,:,2) is location of player 2's pieces and Data(:,:,3) is all zeros if it is
    player 2's turn and 1's if it is player 1's turn.
    """
    Data = np.zeros([10,10,4]).astype(int)
    for i, tile in enumerate(game.board):
        if tile.to_string() == '0':
            Data[i%10, i//10, 0] = 1 #flame
        elif tile.to_string() == '1':
            Data[i%10, i//10, 1] = 1 #player 1
        elif tile.to_string() == '2':
            Data[i%10, i//10, 2] = 1 #player2

    if game.turn == '1':
        Data[:,:,3] = np.ones(10,10)

    return Data

def data_to_board(data):
    pass



# https://towardsdatascience.com/from-scratch-implementation-of-alphazero-for-connect4-f73d4554002a
# https://github.com/plkmo/AlphaZero_Connect4
