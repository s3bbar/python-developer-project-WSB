import pygame
from pygame.locals import QUIT
import sys
import time
import random


class Game:

    def __init__(self):
        self.time_img = None
        self.running = False
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.input_text = ""
        self.word = ""
        self.time_start = 0
        self.total_time = 0
        self.accuracy = "0%"
        self.results = "Czas:0 Dokładność:0% słowa/min:0 "
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)

        pygame.init()
        self.open_img = pygame.image.load("type-speed-open.png")
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load("background.jpg")
        self.bg = pygame.transform.scale(self.bg, (500, 750))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Test szybkości pisania")

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=(self.w / 2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    @staticmethod
    def get_sentence():
        with open("sentences.txt") as file:
            sentences = file.read().split("\n")
            sentence = random.choice(sentences)
            return sentence

    def show_results(self, screen):
        # Obliczanie czasu trwania
        if not self.end:
            self.total_time = time.time() - self.time_start
            # Obliczanie dokładności
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except IndexError:
                    pass
            self.accuracy = count / len(self.word) * 100
            # Obliczanie słów na minutę
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True
            print(self.total_time)
            self.results = "Czas: " + str(round(self.total_time)) + \
                           " sekund   Dokładność: " + str(round(self.accuracy)) + "%" + \
                           "   słowa/minuta: " + str(round(self.wpm))

            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))
            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 140))
            self.draw_text(screen, "Reset", self.h - 70, 26, (100, 100, 100))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()
        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if 50 <= x <= 650 and 250 <= y <= 300:
                        self.active = True
                        self.input_text = ""
                        self.time_start = time.time()
                        # position of reset box
                    if 310 <= x <= 510 and y >= 390 and self.end:
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()

        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))

        pygame.display.update()
        time.sleep(1)
        self.active = False
        self.reset = False
        self.end = False

        self.input_text = "Kliknij aby rozpocząć test"
        self.word = ""
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        self.word = self.get_sentence()
        if not self.word:
            self.reset_game()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Test szybkości pisania"
        self.draw_text(self.screen, msg, 60, 60, self.HEAD_C)
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)

        pygame.display.update()

# Pętla główna programu
if __name__ == "__main__":
    Game().run()
