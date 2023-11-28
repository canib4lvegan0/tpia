import random
from collections import deque

NAIPE = '♠'
# RANKS = 'A23456789TJQK'
RANKS = 'A2345'
N_PILHAS = 1


class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
        self.virada_para_cima = False

    def __repr__(self):
        return f"{self.valor}{self.naipe}"


def checa_movimento_pilha(carta_origem, carta_destino):
    index_origem = RANKS.index(carta_origem.valor)
    index_destino = RANKS.index(carta_destino.valor)

    return index_origem + 1 == index_destino


def checa_movimento_sequencia(carta_origem, sequencia):
    index_origem = RANKS.index(carta_origem.valor)
    if not sequencia:
        return index_origem == 0

    carta_sequencia = sequencia[-1]
    index_destino = RANKS.index(carta_sequencia.valor)
    return index_origem == index_destino + 1


class JogoPaciencia:
    def __init__(self):
        self.baralho = [Carta(NAIPE, valor) for valor in RANKS]
        random.shuffle(self.baralho)
        self.tabuleiro = [deque() for _ in range(N_PILHAS)]
        self.pilha_descarte = deque()
        self.pilha_estoque = deque(self.baralho)
        self.pilha_sequencia = deque()

    def distribuir_cartas(self):
        for i in range(N_PILHAS):
            for j in range(i + 1):
                carta = self.pilha_estoque.pop()
                if j == i:
                    carta.virada_para_cima = True
                self.tabuleiro[j].append(carta)

    def exibir_tabuleiro(self, rodada):
        print('_._' * 30 + '\n ' + '_._' * 13 + f' [Rodada: {rodada}] ' + '_._' * 12)
        print(f'Estoque: {["*" for _ in range(len(self.pilha_estoque))]}')
        print(f'Descarte: {[carta.__str__() for carta in self.pilha_descarte]}')
        print(f'Sequência montada: {[carta.__str__() for carta in self.pilha_sequencia]}')
        i = 0
        for pilha in self.tabuleiro:
            print(f'Pilha[{i}]: {[carta.__str__() for carta in pilha]}')
            i = i + 1
        print('_._' * 30)

    def retirar_estoque(self):
        if self.pilha_estoque:
            carta = self.pilha_estoque.pop()
            self.pilha_descarte.append(carta)
            print(f'Desvirando {carta} do Estoque.')
            return

        print(f'Estoque vazio!')

    def mover_descarte_sequencia(self):
        if not self.pilha_descarte:
            print(f'Descarte vazio!')
            return

        if not self.pilha_sequencia or checa_movimento_sequencia(self.pilha_descarte[-1], self.pilha_sequencia):
            carta = self.pilha_descarte.pop()
            self.pilha_sequencia.append(carta)
            print(f'Movendo {carta} de Descarte para Sequencia.')
        else:
            print(f'Movimento inválido! {self.pilha_descarte[-1]} não encaixa em {self.pilha_sequencia[-1]}.')

    def mover_pilha_sequencia(self, origem):
        pilha_origem: deque = self.tabuleiro[origem]

        if not pilha_origem:
            print(f'Pilha[{origem}] vazia!')
            return

        if not self.pilha_sequencia or checa_movimento_sequencia(pilha_origem[-1], self.pilha_sequencia):
            carta = pilha_origem.pop()
            self.pilha_sequencia.append(carta)
            print(f'Movendo {carta} da Pilha[{origem}] para Sequência.')
        else:
            print(f'Movimento inválido! {pilha_origem[-1]} não encaixa em {self.pilha_sequencia[-1]}.')

    def mover_descarte_pilha_tabuleiro(self, destino):
        if not self.pilha_descarte:
            print(f'Descarte vazio!')
            return

        pilha_destino: deque = self.tabuleiro[destino]
        if not pilha_destino or checa_movimento_pilha(self.pilha_descarte[-1], pilha_destino[-1]):
            carta = self.pilha_descarte.pop()
            pilha_destino.append(carta)
            print(f'Movendo {carta} do Descarte para Pilha[{destino}].')
        else:
            print(f'Movimento inválido! {self.pilha_descarte[-1]} não encaixa em {pilha_destino[-1]}.')

    def mover_entre_pilhas_tabuleiro(self, origem, destino):
        pilha_origem: deque = self.tabuleiro[origem]
        pilha_destino: deque = self.tabuleiro[destino]

        if pilha_origem and (not pilha_destino or checa_movimento_pilha(pilha_origem[-1], pilha_destino[-1])):
            carta = pilha_origem.pop()
            pilha_destino.append(carta)
            print(f'Movendo {carta} da Pilha[{origem}] para Pilha[{destino}].')
        else:
            print(f'Movimento inválido! {pilha_origem[-1]} não encaixa em {pilha_destino[-1]}.')

    def terminou(self):
        # Checa se fechou a sequência
        sequencia_atual = ''.join([carta.valor for carta in self.pilha_sequencia])
        if sequencia_atual == RANKS:
            print('************\nGanhou!\n************')
            return True

        # Checa se ainda tem carta pra virar no estoque
        elif self.pilha_estoque:
            return False

        # Checa se ainda a sequência ainda não foi iniciada ou tem movimento possível entre descarte-sequencência
        elif self.pilha_descarte and (not self.pilha_sequencia or
                                      checa_movimento_sequencia(self.pilha_descarte[-1], self.pilha_sequencia)):
            return False

        # Checa se ainda tem movimento possível entre descarte-pilhas
        elif self.pilha_descarte:
            for pilha in self.tabuleiro:
                if not pilha:
                    return False

                carta_pilha = pilha[-1]
                if checa_movimento_pilha(self.pilha_descarte[-1], carta_pilha):
                    return False

        # Checa se ainda tem movimento possível entre pilhas-sequência
        elif self.tabuleiro:
            for pilha in self.tabuleiro:
                if not pilha:
                    return False

                topo_pilha = pilha[-1]
                if checa_movimento_sequencia(topo_pilha, self.pilha_sequencia):
                    return False

        # Checa se ainda tem movimento possível entre pilhas do tabuleiro
        elif self.tabuleiro:
            for indice_origem in range(N_PILHAS):
                if not self.tabuleiro[indice_origem]:
                    return False

                for indice_destino in range(N_PILHAS):
                    if not self.tabuleiro[indice_destino]:
                        return False

                    if checa_movimento_pilha(self.tabuleiro[indice_origem][-1], self.tabuleiro[indice_destino][-1]):
                        return False

        print('************\nPerdeu!\n************')
        return True


jogadas = 'Jogadas:\n' \
          '[1] Desvirar do Estoque\n' \
          '[2] Mover do Descarte para Sequência\n' \
          '[3] Mover da Pilha[origem] para Sequência\n' \
          '[4] Mover do Descarte para Pilha[destino]\n' \
          '[5] Mover da Pilha[origem] para Pilha[destino]\n' \
          '[0] Sair\n'
jogo = JogoPaciencia()
jogo.distribuir_cartas()
rodadas = 0

while True:
    jogo.exibir_tabuleiro(rodadas)
    print(jogadas)
    jogada = int(input('Escolha: '))
    if jogada == 1:
        jogo.retirar_estoque()
    elif jogada == 2:
        jogo.mover_descarte_sequencia()
    elif jogada == 3:
        indice_pilha_origem = int(input('Digite o indíce da Pilha origem: '))
        jogo.mover_pilha_sequencia(indice_pilha_origem)
    elif jogada == 4:
        indice_pilha = int(input('Digite o indíce da Pilha destino: '))
        jogo.mover_descarte_pilha_tabuleiro(indice_pilha)
    elif jogada == 5:
        indice_pilha_origem = int(input('Digite o indíce da Pilha origem: '))
        indice_pilha_destino = int(input('Digite o indíce da Pilha destino: '))
        jogo.mover_entre_pilhas_tabuleiro(indice_pilha_origem, indice_pilha_destino)
    elif jogada == 0:
        print(f'Terminando o jogo com {rodadas} rodadas.')
        break
    else:
        print('Opção inválida!')
    #     rodadas -= 1
    # rodadas += 1

    if jogo.terminou():
        break
