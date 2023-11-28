import random
from collections import deque


class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
        self.virada_pra_cima = False

    def __repr__(self):
        return f"{self.valor}{self.naipe}"


class JogoPaciencia:
    HEADER = '=+=' * 30 + '\n ' + '=+=' * 13 + f'[Rodada: %s]' + '=+=' * 12
    FOOTER = '=+=' * 30
    NAIPE = '♠'
    BACK = '⍰'
    RANKS = 'A2345'  # 'A23456789TJQK'
    N_PILHAS = 2

    def __init__(self):
        self.baralho = [Carta(self.NAIPE, valor) for valor in self.RANKS]
        random.shuffle(self.baralho)
        self.tabuleiro = [deque() for _ in range(self.N_PILHAS)]
        self.pilha_descarte = deque()
        self.pilha_estoque = deque(self.baralho)
        self.pilha_sequencia = deque()
        self._distribuir_cartas()

    def _checa_movimento_pilha(self, carta_origem, carta_destino):
        return self.RANKS.index(carta_origem.valor) + 1 == self.RANKS.index(carta_destino.valor)

    def _checa_movimento_sequencia(self, carta_origem, sequencia: deque):
        index_origem = self.RANKS.index(carta_origem.valor)
        if not sequencia:
            return index_origem == 0
        return index_origem == self.RANKS.index(sequencia[-1].valor) + 1

    def _distribuir_cartas(self):
        for i in range(self.N_PILHAS):
            for j in range(i + 1):
                carta = self.pilha_estoque.pop()
                if j == i:
                    carta.virada_para_cima = True
                self.tabuleiro[j].append(carta)

    def exibir_tabuleiro(self, rodada):
        print(self.HEADER % rodada)
        print(f'Estoque: {[self.BACK for _ in range(len(self.pilha_estoque))]}')
        print(f'Descarte: {[carta.__str__() for carta in self.pilha_descarte]}')
        print(f'Sequência montada: {[carta.__str__() for carta in self.pilha_sequencia]}')
        i = 0
        for pilha in self.tabuleiro:
            print(f'Pilha[{i}]: {[carta.__str__() for carta in pilha]}')
            i = i + 1
        print(self.FOOTER)

    # 1. Mover carta: Estoque -> Descarte
    def retirar_estoque(self):
        if self.pilha_estoque:
            carta = self.pilha_estoque.pop()
            self.pilha_descarte.append(carta)
            print(f'Desvirando {carta} do Estoque.')
            return True

        print(f'Estoque vazio!')

    # 2. Mover carta: Descarte -> Sequência
    def mover_descarte_sequencia(self):
        if not self.pilha_descarte:
            print(f'Descarte vazio!')
            return

        if not self.pilha_sequencia or self._checa_movimento_sequencia(self.pilha_descarte[-1], self.pilha_sequencia):
            carta = self.pilha_descarte.pop()
            self.pilha_sequencia.append(carta)
            print(f'Movendo {carta} de Descarte para Sequencia.')
            return True
        else:
            print(f'Movimento inválido! {self.pilha_descarte[-1]} não encaixa em {self.pilha_sequencia[-1]}.')

    # 3. Mover carta: Descarte -> Tabuleiro_Pilha[i]
    def mover_descarte_pilha_tabuleiro(self, destino):
        if not self.pilha_descarte:
            print(f'Descarte vazio!')
            return

        pilha_destino: deque = self.tabuleiro[destino]
        if not pilha_destino or self._checa_movimento_pilha(self.pilha_descarte[-1], pilha_destino[-1]):
            carta = self.pilha_descarte.pop()
            pilha_destino.append(carta)
            print(f'Movendo {carta} do Descarte para Pilha[{destino}].')
            return True
        else:
            print(f'Movimento inválido! {self.pilha_descarte[-1]} não encaixa em {pilha_destino[-1]}.')

    # 4. Mover carta: Tabuleiro_Pilha[i] -> Sequência
    def mover_pilha_sequencia(self, origem):
        pilha_origem: deque = self.tabuleiro[origem]

        if not pilha_origem:
            print(f'Pilha[{origem}] vazia!')
            return False

        if not self.pilha_sequencia or self._checa_movimento_sequencia(pilha_origem[-1], self.pilha_sequencia):
            carta = pilha_origem.pop()
            self.pilha_sequencia.append(carta)
            print(f'Movendo {carta} da Pilha[{origem}] para Sequência.')
            return True
        else:
            print(f'Movimento inválido! {pilha_origem[-1]} não encaixa em {self.pilha_sequencia[-1]}.')

    # 5. Mover carta: Tabuleiro_Pilha[i] -> Tabuleiro_Pilha[j]
    def mover_entre_pilhas_tabuleiro(self, origem, destino):
        pilha_origem: deque = self.tabuleiro[origem]
        pilha_destino: deque = self.tabuleiro[destino]

        if pilha_origem and (not pilha_destino or self._checa_movimento_pilha(pilha_origem[-1], pilha_destino[-1])):
            carta = pilha_origem.pop()
            pilha_destino.append(carta)
            print(f'Movendo {carta} da Pilha[{origem}] para Pilha[{destino}].')
            return True
        else:
            print(f'Movimento inválido! {pilha_origem[-1]} não encaixa em {pilha_destino[-1]}.')

    def terminou(self) -> (bool, str):
        # Fechou a sequência
        sequencia_atual = ''.join([carta.valor for carta in self.pilha_sequencia])
        if sequencia_atual == self.RANKS:
            return True, "Ganhou!"

        # Tem no estoque
        if self.pilha_estoque:
            return False

        # Movimento Descarte -> Sequência possível
        if self.pilha_descarte and (not self.pilha_sequencia or
                                    self._checa_movimento_sequencia(self.pilha_descarte[-1], self.pilha_sequencia)):
            return False

        # Movimento Descarte -> Pilha[i] possível
        if self.pilha_descarte:
            for pilha in self.tabuleiro:
                if not pilha or self._checa_movimento_pilha(self.pilha_descarte[-1], pilha[-1]):
                    return False

        # Movimento Pilha[i] -> Sequência possível
        for pilha in self.tabuleiro:
            if not pilha or self._checa_movimento_sequencia(pilha[-1], self.pilha_sequencia):
                return False

        # Movimento Pilha[i] -> Pilha[j] possível
        for indice_origem in range(self.N_PILHAS):
            if not self.tabuleiro[indice_origem]:
                return False

            for indice_destino in range(self.N_PILHAS):
                if not self.tabuleiro[indice_destino] \
                        or self._checa_movimento_pilha(self.tabuleiro[indice_origem][-1],
                                                       self.tabuleiro[indice_destino][-1]):
                    return False

        return True, 'Perdeu!'


class EstadoJogoPaciencia:
    def __init__(self, jogo: JogoPaciencia, movimento=None):
        self.jogo = jogo
        self.movimento = movimento
        self.terminou = jogo.terminou()


def busca_profundidade(estado_atual: EstadoJogoPaciencia, profundidade: 2, visitados):
    if termino := estado_atual.terminou():
        print(termino)


jogadas = 'Jogadas:\n' \
          '[1] Desvirar do Estoque\n' \
          '[2] Mover do Descarte para Sequência\n' \
          '[3] Mover do Descarte para Pilha[destino]\n' \
          '[4] Mover da Pilha[origem] para Sequência\n' \
          '[5] Mover da Pilha[origem] para Pilha[destino]\n' \
          '[0] Sair\n'

jogo = JogoPaciencia()
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
        indice_pilha = int(input('Digite o indíce da Pilha[destino]: '))
        jogo.mover_descarte_pilha_tabuleiro(indice_pilha)
    elif jogada == 4:
        indice_pilha_origem = int(input('Digite o indíce da Pilha[origem]: '))
        jogo.mover_pilha_sequencia(indice_pilha_origem)
    elif jogada == 5:
        indice_pilha_origem = int(input('Digite o indíce da Pilha origem: '))
        indice_pilha_destino = int(input('Digite o indíce da Pilha destino: '))
        jogo.mover_entre_pilhas_tabuleiro(indice_pilha_origem, indice_pilha_destino)
    elif jogada == 0:
        print(f'Terminando o jogo com {rodadas} rodadas.')
        break
    else:
        print('Opção inválida!')
        rodadas -= 1
    rodadas += 1

    if termino := jogo.terminou():
        print(termino[1])
        break
