#Lucas dos Anjos de Castro
#Railson Martins

__name__ = 'João de Santo Cristo'

MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

caminho = []
destinos = []
recurso = []

def custo_H(pos_origem, pos_destino):
    h = abs(pos_origem[1] - pos_destino[1])
    l = abs(pos_origem[0] - pos_destino[0])
    hipotenusa =( (h**2) + (l**2) )** 1/2
    return hipotenusa

def custo_G(map, pos_O, pos_D):
    O = map[tuple(pos_O)]
    D = map[tuple(pos_D)]
    if O == -1: return 10
    if D == -1: return 10
    return abs(D - O - 1)

def f(map, pos_O, pos_D): return (custo_H(pos_O, pos_D)*4) + custo_G(map, pos_O, pos_D)

def expandir(_map, _pos):
    valido = []
    # BORDAS
    if _pos[0] == 0 and _pos[1] == 0:  # cima esquerda <^
        # so posso ir para baixo e para frente
        valido.append(MOVE_RIGHT); valido.append(MOVE_DOWN)
    if _pos[1] == len(_map) - 1 and _pos[0] == 0:  # baixo esquerda <v
        # so posso ir para cima e para frente
        valido.append(MOVE_RIGHT); valido.append(MOVE_UP)
    if _pos[0] == len(_map) - 1 and _pos[1] == 0:  # cima direita ^>
        # so posso ir para baixo e para esquerda
        valido.append(MOVE_DOWN); valido.append(MOVE_LEFT)
    if _pos[0] == len(_map) - 1 and _pos[1] == len(_map) - 1:  # baixo direita V>
        # so posso ir para cima e para esquerda
        valido.append(MOVE_UP); valido.append(MOVE_LEFT)
    # PRIMEIRA LINHA EXCLUINDO BORDAS
    if _pos[1] == 0 and _pos[0] != len(_map) - 1 and _pos[0] != 0:
        # somente posso mover para baixo
        valido.append(MOVE_DOWN); valido.append(MOVE_RIGHT); valido.append(MOVE_LEFT)
    # ULTIMA LINHA EXCLUINDO BORDAS
    if _pos[1] == len(_map) - 1 and _pos[0] != 0 and _pos[0] != len(_map) - 1:
        # somente posso andar para cima
        valido.append(MOVE_UP); valido.append(MOVE_RIGHT); valido.append(MOVE_LEFT)
    # PRIMEIRA COLUNA EXCLUINDO BORDAS
    if _pos[0] == 0 and _pos[1] != 0 and _pos[1] != len(_map) - 1:
        # somente posso andar para direita
        valido.append(MOVE_RIGHT); valido.append(MOVE_UP); valido.append(MOVE_DOWN)
    # ULTIMA COLUNA EXCLUINDO BORDAS
    if _pos[0] == len(_map) - 1 and _pos[1] != 0 and _pos[1] != len(_map) - 1:
        # somente posso andar para esquerda
        valido.append(MOVE_LEFT); valido.append(MOVE_UP); valido.append(MOVE_DOWN)
    # DEMAIS CASOS (FORA DAS MARGENS)
    if _pos[0] > 0 and _pos[0] < len(_map) - 1 and _pos[1] > 0 and _pos[1] < len(_map) - 1:
        # posso movimentar para qualquer lado
        valido.append(MOVE_UP); valido.append(MOVE_DOWN); valido.append(MOVE_RIGHT); valido.append(MOVE_LEFT)
    valido.sort()
    return valido

def gerar_recursos(map, resources, player_base):
    # gerando lista de recursos a coletar
    global destinos
    if len(destinos) == 0:
        for i in range(0, len(resources)):
            if resources[i][3] == True:  # so vou armazenar os recursos que ainda não foram coletados
                destinos.append(((resources[i][0], resources[i][1]), custo_H((resources[i][0], resources[i][1]), player_base)))
        destinos.sort(key=lambda x: x[-1])  # ordenando com base na distancia Manhattan (função custo_H)

def checar(destino, resources):
    achou  = False
    for i in range(0, len(resources)):
        if resources[i][0] == destino[0] and resources[i][1] == destino[1] and resources[i][3] == True:
            achou =  True
    return achou


def andar(player_pos, mov):
    if mov == MOVE_UP: player_pos = list(player_pos); player_pos[1] -= 1
    if mov == MOVE_DOWN: player_pos = list(player_pos); player_pos[1] += 1
    if mov == MOVE_RIGHT: player_pos = list(player_pos); player_pos[0] += 1
    if mov == MOVE_LEFT: player_pos = list(player_pos); player_pos[0] -= 1
    player_pos = list(player_pos)
    return player_pos


def a_estrela(map, pos_origem, pos_destino, carrying):
    global caminho
    aberta = list()
    fechada = list()
    pos_atual = list(pos_origem)
    while pos_atual != list(pos_destino):
        validos = expandir(map, pos_atual)
        for i in range(0, len(validos)):
            # tupla no formato: coordenada, pai da coordenada, movimento que a gerou, custo
            validos[i] = (andar(pos_atual, validos[i]), pos_atual, validos[i], f(map, andar(pos_atual, validos[i]), pos_destino))# arrumar custo g
        achou = False
        destino = list()
        for i in range(0, len(validos)):
            if validos[i][0] == pos_destino:
                destino = validos[i]
                achou = True
        if achou:
            pos_atual = destino[0]
            caminho.append(destino[2])
        else:
            for i in range(0, len(validos)):
                aberta.append(validos[i])
            aberta.sort(key=lambda x: x[-1])
            pos_atual = aberta[0][0]
            fechada.append(aberta[0])
            caminho.append(aberta[0][2])
            del aberta[0]


def ataque(player_base, enemies_bases):
    for i in range(0, len(enemies_bases)):
        destinos.append(((enemies_bases[i]), -1, custo_H(player_base, enemies_bases[i])))
    destinos.sort(key=lambda x: x[-1])

def move(map, resources, enemies_pos, enemies_bases, player_pos, player_base, carrying, score, e_score):
    global caminho
    global recurso
    gerar_recursos(map, resources, player_base)
    recurso = list(destinos[0][0])
    if checar(recurso, resources) == False:
        del destinos[0]
    if len(caminho) == 0: # se não esxistir caminho a seguir
        if player_pos == player_base: # caso me encontre na base
            a_estrela(map, player_base, recurso, carrying)
        else: # caso não me encontre na base
            a_estrela(map, player_pos, player_base, carrying)

    mov = caminho[0]
    if len(caminho) > 0:
        del caminho[0]

    return mov
