import tkinter as tk
from tkinter import messagebox
import math


PLAYER = 'X'
AI = 'O'
EMPTY = '_'


# Evaluate the board and return a score
def evaluate(board):
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == AI:
                return +10
            elif board[row][0] == PLAYER:
                return -10

    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == AI:
                return +10
            elif board[0][col] == PLAYER:
                return -10

    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == AI:
            return +10
        elif board[0][0] == PLAYER:
            return -10

    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == AI:
            return +10
        elif board[0][2] == PLAYER:
            return -10

    return 0

def isMovesLeft(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                return True
    return False

def minimax(board, depth, isMax):
    score = evaluate(board)
    if score == 10:
        return score
    if score == -10:
        return score

    if isMovesLeft(board) == False:
        return 0

    if isMax:
        best = -1000
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = AI
                    best = max(best, minimax(board, depth + 1, not isMax))
                    board[row][col] = EMPTY
        return best

    else:
        best = 1000
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = PLAYER
                    best = min(best, minimax(board, depth + 1, not isMax))
                    board[row][col] = EMPTY
        return best

def findBestMove(board):
    bestVal = -1000
    bestMove = (-1, -1)
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = AI
                moveVal = minimax(board, 0, False)
                board[row][col] = EMPTY
                if moveVal > bestVal:
                    bestRow = row
                    bestCol = col
                    bestVal = moveVal
    return (bestRow, bestCol)



def change_player():
    global player
    player = AI if player == PLAYER else PLAYER

def callback(r,c):
    global player
    global stop_game
    if board[r][c] == EMPTY and stop_game == False:
        b[r][c].config(text=player, state='disabled', disabledforeground=colour[player])
        if player == PLAYER:
            board[r][c] = PLAYER
            if winning(board, PLAYER):
                messagebox.showinfo("Tic-Tac-Toe", "'X' Wins!")
                stop_game = True
            elif isMovesLeft(board) == False:
                messagebox.showinfo("Tic-Tac-Toe", "It's a Tie!")
                stop_game = True
            else:
                change_player()
                move = findBestMove(board)
                board[move[0]][move[1]] = AI
                b[move[0]][move[1]].config(text=AI, state='disabled', disabledforeground=colour[AI])
                if winning(board, AI):
                    messagebox.showinfo("Tic-Tac-Toe", "'O' Wins!")
                    stop_game = True
                elif isMovesLeft(board) == False:
                    messagebox.showinfo("Tic-Tac-Toe", "It's a Tie!")
                    stop_game = True
                change_player()


def winning(board, p):
    winningConditions = [
        [board[0][0], board[0][1], board[0][2]], [board[1][0], board[1][1], board[1][2]], [board[2][0], board[2][1], board[2][2]], 
        [board[0][0], board[1][0], board[2][0]], [board[0][1], board[1][1], board[2][1]], [board[0][2], board[1][2], board[2][2]], 
        [board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]

    return [p,p,p] in winningConditions

root = tk.Tk()
root.title("Tic Tac Toe")
b = []
player = 'X'
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
global stop_game
stop_game = False
colour = {'X' : 'dark red', 'O' : 'dark green'}
font = {'X' : ('Helvetica', 50, 'bold'), 'O' : ('Helvetica', 50, 'bold')}
for i in range(3):
    row = []
    for j in range(3):
        row.append(tk.Button(root, text=' ', width=25, height=10,
                             command=lambda r=i, c=j: callback(r, c)))
        row[-1].grid(row=i, column=j)
    b.append(row)

tk.mainloop()