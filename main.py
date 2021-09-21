from tkinter import * 
import numpy as np
from random import randint
from time import sleep

GRID = 25
SIZE = 1000
SCALE = SIZE / GRID
SLEEP = 0.1


#! CLASSES
class Cell():
    status = False

    def __init__(self, r, c):
        self.r = r
        self.c = c
    
    def check(self, matrix) -> None:
        count = 0
        for x in range(3): 
            for y in range (3): 
                if (x == 1 and y == 1):
                    continue
                elif self._exists(x, y, matrix):
                    count += 1
                else: continue

        if self.status: self.status = count in (2, 3)
        else: self.status = count == 3
    
    def _exists(self, posX, posY, matrix) -> bool:
        nR = self.r + posX - 1
        nC = self.c + posY - 1
        if nR > -1 and nR < len(matrix) and nC > -1 and nC < len(matrix[nR]):
            return matrix[nR][nC].status
        else: 
            return False



#! FUNCTIONS
def produce(window):
    matr = np.empty((GRID, GRID), dtype=object)

    canvas = Canvas(window, width=SIZE, height=SIZE)
    canvas.config(background="#333")
    canvas.pack()

    for i in range(GRID):
        for j in range(GRID):
            matr[i][j] = Cell(i, j)
            tag = f"cell/{i}/{j}"
            canvas.create_rectangle(
                    i*SCALE, j*SCALE, (i+1)*SCALE, (j+1)*SCALE,
                    outline="#000",
                    fill="#333", tags=tag)
            canvas.tag_bind(tag, "<Button-1>", lambda e: click(canvas, e, matr))

    window.bind("<Return>", lambda e: start(matr, canvas, window))
    window.bind("r", lambda e: random(matr, canvas, window))
    window.bind("t", lambda e: (window.destroy(), main()) )
    window.mainloop()

def click(canvas, coords, mx):
    i=int(coords.x//SCALE)
    j=int(coords.y//SCALE)
    status = mx[j][i].status
    mx[j][i].status = not status
    tag = f"cell/{i}/{j}"
    color = "#888" if not status else "#333"

    canvas.create_rectangle(
            i*SCALE, j*SCALE, (i+1)*SCALE, (j+1)*SCALE,
            outline="#000",
            fill=color, tags=tag)
    canvas.tag_bind(tag, "<Button-1>", lambda e: click(canvas, e, mx))

def start(mx, canvas, window):
    while True:
        game(mx, canvas, window)
        sleep(SLEEP)
        canvas.delete("all")

def random(mx, canvas, window):
    for i in range(randint(GRID**2, GRID**2)):
        mx[randint(0, GRID-1)][randint(0, GRID-1)].status = True
    start(mx, canvas, window)

def game(mx, canvas, window):
    counter = 0
    newMx = np.empty((GRID, GRID), dtype=object)
    for i in range(GRID):
        for j in range(GRID):
            newMx[i][j] = Cell(i, j)
            newMx[i][j].status = mx[i][j].status

    for i in range(GRID):
        for j in range(GRID):
            newMx[i][j].check(mx)
            if newMx[i][j].status: 
                canvas.create_rectangle(
                    i*SCALE, j*SCALE, (i+1)*SCALE, (j+1)*SCALE,
                    outline="#000",
                    fill="#888")
                counter += 1
            else:
                canvas.create_rectangle(
                    i*SCALE, j*SCALE, (i+1)*SCALE, (j+1)*SCALE,
                    outline="#000",
                    fill="#333")
    for i in range(GRID):
        for j in range(GRID):
            mx[i][j].status = newMx[i][j].status
    window.update()
    if not counter: 
        window.destroy()
        main()



#! MAIN FUNCTION
def main():    
    window = Tk()
    window.title("The Game of Life")
    window.geometry(f"{SIZE}x{SIZE}")
    window.config(background="#333")
    window.resizable(0,0)
    produce(window)

if __name__ == "__main__": main()