from torch import nn
import torch
import os
from ..utils import readCSVNumber

# torch.cuda.is_available() checks and returns a Boolean True if a GPU is available, else it'll return False
is_cuda = torch.cuda.is_available()

# If we have a GPU available, we'll set our device to GPU. We'll use this device variable later in our code.
if is_cuda:
  device = torch.device("cuda")
else:
  device = torch.device("cpu")

class GRUNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, n_layers, drop_prob=0.2):
        super(GRUNet, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        
        self.gru = nn.GRU(input_dim, hidden_dim, n_layers, batch_first=True, dropout=drop_prob)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()
        
    def forward(self, x, h):
        out, h = self.gru(x, h)
        out = self.fc(self.relu(out[:,-1]))
        return out, h
    
    def initHidden(self, batch_size):
        weight = next(self.parameters()).data
        hidden = weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device)
        return hidden

n_input = 20
n_output = 2
n_hidden = 20
n_layers = 1
gru = GRUNet(n_input, n_hidden, n_output, n_layers)
gru.load_state_dict(torch.load(os.path.dirname(os.path.realpath(__file__)) + '/gru_state'))
gru.eval()


def getVarDiffSequence(data):
  '''
  data shape is different with rnn, shape(token length, 1, 1, embedding length)
  '''
  hidden = gru.initHidden(1)

  predictList = []
  for i in range(data.size()[0]):
    result, hidden = gru(data[i], hidden)
    if int(data[i][0][0][15]) == 1:
      predictList.append([i, float(result[0][1] - result[0][0])])
          
  predictList.sort(key = lambda x: x[1])
  return list(map(lambda x: x[0], predictList))


def judgePosition(filename):
  data = readCSVNumber(filename)
  data = torch.FloatTensor(data)
  data = data.reshape(len(data), 1, 1, -1)
  varSeq = getVarDiffSequence(data)
  return varSeq