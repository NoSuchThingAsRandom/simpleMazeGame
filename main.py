import random
import tkinter as tk
import time
import _thread

class Maze:
    finished = False
    mapData = []
    map = ""
    mapWidth = 20
    mapHeight = 20
    playerSymbol = "\u263A"  # Smiley Face

    def make_maze(self):
        print(self.playerSymbol)
        # https://rosettacode.org/wiki/Maze_generation#Python
        visited = [[0] * self.mapWidth + [1] for _ in range(self.mapHeight)] + [[1] * (self.mapWidth + 1)]
        verticalGrid = [["#  "] * self.mapWidth + ['#'] for _ in range(self.mapHeight)] + [[]]
        horizontalGrid = [["###"] * self.mapWidth + ['#'] for _ in range(self.mapHeight + 1)]

        def walk(x, y):
            visited[y][x] = 1
            movement = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            random.shuffle(movement)
            for (xx, yy) in movement:
                if visited[yy][xx]: continue
                if xx == x: horizontalGrid[max(y, yy)][x] = "#  "
                if yy == y: verticalGrid[y][max(x, xx)] = "   "
                walk(xx, yy)

        walk(random.randrange(self.mapWidth), random.randrange(self.mapHeight))

        out = ""
        for (a, b) in zip(horizontalGrid, verticalGrid):
            #  print(''.join(a + ['\n'] + b + ['\n']))
            out += ''.join(a + ['\n'] + b + ['\n'])
        self.map = out
        print(out)
        self.map = out
        return out

    def convert(self):
        self.mapWidth = 62
        self.mapHeight = 41
        print(self.map)
        index = 0

        for y in range(0, self.mapHeight):
            row = []
            for x in range(0, self.mapWidth):
                if self.map[index] == " ":
                    row.append(" ")
                elif self.map[index] == "#":
                    row.append("#")
                elif self.map[index] == "X":
                    row.append("X")
                    print("The exit is at: " + str(x) + ", " + str(y))
                    test = self.findCoords(index)
                    print(str(test[0]) + ", " + str(test[1]))
                index += 1
            self.mapData.append(row)
        self.mapData[self.mapHeight - 1][self.mapWidth - 3] = "X"
        print("Start")
        print(self.printMap())
        self.player = 0
        self.playerCoords = 1, 1
        """
        #For randomised starting point
        while self.map[self.player] != " ":
            self.player = random.randint(0, index)
        self.playerCoords = self.findCoords(self.player)
        """

        print("The player starts at: " + str(self.player))
        print(str(self.playerCoords[0]) + ", " + str(self.playerCoords[1]))

        self.mapData[self.playerCoords[0]][self.playerCoords[1]] = self.playerSymbol
        print(self.printMap())

    def findCoords(self, index):
        print("Finding: " + str(index))
        row = 0
        col = index
        while col > self.mapWidth:
            row += 1
            col -= self.mapWidth

        return [row, col]

    def printMap(self):
        if self.finished:
            return "VICTORY!"
        else:
            out = ""
            for row in self.mapData:
                val = ""
                for s in row:
                    val += str(s)
                out += val + "\n"
            return out

    def moveCharacter(self, up, right):

        print("Moving the character: " + str(up) + ", " + str(right))
        print("Current: " + str(self.playerCoords[0]) + ", " + str(self.playerCoords[1]))
        row = self.playerCoords[0] + up
        col = self.playerCoords[1] + right
        print("New: " + str(row) + ", " + str(col))
        print("Target coords is: " + self.mapData[row][col])
        if self.mapData[row][col] == " ":
            print("Moving")
            self.mapData[self.playerCoords[0]][self.playerCoords[1]] = " "
            self.mapData[row][col] = self.playerSymbol
            self.playerCoords = row, col
        elif self.mapData[row][col] == "X":
            self.finished = True


class gui:
    root = None
    keywords = ["candyCanes", "mincePies", "christmasPudding", ]

    def __init__(self, m):
        #Initial Timer Setup
        self.time=False
        self.running=False
        self.startTime=time.time()
        
        self.root = tk.Tk("Maze")
        self.root.title("Maze")

        global Maze
        Maze = m
        self.root.resizable(False, False)

        #Creates a frame
        self.frame = tk.Frame(self.root, width=510, height=690)
        self.root.resizable(False, False)
        self.frame.pack()
        self.frame.pack(fill="both", expand=True)
        self.frame.grid_propagate(False)

        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        #Binds controls
        self.root.bind("<Left>", self.left_key)
        self.root.bind("<Right>", self.right_key)
        self.root.bind("<Up>", self.up_key)
        self.root.bind("<Down>", self.down_key)

        #Timer display and controls
        self.timer=tk.Text(self.frame,height=1)
        self.timer.grid(row=0,column=0)
        self.timer.insert(1.0, "0")
        self.timer.config(state="disabled")

        self.startButton=tk.Button(self.frame,text="Start",command=self.start)
        self.startButton.grid(row=0,column=1)

        self.stopButton=tk.Button(self.frame,text="Stop",command=self.stop)
        self.stopButton.grid(row=0,column=2)

        self.resetButton=tk.Button(self.frame,text="Reset",command=self.reset)
        self.resetButton.grid(row=0,column=3)

        #Map Display
        self.editText = tk.Text(self.frame, borderwidth=3)
        self.editText.grid(row=1, column=0,columnspan=4,sticky="nsew", padx=2, pady=2)
        self.editText.insert(1.0, Maze.printMap())
        self.editText.config(state="disabled")

        #Tags
        self.editText.tag_configure("finish", foreground="red")
        self.editText.tag_configure("player", foreground="blue")

        endPos = self.editText.search("X", "1.0", stopindex="end")
        self.editText.tag_add("finish", endPos)
        playerPos = self.editText.search(Maze.playerSymbol, "1.0", stopindex="end")
        self.editText.tag_add("player", playerPos)

        self.start()#Starts timer
        self.root.mainloop()#Shows display

        
        
        

    def timerFunc(self):
        self.time=True 
        while(self.time):
            self.timer.config(state="normal")
            self.timer.delete(1.0, "end")
            self.timer.insert(1.0, str(time.time()-self.startTime))
            self.timer.config(state="disabled")
            time.sleep(0.1)
        self.running=False
    
    def start(self):
        if(not self.running):
            _thread.start_new_thread(self.timerFunc,())
    def stop(self):
        self.time=False
        
    def reset(self):
        self.startTime=time.time()
        self.timer.config(state="normal")
        self.timer.delete(1.0, "end")
        self.timer.insert(1.0, "0.0")
        self.timer.config(state="disabled")

    def right_key(self, event):
        Maze.moveCharacter(0, 1)
        self.editText.config(state="normal")
        self.editText.delete(1.0, "end")
        mapDisplay=Maze.printMap()
        if(mapDisplay=="VICTORY!"):
            self.stop()
            mapDisplay+="\nCompleted in: "+str(self.timer.get("1.0",END))+" seconds"
        self.editText.insert(1.0, mapDisplay)
        self.editText.config(state="disabled")

        endPos = self.editText.search("X", "1.0", stopindex="end")
        self.editText.tag_add("finish", endPos)
        playerPos = self.editText.search(Maze.playerSymbol, "1.0", stopindex="end")
        self.editText.tag_add("player", playerPos)

    def left_key(self, event):
        Maze.moveCharacter(0, -1)
        self.editText.config(state="normal")
        self.editText.delete(1.0, "end")
        mapDisplay=Maze.printMap()
        if(mapDisplay=="VICTORY!"):
            self.stop()
            mapDisplay+="\nCompleted in: "+str(time.time()-self.startTime)+" seconds"
        self.editText.insert(1.0, mapDisplay)
        self.editText.config(state="disabled")

        endPos = self.editText.search("X", "1.0", stopindex="end")
        self.editText.tag_add("finish", endPos)
        playerPos = self.editText.search(Maze.playerSymbol, "1.0", stopindex="end")
        self.editText.tag_add("player", playerPos)

    def up_key(self, event):
        Maze.moveCharacter(-1, 0)
        self.editText.config(state="normal")
        self.editText.delete(1.0, "end")
        mapDisplay=Maze.printMap()
        if(mapDisplay=="VICTORY!"):
            self.stop()
            mapDisplay+="\nCompleted in: "+str(time.time()-self.startTime)+" seconds"
        self.editText.insert(1.0, mapDisplay)
        self.editText.config(state="disabled")

        endPos = self.editText.search("X", "1.0", stopindex="end")
        self.editText.tag_add("finish", endPos)
        playerPos = self.editText.search(Maze.playerSymbol, "1.0", stopindex="end")
        self.editText.tag_add("player", playerPos)

    def down_key(self, event):
        Maze.moveCharacter(1, 0)
        self.editText.config(state="normal")
        self.editText.delete(1.0, "end")
        mapDisplay=Maze.printMap()
        if(mapDisplay=="VICTORY!"):
            self.stop()
            mapDisplay+="\nCompleted in: "+str(time.time()-self.startTime)+" seconds"
        self.editText.insert(1.0, mapDisplay)
        self.editText.config(state="disabled")

        endPos = self.editText.search("X", "1.0", stopindex="end")
        self.editText.tag_add("finish", endPos)
        playerPos = self.editText.search(Maze.playerSymbol, "1.0", stopindex="end")
        self.editText.tag_add("player", playerPos)


if __name__ == "__main__":
    m = Maze()
    m.make_maze()
    m.convert()
    gui(m)
