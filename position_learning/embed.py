import os
import csv
import sys

embeddedName = os.path.dirname(os.path.realpath(__file__)) + '/embedResult'

def readCSV(filename):
  with open(filename, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')

    result = []
    for row in csvreader:
      result.append(list(row))
    return result


def saveCSV(filename, data, sep='\t'):
  with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=sep)

    for row in data:
      csvwriter.writerow(row)

tokenKind = {
  'Keyword': 1,
  'Identifier': 2,
  'Literal': 3,
  'Comment': 4,
  'Punctuation': 5,
  'N/A': 6
}

cursorKind = {
  'VarDecl': 1,
  'DeclRefExpr': 2,
  'FunctionDecl': 3,
  'IntegerLiteral': 4,
  'CharacterLiteral': 5,
  'ParmDecl': 6
}


def embedCSV(filename):
  rawdata = list(filter(lambda x: len(x) == 6, readCSV(filename)))
  changeRow = lambda x: [int(x[0]), int(x[1]), int(x[2]), x[3], x[4], x[5]]
  data = []
  for row in rawdata:
    try:
      data.append(changeRow(row))
    except Exception as e:
      print(e)
      print(sys.exc_info()[0])

  print('read file ' + filename)

  varState = dict()
  embedded = []
  lineMax = int(data[-1][0])
  columnMax = 0
  offsetMax = int(data[-1][2])
  for row in data:
    if row[1] > columnMax:
      columnMax = row[1]
  
  for row in data:
    if (cursorKind.get(row[3], 0) == 1 or
        cursorKind.get(row[3], 0) == 3 or
        cursorKind.get(row[3], 0) == 6):
      varState[row[5]] = {
        'line': row[0] / lineMax,
        'column': row[1] / columnMax,
        'offset': row[2] / offsetMax
      }
    
    embedToken = []

    # the origin line
    # the origin column
    # the origin offset
    if varState.get(row[5]):
      embedToken.append(varState[row[5]]['line'])
      embedToken.append(varState[row[5]]['column'])
      embedToken.append(varState[row[5]]['offset'])
    else:
      embedToken.append(row[0] / lineMax)
      embedToken.append(row[1] / columnMax)
      embedToken.append(row[2] / offsetMax)
    
    # now line
    # now column
    # now offset
    embedToken.append(row[0] / lineMax)
    embedToken.append(row[1] / columnMax)
    embedToken.append(row[2] / offsetMax)

    # cursor kind
    # token kind
    # one-hot encoding
    positionInfo = 6
    encoding = 7
    for i in range(0, encoding * 2):
      embedToken.append(0)
    embedToken[positionInfo + cursorKind.get(row[3], 0)] = 1
    embedToken[positionInfo + encoding + tokenKind.get(row[4], 0)] = 1

    embedded.append(embedToken)
  
  # save result
  if len(embedded) == 0:
    return

  saveCSV(embeddedName, embedded)
