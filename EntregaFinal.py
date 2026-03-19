from itertools import combinations
from Logica import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from types import MethodType
import random 



def escribir_casillas(self, literal):
    if '-' in literal:
        atomo = literal[1:]
        neg = ' NO'
    else:
        atomo = literal
        neg = ''
    x, y  = self.inv(atomo)
    return f"La casilla ({x},{y}) {neg} esta rellena"


      



class Nanograma:
    
    '''Clase representada para dar solucion al Nanograma 
        referencia: https://nonogramas.relaxweb.es/nonograma/96041
    '''


    def __init__(self):
        self.RenC = Descriptor([5,5])
        self.RenC.escribir = MethodType(escribir_casillas, self.RenC)
        self.condiciones_iniciales =  {x : None for x in range(10)}
        
        #Condiciones iniciales de las filas
        self.condiciones_iniciales[0] = [2,1]
        self.condiciones_iniciales[1] = 3
        self.condiciones_iniciales[2] = 4
        self.condiciones_iniciales[3] = [1,3]
        self.condiciones_iniciales[4] = 0
        
        #Condiciones iniciales de las columnas
        self.condiciones_iniciales[5] = [1,1]
        self.condiciones_iniciales[6] = 3
        self.condiciones_iniciales[7] = 3
        self.condiciones_iniciales[8] = 3
        self.condiciones_iniciales[9] = [1,2]
        


        self.reglas = []
        
#
    
    def clasificador_reglas(self):
        
        # Este metodo esta encargado de elegir las 10 reglas que se van a necesitar para resolver el nanograma
        # Dadas las condiciones iniciales
        
        
        # Al iniciar         self.reglas = []
        # finalizando este ciclo self.reglas tendra 10 reglas las cuales son la Ytoria de la solucion
        for x in self.condiciones_iniciales.keys(): 
            # Si la condicion es un numero solo va a hacer append de la regla a self.reglas dependiendo del numero que es la condicion inicial
            # Para esa fila y/o columna
            try:
                funciones_regla = {0: self.regla1, 1: self.regla2, 2: self.regla3,3: self.regla4, 4: self.regla5, 5: self.regla6}
                valor_condicion = self.condiciones_iniciales[x]
                if valor_condicion in funciones_regla:
                    self.reglas.append(funciones_regla[valor_condicion](x))

            except TypeError: 
                
                # Si la condicion es una secuencia de numeros solo va a hacer append de la regla dependiendo del numero que es la condicion inicial
                # Para esa fila y/o columna
                
                
                
                if self.condiciones_iniciales[x] == [1,1]: self.reglas.append(self.regla7(x))
                elif self.condiciones_iniciales[x] == [1,2]: self.reglas.append(self.regla8(x))
                elif self.condiciones_iniciales[x] == [1,3]: self.reglas.append(self.regla9(x))
                
                elif self.condiciones_iniciales[x] == [2,1]: self.reglas.append(self.regla10(x))
                elif self.condiciones_iniciales[x] == [2,2]: self.reglas.append(self.regla11(x))
                
                elif self.condiciones_iniciales[x] == [3,1]: self.reglas.append(self.regla12(x))
                
                elif self.condiciones_iniciales[x] == [1,1,1]: self.reglas.append(self.regla13(x))

                

    # Ninguna casilla rellena
    def regla1(self, cr): 
        lista = []
        
        #Caso para condicion incial en fila
        if cr < 5: 
            #el intervalo para la fila cr seria  [(cr, 0) (cr,1), (cr,2), (cr,3), (cr,4)] donde cr es el numero de fila
            intervalo_actual = [(cr, x) for x in range(5)]
        
        
        #caso para condicion inicial en columna donde cr-5 es el numero de columna
        else:  
            #el intervalo para la colmna cr seria [(0,cr), (1,cr), ..., (4,cr)] donde cr es el numero de columna
            intervalo_actual = [(x, cr-5 ) for x in range(5)]
        lista_negaciones = ['-' + self.RenC.P([*i]) for i in intervalo_actual]
        lista.append(Ytoria(lista_negaciones))

        return Otoria(lista)
    
    
    #unica casilla rellena
    def regla2(self, cr): 
        lista = []
        if cr < 5: 
            intervalo_actual= [(cr, x) for x in range(5)]
            for x in range(5):
                iterales = [self.RenC.P([cr,x])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] != x ]
                lista.append( Ytoria(iterales + lista_negaciones))     
        else:  
            intervalo_actual = [(x,cr-5) for x in range(5)]
            for x in range(5):
                iterales = [self.RenC.P([x,cr-5])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] != x ]
                lista.append(Ytoria(iterales + lista_negaciones))
        return Otoria(lista)        
        
    #relleno en dos casillas consecutivas
    
    def regla3(self, cr):
        lista = []
        if cr <5:
            intervalo_actual= [(cr,x) for x in range(5)]
            for x in range(4):
                iterales = [self.RenC.P([cr,x]), self.RenC.P([cr,x+1])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] != x and i[1] != x+1 ]
                lista.append(Ytoria(iterales + lista_negaciones ))
              
        else:
            
            intervalo_actual= [(x,cr-5) for x in range(5)]
            for x in range(4):
                iterales = [self.RenC.P([x, cr-5]), self.RenC.P([x+1, cr-5,])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] != x and i[0] != x+1 ]
                lista.append(Ytoria(iterales + lista_negaciones ))
            
        return Otoria(lista)
    
    
    #relleno en tres casilla consecutivas
    def regla4(self,cr):
        lista = []
        if cr<5:
            intervalo_actual= [(cr,x) for x in range(5)]
            for x in range(3):
                iterales = [self.RenC.P([cr,x]), self.RenC.P([cr,x+1]), self.RenC.P([cr, x+2])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] not in range(x, x+3)]
                lista.append(Ytoria(iterales + lista_negaciones))
                
        else: 
            intervalo_actual= [(x,cr-5) for x in range(5)]
            for x in range(3):
                iterales = [self.RenC.P([x, cr-5]), self.RenC.P([x+1, cr-5,]), self.RenC.P([x+2, cr-5])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] not in range(x, x+3)]
                lista.append(Ytoria(iterales + lista_negaciones))

        return Otoria(lista)
    
    
    # relleno en cuatro casillas consecutivas
    def regla5(self, cr):
        lista = []
        if cr<5:
            intervalo_actual= [(cr,x) for x in range(5)]
            for x in range(2):
                iterales = [self.RenC.P([cr,x]), self.RenC.P([cr,x+1]), self.RenC.P([cr, x+2]), self.RenC.P([cr, x+3])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] not in range(x, x+4)]
                lista.append(Ytoria(iterales + lista_negaciones))
                
        else:
            intervalo_actual= [(x,cr-5) for x in range(5)]
            for x in range(2):
                iterales = [self.RenC.P([x, cr-5]), self.RenC.P([x+1, cr-5,]), self.RenC.P([x+2, cr-5]), self.RenC.P([x+3, cr-5])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] not in range(x, x+4)]
                lista.append(Ytoria(iterales + lista_negaciones))
        return Otoria(lista)

    #relleno en 5 casillas consecutivas
    def regla6(self,cr):
        lista = []
        
        if cr<5: intervalo_actual= [(cr,x) for x in range(5)]
        else:  intervalo_actual = [(x, cr-5 ) for x in range(5)]
        
        lista.append(Ytoria([self.RenC.P([*i]) for i in intervalo_actual]))
        return Otoria(lista)            
        
            
                
    # rellenas dos casillas con minimo un espacio entre ambas input[1,1]
    def regla7(self,cr):
        lista = []
        if cr<5: 
            intervalo_actual= [(cr,x) for x in range(5)]
            for x in range(2,5):
                iterales = [self.RenC.P([cr,0]), self.RenC.P([cr,x])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] != x and i[1] != 0]
                lista.append(Ytoria(iterales + lista_negaciones)) 
                
            for x in range(3,5):
                iterales = [self.RenC.P([cr,1]), self.RenC.P([cr,x])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] != x and i[1] != 1]
                lista.append(Ytoria(iterales + lista_negaciones)) 
                
            lista.append(Ytoria([self.RenC.P([cr,2]), self.RenC.P([cr,4])]+ [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] != 2 and i[1] != 4]))
                
            
        else:
            intervalo_actual = [(x, cr-5 ) for x in range(5)]
            for x in range(2,5):
                iterales = [self.RenC.P([0,cr-5]), self.RenC.P([x,cr-5])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] != x and i[0] != 0]
                lista.append(Ytoria(iterales + lista_negaciones)) 

            for x in range(3,5):
                iterales = [self.RenC.P([1,cr-5]), self.RenC.P([x,cr-5])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] != x and i[0] != 1]
                lista.append(Ytoria(iterales + lista_negaciones)) 
                
            lista.append(Ytoria([self.RenC.P([2, cr-5]), self.RenC.P([4, cr-5])]+ [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] != 2 and i[0] != 4]))
            

        return Otoria(lista)            
            
    
            
     # rellenas una casilla, luego minimo un espacio hasta dos consecutivas  input: [1,2]     
    def regla8(self, cr):
        lista = []
        if cr<5:
            intervalo_actual = [(cr,x) for x in range(5)]
            for x in range(2,4):
                iterales = [self.RenC.P([cr,0]), self.RenC.P([cr,x]), self.RenC.P([cr,x+1])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] != x and i[1] != 0 and i[1] != x+1]
                lista.append(Ytoria(iterales + lista_negaciones))
            lista.append(Ytoria([self.RenC.P([cr,1]), self.RenC.P([cr,3]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] != 1 and i[1] != 3 and i[1] !=4] ))

        else:
            intervalo_actual = [(x, cr-5) for x in range(5)]
            for x in range(2,4):
                iterales = [self.RenC.P([0, cr-5]), self.RenC.P([x, cr-5]), self.RenC.P([x+1, cr-5])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] != x and i[0] != 0 and i[0] != x+1]
                lista.append(Ytoria(iterales + lista_negaciones))
            lista.append(Ytoria([self.RenC.P([1, cr-5]), self.RenC.P([3, cr-5]), self.RenC.P([4, cr-5])] +  [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] != 1 and i[0] != 3 and i[0] !=4] ))




        return Otoria(lista)       
    
    
    
    #rellena una casilla,luego minimo un espacio hasta 3 consecutivas input:[ 1,3]
    def regla9(self, cr):
        if cr<5: return Ytoria([self.RenC.P([cr,0]) ,self.RenC.P([cr,2]), self.RenC.P([cr,3]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([cr,1])])

        else: return Ytoria([self.RenC.P([0, cr-5]) ,self.RenC.P([2, cr-5]), self.RenC.P([3, cr-5]), self.RenC.P([4, cr-5])] +  [ '-' + self.RenC.P([1, cr-5])])

        
        
        
    #rellenas dos casillas consecutivas hata minimo un espacio y luego una rellena input:[2,1]
    
    def regla10(self, cr):
        lista = []
        if cr<5:
            intervalo_actual= [(cr,x) for x in range(5)]
            for x in range(3,5):
                iterales = [self.RenC.P([cr,0]), self.RenC.P([cr,1]), self.RenC.P([cr,x])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[1] != x and i[1] != 1 and i[1]!=0]
                lista.append(Ytoria(iterales + lista_negaciones))
            lista.append(Ytoria([self.RenC.P([cr,1]),self.RenC.P([cr,2]), self.RenC.P([cr,4])]+ [ '-' + self.RenC.P([cr,0]), '-' + self.RenC.P([cr,3]) ])) 
            
        else:
            intervalo_actual = [(x, cr-5 ) for x in range(5)]       
            for x in range(3,5):
                iterales = [self.RenC.P([0,cr-5]), self.RenC.P([1, cr-5]), self.RenC.P([x, cr-5])]
                lista_negaciones = [ '-' + self.RenC.P([*i])  for i in intervalo_actual if i[0] != x and i[0] != 1 and i[0]!=0]
                lista.append(Ytoria(iterales + lista_negaciones))
            lista.append(Ytoria([self.RenC.P([1, cr-5]),self.RenC.P([2, cr-5]), self.RenC.P([4, cr-5])]+ [ '-' + self.RenC.P([0, cr-5]), '-' + self.RenC.P([3, cr-5]) ])) 
            
        
        return Otoria(lista)

    
    # rellenas dos casillas consecutivas hasta un espacio y luego otras dos input: [2,2]
    def regla11(self, cr):
        if cr<5: return Ytoria([self.RenC.P([cr,0]) ,self.RenC.P([cr,1]), self.RenC.P([cr,3]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([cr,2])])

        else: return Ytoria([self.RenC.P([0, cr-5]) ,self.RenC.P([1, cr-5]), self.RenC.P([3, cr-5]), self.RenC.P([4, cr-5])] +  [ '-' + self.RenC.P([2, cr-5])])

    # rellenas tres consecutivas hasta un espacio y luego una rellena input:[3,1]
    def regla12(self,cr):
        if cr<5: return Ytoria([self.RenC.P([cr,0]) ,self.RenC.P([cr,1]), self.RenC.P([cr,2]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([cr,3])])
        else: return Ytoria([self.RenC.P([0, cr-5]) ,self.RenC.P([1, cr-5]), self.RenC.P([2, cr-5]), self.RenC.P([4, cr-5])] +  [ '-' + self.RenC.P([3, cr-5])])

    
    #rellenas tres con espacios input [1,1,1]
    def regla13(self, cr):
        
        if cr<5: return Ytoria([self.RenC.P([cr,0]) ,self.RenC.P([cr,2]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([cr,1]), '-' + self.RenC.P([cr,3])])
        else: return Ytoria([self.RenC.P([0, cr-5]) ,self.RenC.P([2, cr-5]),  self.RenC.P([4, cr-5])] +  ['-' + self.RenC.P([1, cr-5]),'-' + self.RenC.P([3, cr-5])])

    
        

    
    def visualizar(self, I):  

        fig, axes = plt.subplots()
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        step = 1./5
        tangulos = []
        

        for i in range(3):
            for j in range(3):
                tangulos.append(patches.Rectangle((i * step, j * step), step, step, facecolor='white'))
        
        
        for j in range(5):
            locacion = j * step
            tangulos.append(patches.Rectangle((0, step + locacion), 1, 0.005, facecolor='black'))
            tangulos.append(patches.Rectangle((step + locacion, 0), 0.005, 1, facecolor='black'))

            
        for f in tangulos:
            axes.add_patch(f)
        
        arr_img = plt.imread("./img/cuadrado.png", format='png')
        imagebox = OffsetImage(arr_img, zoom=0.161)
        imagebox.image.axes = axes

        
        direcciones = {(x,y): (0.100 + 0.200 * y, 0.880 - 0.200 * x) for x in range(5) for y in range(5)}
        
        for l in I:
            
            if I[l]:
                try:
                    x, y = self.RenC.inv(l)
                    ab = AnnotationBbox(imagebox, direcciones[(x, y)], frameon=False)
                    axes.add_artist(ab)
                except KeyError: pass
            
        plt.show()

        
    
import time
 
    

    
    
c = Nanograma()
c.clasificador_reglas()
print(c.condiciones_iniciales)
# print(c.condiciones_iniciales)

A = inorder_to_tree(Ytoria(c.reglas))
print(A.ver(c.RenC))



## DPLL

start_time = time.time()

A = Ytoria(c.reglas)
S = tseitin(A)
S, I = dpll(S, {})


if I != None:
    for k in I:
        c.RenC.escribir(k), I[k]
            
        
else:
    print('¡No hay solución!')

c.visualizar(I)

print("--- %s seconds ---" % (time.time() - start_time))  




## SAT tableaux

# start_time = time.time()

# A = inorder_to_tree(Ytoria(c.reglas[0:5]))
# I = A.SATtabla()


# if I != None:
#     for k in I:
#         print(c.RenC.escribir(k), I[k])
# else:
#     print('¡No hay solución!')
    
# c.visualizar(I)

# print("--- %s seconds ---" % (time.time() - start_time))  





##WalkSAT

# start_time = time.time()

# A = Ytoria(c.reglas)
# S = tseitin(A)
# S, I = walkSAT(S)


# if I != None:
#     for k in I:
#         print(c.RenC.escribir(k), I[k])
            
        
# else:
#     print('¡No hay solución!')

# c.visualizar(I)


# print("--- %s seconds ---" % (time.time() - start_time))  

