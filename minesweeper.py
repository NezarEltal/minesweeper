import random

# small -   8 x 8  | 10
# medium - 16 x 16 | 40
# large -  16 x 30 | 99

class MinesweeperGame():
    def __init__(self, size="small"):
        self.size = size
        self.newGame()

    def newGame(self):
        self.game_is_over = False
        self.bomb_locations = []
        self.gameSize()
        self.gameboard = []
        self.createNewBoard()
        self.setNumbersOnBoard()
        self.spaces_to_change = []

    def createNewBoard(self):
        self.determineWhereBombsAreLocated()
        current = 0
        for i in range(self.rows):
            temp_row = []
            for j in range(self.columns):
                if current in self.bomb_locations:
                    temp_row.append("X")
                else:
                    temp_row.append(".")
                current += 1
            self.gameboard.append(temp_row)

    def gameSize(self):
        if self.size == "small":
            self.rows = 8
            self.columns = 8
            self.bomb_count = 10
        elif self.size == "medium":
            self.rows = 16
            self.columns = 16
            self.bomb_count = 40
        else:
            self.rows = 16
            self.columns = 30
            self.bomb_count = 99

    def determineWhereBombsAreLocated(self):
        while len(self.bomb_locations) < self.bomb_count:
            location = random.randint(0, self.rows*self.columns)
            if location not in self.bomb_locations:
                self.bomb_locations.append(location)

    def setNumbersOnBoard(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.gameboard[i][j] != "X":
                    self.gameboard[i][j] = self.bombsAdjacentToSpace([i,j])

    def bombsAdjacentToSpace(self, position):
        directions = [[0, 1], [1,0], [1,1], [-1, 0], [-1, 1], [1, -1], [0, -1], [-1,-1]]
        bombs = 0
        for d in directions:
            if self.isPositionOnBoard(position, d) and self.gameboard[position[0]+d[0]][position[1]+d[1]] == "X":
                bombs += 1
        if bombs == 0:
            return "."
        return str(bombs)

    def isPositionOnBoard(self, position, direction):
        row = position[0] + direction[0]
        col = position[1] + direction[1]
        return row >= 0 and row < self.rows and col >= 0 and col < self.columns

    def clickOnLocation(self, position):
        if self.gameboard[position[0]][position[1]] == "X":
            self.revealSpace(position)
            self.gameOver(position)
            return self.spacesToChange()
        elif self.gameboard[position[0]][position[1]][-1] != 'f':
            self.revealSpace(position)
            return self.spacesToChange()
        else:
            return []


    def revealSpace(self, position):
        adjacentSpaces = []
        directions = [[0, 1], [1,0], [1,1], [-1, 0], [-1, 1], [1, -1], [0, -1], [-1,-1]]

        if self.gameboard[position[0]][position[1]] == ".":
            for d in directions:
                if self.isPositionOnBoard(position, d):
                    adjacentSpaces.append([position[0]+d[0], position[1]+d[1]])
        if self.gameboard[position[0]][position[1]][-1] != 'r':
            self.gameboard[position[0]][position[1]] = self.gameboard[position[0]][position[1]] + "r"
            self.spaces_to_change.append([position[0], position[1]])
        for space in adjacentSpaces:
            if self.gameboard[space[0]][space[1]][-1] != 'r' and self.gameboard[space[0]][space[1]][-1] != 'f':
                self.revealSpace(space)

    def setFlagOnSpace(self, position):
        if self.gameboard[position[0]][position[1]][-1] == 'f':
            self.gameboard[position[0]][position[1]] = self.gameboard[position[0]][position[1]][0]
            return "remove"
        elif self.gameboard[position[0]][position[1]][-1] != 'r':
            self.gameboard[position[0]][position[1]] = self.gameboard[position[0]][position[1]] + 'f'
            return "add"

    def gameOver(self, position):
        self.game_is_over = True
        current = 0
        self.gameboard[position[0]][position[1]] = self.gameboard[position[0]][position[1]] + "g"
        for i in range(self.rows):
            for j in range(self.columns):

                if current in self.bomb_locations:
                    if self.gameboard[i][j] == "X":
                        self.gameboard[i][j] = self.gameboard[i][j] + "r"
                        self.spaces_to_change.append([i,j])
                current += 1

    def spacesToChange(self):
        result = self.spaces_to_change[:]
        self.spaces_to_change = []
        return result

    def printBoard(self):
        for row in self.gameboard:
            for col in row:
                print(col, end=" ")
            print()




if __name__ == "__main__":
    minesweeper = MinesweeperGame("small")
    minesweeper.printBoard()
    minesweeper.setFlagOnSpace([1,2])
    minesweeper.clickOnLocation([1,1])
