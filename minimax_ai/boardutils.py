def initColumn(colNumber):
    column = [False]*64
    while (colNumber<64):
        column[colNumber] = True
        colNumber+=8
    return column

def initRow(rowNumber):
    row = [False]*64
    for i in range(rowNumber, rowNumber+8):
        #print(i, row[i])
        row[i] = True
        #print(row[i])
    return row

col1=col2=col7=col8=[]



numTiles = 64
numTilesPerRow = 8

#add one col# and row# variable for each row and col on board
col1 = initColumn(0) #[0,8,16,24,32,40,48,56] array of booleans in these spots
col2 = initColumn(1) #[1,9,17,25,33,41,49,57
col7 = initColumn(6)
col8 = initColumn(7)

row1 = initRow(0)
row2 = initRow(8)
row7 = initRow(48)
row8 = initRow(56)