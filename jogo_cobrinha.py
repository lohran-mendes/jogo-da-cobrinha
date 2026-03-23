import pygame
import random
import sys
import os

LARGURA = 600
ALTURA = 600
TAMANHO_BLOCO = 40
COLUNAS = LARGURA // TAMANHO_BLOCO
LINHAS = ALTURA // TAMANHO_BLOCO
FPS_JOGO = 7

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERMELHO = (255, 0, 0)
CINZA = (160, 160, 160)

CIMA = (0, -1)
BAIXO = (0, 1)
ESQUERDA = (-1, 0)
DIREITA = (1, 0)

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGENS_DIR = os.path.join(ASSETS_DIR, "imagens")


def carregar_imagem(nome, fallback_cor=None, tamanho=None):
    caminho = os.path.join(IMAGENS_DIR, nome)
    try:
        img = pygame.image.load(caminho).convert()
        if tamanho:
            img = pygame.transform.scale(img, tamanho)
        return img
    except (pygame.error, FileNotFoundError):
        tam = tamanho or (TAMANHO_BLOCO, TAMANHO_BLOCO)
        surf = pygame.Surface(tam)
        if fallback_cor:
            surf.fill(fallback_cor)
        return surf


def desenhar_texto(tela, texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont("consolas", tamanho)
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect(center=(x, y))
    tela.blit(superficie, rect)


class Cobra:
    def __init__(self):
        self.resetar()

    def resetar(self):
        centro_x = COLUNAS // 2
        centro_y = LINHAS // 2
        self.corpo = [
            (centro_x, centro_y),
            (centro_x - 1, centro_y),
            (centro_x - 2, centro_y),
        ]
        self.direcao = DIREITA
        self.crescer = False

    def definir_direcao(self, nova_direcao):
        oposta = (-self.direcao[0], -self.direcao[1])
        if nova_direcao != oposta:
            self.direcao = nova_direcao

    def mover(self):
        cabeca_x, cabeca_y = self.corpo[0]
        dx, dy = self.direcao
        nova_cabeca = (cabeca_x + dx, cabeca_y + dy)
        self.corpo.insert(0, nova_cabeca)
        if not self.crescer:
            self.corpo.pop()
        self.crescer = False

    def colidiu_parede(self):
        x, y = self.corpo[0]
        return x < 0 or x >= COLUNAS or y < 0 or y >= LINHAS

    def colidiu_corpo(self):
        return self.corpo[0] in self.corpo[1:]

    def desenhar(self, tela, img_cabeca, img_corpo):
        for segmento in self.corpo[1:]:
            x = segmento[0] * TAMANHO_BLOCO
            y = segmento[1] * TAMANHO_BLOCO
            tela.blit(img_corpo, (x, y))
        cabeca = self.corpo[0]
        x = cabeca[0] * TAMANHO_BLOCO
        y = cabeca[1] * TAMANHO_BLOCO
        tela.blit(img_cabeca, (x, y))


class Comida:
    def __init__(self):
        self.posicao = (0, 0)

    def reposicionar(self, corpo_cobra):
        while True:
            pos = (random.randint(0, COLUNAS - 1), random.randint(0, LINHAS - 1))
            if pos not in corpo_cobra:
                self.posicao = pos
                return

    def desenhar(self, tela, img_maca):
        x = self.posicao[0] * TAMANHO_BLOCO
        y = self.posicao[1] * TAMANHO_BLOCO
        tela.blit(img_maca, (x, y))


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Jogo da Cobrinha")
        self.relogio = pygame.time.Clock()

        self.img_fundo = carregar_imagem("fundo.png", PRETO, (LARGURA, ALTURA))
        self.img_maca = carregar_imagem("maca.png", VERMELHO)
        self.img_corpo = carregar_imagem("corpo.png", VERDE)
        self.img_cabeca = carregar_imagem("cabeca.png", (0, 255, 0))

        self.cobra = Cobra()
        self.comida = Comida()
        self.pontuacao = 0
        self.recorde = 0
        self.estado = "menu"

    def executar(self):
        while True:
            if self.estado == "menu":
                self.tela_menu()
            elif self.estado == "jogando":
                self.tela_jogo()
            elif self.estado == "game_over":
                self.tela_game_over()

    def tela_menu(self):
        while self.estado == "menu":
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        self.iniciar_jogo()
                        return
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.tela.fill(PRETO)

            desenhar_texto(self.tela, "JOGO DA COBRINHA", 40, BRANCO, LARGURA // 2, 80)

            desenhar_texto(self.tela, "CONTROLES", 24, BRANCO, LARGURA // 2, 180)
            desenhar_texto(self.tela, "Setas / WASD - Mover", 20, CINZA, LARGURA // 2, 220)
            desenhar_texto(self.tela, "ENTER - Iniciar / Reiniciar", 20, CINZA, LARGURA // 2, 255)
            desenhar_texto(self.tela, "ESPACO - Pausar / Continuar", 20, CINZA, LARGURA // 2, 290)
            desenhar_texto(self.tela, "ESC - Sair", 20, CINZA, LARGURA // 2, 325)

            if self.recorde > 0:
                desenhar_texto(self.tela, f"Recorde: {self.recorde}", 22, BRANCO, LARGURA // 2, 400)

            if pygame.time.get_ticks() % 1000 < 600:
                desenhar_texto(self.tela, "Pressione ENTER para jogar", 24, BRANCO, LARGURA // 2, 500)

            pygame.display.flip()
            self.relogio.tick(30)

    def iniciar_jogo(self):
        self.cobra.resetar()
        self.comida.reposicionar(self.cobra.corpo)
        self.pontuacao = 0
        self.estado = "jogando"

    def tela_jogo(self):
        pausado = False

        while self.estado == "jogando":
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = "menu"
                        return
                    if evento.key == pygame.K_SPACE:
                        pausado = not pausado
                        continue

                    if not pausado:
                        if evento.key in (pygame.K_UP, pygame.K_w):
                            self.cobra.definir_direcao(CIMA)
                        elif evento.key in (pygame.K_DOWN, pygame.K_s):
                            self.cobra.definir_direcao(BAIXO)
                        elif evento.key in (pygame.K_LEFT, pygame.K_a):
                            self.cobra.definir_direcao(ESQUERDA)
                        elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                            self.cobra.definir_direcao(DIREITA)

            if not pausado:
                self.cobra.mover()

                if self.cobra.colidiu_parede() or self.cobra.colidiu_corpo():
                    if self.pontuacao > self.recorde:
                        self.recorde = self.pontuacao
                    self.estado = "game_over"
                    return

                if self.cobra.corpo[0] == self.comida.posicao:
                    self.cobra.crescer = True
                    self.pontuacao += 10
                    self.comida.reposicionar(self.cobra.corpo)

            self.tela.blit(self.img_fundo, (0, 0))
            self.comida.desenhar(self.tela, self.img_maca)
            self.cobra.desenhar(self.tela, self.img_cabeca, self.img_corpo)

            desenhar_texto(self.tela, f"Pontos: {self.pontuacao}", 20, BRANCO, 70, 15)
            desenhar_texto(self.tela, f"Recorde: {self.recorde}", 20, BRANCO, LARGURA - 80, 15)

            if pausado:
                desenhar_texto(self.tela, "PAUSADO", 40, BRANCO, LARGURA // 2, ALTURA // 2)

            pygame.display.flip()
            self.relogio.tick(FPS_JOGO)

    def tela_game_over(self):
        while self.estado == "game_over":
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        self.iniciar_jogo()
                        return
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = "menu"
                        return

            self.tela.fill(PRETO)

            desenhar_texto(self.tela, "GAME OVER", 48, VERMELHO, LARGURA // 2, 200)
            desenhar_texto(self.tela, f"Pontuacao: {self.pontuacao}", 28, BRANCO, LARGURA // 2, 280)
            desenhar_texto(self.tela, f"Recorde: {self.recorde}", 24, BRANCO, LARGURA // 2, 320)

            if pygame.time.get_ticks() % 1000 < 600:
                desenhar_texto(self.tela, "ENTER - Jogar novamente", 22, BRANCO, LARGURA // 2, 420)
            desenhar_texto(self.tela, "ESC - Voltar ao menu", 20, CINZA, LARGURA // 2, 460)

            pygame.display.flip()
            self.relogio.tick(30)


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
