import pygame

pygame.init()

tamanho_tela = (900, 900)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")

tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)
tamanho_jogador = 100
jogador = pygame.Rect(350, 750, tamanho_jogador, 15)

qtde_blocos_linha = 8
qtde_linhas_blocos = 5
qtde_total_blocos = qtde_blocos_linha * qtde_linhas_blocos

def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / 8 - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10

    blocos = []
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos

cores = {
    "branca": (255, 255, 255),
    "preta": (0, 0, 0),
    "amarela": (255, 255, 0),
    "azul": (0,191,255),
    "verde": (0,250,154),
    "rosa": (255,105,180)
}

fim_jogo = False
pontuacao = 0
movimento_bola = [8, -8]

def desenhar_inicio_jogo():
    tela.fill(cores["preta"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["rosa"], bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)

def movimentar_jogador(teclas_pressionadas):
    if teclas_pressionadas[pygame.K_RIGHT] and jogador.x + tamanho_jogador < tamanho_tela[0]:
        jogador.x += 5
    if teclas_pressionadas[pygame.K_LEFT] and jogador.x > 0:
        jogador.x -= 5

def movimentar_bola(bola):
    bola.x += movimento_bola[0]
    bola.y += movimento_bola[1]

    if bola.x <= 0 or bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento_bola[0] = -movimento_bola[0]
    if bola.y <= 0:
        movimento_bola[1] = -movimento_bola[1]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        return False

    if jogador.colliderect(bola):
        movimento_bola[1] = -movimento_bola[1]

    for bloco in blocos:
        if bloco.colliderect(bola):
            blocos.remove(bloco)
            movimento_bola[1] = -movimento_bola[1]
            break
    return True

def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", 1, cores["amarela"])
    tela.blit(texto, (0, 780))
    if pontuacao >= qtde_total_blocos:
        return True
    else:
        return False

blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)

while not fim_jogo:
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    fim_jogo = atualizar_pontuacao(qtde_total_blocos - len(blocos))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo = True

    teclas_pressionadas = pygame.key.get_pressed()
    movimentar_jogador(teclas_pressionadas)

    if not movimentar_bola(bola):
        fim_jogo = True

    pygame.time.wait(20)
    pygame.display.flip()

pygame.quit()