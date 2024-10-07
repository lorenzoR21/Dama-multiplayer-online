from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QMessageBox, QPushButton, QGraphicsProxyWidget, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QRectF, QFile, QObject, Signal, Slot
import json
import time


class Board(QGraphicsView):
    send_move = Signal(QGraphicsView)

    def __init__(self, mode, difficulty, playerIsWhite, up, turn, s, username):
        super().__init__()
        self.sio = s
        self._n = 8
        self._scene = None
        self._cells = None
        self._gMode = mode
        self._difficulty = difficulty
        self._playerIsWhite = playerIsWhite
        self._game = None
        self._col = ""
        self._numberOfMoves = 0
        self._username = username

        if self._gMode == "HUMAN_VS_HUMAN":
            if (turn and self._playerIsWhite) or (not turn and not self._playerIsWhite):
                _col = "White turn"
            elif (turn and not self._playerIsWhite) or (not turn and self._playerIsWhite):
                _col = "Black turn"


        self.setBackgroundBrush(QColor(139, 69, 19))
        self._scene = QGraphicsScene()
        self.setInteractive(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.reset(up, turn)
        self.resizeEvent(None)

        self.button = QPushButton("WITHDRAW")
        self.button.setFixedSize(120, 50)
        self.button.clicked.connect(self.on_button_click)
        self.button.setStyleSheet("""QPushButton {
                                            border: 2px solid black;       
                                            background-color: white;     
                                            color: black;                
                                            padding: 10px;                   
                                        }
                                        QPushButton:hover {
                                            background-color: lightgray; 
                                        }
                                    """)

        self.proxy_widget = QGraphicsProxyWidget()
        self.proxy_widget.setWidget(self.button)

        self.proxy_widget.setPos(self._scene.width() - self.button.width() + 190, 10)
        self._scene.addItem(self.proxy_widget)
        self.label = QLabel(username)
        self.label.setFixedSize(180, 60)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""QLabel {
                                            border: 2px solid black;       
                                            background-color: rgb(139, 69, 19);     
                                            color: black;                
                                            font-size: 20px;        
                                        }
                                    """)

        self.proxy_widget_label = QGraphicsProxyWidget()
        self.proxy_widget_label.setWidget(self.label)
        self.proxy_widget_label.setPos(-200, self._scene.height() - self.label.height() - 10)
        self._scene.addItem(self.proxy_widget_label)
        self.setScene(self._scene)


    def on_button_click (self):
        print("VOGLIO ARRENDERMI")
        self.sio.emit('withdraw',self._username)

    def resizeEvent(self, e):
        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    def reset(self, up, turn):
        if self._cells:
            for i in range(self._n):
                for j in range(self._n):
                    self._scene.removeItem(self._cells[i][j])
                    del self._cells[i][j]
                del self._cells[i]
            del self._cells

        self._scene.clear()
        from views.cell import Cell
        self._scene.setSceneRect(QRectF(0, 0, Cell.cellsize * self._n, Cell.cellsize * self._n))
        self._cells = [[Cell(self, j, i) for j in range(self._n)] for i in range(self._n)]
        for i in range(self._n):
            for j in range(self._n):
                self._cells[i][j].setPos(j, i)
                self._scene.addItem(self._cells[i][j])
        from gameEngine.game import Game
        self._game = Game(self._difficulty, self._playerIsWhite, up, turn)

        self.updateBoard()

    @Slot(int, int, int, int)
    def move(self, x0, y0, x1, y1):
        if self._gMode == "HUMAN_VS_HUMAN":
            from views.cell import Cell
            if ((self._game.myTurn() and self._playerIsWhite) or (not self._game.myTurn() and not self._playerIsWhite)) and (self._cells[y0][x0]._content == Cell.PIECE_W or self._cells[y0][x0]._content == Cell.P_DAMA_W):
                multiple_eat = False 
                boolMove, multiple_eat = self._game.move(x0, y0, x1, y1, multiple_eat)

                if not boolMove:
                    return

                self.updateBoard()

                if multiple_eat:
                    return

                self._game.eat_rules()
                self._col = "Black turn"

            elif ((not self._game.myTurn() and self._playerIsWhite) or (self._game.myTurn() and not self._playerIsWhite)) and (self._cells[y0][x0]._content == Cell.PIECE_B or self._cells[y0][x0]._content == Cell.P_DAMA_B):
            
                multiple_eat = False  
                boolMove, multiple_eat = self._game.move(x0, y0, x1, y1, multiple_eat)

                if not boolMove:
                    return

                self.updateBoard()

                if multiple_eat:
                    return

                self._game.eat_rules()
                self._col = "White turn"

        elif self._gMode == "HUMAN_VS_AI":
            if self._game.myTurn() and not self.valid_selection(x0, y0):
                return

            if self._game.isThinking():
                return

            self._game.eat_rules()
            multiple_eat = False  
            boolMove, multiple_eat = self._game.move(x0, y0, x1, y1, multiple_eat)

            if not boolMove:
                return

            self.updateBoard()
            self.win_lose_mex()

            if multiple_eat:
                self._numberOfMoves = self._numberOfMoves + 1
                return

            self._col = "Your turn"
            self._game._myTurn = False

            if self._gMode == "HUMAN_VS_AI" and not self._game.myTurn():
                self._game._isThinking = True
                moveDid = self._game._moves[-(self._numberOfMoves + 1):]
                for move in moveDid:
                    move._x0 = 7 - move._x0
                    move._y0 = 7 - move._y0
                    move._x1 = 7 - move._x1
                    move._y1 = 7 - move._y1
                moves_dict_list = [move.to_dict_coordinates() for move in moveDid]
                moves_json = json.dumps(moves_dict_list, indent=4)
                self._numberOfMoves = 0
                self.sio.emit('moves', moves_json)
            
                

    def updateBoard_fromOpponent(self, o_moves):
        time.sleep(1)
        opponent_moves = json.loads(o_moves)
        self._game._forced_moves.clear()
        for move in opponent_moves:
            multiple_eat = False  
            boolMove, multiple_eat = self._game.move(move['x0'], move['y0'], move['x1'], move['y1'], multiple_eat)
        
        self.updateBoard()
        self.win_lose_mex()
        self._game._myTurn = True
        self._game._isThinking = False

    def updateBoard(self):
        from views.cell import Cell
        player = Cell.PIECE_W if self._playerIsWhite else Cell.PIECE_B
        playerK = Cell.P_DAMA_W if self._playerIsWhite else Cell.P_DAMA_B
        AI = Cell.PIECE_B if self._playerIsWhite else Cell.PIECE_W
        AIk = Cell.P_DAMA_B if self._playerIsWhite else Cell.P_DAMA_W
        i = 0
        j = 0
        for i in range(self._n):
            for j in range(self._n):
                if self._game.pieceBoard()[i][j] != None:
                    piece = self._game.pieceBoard()[i][j]
                    if piece.white() and not piece.king():
                        self._cells[i][j].setContent(player)
                    elif not piece.white() and not piece.king():
                        self._cells[i][j].setContent(AI)
                    elif piece.white() and piece.king():
                        self._cells[i][j].setContent(playerK)
                    elif not piece.white() and piece.king():
                        self._cells[i][j].setContent(AIk)
                else:
                    self._cells[i][j].setContent(Cell.EMPTY)

    def win_lose_mex(self):
        if not self._game.ended():
            return

        if self._gMode == "HUMAN_VS_AI":
            if self._game.wins() == 1:
                self.sio.emit('game_end', [self._username, 1])
            elif self._game.wins() == 2:
                self.sio.emit('game_end', [self._username, 2])

    def display_cells(self, xy_s, xy_n):
        if not self._game.isThinking():
            self._cells[xy_s // self._n][xy_s % self._n].setSuggested(True)
            self._cells[xy_n // self._n][xy_n % self._n].setSuggested(True)

    def forced_cells(self):
        if not self._game._forced_moves:
            return False
        else:
            if self._game._moves:
                if self._game._moves[-1]._multiple_eat:
                    app = self._game._forced_moves[:]
                    for p in app:
                        if p[0] != self._game._moves[-1]._y1 * self._n + self._game._moves[-1]._x1:
                            self._game._forced_moves.remove(p)
            for p in self._game._forced_moves:
                self.display_cells(p[0], p[1])
        return True

    def valid_selection(self, x0, y0):
        from views.cell import Cell
        if self._playerIsWhite and (self._cells[y0][x0]._content == Cell.PIECE_B or self._cells[y0][x0]._content == Cell.P_DAMA_B):
            return False
        if not self._playerIsWhite and (self._cells[y0][x0]._content == Cell.PIECE_W or self._cells[y0][x0]._content == Cell.P_DAMA_W):
            return False
        return True
