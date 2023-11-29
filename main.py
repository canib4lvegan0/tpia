from paciencia import *


class EstadoPaciencia:
    def __init__(self, tabuleiro):
        self.tabuleiro = tabuleiro  # Estrutura de dados para representar o estado do jogo
        self.movimentos = []  # Lista para armazenar os movimentos realizados até agora


def gerar_movimentos_possiveis(estado: JogoPaciencia):
    _, _, movimentos_possiveis, _ = estado.terminou()
    # Função para gerar todos os movimentos possíveis a partir de um estado do jogo
    return movimentos_possiveis


def realizar_movimento(estado, movimento):
    try:
        return movimento()
    except:
        print('Movimento inválido!')
    return False


def resolver_paciencia(estado_atual, max_profundidade, visitados):
    terminou, _, _, estado_atual = estado_atual.terminou()
    if terminou:
        return estado_atual  # Solução encontrada

    if max_profundidade <= 0:
        return None  # Limite de profundidade atingido

    movimentos_possiveis = gerar_movimentos_possiveis(estado_atual)
    print(f'Movimentos possíves -> {[movimento.__name__ for movimento in movimentos_possiveis]}')
    estado_atual.exibir_tabuleiro()
    for possivel_movimento in movimentos_possiveis:
        print(f'Possivel movimento -> {possivel_movimento.__name__}')
        movimento_realizado = realizar_movimento(estado_atual, possivel_movimento)
        estado_atual.exibir_tabuleiro()
        if movimento_realizado and estado_atual not in visitados:
            visitados.add(estado_atual)
            resultado = resolver_paciencia(estado_atual, max_profundidade - 1, visitados)
            if resultado is not None:
                return resultado  # Solução encontrada
            break

    return None  # Nenhuma solução encontrada até a profundidade máxima


if __name__ == "__main__":
    coletor_jogadas = []
    # Defina a profundidade máxima para a busca
    profundidade_maxima = 1000

    for _ in range(10):
        # Exemplo de uso:
        # Inicialize o jogo com um estado inicial
        estado_inicial = JogoPaciencia()
        estado_inicial.exibir_tabuleiro()

        # Conjunto para rastrear estados visitados
        estados_visitados = set()

        # Resolva o jogo de paciência usando busca em profundidade
        solucao = resolver_paciencia(estado_inicial, profundidade_maxima, estados_visitados)

        if solucao is not None:
            print("Solução encontrada!")
            coletor_jogadas.append(solucao)
            # Exibir ou aplicar os movimentos da solução no jogo
        else:
            print("Não foi encontrada uma solução.")

    print(f'Foram encontradas {len(coletor_jogadas)} soluções!')
