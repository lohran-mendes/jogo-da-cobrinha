import pygame
import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
IMAGENS_DIR = os.path.join(ASSETS_DIR, "imagens")

os.makedirs(IMAGENS_DIR, exist_ok=True)


def gerar_imagens():
    pygame.init()

    surf = pygame.Surface((600, 600))
    surf.fill((0, 0, 0))
    pygame.image.save(surf, os.path.join(IMAGENS_DIR, "fundo.png"))

    surf = pygame.Surface((40, 40))
    surf.fill((255, 0, 0))
    pygame.image.save(surf, os.path.join(IMAGENS_DIR, "maca.png"))

    surf = pygame.Surface((40, 40))
    surf.fill((0, 200, 0))
    pygame.image.save(surf, os.path.join(IMAGENS_DIR, "corpo.png"))

    surf = pygame.Surface((40, 40))
    surf.fill((0, 255, 0))
    pygame.image.save(surf, os.path.join(IMAGENS_DIR, "cabeca.png"))

    pygame.quit()


if __name__ == "__main__":
    print("Gerando imagens...")
    gerar_imagens()
    print("Assets gerados com sucesso em:", ASSETS_DIR)
