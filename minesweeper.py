# Sunny Parawala paraw001

#Import Statements
import turtle,random,math,time

class Cell:
    def __init__(self,t,xmin,ymin,w=10,h=10): 
        self.__xmin=xmin
        self.__ymin=ymin
        self.__xmax=self.__xmin+w
        self.__ymax=self.__ymin+h
        self.__t=t
        self.__t.speed(0)
        self.__bomb=False
        self.__cleared=False 

    def isIn(self,x,y):
        #Returns true if x,y are within boundaries of the cell else False
        if (x <= self.__xmax and x >= self.__xmin) and (y <= self.__ymax and y >= self.__ymin):
            return True
        else:
            return False
    
    def setBomb(self):
        # Change the variable bomb if mine is present
        self.__bomb=True

    def isBomb(self):
        return self.__bomb
    
    def clear(self):
        # Change the variable cleared if cell is cleared
        self.__cleared=True
        self.draw()
    
    def isCleared(self):
        # Returns true if cell already cleared
        return self.__cleared
                
    def showCount(self,c):
        # Displays neighboring mines or asterisk
        if c=='*':
            self.__t.goto(self.__xmin+4,self.__ymin-5)
            self.__t.write(c,font=("Arial", 12, "normal"))
        else:
            self.__t.goto(self.__xmin+3,self.__ymin-2)
            self.__t.write(c,font=("Arial", 10, "normal"))

    
    def draw(self):
        # Draws the cell, different colors
        self.__t.penup()
        self.__t.goto(self.__xmin,self.__ymin)
        self.__t.pendown()
        if self.isCleared():
            if self.isBomb():
                self.__t.fillcolor('red')
            else:
                self.__t.fillcolor('grey')
        else:
            self.__t.fillcolor('green')
        self.__t.begin_fill()
        self.__t.fd(self.__xmax-self.__xmin)
        self.__t.left(90)
        self.__t.fd(self.__ymax-self.__ymin)
        self.__t.left(90)
        self.__t.fd(self.__xmax-self.__xmin)
        self.__t.left(90)
        self.__t.fd(self.__ymax-self.__ymin)
        self.__t.left(90)
        self.__t.end_fill()
        self.__t.penup()

class Minesweeper():
    def __init__(self,rows=20,columns=20,mines=15,bombs_visible=False):
        self.__rows= rows
        self.__columns=columns
        self.__mines=mines
        self.__bombs_visible=bombs_visible
        self.__t=turtle.Turtle()
        self.__scr=self.__t.getscreen()
        self.__scr.tracer(0)
        self.__grid = []
        self.__scr.listen() 
        for i in range(self.__rows): # Constructing Grid
            self.__grid.append([])
            for j in range(self.__columns):
                x=-100+10*j
                y=-100+10*i
                self.__grid[i].append(Cell(self.__t,x,y))  # Can send height and width too

        for i in range(self.__rows): # Constructing Minefield in Turtle 
            for j in range(self.__columns):
                obj=self.__grid[i][j]
                obj.draw()
        
        minelist=[]
        m=0
        while m<self.__mines:
            random_row=random.randint(0,self.__rows-1)
            random_column=random.randint(0,self.__columns-1)
            if ([random_row,random_column]) in minelist:
                m=m-1 # Get other numbers
            else:
                obj=self.__grid[random_row][random_column]
                obj.setBomb()
                obj.draw()
                minelist.append([random_row,random_column])

            m+=1
        if self.__bombs_visible==True:
            self.debug()
    def debug(self):
        self.__bombs_visible=True
        for i in range(self.__rows): # Constructing Minefield in Turtle 
            for j in range(self.__columns):
                obj=self.__grid[i][j]
                if obj.isBomb():
                    obj.clear()
                obj.draw()

        

    def countBombs(self,row,col):
        # Returns number of neighboring mines
        checklist=[[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0]]
        minecount=0
        j=0
        #CONVERT ROWS AND COLUMNS TO CO-ORDINATES BEFORE PROCEEDING
        while j < 8:
            x_cor=-99+(row+checklist[j][0])*10 
            y_cor=-99+(col+checklist[j][1])*10
            if self.inGrid(x_cor,y_cor):
                obj=self.__grid[row+checklist[j][0]][col+checklist[j][1]]                   
                if obj.isBomb():
                    minecount+=1 
            j=j+1
        return minecount

    def inGrid(self,x,y):  #Helper Function to check whether x and y are in grid
        if (x>=-100 and x<=-100+10*self.__columns) and (y>=-100 and y<=-100+10*self.__rows):
            return True
        else:
            return False
    def cellsRemaining(self): #Returns number of non mine cells remaining to be cleared
        counter=0
        for i in range(self.__rows): 
            for j in range(self.__columns):
                obj=self.__grid[i][j]
                if obj.isCleared()==False and obj.isBomb()==False:
                    counter+=1
        return counter

    def getRowCol(self,x,y): #Returns Row Number and column number
        if self.inGrid(x,y)==False:
            return -1,-1  
        else:
            temp_x=math.floor(x)-(math.floor(x))%10
            temp_y=math.floor(y)-(math.floor(y))%10
            column=int((temp_x+100)/10) 
            row=int((temp_y+100)/10)
            return row,column

    def __mouseClick(self,x,y): #Function that is called after every mouse click
        row,col=self.getRowCol(x,y) 
        if (col,row)!=(-1,-1):
            obj=self.__grid[row][col]
            if obj.isBomb():
                self.__t.goto(-50,-200)
                self.__t.write("GAME OVER !! ",font=("Arial", 18, "bold")) 
                self.__t.goto(-50,-220)
                self.__t.write("Click to Quit ",font=("Arial", 18, "bold"))
                # DISPLAY ALL MINES ON BOARD NOW
                obj.clear()
                obj.draw()
                obj.showCount('*')
                (self.__scr.onclick(self.screen_hold))

            if obj.isCleared()==False:
                self.clearCell(row,col)
            if self.cellsRemaining()==0:
                self.__t.goto(-100,-200)
                self.__t.write("Congratulations !! You Win . ",font=("Arial", 18, "bold"))
                self.__t.goto(-50,-220)
                self.__t.write("Click to Quit ",font=("Arial", 18, "bold"))
                (self.__scr.onclick(self.screen_hold)) 

    def clearCell(self,row,col):
        adj_mine=self.countBombs(row,col)
        
        if adj_mine!=0: #Base Case: Has Adjacent Mine
            obj=self.__grid[row][col]
            obj.clear()
            c=self.countBombs(row,col)
            obj.showCount(c)
            return True
        else:
            objnew=self.__grid[row][col]
            objnew.clear()
            checklist=[[0,1],[-1,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0]]
            j=0
            while j<8:
                new_row = row + checklist[j][0]
                new_col = col + checklist[j][1]
                if (new_row >=0 and new_row<self.__rows) and (new_col>=0 and new_col<self.__columns):
                    objnew=self.__grid[new_row][new_col]
                    if objnew.isCleared()==False:             
                        self.clearCell(new_row,new_col)  
                j+=1
        
    def screen_hold(self,x,y): # Method to keep the program on hold 
        self.__scr.onclick(quit())

    def run_game(self):
        (self.__scr.onclick(self.__mouseClick)) 
            
            
def main():
    ms=Minesweeper(20,20,50) 
    ms.run_game()
if __name__=='__main__':
    main()

