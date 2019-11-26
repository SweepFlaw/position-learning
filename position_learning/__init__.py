from .rnn import judgePosition
from .lex import lexCode, saveName
from .embed import embedCSV, embeddedName

def getRecommendList(filename):
  lexCode(filename)
  embedCSV(saveName)
  return judgePosition(embeddedName)