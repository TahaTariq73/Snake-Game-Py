import pygame
import random
import os

pygame.init()
pygame.mixer.init()

class SnakeGame:

    def __init__(self):
        self.font = pygame.font.SysFont("comicsansms", 20)
        self.clock = pygame.time.Clock()
        self.fps = 30

        # Colors
        self.white = (255, 255, 255)
        self.green = (112, 247, 5)

        self.exit_game = False
        self.game_over = False

    def gameWindow(self):
         """ Creating game window with title """
         self.window = pygame.display.set_mode((740, 460))
         pygame.display.set_caption("Snake Game") # Setting Caption
         icon = pygame.image.load("Images/icon.ico")
         pygame.display.set_icon(icon) # Setting game icon
         pygame.display.update()

    def game_score(self, txt, color, x, y):
        """ Rendering text when needed """
        text = self.font.render(txt, True, color)
        self.window.blit(text, [x, y])

    def plotting_snakePieces(self, window, color, snake_list, size, snake_borders):
        """ Plotting snake pieces """
        for index, i in enumerate(snake_list):
            pygame.draw.rect(window, color, [i[0], i[1], size, size], 0, *snake_borders)

    def place_img(self, path):
        """ Placing image when needed """
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (740, 460)).convert_alpha()

    def play_music(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def welcome_window(self):
        """ Welcoming the user """
        self.gameWindow()

        self.exit_game = False
        self.game_over = False

        while not self.exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.gameLoop()

            self.window.fill(self.white)
            self.window.blit(self.place_img("Images/home_screen.jpg"), (0, 0))
            pygame.display.update()

    def gameLoop(self):
        """ Running the gameloop for change changing frames """
        self.play_music("Music/background_music.mp3")

        # Snake position
        x_axis = 40
        y_axis = 60

        # Snake speed
        x_velocity = 0
        y_velocity = 0

        # Food position
        food = pygame.image.load("Images/food.png")
        x_food = random.randint(0, 500)
        y_food = random.randint(0, 310)

        score = 0  # Game score
        snake_list = []
        snake_lenght = 1
        snake_borders = [6 for i in range(4)]

        size = 20  # Snake size

        if not os.path.exists("highscore.txt"):
            with open("highscore.txt", "w") as f:
                f.write("0")
        with open("highscore.txt", "r") as f:
            highscore = f.read()

        while not self.exit_game:

            if self.game_over == True:

                with open("highscore.txt", "w") as f:
                    f.write(str(highscore))
                self.game_score(f"Game over! Press enter to restart.", self.green, 200, 200)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.welcome_window()

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit_game = True

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_RIGHT:
                            x_velocity = 10
                            y_velocity = 0

                        elif event.key == pygame.K_LEFT:
                            x_velocity = -10
                            y_velocity = 0

                        elif event.key == pygame.K_UP:
                            y_velocity = -10
                            x_velocity = 0

                        elif event.key == pygame.K_DOWN:
                            y_velocity = 10
                            x_velocity = 0

                x_axis += x_velocity
                y_axis += y_velocity

                if abs(x_axis - x_food) < 20 and abs(y_axis - y_food) < 20:
                    score += 1
                    x_food = random.randint(0, 500)
                    y_food = random.randint(0, 310)
                    snake_lenght += 1
                    if score > int(highscore):
                        highscore = score

                self.window.fill(self.white)
                self.window.blit(self.place_img("Images/playing_screen.jpg"), (0, 0))
                self.game_score(f"Score : {score}", self.green, 12, 12)
                self.game_score(f"Highscore : {highscore}", self.green, 590, 12)

                food = pygame.transform.scale(food, (30, 30)).convert_alpha()
                self.window.blit(food, (x_food, y_food))

                head = []
                head.append(x_axis)
                head.append(y_axis)
                snake_list.append(head)

                if len(snake_list) > snake_lenght:
                    del snake_list[0]

                if head in snake_list[:-1]:
                    self.play_music("Music/game_over.mp3")
                    self.game_over = True

                if x_axis < 0 or x_axis > 740 or y_axis < 0 or y_axis > 460:
                    self.play_music("Music/game_over.mp3")
                    self.game_over = True

                self.plotting_snakePieces(self.window, self.green, snake_list, size, snake_borders)
            pygame.display.update()
            self.clock.tick(self.fps)

if __name__ == '__main__':
    game = SnakeGame()
    game.welcome_window()