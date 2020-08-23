#Definindo Infinito
INF = 100000000
#Definindo a distancia total inicial como 0
dist_total = 0

#Função que imprimi as ruas entre coordenadas
def printRuas(ruas):
    #Como as ruas foram armazenadas a partir do destino então 
    # a lista deve ser invertida
    imprimi = ruas[::-1]
    #Variavel que armazena a rua que esta sendo percorrida no momento
    nomeRua = "vazio"
    print("--------------Trajeto---------------")
    print("[", end="")

    #Percorre a lista de ruas
    for i in range(len(ruas)):
        #Caso a rua seja diferente da atual, então a rua atual é atualizada e impressa,
        #caso contrario nada é impresso
        if(imprimi[i] != nomeRua):
            if(i == len(ruas)):
                print(imprimi[i], end="")
            else:
                print(imprimi[i], end=" -> ")
            
            nomeRua = imprimi[i]
    print("]")
    return 0

#Com a distacia anteriormente é impresso a distancia nas seguintes formas:
# Se a distancia for maior que 1 km: "X" kilometro(s) e "Y" metros
#Se não: "X" metros
#Essa função tbm soma todas as distancias calculadas para chegar a distancia total da rota
def printDist(dist):

    global dist_total
    dist_total = dist_total + dist

    if(dist >= 1000):
        dist = dist/1000

        ns = str(dist)
        if(ns[0] == "1"):    
            print("Distancia Total: " + ns[0],end=" kilometro e ")
        else:
            print("Distancia Total: " + ns[0],end=" kilometros e ")
        for i in range(len(ns)):
            if(i > 1):
                print(ns[i], end="")
        print(" metros")
    else:
        print("Distancia Total: " + str(dist) + " metros")
    
    print()
    
    return 0 

#Função que mostra a menor rota com base nos pais de cada vertice
def solução(pai, grafo, origem, destino):
    #A função comela a partir do destino e vai até a origem
    t_atual = destino
    dist = 0
    ruas = []

    #Se o destino for igual a origem então é impresso a seguinte afirmação
    if(origem == destino):
        print("Origem é igual ao destino")
    #Caso contrario é percorrido o pai de cada vertice até chegar na origem
    else:
        while(t_atual != origem):
            #O proximo vertice deve ser o pai do vertice atual
            prox = pai[t_atual]
            #Todos os vizinhos do vertice pai é percorrido até encontrar o vertice do vertice atual
            #Então é calculada a distancia e armazenada a rua percorrida
            for ant in grafo[prox]:
                if(ant[0] == t_atual):
                    dist = dist + ant[2]
                    ruas.append(ant[1])
            #t_atual passa a ser então o pai do vertice
            t_atual = prox

    #Imprimi todas as ruas percorridas
    printRuas(ruas)
    #Imprimi a distancia total entre as coordenadas
    printDist(dist)

    return 0

#Função que encontra o vizinho de menor distancia de um determinado vertice
def min(dist, visitado, N):
    min = INF

    for i in range(N):
        if(visitado[i] == 0 and dist[i] <= min):
            min = dist[i]
            index = i
    
    return index

#Função que calculara a menor rota dado dois vertices do grafo
def dijkstra(grafo, origem, destino):

    #numero de vertices
    N = len(grafo)

    #Listas contendo o pai de cada vertice, se o vertice ja foi visitado e a distancia 
    # apos a aplicação do relax
    pai = [-1 for i in range(N)]
    visitado = [0 for i in range(N)]
    dist = [INF for i in range(N)]
    
    #Vertice origem tem distancia 0
    dist[origem] = 0
    
    t_atual = origem

    #Percorre todos os vertices menos a partir da origem
    for i in range(N-1):
        #Variavel que recebe o menor vizinho do vertice atual
        t_atual = min(dist, visitado, N)
        #Se visitado for 1 então significa que o vertice foi visitado
        visitado[t_atual] = 1
        #A partir do vertice atual é feito o relax para cada vizinho
        for vertice in grafo[t_atual]:
            if(grafo[vertice[0]] != [] and dist[t_atual] + vertice[2] < dist[vertice[0]]):
                dist[vertice[0]] = dist[t_atual] + vertice[2]
                pai[vertice[0]] = t_atual
    
    #Com os resultados do dijkstra é calculado a solução do problema
    solução(pai, grafo, origem, destino)
    
    return 0

#Função que cria o grafo com base nos dados do arquivo com os vertices
# armazenados em uma lista de vertices
def cria_grafo(listaDeInformações):
    #O grafo é representado por um discionario, que funciona como uma
    # lista de adjacencia
    grafo = {}

    #Define cada vertice como uma chave do dicionario
    for i in range(274):
        grafo[i] = []
    
    #Em cada linha esta o vertice de origem, vertice de destino,
    # o nome da rua e a distancia de cada aresta
    for linha in listaDeInformações:
        #Cada linha é uma string, então é usada a função .split() para
        # pegar as informações relevantes
        dados = linha.split(",")
        #lista contendo as informações relevantes
        informações = []

        #Em informações serão armazenados os dados na seguinte ordem:
        # vertice destino -> nome da rua -> distancia
        informações.append(int(dados[1]))
        informações.append(dados[2])
        informações.append(int(dados[3]))
        
        #A posição 0 de dados contem o vertice origem que sera usado como chave no discionario
        grafo[int(dados[0])].append(informações)

    return grafo

#Função que ira ler o arquivo contendo o percurso do onibus
# e usando ele é calculada a menor distancia total usando o algoritmo de dijkstra
def imprimiPercurso(grafo):
    #Variavel global para o calculo da distancia entre todos os pontos listados no arquivo
    global dist_total
    #Abertura do aquivo contendo todas as coordenadas que serão percorridas
    arquivoPercurso = open("percurso.txt")
    percurso = arquivoPercurso.readlines()

    #Para cada coordenada armazenada é chamada o algoritmo de dijkstra para calcular a menor
    # rota entre os dois pontos
    for coordenada in percurso:
        pontos = coordenada.split(",")
        dijkstra(grafo, int(pontos[0]),int(pontos[1]))
    
    arquivoPercurso.close()

    #imprimi a distancia total de todas as coordenadas
    print("-------------- Rota Inteira ----------------")
    printDist(dist_total)
    print("Distancia total da rota usada pela empresa: 5 kilometros e 500 metros")
    print()

    return 0

#Função Main que é chamada para inicializar o programa      
def main():
    #Abertura do arquivo que lista todos os vertices que representam 
    # o mapa do centro de Lavras, suas respectivas arestas, o nome da rua
    # e a distancia
    arquivo = open("LavrasRuas.txt")
    listaDeInformações = arquivo.readlines()

    #Função que cria o grafo com base nos dados do arquivo
    grafo = cria_grafo(listaDeInformações)

    arquivo.close()

    print("Calculo realizado com sucesso!")

    return grafo

def imprimiMenu():
    print("1 - Modelar mapa\n"
          "2 - Mostrar trajeto Lavrinhas/Centro\n"
          "3 - Calcular distancia entre dois pontos(1 a 274)\n"
          "0 - Sair\n")


def inicia():
    global dist_total
    
    imprimiMenu()

    gerouGrafo = False
    
    print("Digite a opção: ", end="")

    entrada = int(input())

    print()

    while(entrada != 0):
        if(entrada == 1):
            if not(gerouGrafo):
                #Chamada a função que ira dar inicio ao programa
                grafo = main()
                gerouGrafo = True
            else:
                print("Grafo já foi gerado!")
        elif(entrada == 2):
            if(gerouGrafo):
                dist_total = 0
                #Função que imprimi o percuso a ser realizado pelo onibus
                imprimiPercurso(grafo)
            else:
                print("Dados do grafo não carregados.")
        elif(entrada == 3):
            if(gerouGrafo):
                
                print("Digite o ponto origem:", end=" ")
                a = int(input())
                print()

                print("Digiteo o ponto de destino:", end=" ")
                b = int(input())

                dist_total = 0
                dijkstra(grafo, a, b)
            else:
                print("Dados do grafo não carregados.")
        
        print("Digite a opção: ", end="")
        
        entrada = int(input())
    
        print()

    return 0

inicia()



