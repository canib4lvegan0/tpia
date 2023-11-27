import random
from collections import deque

NAIPES = '♠♥♦♣'
RANKS = 'A23456789TJQK'

class Carta:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor

    def __repr__(self):
        return f"{self.valor}{self.naipe}"


def movimento_possivel_descarte(origem, topo_destino):
    index_origem = RANKS.index(origem.valor)
    index_destino = RANKS.index(topo_destino.valor)

    return index_origem + 1 == index_destino

def movimento_possivel_coluna(origem, topo_destino):
    index_origem = RANKS.index(origem.valor)
    index_destino = RANKS.index(topo_destino.valor)

    return index_origem < index_destino


class JogoSoiterie:
    def __init__(self):
        self.baralho = [Carta(naipe, valor) for naipe in NAIPES for valor in RANKS]
        random.shuffle(self.baralho)
        self.tabuleiro = [deque() for _ in range(7)]
        self.pilha_descarte = deque()
        self.pilha_estoque = deque(self.baralho)

    def distribuir_cartas(self):
        for i in range(7):
            for j in range(i + 1):
                carta = self.pilha_estoque.pop()
                if j == i:
                    carta.virada_para_cima = True
                self.tabuleiro[j].append(carta)

    def exibir_tabuleiro(self):
        print('_._' * 20)
        print(f'Monte: {self.pilha_estoque.__str__()}')
        print(f'Slot: [{self.pilha_descarte}]')
        i = 0
        for pilha in self.tabuleiro:
            print(f'Coluna {i} -> ' + ' '.join(str(carta) for carta in pilha))
            i = i + 1
        print('*' * 10)

    # Aqui você pode adicionar métodos para as regras do jogo, movimentos de cartas, etc.

    def mover_estoque_para_descarte(self):
        if self.pilha_estoque:
            # TODO: add regra pra adicionar carta no descarte -- ex: K > Q > ... > A
            if movimento_possivel_descarte(self.pilha_estoque[-1], self.pilha_descarte):
                carta = self.pilha_estoque.pop()
                self.pilha_descarte.append(carta)
                print(f'Movendo {carta} para {self.pilha_estoque}')
            else:
                print(f'Movimento inválido! {self.pilha_estoque[-1]} > {self.pilha_descarte[-1]}')

    def mover_estoque_para_tabuleiro(self, posicao):
        if self.pilha_estoque:
            pilha_destino: deque = self.tabuleiro[posicao]
            if movimento_possivel_coluna(self.pilha_estoque[-1], pilha_destino[-1]):
                carta = self.pilha_estoque.pop()
                pilha_destino.append(carta)
            else:
                print(f'Movimento inválido! {self.pilha_estoque[-1]} > {pilha_destino[-1]}')

    # def virar_carta_descarte(self):
    #     if self.pilha_estoque:
    #         carta = self.pilha_estoque.pop()
    #         carta.virada_para_cima = True
    #         self.pilha_descarte.append(carta)
    #
    # def mover_descarte_para_tabuleiro(self, posicao):
    #     if self.pilha_descarte:
    #         carta_descarte = self.pilha_descarte[-1]
    #         pilha_destino = self.tabuleiro[posicao]
    #         if not pilha_destino or (carta_descarte.valor == 'K' and not pilha_destino[-1]):
    #             carta = self.pilha_descarte.pop()
    #             pilha_destino.append(carta)
    #         else:
    #             print("Movimento inválido")
    #
    # def mover_entre_pilhas_tabuleiro(self, origem, destino):
    #     pilha_origem = self.tabuleiro[origem]
    #     pilha_destino = self.tabuleiro[destino]
    #
    #     if pilha_origem and (not pilha_destino or (pilha_destino[-1].valor == RANKS[RANKS.index(pilha_origem[-1].valor) - 1])):
    #         carta = pilha_origem.pop()
    #         pilha_destino.append(carta)
    #     else:
    #         print("Movimento inválido")


# Exemplo de uso:
jogo = JogoSoiterie()
jogo.distribuir_cartas()
jogo.exibir_tabuleiro()

# Realizando alguns movimentos de exemplo
# jogo.mover_estoque_para_descarte()
# jogo.virar_carta_descarte()
# jogo.mover_descarte_para_tabuleiro(3)
# jogo.mover_entre_pilhas_tabuleiro(2, 1)
# jogo.exibir_tabuleiro()

print()
print('Hora de jogar!')
print()
enter = -1

jogadas = 'Jogadas:\n' \
          '1 - Mover do estoque para descarte\n' \
          '2 - Mover do estoque para Coluna N\n' \
          '3 - Mover Coluna N para descarte.\n'

while enter >= -1:
    print(jogadas)
    enter = int(input('Escolha: '))
    if enter == 1:
      jogo.mover_estoque_para_descarte()
    elif enter == 2:
        jogo.mover_estoque_para_tabuleiro(int(input('Digite a posicao da coluna: ')))
    elif enter == 3:
        pass
    else:
        print('Opção inválida!')

    jogo.exibir_tabuleiro()
