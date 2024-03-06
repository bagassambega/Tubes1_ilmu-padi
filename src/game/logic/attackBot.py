from typing import Tuple, Optional
from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from ..util import get_direction

class attackBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    
    def calculateDistanceToBots(self, board_bot: GameObject, enemy_bot: GameObject):
        # Menghitung jarak (x, y) dari enemy bot ke kita
        return (enemy_bot.position.x - board_bot.position.x, enemy_bot.position.y - board_bot.position.y)
    
    
    def findAllBots(self, board_bot: GameObject, board: Board):
        # Mencari semua bot yang memiliki diamonds > 3 saja dan diamonds nya lebih banyak dari kita
        listBots = []
        for bot in board.bots:
            if (bot.id != board_bot.id):
                if (bot.properties.diamonds > board_bot.properties.diamonds and bot.properties.diamonds >= 3):
                    listBots.append(bot)
        return listBots
    
    def chaseBots(self, board_bot: GameObject, listBots: Optional[GameObject], board: Board):
        for bot in listBots:
            dist = self.calculateDistanceToBots(board_bot, bot)
            if (dist[0] <= 3 and dist[1] <= 3):
                self.goal_position = bot.position
                print("chase bot")
                return
    
    
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        bots = self.findAllBots(board_bot, board)
        self.chaseBots(board_bot, bots, board)
        if self.goal_position != None:
            x, y = get_direction(board_bot.position.x, board_bot.position.y,
                        self.goal_position.x, self.goal_position.y)
        else:
            x, y = 0, 1
        return x, y