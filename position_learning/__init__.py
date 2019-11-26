from .rnn import judgePosition
from .lex import lexCode, saveName
from .embed import embedCSV, embeddedName

def getRecommendList(filename):
  lexCode(filename)
  lexData = embedCSV(saveName)
  indexList = judgePosition(embeddedName)

  result = []
  for idx in indexList:
    result.append([lexData[idx][0], lexData[idx][1]])

  return result