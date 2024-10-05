###       Input and display        ###

import pygame
import chess_engine, AI
pygame.init()

WIDTH = HEIGHT = 800
SQ_SIZE = WIDTH//8
screen = pygame.display.set_mode((WIDTH+WIDTH*0.1+WIDTH*0.5, HEIGHT+WIDTH*0.1))
Game_State = chess_engine.Game_State()
FPS = 15
clock = pygame.time.Clock()

WHITE_SQ = (104, 113, 130)
DARK_SQ = (41, 46, 59)
BORDER_COLOR = (37, 40, 53)
SQ_BORDER_COLOR = (200, 200, 200)

images = {}
def load_imgages(): #запускается 1 раз до главного цикла while  
    pieces = ("bB", "bK", "bN", "bP", "bQ", "bR", "wB", "wK", "wN", "wP", "wQ", "wR", 'valid_move', 'valid_move2')
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (SQ_SIZE,SQ_SIZE))
    # библиотека key = называние фигуры, value = путь до картинки



def draw_board(screen):
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH+WIDTH*0.1, HEIGHT+WIDTH*0.1))
    pygame.draw.rect(screen, WHITE_SQ, (0+WIDTH*0.05, 0+WIDTH*0.05, WIDTH, HEIGHT))
    for column in range(8):
        for row in range(0, 8, 2):
                if column % 2 != 0:
                    pygame.draw.rect(screen, DARK_SQ, (row*SQ_SIZE+WIDTH*0.05, column*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE))
                else:
                    pygame.draw.rect(screen, DARK_SQ, (row*SQ_SIZE+SQ_SIZE+WIDTH*0.05, column*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != "--":
                screen.blit(images[piece], (column*SQ_SIZE+WIDTH*0.05, row*SQ_SIZE+WIDTH*0.05))
                #вызывает key из библиотеки images, возвращает картинку фигуры по координатам

def draw_board_for_black(screen):
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH+WIDTH*0.1, HEIGHT+WIDTH*0.1))
    pygame.draw.rect(screen, DARK_SQ, (0+WIDTH*0.05, 0+WIDTH*0.05, WIDTH, HEIGHT))
    for column in range(8):
        for row in range(0, 8, 2):
                if column % 2 != 0:
                    pygame.draw.rect(screen, WHITE_SQ, (row*SQ_SIZE+WIDTH*0.05, column*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE))
                else:
                    pygame.draw.rect(screen, WHITE_SQ, (row*SQ_SIZE+SQ_SIZE+WIDTH*0.05, column*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE))

def draw_pieces_for_black(screen, board):
    for row in range(8):
        for column in range(8):
            piece = board[-row-1][-column-1]
            if piece != "--":
                screen.blit(images[piece], (column*SQ_SIZE+WIDTH*0.05, row*SQ_SIZE+WIDTH*0.05))

def draw_gamestate(screen, Game_State):
    draw_board(screen)
    if len(Game_State.move_log) != 0:
        highlight_lastmove(Game_State.move_log[-1])
    if len(player_clicks) == 1:
        active_piece(last_click[0], last_click[1])
    draw_pieces(screen, Game_State.board)
    #active_SQ(mouse_position[0], mouse_position[1])

def draw_gamestate_for_black(screen, Game_State):
    draw_board_for_black(screen)
    if len(Game_State.move_log) != 0:
        highlight_lastmove(Game_State.move_log[-1])
    if len(player_clicks) == 1:
        active_piece(last_click[0], last_click[1])
    draw_pieces_for_black(screen, Game_State.board)

def active_SQ(x, y):
    for row in range(8):
        for column in range(8):
            if column*SQ_SIZE+WIDTH*0.05<x<column*SQ_SIZE+WIDTH*0.05+SQ_SIZE and row*SQ_SIZE+WIDTH*0.05<y<row*SQ_SIZE+WIDTH*0.05+SQ_SIZE:
                square = (column*SQ_SIZE+WIDTH*0.05, row*SQ_SIZE+WIDTH*0.05)
                pygame.draw.rect(screen, SQ_BORDER_COLOR, (square[0], square[1], SQ_SIZE, SQ_SIZE), 2)
    
def active_piece(row, column):
    piece = Game_State.board[row][column]
    piece_moves = Game_State.castlemoves(row, column)
    if piece[1] != '-':
        Game_State.move_functions[piece[1]](row, column, piece_moves)
    for i in piece_moves:
        if i in validmoves:
            if Game_State.whitetomove:
                pygame.draw.rect(screen, SQ_BORDER_COLOR, (column*SQ_SIZE+WIDTH*0.05, row*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE), 6)
                if i.capturedpiece == '--':
                    screen.blit(images['valid_move'], (i.second_column*SQ_SIZE+WIDTH*0.05, i.second_row*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE))
                else:
                    screen.blit(images['valid_move2'], (i.second_column*SQ_SIZE+WIDTH*0.05, i.second_row*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE))
            else:
                pygame.draw.rect(screen, SQ_BORDER_COLOR, ((7-column)*SQ_SIZE+WIDTH*0.05, (7-row)*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE), 6)
                if i.capturedpiece == '--':
                    screen.blit(images['valid_move'], ((7-i.second_column)*SQ_SIZE+WIDTH*0.05, (7-i.second_row)*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE))
                else:
                    screen.blit(images['valid_move2'], ((7-i.second_column)*SQ_SIZE+WIDTH*0.05, (7-i.second_row)*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE))

def highlight_lastmove(move):
    if playerOne:
        pygame.draw.rect(screen, SQ_BORDER_COLOR, (move.first_column*SQ_SIZE+WIDTH*0.05, move.first_row*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE), 6)
        pygame.draw.rect(screen, SQ_BORDER_COLOR, (move.second_column*SQ_SIZE+WIDTH*0.05, move.second_row*SQ_SIZE+WIDTH*0.05, SQ_SIZE, SQ_SIZE), 6)
    else:
        pygame.draw.rect(screen, SQ_BORDER_COLOR, (((7-move.first_column)*SQ_SIZE+WIDTH*0.05), ((7-move.first_row)*SQ_SIZE+WIDTH*0.05), SQ_SIZE, SQ_SIZE), 6)
        pygame.draw.rect(screen, SQ_BORDER_COLOR, (((7-move.second_column)*SQ_SIZE+WIDTH*0.05), ((7-move.second_row)*SQ_SIZE+WIDTH*0.05), SQ_SIZE, SQ_SIZE), 6)

def draw_move_log(screen, move_notation_log):   ################################ Стыдоба
    move_log_rect = pygame.Rect(WIDTH+WIDTH*0.1, 0, WIDTH*0.5, HEIGHT+HEIGHT*0.1)
    pygame.draw.rect(screen, (32, 35, 42), move_log_rect)
    font = pygame.font.SysFont('Helvicta', WIDTH//35, True, False)
    counter = 0
    turn = 1
    text_location = (WIDTH+WIDTH*0.1, WIDTH//50)
    text_location_2 = (WIDTH+WIDTH*0.1+ SQ_SIZE*1.3, WIDTH//50*(turn-50))
    text_location_3 = (WIDTH+WIDTH*0.1+ SQ_SIZE*2.6, WIDTH//50*(turn-100))
    if len(move_notation_log) > 0:
        for i in range(0, len(move_notation_log)):
            if counter == 0:
                text_object = font.render(f'{turn}. {move_notation_log[i]}', True, SQ_BORDER_COLOR)
                screen.blit(text_object, text_location)
                if len(move_notation_log) > 100:
                    screen.blit(text_object, text_location_2)
                if len(move_notation_log) > 200:
                    screen.blit(text_object, text_location_3)
                counter += 1
                continue
            if counter == 1:
                text_object = font.render(f'                     {move_notation_log[i]}', True, SQ_BORDER_COLOR)
                screen.blit(text_object, text_location)
                if len(move_notation_log) > 100:
                    screen.blit(text_object, text_location_2)
                if len(move_notation_log) > 200:
                    screen.blit(text_object, text_location_3)
                counter += 1
                turn += 1
            if counter == 2:
                text_location = (WIDTH+WIDTH*0.1, WIDTH//50*turn)
                if len(move_notation_log) > 100:
                    text_location_2 = (WIDTH+WIDTH*0.1+ SQ_SIZE*1.3, WIDTH//50*(turn-50))
                if len(move_notation_log) > 200:
                    text_location_3 = (WIDTH+WIDTH*0.1+ SQ_SIZE*2.6, WIDTH//50*(turn-100))
                counter = 0
    move_log_rect = pygame.Rect(WIDTH+WIDTH*0.1, (WIDTH//50)-SQ_SIZE, WIDTH*0.5, SQ_SIZE)
    pygame.draw.rect(screen, (32, 35, 42), move_log_rect)
    move_log_rect = pygame.Rect(WIDTH+WIDTH*0.1, (WIDTH//50)*51, WIDTH*0.5, SQ_SIZE)
    pygame.draw.rect(screen, (32, 35, 42), move_log_rect)

def draw_endgame_text(screen, text):
    font = pygame.font.SysFont('Helvicta', 32, True, False)
    text_object = font.render(text, 0, SQ_BORDER_COLOR)
    text_location = pygame.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
 
#def main()
#  if __name__ == "__main__":  
#      main()   

""""""""""""""""""""""""""""""""""""""""""""""""""""""
mouse_position = (0, 0) #стартовая позиция мыши для active_SQ
last_click = () #(row, col)
player_clicks = [] # [(row, col),(row, col)]
running = True
playerOne = True
playerTwo = False
validmoves = Game_State.validmoves() #список легальных ходов для начала партии
gameover = False
move_was_made = False #флаг для вычисления легальных ходов только после совершения хода
move_notation_log = []                                                                        ####################################################
load_imgages()

move_log_rect = pygame.Rect(WIDTH+WIDTH*0.1, 0, WIDTH*0.5, HEIGHT+HEIGHT*0.1)                 ####################################################
pygame.draw.rect(screen, (32, 35, 42), move_log_rect)                                         ####################################################
if playerOne:# отрисовка доски с точки зрения первого или второго игрока
    draw_gamestate(screen, Game_State)
else:
    draw_gamestate_for_black(screen, Game_State)


while running:
    human_turn = (playerOne and Game_State.whitetomove) or (playerTwo and not Game_State.whitetomove)
    #Ход игрока
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    Game_State.undo_move()
                    Game_State.undo_move()
                    gameover = False
                    if len(move_notation_log) > 1: ######################################################
                        move_notation_log.pop()    ###################################################### 
                        move_notation_log.pop()    ######################################################
                    else:                          ######################################################
                        move_notation_log = []     ######################################################
                    move_log_rect = pygame.Rect(WIDTH+WIDTH*0.1, 0, WIDTH*0.5, HEIGHT+HEIGHT*0.1)########
                    pygame.draw.rect(screen, (32, 35, 42), move_log_rect)################################
                    move_was_made = True
                    validmoves = Game_State.validmoves()
        elif event.type == pygame.MOUSEMOTION:
            mouse_position = event.pos
            #print(mouse_position)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_pressed = True    # raise the flag
        elif event.type == pygame.MOUSEBUTTONUP:
            if not mouse_button_pressed:
                # simply ignore 
                continue
            mouse_button_pressed = False
            if not gameover and human_turn: #Ограничение команд от мыши во время хода ИИ
                if Game_State.whitetomove:
                    row = (mouse_position[1]-int(WIDTH*0.05))//SQ_SIZE
                    column = (mouse_position[0]-int(WIDTH*0.05))//SQ_SIZE
                else:
                    row = 7-(mouse_position[1]-int(WIDTH*0.05))//SQ_SIZE
                    column = 7-(mouse_position[0]-int(WIDTH*0.05))//SQ_SIZE
                if -1 < row < 8 and -1 < column < 8:
                    last_click = (row, column)
                    player_clicks.append(last_click)
                if len(player_clicks) == 2:
                    if player_clicks[0] != player_clicks[1]:
                        move = chess_engine.move(player_clicks[0], player_clicks[1], Game_State.board)
                        #Костыль для рокировки
                        if Game_State.board[player_clicks[0][0]][player_clicks[0][1]][1] == 'K' and abs(player_clicks[0][1]-player_clicks[1][1]) == 2:
                            move = chess_engine.move(player_clicks[0], player_clicks[1], Game_State.board, castling=True)
                        #Костыль для анпасана
                        if Game_State.board[player_clicks[0][0]][player_clicks[0][1]][1] == 'P' and player_clicks[1] == Game_State.enpassantpossible:
                            move = chess_engine.move(player_clicks[0], player_clicks[1], Game_State.board, enpassant=True)
                        if move in validmoves:
                            Game_State.make_move(move)
                            move_notation_log.append(move.get_movenotation(Game_State, validmoves))  ################################################
                            last_click = ()
                            player_clicks = []
                            move_was_made = True
                            
                        else:
                            last_click = (row, column)
                            player_clicks = []
                            player_clicks.append(last_click)
                    else:
                        last_click = ()
                        player_clicks = []
                        #print("canceled")
                        #Дважды нажатая одна и та же клетка не произведет хода, действие мышкой отменяется
    #Ход ИИ
    if not gameover and not human_turn:
        AImove = AI.random_move(validmoves)
        Game_State.make_move(AImove)
        move_notation_log.append(AImove.get_movenotation(Game_State, validmoves))               #####################################################
        move_was_made = True
        

    if move_was_made:
        validmoves = Game_State.validmoves()
        if len(Game_State.move_log) > 0:
            draw_move_log(screen, move_notation_log)                                              #####################################################
            move_was_made = False
        
    if playerOne: # отрисовка доски с точки зрения первого или второго игрока
        draw_gamestate(screen, Game_State)
    else:
        draw_gamestate_for_black(screen, Game_State)

    if Game_State.checkmate:
        gameover = True
        if Game_State.whitetomove:
            draw_endgame_text(screen, ('BLACK WINS BY CHECKMATE'))
        else:
            draw_endgame_text(screen, ('WHITE WINS BY CHECKMATE'))
    elif Game_State.stalemate:
            gameover = True
            draw_endgame_text(screen, ('STALEMATE'))
     
    

    clock.tick(FPS)
    #Функция clock.tick() приостанавливает выполнение кода до тех пор, пока не пройдет достаточно времени, чтобы достичь нужной частоты кадров.
    pygame.display.flip()
    

