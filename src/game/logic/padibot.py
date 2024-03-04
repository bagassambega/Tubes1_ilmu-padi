import random
from typing import Optional
from typing import List
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class Padibot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def diamondsaroundbase(self, board_bot: GameObject, board:Board):
        # fungsi mengambil lokasi kumpulan diamond yang ada di sekitar base dalam bentuk list
        props = board_bot.properties
        diamonds = board.diamonds
        
        base_x, base_y = props.base.x, props.base.y
        diamond_loc = [diamond.position for diamond in diamonds
                       if base_x - 3 <= diamond.position.x <= base_x + 3
                       and base_y - 3 <= diamond.position.y <= base_y + 3]
        
        return diamond_loc
    
    def botaroundbase(self, board_bot: GameObject):
        # memeriksa apakah lokasi bot lagi di sekitar base
        props = board_bot.properties
        current_position = board_bot.position
        return ((props.base.x-3) <= current_position.x <= (props.base.x+3) and (props.base.y-3) <= current_position.y <= (props.base.y+3))
    
    def closestdiamondbase(self, board_bot: GameObject, diamonds: List[Position]):
        # mencari diamond yang paling dekat base dengan posisi bot
        current_position = board_bot.position
        closest_diamond = min(diamonds, key=lambda diamond: abs(diamond.x - current_position.x) + abs(diamond.y - current_position.y))
        return closest_diamond
    
    def cekdiamondbase(self, board_bot: GameObject, board:Board):
        # cek apakah ada diamond sekitar base
        ada = False
        diamonds = board.diamonds
        
        # lokasi diamonds sekitar base
        for diamond in diamonds:
            if (board_bot.properties.base.x-2) <= diamond.position.x <= (board_bot.properties.base.x+2) and (board_bot.properties.base.y-2) <= diamond.position.y <= (board_bot.properties.base.y+2):
               return True
                
        return ada
    
    def closestdiamond(self, board_bot: GameObject,board:Board):
        # cari diamond terdekat dengan bot (bebas di mana aja)
        current_position = board_bot.position
        closest_diamond = min(board.diamonds, key=lambda diamond: (abs(diamond.position.x-current_position.x)+abs(diamond.position.y-current_position.y)))
        return closest_diamond.position
    
    def closestdiamonddist(self, board_bot: GameObject,board: Board):
        # mencari jarak bot dengan diamond terdekat
        closest = self.closestdiamond(board_bot, board)
        current_position = board_bot.position
        return abs(closest.x-current_position.x)+abs(closest.y-current_position.y)
    
    def get_directions(self,current_x, current_y, dest_x, dest_y):
        # bikin biar geraknya rada zigzag
        # cari jarak x dan y nya dulu
        delta_x = abs(dest_x - current_x)
        delta_y = abs(dest_y - current_y)
        x=0
        y=0

        if (dest_x - current_x)<0:
            x = -1 # jalan ke kiri
        else:
            x = 1 # jalan ke kanan

        if (dest_y - current_y)<0:
            y = -1 # jalan ke bawah
        else:
            y = 1 # jalan ke atas

        if delta_x >= delta_y: # ini kalau posisinya belum kotak dia bakal gerak horizontal sampai kotak
            dx = x
            dy = 0
        elif delta_x < delta_y: # kalau udah kotak dia bakal jalan vertikal
            dy = y
            dx = 0

        return (dx, dy)

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        
        # kalau diamond yang dimiliki sudah lebih dari 3 maka bot diarahkan balik ke base
        if props.diamonds >=3:
            # kalau pas jalan pulang ternyata ada diamond yang deket dan inventory belum penuh (sekalian ambil)
            if(self.closestdiamonddist(board_bot,board)==1) and props.diamonds <5:
                self.goal_position = self.closestdiamond(board_bot,board)
            else:
                base = board_bot.properties.base
                self.goal_position = base
            
        # kalau masih kurang 3 akan cari diamond
        elif props.diamonds < 3:
            # didahuluin cari yang ada di sekitar base dulu
            if self.cekdiamondbase(board_bot,board) and self.botaroundbase(board_bot):
                diamond_list = self.diamondsaroundbase(board_bot,board)
                self.goal_position = self.closestdiamondbase(board_bot,diamond_list)
            # kalau gak ada baru cari yang lebih jauh
            else:
                self.goal_position = self.closestdiamond(board_bot,board)

        if self.goal_position is not None:
            delta_x, delta_y = self.get_directions(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y
