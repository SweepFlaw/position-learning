from .models.rnn import judgePosition as judgeByRNN
from .models.gru import judgePosition as judgeByGRU
from .lex import lexCode, saveName
from .embed import embedCSV, embeddedName

def getRecommendList(filename, modelType='GRU'):
  lexCode(filename)
  lexData = embedCSV(saveName)

  if modelType=='GRU':
    indexList = judgeByGRU(embeddedName)
  else:
    indexList = judgeByRNN(embeddedName)

  result = []
  for idx in indexList:
    result.append([lexData[idx][0], lexData[idx][1]])

  return result