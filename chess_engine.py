# gamestate, move log
class Game_State():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR",],
            ]
        self.whitetomove = True
        self.move_log = []
        self.move_functions = {'P': self.pawnmoves, 'R': self.rookmoves, 'N': self.knightmoves, 
                      'B': self.bishopmoves, 'Q': self.queenmoves, 'K': self.kingmoves}
        self.whiteking_location = (7, 4)
        self.blackking_location = (0, 4)
        self.checkmate = False
        self.stalemate = False

        self.castle_log = []
        self.queensidecastle_white = True
        self.kingsidecastle_white = True
        self.queensidecastle_black = True
        self.kingsidecastle_black = True

        self.enpassantpossible = ()

    def make_move(self, move):
        if move.movedpiece != "--":
            self.board[move.first_row][move.first_column] = "--"
            self.board[move.second_row][move.second_column] = move.movedpiece
            #делает ход, меняя местами два кликнутых значения в board
            if move.castling:
                if move.second_column - move.first_column == 2:
                    self.board[move.second_row][move.second_column-1] = self.board[move.second_row][move.second_column+1]
                    self.board[move.second_row][move.second_column+1] = '--'
                else:
                    self.board[move.second_row][move.second_column+1] = self.board[move.second_row][move.second_column-2]
                    self.board[move.second_row][move.second_column-2] = '--'
            # Дополнение к обычному ходу, если рокировка

            if move.enpassant:
                self.board[move.first_row][move.second_column] = '--'
            # Дополнение к ходу, если анпасан
            if move.movedpiece[1] == 'P' and abs(move.first_row - move.second_row) == 2:
                self.enpassantpossible = ((move.first_row + move.second_row)//2, move.first_column)#возможность сделать анпасан после этого хода
            else:
                self.enpassantpossible = ()
            # назначение клетки, в которую теоретически можно сделать анпасан
            
            
            self.move_log.append(move)
            #В мувлог записывается класс мув (координаты первой, второй нажатых клеток, двинутой и съеденой фигуры)
            self.whitetomove = not self.whitetomove

            if move.movedpiece == "wK":
                self.whiteking_location = (move.second_row, move.second_column)
                self.queensidecastle_white = False
                self.kingsidecastle_white = False
            elif move.movedpiece == "bK":
                self.blackking_location = (move.second_row, move.second_column)
                self.queensidecastle_black = False
                self.kingsidecastle_black = False
            #отслеживание королей для проверки на шах и возможность рокировки    

            if move.first_row == 7 and move.first_column == 0 and move.movedpiece == 'wR':
                self.queensidecastle_white = False
            if move.first_row == 7 and move.first_column == 7 and move.movedpiece == 'wR':
                self.kingsidecastle_white = False
            if move.first_row == 0 and move.first_column == 0 and move.movedpiece == 'bR':
                self.queensidecastle_black = False
            if move.first_row == 0 and move.first_column == 7 and move.movedpiece == 'bR':
                self.kingsidecastle_black = False
            #отслеживание ладей для проверки на возможность рокировки

            self.castle_log.append((self.queensidecastle_white, self.kingsidecastle_white, self.queensidecastle_black, self.kingsidecastle_black,))
            #пополнение мувлога возможности рокировки

            #промоушн пешки(тут можно реализовать вопрос к игроку во что превращать пешку, по умолчанию Q)
            if (move.movedpiece == 'wP' and move.second_row == 0) or (move.movedpiece == 'bP' and move.second_row == 7):
                self.board[move.second_row][move.second_column] = move.movedpiece[0]+'Q'
    
    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.first_row][move.first_column] = move.movedpiece
            self.board[move.second_row][move.second_column] = move.capturedpiece
            #Выдергивает последний элемент в мувлоге(объект класс) и на основе него отменяет ход

            if move.castling:
                if move.second_column - move.first_column == 2:
                    self.board[move.second_row][move.second_column+1] = self.board[move.second_row][move.second_column-1]
                    self.board[move.second_row][move.second_column-1] = '--'
                else:
                    self.board[move.second_row][move.second_column-2] = self.board[move.second_row][move.second_column+1]
                    self.board[move.second_row][move.second_column+1] = '--'
            # Дополнение к отмене обычного хода, если рокировка

            if move.enpassant:
                self.board[move.second_row][move.second_column] = '--'
                self.board[move.first_row][move.second_column] = move.capturedpiece
                self.enpassantpossible = (move.second_row, move.second_column)
            #Отмена анпасана

            if move.movedpiece[1] == 'P' and abs(move.first_row - move.second_row) == 2:
                self.enpassantpossible = ()
            #значения клетки теоретически возможного анпасана
            
            self.whitetomove = not self.whitetomove
            
            if move.movedpiece == "wK":
                self.whiteking_location = (move.first_row, move.first_column)
            elif move.movedpiece == "bK":
                self.blackking_location = (move.first_row, move.first_column)
            # отмена координат королей

        if len(self.castle_log) > 1:
            last = self.castle_log[-2]
            self.queensidecastle_white = last[0]
            self.kingsidecastle_white = last[1]
            self.queensidecastle_black = last[2]
            self.kingsidecastle_black = last[3]
            del self.castle_log[-1]
            #откат мувлога возможности рокировок и присвоение предыдущих значений

    

    def validmoves(self, possible_moves): #фильтрует ходы с возможных до валидных в переданном списке(пропускает рокировку без фильтра)
        temp_empassanpossible = self.enpassantpossible
        moves = possible_moves
        castlingmoves = self.castlemoves(self.whiteking_location[0], self.whiteking_location[1]) if self.whitetomove else self.castlemoves(self.blackking_location[0], self.blackking_location[1])#рокировка не проходит проверку ниже, тк вызывает рекурсию, имеет проверку внутри себя
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i]) #Делает "фантомный ход" для каджого из возможного в списке
            self.whitetomove = not self.whitetomove
            if self.check():                      
                moves.remove(moves[i])  #если проверка на шах прошла, то удаляет текущий ход из списка возможных                 
            self.whitetomove = not self.whitetomove
            self.undo_move() #отменяет "фантомный ход"
        if len(moves) == 0: #Мат или Пат
            if self.check():
                self.checkmate = True
            else:
                self.stalemate = True
        self.enpassantpossible = temp_empassanpossible
        return moves+castlingmoves

    def check(self): #проверка на шах
        if self.whitetomove:
            return self.square_under_attack(self.whiteking_location[0], self.whiteking_location[1])
        else:
            return self.square_under_attack(self.blackking_location[0], self.blackking_location[1])

    def square_under_attack(self, row, column): # проверка под атакой ли клетка 
        self.whitetomove = not self.whitetomove #смена хода для расчета ходов оппонента
        opponent_moves = self.possiblemoves() #список потенциальных возможных ходов оппонента ПОСЛЕ нашего хода
        self.whitetomove = not self.whitetomove # после генерации ходов оппонента вернуть ход обратно к себе
        for move in opponent_moves:
            if move.second_row == row and move.second_column == column: # данная клетка под атакой одной из фигур оппонента
                return True
        return False

    def possiblemoves(self): #возвращает все теоретически возможные ходы для всех фигур на доске
        moves = []
        for row in range(8):
            for column in range(8):
                color = self.board[row][column][0]
                if (color == "w" and self.whitetomove) or (color == "b" and not self.whitetomove):
                    piece = self.board[row][column][1]    
                    self.move_functions[piece](row, column, moves)
        return moves

    #функции для ходов каждой из фигур
    def pawnmoves(self, row, column, moves):#пешка без промоушена
        if self.whitetomove:
            if self.board[row-1][column] == '--':
                moves.append(move((row, column),(row-1, column), self.board))
                if row == 6 and self.board[row-2][column] == '--':
                    moves.append(move((row, column),(row-2, column), self.board))
                    #ход вперед+ ход через клетку со стартовой позиции

            if column-1 >= 0: #проверка левого края борта
                if self.board[row-1][column-1][0] == 'b':
                    moves.append(move((row, column),(row-1, column-1), self.board))
                elif (row-1, column-1) == self.enpassantpossible:
                    moves.append(move((row, column),(row-1, column-1), self.board, enpassant=True))
            if column+1 <= 7: #проверка правого края борта
                if self.board[row-1][column+1][0] == 'b':
                    moves.append(move((row, column),(row-1, column+1), self.board))
                elif (row-1, column+1) == self.enpassantpossible:
                    moves.append(move((row, column),(row-1, column+1), self.board, enpassant=True))
                
        else:# для черных
            if self.board[row+1][column] == '--':
                moves.append(move((row, column),(row+1, column), self.board))
                if row == 1 and self.board[row+2][column] == '--':
                    moves.append(move((row, column),(row+2, column), self.board))
                    #ход вперед+ ход через клетку со стартовой позиции

            if column-1 >= 0: #проверка левого края борта
                if self.board[row+1][column-1][0] == 'w':
                    moves.append(move((row, column),(row+1, column-1), self.board))
                elif (row+1, column-1) == self.enpassantpossible:
                    moves.append(move((row, column),(row+1, column-1), self.board, enpassant=True))
            if column+1 <= 7: #проверка правого края борта
                if self.board[row+1][column+1][0] == 'w':
                    moves.append(move((row, column),(row+1, column+1), self.board))
                elif (row+1, column+1) == self.enpassantpossible:
                    moves.append(move((row, column),(row+1, column+1), self.board, enpassant=True))

    def rookmoves(self, row, column, moves):#Сканирует каждую из сторон
            opponentcolor = 'b' if self.whitetomove else 'w'
            alliescolor = 'w' if self.whitetomove else 'b'
            for i in range(1,row+1):#вверх
                if self.board[row-i][column][0] == opponentcolor:
                        moves.append(move((row, column),(row-i, column), self.board))
                        break
                elif self.board[row-i][column][0] == alliescolor:
                        break
                moves.append(move((row, column),(row-i, column), self.board))
            for i in range(1,7-row+1):#вниз
                if self.board[row+i][column][0] == opponentcolor:
                        moves.append(move((row, column),(row+i, column), self.board))
                        break
                elif self.board[row+i][column][0] == alliescolor:
                        break
                moves.append(move((row, column),(row+i, column), self.board))
            for i in range(1,column+1):#влево
                if self.board[row][column-i][0] == opponentcolor:
                        moves.append(move((row, column),(row, column-i), self.board))
                        break
                elif self.board[row][column-i][0] == alliescolor:
                        break
                moves.append(move((row, column),(row, column-i), self.board))
            for i in range(1,7-column+1):#вправо
                if self.board[row][column+i][0] == opponentcolor:
                        moves.append(move((row, column),(row, column+i), self.board))
                        break
                elif self.board[row][column+i][0] == alliescolor:
                        break
                moves.append(move((row, column),(row, column+i), self.board))

    def knightmoves(self, row, column, moves):#5х5 вокруг себя на теореме пифагора
        opponentcolor = 'b' if self.whitetomove else 'w'
        for r in range(row-2, row+3):
            if 0<=r<=7:
                for c in range(column-2, column+3):
                    if 0<=c<=7:     
                        if (row-r)**2+(column-c)**2 == 5:
                            if self.board[r][c][0] == opponentcolor or self.board[r][c][0] == '-':
                                moves.append(move((row, column),(r, c), self.board))
     
    def bishopmoves(self, row, column, moves):# питон его знает, в бубен стукнуть надо, чтобы работало
        opponentcolor = 'b' if self.whitetomove else 'w'
        alliescolor = 'w' if self.whitetomove else 'b'
        for i in range(1,7):
            if 0 <= row-i <= 7 and 0 <= column-i <= 7:
                if self.board[row-i][column-i][0] == opponentcolor:
                    moves.append(move((row, column),(row-i, column-i), self.board))
                    break
                elif self.board[row-i][column-i][0] == alliescolor:
                    break
                moves.append(move((row, column),(row-i, column-i), self.board))
        
        for i in range(1,7):
            if 0 <= row+i <= 7 and 0 <= column+i <= 7:
                if self.board[row+i][column+i][0] == opponentcolor:
                    moves.append(move((row, column),(row+i, column+i), self.board))
                    break
                elif self.board[row+i][column+i][0] == alliescolor:
                    break
                moves.append(move((row, column),(row+i, column+i), self.board))

        for i in range(1,7):
            if 0 <= row-i <= 7 and 0 <= column+i <= 7:
                if self.board[row-i][column+i][0] == opponentcolor:
                    moves.append(move((row, column),(row-i, column+i), self.board))
                    break
                elif self.board[row-i][column+i][0] == alliescolor:
                    break
                moves.append(move((row, column),(row-i, column+i), self.board))
        
        for i in range(1,7):
            if 0 <= row+i <= 7 and 0 <= column-i <= 7:
                if self.board[row+i][column-i][0] == opponentcolor:
                    moves.append(move((row, column),(row+i, column-i), self.board))
                    break
                elif self.board[row+i][column-i][0] == alliescolor:
                    break
                moves.append(move((row, column),(row+i, column-i), self.board))
        
    def queenmoves(self, row, column, moves):#Ладья+слон
        self.rookmoves(row, column, moves)
        self.bishopmoves(row, column, moves)

    def kingmoves(self, row, column, moves):#рассматривает 3х3 клетки вокруг себя, добавляет, если пусто или враг + рокировка
        opponentcolor = 'b' if self.whitetomove else 'w'
        for r in range(row-1, row+2):
            if 0<=r<=7:
                for c in range(column-1, column+2):
                    if 0<=c<=7:     
                        if self.board[r][c][0] == opponentcolor or self.board[r][c][0] == '-':
                            moves.append(move((row, column),(r, c), self.board))

    def castlemoves(self, row, column):
        castlemoves = []
        if self.whitetomove:
            if self.kingsidecastle_white:
                if not self.check():
                    if self.board[row][column+1] == '--' and self.board[row][column+2] == '--':
                        if not self.square_under_attack(row, column+1) and not self.square_under_attack(row, column+2):
                           castlemoves.append(move((row, column),(row, column+2), self.board, castling=True))
            if self.queensidecastle_white:
                if not self.check():
                    if self.board[row][column-1] == '--' and self.board[row][column-2] == '--' and self.board[row][column-3] == '--':
                        if not self.square_under_attack(row, column-1) and not self.square_under_attack(row, column-2):
                           castlemoves.append(move((row, column),(row, column-2), self.board, castling=True))
        else:
            if self.kingsidecastle_black:
                if not self.check():
                    if self.board[row][column+1] == '--' and self.board[row][column+2] == '--':
                        if not self.square_under_attack(row, column+1) and not self.square_under_attack(row, column+2):
                           castlemoves.append(move((row, column),(row, column+2), self.board, castling=True))
            if self.queensidecastle_black:
                if not self.check():
                    if self.board[row][column-1] == '--' and self.board[row][column-2] == '--' and self.board[row][column-3] == '--':
                        if not self.square_under_attack(row, column-1) and not self.square_under_attack(row, column-2):
                           castlemoves.append(move((row, column),(row, column-2), self.board, castling=True))
        return castlemoves

        

class move():# Первая и вторая нажатые клетки, двинутая и съеденая фигура опциональные параметры для рокировки и анпасана
    def __init__(self, first_SQ, second_SQ, board, castling=False, enpassant=False): #откуда(1,1), куда(2,2), gamestate.board
        self.first_row = first_SQ[0]
        self.first_column = first_SQ[1]
        self.second_row = second_SQ[0]
        self.second_column = second_SQ[1]
        self.movedpiece = board[self.first_row][self.first_column]
        self.capturedpiece = board[self.second_row][self.second_column]
        self.moveID = self.first_row * 1000 + self.first_column * 100 + self.second_row * 10 + self.second_column
        # moveID - уникальный идентификатор хода из клетки 1 в клетку 2
        self.castling=castling
        self.enpassant=enpassant
        if self.enpassant:
            self.capturedpiece = 'bP' if self.movedpiece == 'wP' else 'wP'
        
    
    def __eq__(self, other):
        if isinstance(other, move):
            return self.moveID == other.moveID
    #питон не может сравнить два объекта класс, он видит каждый ход(объект класс) как уникальные
    #объекты, поэтому дополняем базовый метод сравнения, ходы он будет сравнивать через moveID

    ranks_to_rows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0,}
    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}
    files_to_columns = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7,}
    columns_to_files = {value: key for key, value in files_to_columns.items()}
    # библиотеки для перевода координат из board в стандартные шахматные координаты
    # board[1][1]->b7
    def get_rankfile(self, row, column): #возвращает строку с кординатой клетки 'e2'
        return self.columns_to_files[column] + self.rows_to_ranks[row]

    def get_movenotation(self): #Дальше реализовать тут все общепринятые правила записи ходов
        return self.get_rankfile(self.first_row, self.first_column) + self.get_rankfile(self.second_row, self.second_column)