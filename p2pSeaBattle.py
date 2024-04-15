import socket 
import os 
import threading 
import asyncio 
import random 

port = random.randint(1000, 8000)
data = ''

class SeaBattle:
    res = '' 
    def __init__(self) -> list:
        self.map = [['.' for _ in range(10)] for _ in range(10)]
    
    def create_battle_board(self):
        ships = 10 
        print(f'place ships on board\nleft>>> {ships}')
        while ships != 0:
            print(f'ships left {ships}')
            print('')
            for i in self.map:
                print(i)
            a, b = map(int, input("space separated input field>>> ").split())
            self.map[a][b] = 'X'
            ships -= 1
        print('congrulations!!!1111!!111!1!11!11!!1111!1')
    
    def shoot(self, row, col):
        if self.map[row][col] == '.':
            self.map[row][col] = '*'
            print('miss')
            return 'miss1'
        elif self.map[row][col] == '*':
            print('miss against')
            return 'miss2'
        else:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < 10 and 0 <= j < 10:
                        if self.map[i][j] == '.':
                            self.map[i][j] = '*'
            self.map[row][col] = 'X'
            for j in range(len(self.map)):  # Если корабль расположен горизонтально
                if self.map[row][j] == 'X':
                    col = j
                    for i in range(row - 1, row + 2):
                        for u in range(col - 1, col + 2):
                            if 0 <= i < 10 and 0 <= u < 10:
                                if self.map[i][u] == '.':
                                    self.map[i][u] = '*'
            for v in range(len(self.map)): # Если корабль расположен вертикально
                if self.map[v][col] == 'X':
                    row = v
                    for v in range(row - 1, row + 2):
                        for u in range(col - 1, col + 2):
                            if 0 <= v < 10 and 0 <= u < 10:
                                if self.map[v][u] == '.':
                                    self.map[v][u] = '*'
            print('sink')
            return 'sink'
    
    def __str__(self) -> str:
        global res 
        res = ''
        for i in self.map:
            for j in i:
                res += '['
                res += str(j)
                res += ']'
            res += '\n'
        return res 
    
    def get_board(self) -> str:
        res = ''
        for i in self.map:
            for j in i:
                res += '['
                res += str(j)
                res += ']'
            res += '\n'
        return res 
    
    def get_matrix_by_index(self, indx):
        return self.map[indx]
    
    def get_matrix_by_index_2(self, a, b):
        return self.map[a][b]
    
    def get_win_status(self) -> bool:
        f = 0 
        for i in self.map:
            for j in i:
                if j == 'X':
                    f += 1
        if f == 0:
            return True 
        return False 
    
myboard = SeaBattle()
opponentboard = SeaBattle()

def server():
    global board 
    global port
    global data  
    ip = socket.gethostbyname(socket.gethostname())
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    print(f'Server started on {ip}:{port}')
    server.listen(1)
    conn, addr = server.accept()

    while True:
        data = conn.recv(1024)
        if data.decode('utf-8') == '/stop':
            print('Ktoto>>> /stop')
            print('Ktoto has leave')
            server.close()
            return 'its over'
        else:
            print(f'Ktoto>>> {data.decode("utf-8")}')
            try:
                a, b = data.decode('utf-8').split()
                myboard.shoot(int(a), int(b))
                gamma = myboard.get_matrix_by_index_2(int(a), int(b))
                conn.send(gamma.encode('utf-8'))
            except:
                print('invalid coords')
                print(data.encode('utf-8'))

def client():
    global data
    global board 
    server = socket.socket()
    print(f'your ip>>> {socket.gethostbyname(socket.gethostname())}')
    while True:  
        ip = input('ip to connect>>> ')
        port = int(input('port to connect>>>'))
        try:
            server.connect((ip, port))
            break
        except:
            print('invalid ip/port or connect error')

    myboard.create_battle_board()
    while True:  
        print('your board: \t\t\t\t\t\topponent board:')
        for i in range(0, 10):
            print(myboard.get_matrix_by_index(i), opponentboard.get_matrix_by_index(i))
        message = input('You>>> ')
        if message == '/stop':
            server.send(message.encode("utf-8"))
            server.close()
            return None
        elif message == '/help':
            print('---------------------------------\n/stop - disconnect from opponent\n'
                  '/help - get list of commands\n---------------------------------\n'
                  '')
            continue
        else:
            server.send(message.encode("utf-8"))
        


p1 = threading.Thread(target=server, name="t1")
p2 = threading.Thread(target=client, name="t2")

p1.start()
p2.start()
