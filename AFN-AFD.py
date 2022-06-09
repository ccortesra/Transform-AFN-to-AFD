from hashlib import new
from tkinter import image_names


class Estado:
    def __init__(self, nombre):   
        self.nombre = nombre
        self.funcionTransicion = {} # función definida para este estado
        self.inicial = False
        self.terminal = False
        self.pasadoAFN = []

    def CrearFuncion(self, alfabeto):
        """
        CrearFuncion
        param: alfabeto -> Alfabeto general del automata
        procedure:
        CrearFuncion() va por cada simbolo del alfabeto que tenemos para el 
        automata, pide los estados resultantes por cada uno, despues los 
        asigna al diccionario de este estado, que almacena con la llave, que es el
        simbolo, su respectiva imagen en delta
        """
        for simbolo in alfabeto:
            estadosResultantes = list(input(f"Ingrese los estados resultantes de d({self.nombre},{simbolo}) separandolos por espacios: \n").split(' '))
            self.funcionTransicion[simbolo] = estadosResultantes 
    
# def SolveAFN(conjuntoEstados,listaSimbolos,pasadoAFN=None):
#     newName = input(f"Ingrese un nombre nuevo para el estado resultande de {conjuntoEstados}: \n")
#     newEstado = Estado(newName)
#     Estado[newName] = newEstado
#     for x in listaSimbolos:
#         newEstado.funcionTransicion[x] = set()
#         for c in conjuntoEstados:
#             # Este for va por cada estado del conjunto de estados, en ese simbolo 
#             # en particular añadira la imagen de ese estado, hasta completarlos todos
#             # el set asegura que no se repitan
#             newEstado.funcionTransicion[x].update(c.funcionTransicion[x])
#         newEstado.funcionTransicion[x] = list(newEstado.funcionTransicion[x])
#         if len(newEstado.funcionTransicion[x]) > 1:
#             SolveAFN(newEstado.funcionTransicion[x])



# La función delta para AFN esta definida como: 
# d(q,x) = {q0,q1,q2,..,qn}, QxE -> P(Q) <<partes de Q>>  

# Podriamos usar dataframes de pandas para representar 
# la matriz del automata*


def ImprimeAutomata(Estados):
    for nombreEstado in Estados:
        estado = Estados[nombreEstado]
        print(f'{nombreEstado} ----------------------------------------')
        print(estado.funcionTransicion)


def main():
    listaEstados = list(input("Ingrese los estados separandolos por espacios: \n").split(' '))  
    listaSimbolos = list(input("Ingrese los simbolos separandolos por espacios: \n").split(' ')) 
    eInicial = list(input("Ingrese el estado inicial: \n"))
    listaTerminales = list(input("Ingrese los estados terminales separandolos por espacios: \n").split(' '))
    print(listaEstados)
    print(listaSimbolos)

    # **********************************************************************
    # 1. Preparamos el ambiente para los estados, definimos quienes son iniciales
    # y quienes son finales, cresmos sus funciones
    global Estados
    Estados = {}
    for q in listaEstados:
        newEstado = Estado(q)
        # El siguiente bloque de codigo configura los estados iniciales y terminales
        if newEstado.nombre in eInicial:
            newEstado.inicial = True
        elif newEstado.nombre in listaTerminales:
            newEstado.terminal = True

        newEstado.CrearFuncion(listaSimbolos)
        Estados[newEstado.nombre] = newEstado

    # ************************************************************************
    # 2. Iteramos por todos los estados, buscando las d(q,s), que tengan más 
    # de un estado ej [q1,q2,...,qn-1,qn], los añadimos a una cola para resolverlos

    
    queue = []
    for q in Estados.values():
        for key in q.funcionTransicion: # por cada simbolo en delta
            if(len(q.funcionTransicion[key]) > 1): 
                # Si encuentra una imagen de delta con mas de un elemento
                # se mete a la queue, donde luego los resolveremos
                queue.append(q.funcionTransicion[key])

    # ************************************************************************
    # 3. Ahora sacamos los elementos de la cola, y algoritmicamente, creamos
    # las funciones para estos [q1,q2,...,qn], puede que aparezcan de despues 
    # de resueltos, por ello tenemos una lista de resueltos, y si ya estan ahí
    # no hacemos el proceso
    resueltos = []
    while queue != []:
        conjuntoEstados = queue.pop(0) 
        if not(sorted(conjuntoEstados) in resueltos):
            newName = str(sorted(conjuntoEstados))
            newEstado = Estado(newName)
            Estados[newName] = newEstado
            for x in listaSimbolos:
                newEstado.funcionTransicion[x] = set()
                for c in conjuntoEstados:
                    # Este for va por cada estado del conjunto de estados, en ese simbolo 
                    # en particular añadira la imagen de ese estado, hasta completarlos todos
                    # el set asegura que no se repitan
                    Ec = Estados[c]
                    if Ec.funcionTransicion[x] != ['']:
                        newEstado.funcionTransicion[x].update(Ec.funcionTransicion[x])
                newEstado.funcionTransicion[x] = list(newEstado.funcionTransicion[x])
                if len(newEstado.funcionTransicion[x]) > 1 and not(newEstado.funcionTransicion[x] in resueltos):
                    queue.append(newEstado.funcionTransicion[x])
            resueltos.append(sorted(conjuntoEstados))
    
    ImprimeAutomata(Estados)
    print(resueltos)
    
    # *******************************************************************
    # 4. Con los estados multiples que esten en resueltos, iremos iterando por
    # estados, y cambiando todas las "casillas donde esté este estado"
    for estadoMultiple in resueltos:
        newName = input(f"Ingrese un nuevo nombre para el"
        f"estado multiple {estadoMultiple}: \n")
        # Cabiar el estado en si mismo
        Estados[newName] = Estados[str(estadoMultiple)]
        del Estados[str(estadoMultiple)] 
        Estados[newName].nombre = newName
        # Iterar por cada casilla
        for q in Estados:
            for x in listaSimbolos:
                if sorted(Estados[q].funcionTransicion[x]) == estadoMultiple:
                    Estados[q].funcionTransicion[x] = newName
    ImprimeAutomata(Estados)

   
    
main()