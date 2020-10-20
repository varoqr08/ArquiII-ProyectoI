import threading
import time 
import numpy as np
import random
from memory import Memory
from asociate import asociate
from L1 import L1
from BusAux import BusAux
import logging
from tkinter import *
from table import Table


def main():
    main_memory = Memory()
    cache_L1_00 = L1(0,'P0')
    cache_L1_01 = L1(0,'P1')
    cache_L1_10 = L1(1,'P0')
    cache_L1_11 = L1(1,'P1')

    cache_BusAux_0 = BusAux(0)
    cache_BusAux_1 = BusAux(1)



    time.sleep(5)

    #Invocacion para generar los asociates
    asociate0 = asociate(0, main_memory, cache_L1_00, cache_L1_01, cache_L1_10, cache_L1_11, cache_BusAux_0, cache_BusAux_1)
    asociate1 = asociate(1, main_memory, cache_L1_00, cache_L1_01, cache_L1_10, cache_L1_11, cache_BusAux_0, cache_BusAux_1)
    asociate0.start()
    asociate1.start()

    root = Tk()
    root.configure(bg='light blue')
    root.geometry('1400x700')

    frame = Frame(root)
    frame.pack()
    
    button = Button (frame, text = "Close Window", command=root.destroy)
    button.pack()

    
    #Titulo de tablas
    #Cache L1 P1
    label_titulo_L100 = Label(text = 'Cache L1, Procesador1')
    label_titulo_L100.config(font=('Sans', 20))
    label_titulo_L100.config(bg="light blue") 
    label_titulo_L100.place(x=85,y=150)

    #Cache L1 P2
    label_titulo_L101 = Label(text = 'Cache L1, Procesador2')
    label_titulo_L101.config(font=('Sans', 20))
    label_titulo_L101.config(bg="light blue") 
    label_titulo_L101.place(x=85,y=300)


    #Cache L1 10
    label_titulo_L100 = Label(text = 'Cache L1, Procesador3')
    label_titulo_L100.config(font=('Sans', 20))
    label_titulo_L100.config(bg="light blue") 
    label_titulo_L100.place(x=900,y=150)

    #Cache L1 11
    label_titulo_L101 = Label(text = 'Cache L1, Procesador4')
    label_titulo_L101.config(font=('Sans', 20))
    label_titulo_L101.config(bg="light blue") 
    label_titulo_L101.place(x=900,y=300)
    
    #Memoria
    label_titulo_M = Label(text = 'Memoria Principal')
    label_titulo_M.config(font=('Sans', 20))
    label_titulo_M.config(bg="light blue") 
    label_titulo_M.place(x=530,y=100)

    #Tablas
    #Tabla para cache L1 P0 asociate 0
    table_L100 = Table(root, 5, 4)
    titles = ['#Linea','Estado','Dir Memoria','Dato']
    table_L100.createTable(titles, 'gray', 'white', True)
    table_L100.place(x=80, y=200)

    #Tabla para cache L1 P1 asociate 0
    table_L101 = Table(root, 5, 4)
    titles = ['#Linea','Estado','Dir Memoria','Dato']
    table_L101.createTable(titles, 'gray', 'white', True)
    table_L101.place(x=80, y=350)


    #Tabla para cache L1 P0 asociate 1
    table_L110 = Table(root, 5, 4)
    titles = ['#Linea','Estado','Dir Memoria','Dato']
    table_L110.createTable(titles, 'gray', 'white', True)
    table_L110.place(x=900, y=200)

     #Tabla para cache L1 P0 asociate 1
    table_L111 = Table(root, 5, 4)
    titles = ['#Linea','Estado','Dir Memoria','Dato']
    table_L111.createTable(titles, 'gray', 'white', True)
    table_L111.place(x=900, y=350)

    #Tabla para cache BusAux asociate 0
    table_memory = Table(root, 17, 3)
    titles = ['Direccion','Estado','Dato']
    table_memory.createTable(titles, 'gray', 'white', False)
    table_memory.place(x=530, y=150)

    #Tabla de instrucciones
    #Tabla para cache BusAux asociate 0
    inst_1 = StringVar()
    instruction00 = Label(textvariable = inst_1, font=("Papayrus", 14), bg='light blue')
    instruction00.pack()
    instruction00.place(x=80, y=50)

    inst_2 = StringVar()
    instruction01 = Label(textvariable = inst_2, font=("Papayrus", 14), bg='light blue')
    instruction01.pack()
    instruction01.place(x=80, y=100)

    inst_3 = StringVar()
    instruction10 = Label(textvariable = inst_3, font=("Papayrus", 14), bg='light blue')
    instruction10.pack()
    instruction10.place(x=900, y=50)

    inst_4 = StringVar()
    instruction11 = Label(textvariable = inst_4, font=("Papayrus", 14), bg='light blue')
    instruction11.pack()
    instruction11.place(x=900, y=100)


    
    

    while(True):
        time.sleep(1) # Need this to slow the changes down

        inst_1.set("Procesador 1: "+asociate0.core0.instruction)
        inst_2.set("Procesador 2: "+asociate0.core1.instruction)
        inst_3.set("Procesador 3: "+asociate1.core0.instruction)
        inst_4.set("Procesador 4: "+asociate1.core1.instruction)

        #Tabla de cache L1 P1 actualizada
        table_L100.set(1,1,cache_L1_00.lines[0].state)
        table_L100.set(1,2,cache_L1_00.lines[0].directionBin)
        table_L100.set(1,3,cache_L1_00.lines[0].data)
        table_L100.set(2,1,cache_L1_00.lines[1].state)
        table_L100.set(2,2,cache_L1_00.lines[1].directionBin)
        table_L100.set(2,3,cache_L1_00.lines[1].data)
        table_L100.set(3,1,cache_L1_00.lines[0].state)
        table_L100.set(3,2,cache_L1_00.lines[0].directionBin)
        table_L100.set(3,3,cache_L1_00.lines[0].data) 
        table_L100.set(4,1,cache_L1_00.lines[1].state)
        table_L100.set(4,2,cache_L1_00.lines[1].directionBin)
        table_L100.set(4,3,cache_L1_00.lines[1].data)


        


        #Tabla de cache L1 P2 actualizada
        table_L101.set(1,1,cache_L1_01.lines[0].state)
        table_L101.set(1,2,cache_L1_01.lines[0].directionBin)
        table_L101.set(1,3,cache_L1_01.lines[0].data)
        table_L101.set(2,1,cache_L1_01.lines[1].state)
        table_L101.set(2,2,cache_L1_01.lines[1].directionBin)
        table_L101.set(2,3,cache_L1_01.lines[1].data)
        table_L101.set(3,1,cache_L1_00.lines[0].state)
        table_L101.set(3,2,cache_L1_00.lines[0].directionBin)
        table_L101.set(3,3,cache_L1_00.lines[0].data) 
        table_L101.set(4,1,cache_L1_00.lines[1].state)
        table_L101.set(4,2,cache_L1_00.lines[1].directionBin)
        table_L101.set(4,3,cache_L1_00.lines[1].data)


        #Tabla de cache L1 P3 actualizada
        table_L110.set(1,1,cache_L1_10.lines[0].state)
        table_L110.set(1,2,cache_L1_10.lines[0].directionBin)
        table_L110.set(1,3,cache_L1_10.lines[0].data)
        table_L110.set(2,1,cache_L1_10.lines[1].state)
        table_L110.set(2,2,cache_L1_10.lines[1].directionBin)
        table_L110.set(2,3,cache_L1_10.lines[1].data)
        table_L110.set(3,1,cache_L1_00.lines[0].state)
        table_L110.set(3,2,cache_L1_00.lines[0].directionBin)
        table_L110.set(3,3,cache_L1_00.lines[0].data) 
        table_L110.set(4,1,cache_L1_00.lines[1].state)
        table_L110.set(4,2,cache_L1_00.lines[1].directionBin)
        table_L110.set(4,3,cache_L1_00.lines[1].data)

        #Tabla de cache L1 P4 actualizada
        table_L111.set(1,1,cache_L1_11.lines[0].state)
        table_L111.set(1,2,cache_L1_11.lines[0].directionBin)
        table_L111.set(1,3,cache_L1_11.lines[0].data)
        table_L111.set(2,1,cache_L1_11.lines[1].state)
        table_L111.set(2,2,cache_L1_11.lines[1].directionBin)
        table_L111.set(2,3,cache_L1_11.lines[1].data)
        table_L111.set(3,1,cache_L1_00.lines[0].state)
        table_L111.set(3,2,cache_L1_00.lines[0].directionBin)
        table_L111.set(3,3,cache_L1_00.lines[0].data) 
        table_L111.set(4,1,cache_L1_00.lines[1].state)
        table_L111.set(4,2,cache_L1_00.lines[1].directionBin)
        table_L111.set(4,3,cache_L1_00.lines[1].data)


        #Tabla de memoria principal actualizada
        table_memory.set(1,1,main_memory.lines[0].state)
        table_memory.set(1,2,main_memory.lines[0].data)

        table_memory.set(2,1,main_memory.lines[1].state)
        table_memory.set(2,2,main_memory.lines[1].data)

        table_memory.set(3,1,main_memory.lines[2].state)
        table_memory.set(3,2,main_memory.lines[2].data)

        table_memory.set(4,1,main_memory.lines[3].state)
        table_memory.set(4,2,main_memory.lines[3].data)

        table_memory.set(5,1,main_memory.lines[4].state)
        table_memory.set(5,2,main_memory.lines[4].data)

        table_memory.set(6,1,main_memory.lines[5].state)
        table_memory.set(6,2,main_memory.lines[5].data)

        table_memory.set(7,1,main_memory.lines[6].state)
        table_memory.set(7,2,main_memory.lines[6].data)

        table_memory.set(8,1,main_memory.lines[7].state)
        table_memory.set(8,2,main_memory.lines[7].data)

        table_memory.set(9,1,main_memory.lines[8].state)
        table_memory.set(9,2,main_memory.lines[8].data)

        table_memory.set(10,1,main_memory.lines[9].state)
        table_memory.set(10,2,main_memory.lines[9].data)

        table_memory.set(11,1,main_memory.lines[10].state)
        table_memory.set(11,2,main_memory.lines[10].data)

        table_memory.set(12,1,main_memory.lines[11].state)
        table_memory.set(12,2,main_memory.lines[11].data)

        table_memory.set(13,1,main_memory.lines[12].state)
        table_memory.set(13,2,main_memory.lines[12].data)

        table_memory.set(14,1,main_memory.lines[13].state)
        table_memory.set(14,2,main_memory.lines[13].data)

        table_memory.set(15,1,main_memory.lines[14].state)
        table_memory.set(15,2,main_memory.lines[14].data)

        table_memory.set(16,1,main_memory.lines[15].state)
        table_memory.set(16,2,main_memory.lines[15].data)

        root.update_idletasks()
        root.update()



    root.mainloop()
    


   
    

if __name__ == "__main__":
    main()

    
    
