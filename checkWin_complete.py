# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 08:45:20 2019

@author: Samuel Fisher, Intern
Johns Hopkins University Applied Physics Laboratory
"""

#Display who won and add to win counter
def whoWin(x,End,Xwin,Owin): 
    Xwin = 0
    Owin = 0
    if x == 1:
        End.configure(text="Player 1 has won!", background = 'white')
        Xwin = 1
    elif x == 2:
        End.configure(text="Player 2 has won!", background = 'white')
        Owin = 1
    else:
        End.configure(text="Nobody Wins", background = 'white')
    gameover = 1
    L = [Xwin,Owin,gameover]
    return L

#Check if there is a three in a row
#If there is a win, a display which team one and count that win
def checkWin(place,AIturn,End,Xwin,Owin,turn, aiSkill): 
    if place[1] == place[0] and place[0] == place[2] and place[1] != 0:
        print ("Player",place[1]," wins")
        return whoWin(place[1],End,Xwin,Owin)
    if place[0] == place[3] and place[0] == place[6] and place[0] != 0:
        print ("Player",place[0]," wins")
        return whoWin(place[0],End,Xwin,Owin)
    if place[0] == place[4] and place[0] == place[8] and place[0] != 0:
        print ("Player",place[0]," wins")
        return whoWin(place[0],End,Xwin,Owin)
    if place[1] == place[4] and place[1] == place[7] and place[1] != 0:
        print ("Player",place[1]," wins")
        return whoWin(place[1],End,Xwin,Owin)
    if place[2] == place[4] and place[2] == place[6] and place[2] != 0:
        print ("Player",place[2]," wins")
        return whoWin(place[2],End,Xwin,Owin)
    if place[2] == place[5] and place[2] == place[8] and place[2] != 0:
        print ("Player",place[2]," wins")
        return whoWin(place[2],End,Xwin,Owin)
    if place[3] == place[4] and place[3] == place[5] and place[3] != 0:
        print ("Player",place[3]," wins")
        return whoWin(place[3],End,Xwin,Owin)
    if place[6] == place[7] and place[8] == place[6] and place[6] != 0:
        print ("Player",place[6]," wins")
        return whoWin(place[7],End,Xwin,Owin)
    tie = 1
    for i in place:
        if i == 0:
            tie = 0
    if tie == 1:
        return whoWin(3,End,Xwin,Owin)
        
    return [0,0,0]

#Check who won without calling whoWin
#Necessary for MiniMax
def checkWin2(place):
    if place[1] == place[0] and place[0] == place[2] and place[1] != 0:
        return place[1]
    if place[0] == place[3] and place[0] == place[6] and place[0] != 0:
        return place[0]
    if place[0] == place[4] and place[0] == place[8] and place[0] != 0:
        return place[0]
    if place[1] == place[4] and place[1] == place[7] and place[1] != 0:
        return place[1]
    if place[2] == place[4] and place[2] == place[6] and place[2] != 0:
        return place[2]
    if place[2] == place[5] and place[2] == place[8] and place[2] != 0:
        return place[2]
    if place[3] == place[4] and place[3] == place[5] and place[3] != 0:
        return place[3]
    if place[6] == place[7] and place[8] == place[6] and place[6] != 0:
        return place[6]
    tie = 1
    for i in place:
        if i == 0:
            tie = 0
    if tie == 1:
        return 0
        
    return [0,0,0]

########################### start of PART A OF PART 2 OF HW5 ###########################
#Check possibilities for wins in the next move
def checkWinPos(place):

    player1WinCombs = determineWinConditions(place, 1)
    player2WinCombs = determineWinConditions(place, 2)

    # Check if AI has a win and if so take it
    if(len(player2WinCombs)):
        return player2WinCombs[0]
    # Check if User has a win and if so block him by taking the spot
    elif(len(player1WinCombs)):
        return player1WinCombs[0]

   #Create checkWinPos here
    return None

def determineWinConditions(place, numAssociatedPlayer):
    possibleWinRowList = []
    win3inRowPositions = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)];
    for winRowPos in win3inRowPositions:
        rowVals = [place[winRowPos[0]], place[winRowPos[1]], place[winRowPos[2]]]
        # if only 2 positions in this row were taken up by the same player
        if(sum(rowVals) == 2*numAssociatedPlayer and rowVals.count(numAssociatedPlayer) == 2):
            # then the place with the 0 value is the winning position
            possibleWinRowList.append(winRowPos[rowVals.index(0)])
    return possibleWinRowList
########################### end of PART A OF PART 2 OF HW5 ###########################

########################### start of PART B OF PART 2 OF HW5 ###########################
def determineTerminalState(place, numAssociatedPlayer):
    win3inRowPositions = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)];
    for winRowPos in win3inRowPositions:
        rowVals = [place[winRowPos[0]], place[winRowPos[1]], place[winRowPos[2]]]
        # if only 3 positions in this row were taken up by the same player
        sumRowVals = sum(rowVals)
        countRowVals = rowVals.count(numAssociatedPlayer)
        if(sumRowVals == 3*numAssociatedPlayer and countRowVals == 3):
           return True
    return False


def getSpotsOnBoard(board):
    return [i for i, spot in enumerate(board) if spot == 0]

def minimaxalg(board, playerNum):

    # get available spots
    availableSpots = getSpotsOnBoard(board)

    # if the num availableSpots are 0 then it is a draw
    if(len(availableSpots) == 0):
        return (None, 0)

    # the current state was done by the last player so let's determine if what
    # they did caused them to win
    prevPlayer = 1 if (playerNum == 2) else 2
    if(determineTerminalState(board, prevPlayer)):
        if (prevPlayer == 1):
            return (None, 1)
        elif (prevPlayer == 2):
            return (None, -1)


    # to cache all scores we've recursively seen in the subtrees
    scoreObjArr = []
    # check if terminal state
    for availableSpot in availableSpots:

        # change the current spot to be taken in this example
        board[availableSpot] = playerNum

        # now it's the next person's turn to play
        nextPlayer = 2 if (playerNum == 1) else 1
        # recurse
        scoreObj = minimaxalg(board, nextPlayer)
        # the result score is a tuple of the spot that was taken and the score
        # the recursive calls gives us
        resultScoreObj = (availableSpot, scoreObj[1])
        scoreObjArr.append(resultScoreObj)

        # turn it back to an empty
        board[availableSpot] = 0


    if(playerNum == 1): # X player which is the human which we want to max
        # get the highest score in the cache list and return it
        highestScoreObj = None
        for scoreObj in scoreObjArr:
            if(highestScoreObj == None):
                highestScoreObj = scoreObj
                continue
            if(scoreObj[1] > highestScoreObj[1]):
                highestScoreObj = scoreObj
        return highestScoreObj

    if (playerNum == 2):  # O player which is the AI which we want to min
        # get the lowest score in the cache list and return it
        lowestScoreObj = None
        for scoreObj in scoreObjArr:
            if (lowestScoreObj == None):
                lowestScoreObj = scoreObj
                continue
            if (scoreObj[1] < lowestScoreObj[1]):
                lowestScoreObj = scoreObj
        return lowestScoreObj
########################### end of PART B OF PART 2 OF HW5 ###########################
