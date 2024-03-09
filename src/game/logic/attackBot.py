from typing import Optional
from typing import List
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position


class attackBot(BaseLogic):
    #! INITIALIZATION
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.chaseSteps = 0
        self.isPortal = False


    #! DIAMOND SECTION
    # fungsi mengambil lokasi kumpulan diamond yang ada di sekitar base dalam bentuk list
    def diamondsaroundbase(self, board_bot: GameObject, board:Board):
        props = board_bot.properties
        diamonds = board.diamonds
        
        base_x, base_y = props.base.x, props.base.y
        diamond_loc = [diamond.position for diamond in diamonds
                       if base_x - 3 <= diamond.position.x <= base_x + 3
                       and base_y - 3 <= diamond.position.y <= base_y + 3]
        
        return diamond_loc
    
    # memeriksa apakah lokasi bot kita lagi di sekitar base
    def botaroundbase(self, board_bot: GameObject):
        props = board_bot.properties
        current_position = board_bot.position
        return ((props.base.x-3) <= current_position.x <= (props.base.x+3) and (props.base.y-3) <= current_position.y <= (props.base.y+3))
    
    # mencari diamond yang paling dekat base dengan posisi bot
    def closestdiamondbase(self, board_bot: GameObject, diamonds: List[Position]):
        current_position = board_bot.position
        closest_diamond = min(diamonds, key=lambda diamond: abs(diamond.x - current_position.x) + abs(diamond.y - current_position.y))
        return closest_diamond

    # cek apakah ada diamond sekitar base
    def cekdiamondbase(self, board_bot: GameObject, board:Board):
        ada = False
        diamonds = board.diamonds
        
        # lokasi diamonds sekitar base
        for diamond in diamonds:
            if (board_bot.properties.base.x-2) <= diamond.position.x <= (board_bot.properties.base.x+2) and (board_bot.properties.base.y-2) <= diamond.position.y <= (board_bot.properties.base.y+2):
                return True
                
        return ada
    
    # cari diamond terdekat dengan bot (bebas di mana aja)
    def closestdiamond(self, board_bot: GameObject,board:Board):
        current_position = board_bot.position
        closest_diamond = min(board.diamonds, key=lambda diamond: (abs(diamond.position.x-current_position.x)+abs(diamond.position.y-current_position.y)))
        return closest_diamond.position
    
    
    # cari red diamond terdekat dengan bot (bebas di mana aja)
    def closestreddiamond(self, board_bot: GameObject, board:Board):
        current_position = board_bot.position
        red_diamonds = [diamond for diamond in board.diamonds if diamond.points == 2]

        if not red_diamonds:
            return None  # Jika tidak ada red diamond, kembalikan None

        closest_red_diamond = min(red_diamonds, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))
        return closest_red_diamond.position

    # Mencari diamond terdekat
    def closestdiamonddist(self, board_bot: GameObject,board: Board):
        # mencari jarak bot dengan diamond terdekat
        closest = self.closestdiamond(board_bot, board)
        current_position = board_bot.position
        return abs(closest.x-current_position.x)+abs(closest.y-current_position.y)
    
    # mencari jarak bot dengan diamond merah terdekat
    def closestreddiamonddist(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        red_diamonds = [diamond for diamond in board.diamonds if diamond.properties.points == 2]

        if not red_diamonds:
            return None  # Jika tidak ada red diamond, kembalikan None

        closest_red_diamond = min(red_diamonds, key=lambda diamond: abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y))
        distance = abs(closest_red_diamond.position.x - current_position.x) + abs(closest_red_diamond.position.y - current_position.y)
        return distance

    def basedistance(self, board_bot: GameObject, board: Board):
        # mencari jarak bot dengan base
        current_position = board_bot.position
        base = board_bot.properties.base
        return abs(base.x - current_position.x) + abs(base.y - current_position.y)
        
        
    #! BOT SECTION
    # Menghitung jarak (x, y) dari enemy bot ke kita
    def calculateDistanceToBots(self, board_bot: GameObject, enemy_bot: GameObject):
        return (enemy_bot.position.x - board_bot.position.x, enemy_bot.position.y - board_bot.position.y)
    
    # Mencari semua bot yang memiliki diamonds > 3 saja dan diamonds nya lebih banyak dari kita
    def findAllBots(self, board_bot: GameObject, board: Board):
        listBots = []
        for bot in board.bots:
            if (bot.id != board_bot.id):
                if (bot.properties.diamonds > board_bot.properties.diamonds and bot.properties.diamonds >= 3):
                    listBots.append(bot)
        return listBots
    
    # Menjadikan bot sebagai goal_position, jika jarak ke bot musuh adalah 3
    def chaseBots(self, board_bot: GameObject, listBots: Optional[GameObject]) -> bool:
        for bot in listBots:
            dist = self.calculateDistanceToBots(board_bot, bot)
            if (dist[0] <= 3 and dist[1] <= 3):
                self.goal_position = bot.position
                return True
        return False
    
    
    #! RED BUTTON
    # Mencari red button
    def findRedButton(self, board: Board):
        for item in board.game_objects:
            if item.type == "DiamondButtonGameObject":
                return item
    
    # Compare jarak closest diamond dengan red button. Lebih baik generate ulang daripada ke diamond jauh
    # Hanya jika diamond yang ada di board sedikit (pre-checked in next_move)
    def compareClosestDiamondToRedButton(self, board_bot: GameObject, board: Board):
        if self.calculateDistanceRedButton(board_bot, board) < self.closestdiamonddist(board_bot, board):
            return True
        return False
    
    # Menghitung jarak ke red button 
    def calculateDistanceRedButton(self, board_bot: GameObject, board: Board):
        redButton = self.findRedButton(board)
        return abs(redButton.position.x - board_bot.position.x) + abs(redButton.position.y - board_bot.position.y)
    
    #! TELEPORTER
    # Mencari semua teleporter yang ada
    def findAllTeleporter(self, board_bot: GameObject, board: Board):
        teleporters = [item for item in board.game_objects if item.type == "TeleportGameObject"]
        return sorted(teleporters, key=lambda tele: (abs(tele.position.x - board_bot.position.x) + abs(tele.position.y - board_bot.position.y)))
    
    # Deteksi diamond di sekitar teleporter yang jauh jika diamond dekat kita atau base habis
    def detectDiamondTeleporter(self, board_bot: GameObject, board: Board):
        teleporters = self.findAllTeleporter(board_bot, board)
        # Closest teleporter: 0, furthest: 1
        farTeleporter = teleporters[1]
        diamondCloseTeleporter = []
        for diamond in board.diamonds:
            if abs(diamond.position.x - farTeleporter.position.x) <= 3 and abs(diamond.position.y - farTeleporter.position.y) <= 3:
                diamondCloseTeleporter.append(diamond)
        return len(diamondCloseTeleporter) >= 3
        # Hanya jika worth it, diamond > 3
             
    
    #! GET DIRECTIONS
    # Set direction and move, 2nd main function
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
        max_travel_time = props.milliseconds_left # 1 detik buat jaga-jaga
        distance_to_base = abs(props.base.x - current_position.x) + abs(props.base.y - current_position.y)
        time_to_return = distance_to_base #sesuain disini kalau bot kita bisa gerak lbh cepet dr 1 detik
        
        # kalau mepet waktu, langsung balik ke base
        if time_to_return >= max_travel_time:
            base = board_bot.properties.base
            self.goal_position = base
        
        # kalau pas lewat base ke base dulu
        elif (self.basedistance(board_bot, board)==2 and props.diamonds >2) or (self.basedistance(board_bot, board)==1 and props.diamonds >0):
            base = board_bot.properties.base
            self.goal_position = base

        elif props.diamonds ==5:
            print("full capacity")
            base = board_bot.properties.base
            self.goal_position = base

        # kalau diamond yang dimiliki sudah lebih dari 3 maka bot diarahkan balik ke base
        elif props.diamonds >=3:
            print("diamond 3")
            # kalau pas jalan pulang ternyata ada diamond yang deket dan inventory belum penuh (sekalian ambil)
            if self.cekdiamondbase(board_bot,board):
                print("diamond base lebih muatan bro")
                diamond_list = self.diamondsaroundbase(board_bot,board)
                self.goal_position = self.closestdiamondbase(board_bot,diamond_list)
            elif(self.closestdiamonddist(board_bot,board)==1) and self.closestdiamond(board_bot,board) is not None:
                self.goal_position = self.closestdiamond(board_bot,board)
            else:
                base = board_bot.properties.base
                self.goal_position = base
            
        # kalau masih kurang 3 akan cari diamond
        elif props.diamonds <3:
            print("diamond kurang dari 3")
            # didahuluin cari yang ada di sekitar base dulu
            if (self.cekdiamondbase(board_bot,board) and self.botaroundbase(board_bot)) or (self.cekdiamondbase(board_bot,board) and len(self.diamondsaroundbase(board_bot,board))>=2) :
                print("diamond base")
                diamond_list = self.diamondsaroundbase(board_bot,board)
                self.goal_position = self.closestdiamondbase(board_bot,diamond_list)
            # kalau gak ada baru cari yang lebih jauh
            
                # Prioritaskan red diamond jika lebih dekat dari pada diamond biasa
            elif self.closestreddiamond(board_bot, board) is not None: 
                if (self.closestdiamond(board_bot, board) is not None):
                    if (self.closestreddiamonddist(board_bot, board) < self.closestdiamonddist(board_bot, board)) :
                        print("red diamond @1")
                        self.goal_position = self.closestreddiamond(board_bot,board)
                    else:
                        print("red diamond @2")
                        self.goal_position = self.closestdiamond(board_bot, board)
                else:
                    self.goal_position = self.closestreddiamond(board_bot,board)

            else:
                print("diamond biru")
                self.goal_position = self.closestdiamond(board_bot, board)

        if self.goal_position is not None:
            delta_x, delta_y = self.get_directions(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
                board_bot,board
            )
        else:
            self.goal_position = board_bot.properties.base
            delta_x, delta_y = self.get_directions(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
                board_bot,board
            )

        return delta_x, delta_y
