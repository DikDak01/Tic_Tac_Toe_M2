from colorama import *
import sqlite3
import datetime as dt


#Initialize colorama
init(autoreset=True)


class Gamefield:
    
    def __init__(self):
        self.field = [" ",
                      "1", "2", "3",
                      "4", "5", "6",
                      "7", "8", "9"]
        
        
    def playground(self):
        print(Fore.RED + self.field[1] + "|" + self.field[2] + "|" + self.field[3])
        print(Fore.RED + self.field[4] + "|" + self.field[5] + "|" + self.field[6])
        print(Fore.RED + self.field[7] + "|" + self.field[8] + "|" + self.field[9])


    def playerinput(self, current_player):
        while True:
            try:
                if current_player == 'X':
                    inputplayer = input(Fore.MAGENTA + f"{self.userx}, choose a Field: ")
                elif current_player == 'O':
                    inputplayer = input(Fore.MAGENTA + f"{self.usero}, choose a Field: ")
                inputplayer = int(inputplayer)

                if 0 <= inputplayer <= 9 and self.field[inputplayer] != "X" and self.field[inputplayer] != "O":
                    self.field[inputplayer] = current_player
                    break
                else:
                    print(Fore.RED + "Invalid input or field already taken, try again.")
                    
            except:
                print("something went wrong")

class Check(Gamefield):
    def checkwin(self):
        win_combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9),
                            (1, 4, 7), (2, 5, 8), (3, 6, 9),
                            (1, 5, 9), (3, 5, 7)]

        for combination in win_combinations:
            if self.field[combination[0]] == self.field[combination[1]] == self.field[combination[2]] != " ":
                return self.field[combination[0]]
        return None

    def checkdraw(self):
        return all(field == 'X' or field == 'O' for field in self.field[1:])

class Database(Check):
    
    def username(self):
        self.userx = input("Player X, please write your player name in the field:")
        self.userx = str(self.userx)
        
        self.usero = input("Player O, please write your player name in the field:")
        self.usero = str(self.usero)


    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS game_results
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT,
                            player_x_name TEXT,
                            player_o_name TEXT,
                            winner TEXT)''')
        self.conn.commit()

    def insert_result(self, player_x_name, player_o_name, winner):
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''INSERT INTO game_results (date, player_x_name, player_o_name, winner)
                           VALUES (?, ?, ?, ?)''', (date, player_x_name, player_o_name, winner))
        self.conn.commit()
        
class Game(Database):
    def start(self):
        print(Fore.MAGENTA + 50 * "=")
        print(Fore.CYAN + "Welcome to my Tic Tac Toe Mark 2")
        print(Fore.GREEN + "I guess you know the rules")
        print(Fore.CYAN + "Have Fun, great wishes Nik Nak :)")
        print(Fore.MAGENTA + 50 * "=")

        with open('/Users/niknak/Documents/01 Projekte/Programming/Python/Games/Mark 2/ascii-art.txt', 'r') as file:
            contents = file.read()
            print(contents)
            
        #usernames for individual playing, see on class Database
        self.username()
        
        current_player = 'X'
 
        
        self.playground()

        while True:
            self.playerinput(current_player)
            self.playground()
            if self.checkwin():
                if current_player == 'X':
                    print(Fore.GREEN + f"Player {self.userx} wins!")
                    self.insert_result(self.userx, self.usero, self.userx)

                elif current_player == 'O':
                    print(Fore.GREEN + f"Player {self.usero} wins!")
                    self.insert_result(self.userx, self.usero, self.usero)

                break
            
            if self.checkdraw():
                print(Fore.YELLOW + "It's a draw!")
                self.insert_result(self.userx, self.usero, "Draw")
                break
            
            current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    game = Game()
    game.start()
