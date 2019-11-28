from torch import nn
import torch
from ..utils import readCSVNumber


class RNN(nn.Module):
  '''
  simple rnn structure
  '''
  def __init__(self, input_size, hidden_size, output_size):
    super(RNN, self).__init__()
    
    self.hidden_size = hidden_size
    
    self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
    self.i2o = nn.Linear(input_size + hidden_size, output_size)
    self.softmax = nn.LogSoftmax(dim=1)
      
  def forward(self, input, hidden):
    combined = torch.cat((input, hidden), 1)
    hidden = self.i2h(combined)
    output = self.i2o(combined)
    output = self.softmax(output)
    return output, hidden
  
  def initHidden(self):
    return torch.zeros(1, self.hidden_size)

n_input = 20
n_output = 2
n_hidden = 20
# load rnn data
rnn = RNN(n_input, n_hidden, n_output)
rnn.load_state_dict(torch.load('rnn_state'))
rnn.eval()


def getVarDiffSequence(data):
  '''
  data shape is different with gru, shape(token length, 1, embedding length)
  '''
  hidden = torch.zeros(1, n_hidden)

  predictList = []
  for i in range(data.size()[0]):
    result, hidden = rnn(data[i], hidden)
    if int(data[i][0][15]) == 1:
      predictList.append([i, float(result[0][1] - result[0][0])])
          
  predictList.sort(key = lambda x: x[1])
  return list(map(lambda x: x[0], predictList))


def heuristicSort(varSeq):
  length = len(varSeq)
  newSeq = []

  if length > 50:
    back = varSeq[-20:]
    back.reverse()
    newSeq += varSeq[0:20] + back + varSeq[20:-20]
  else:
    newSeq = varSeq
  return newSeq


def judgePosition(filename):
  data = readCSVNumber(filename)
  data = torch.FloatTensor(data)
  data = data.reshape(len(data), 1, -1)
  varSeq = getVarDiffSequence(data)
  varSeq = heuristicSort(varSeq)
  return varSeq