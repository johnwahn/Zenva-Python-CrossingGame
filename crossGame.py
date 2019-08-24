#Pygame development
#Setting up display

#importing the pygame module
import pygame

#Size of the screen
SCREEN_TITLE = 'Cross RPG'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
#Colors according to RGB codes
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)

#Getting our clock variable
clock = pygame.time.Clock()

#font
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:

    #Making our game run 60FPS
    TICK_RATE = 60

    def __init__(self,image_path, title, width, height):

        self.title = title
        self.width = width
        self.height = height

        #variable that represents our game screen
        self.game_screen = pygame.display.set_mode((width, height))

        #color of our game screen
        self.game_screen.fill(WHITE_COLOR)

        #Screen title for the display
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self):

        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('player.png', 375, 700, 50,50)
        enemy_0 = enemyPlayerCharacter('enemy.png',20, 400, 50, 50)
        treasure = GameObject('treasure.png',375, 50, 50, 50)

        #Our game loop in order display the game screen
        while not is_game_over:

            #events include move movement, mouse and key clicks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        direction = 5
                    elif event.key == pygame.K_DOWN:
                        direction = -5
                # detects when the key is released
                elif event.type == pygame.KEYUP:

                    # Stop movement if up and down key is not pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                        
                print(event)
            # Redraw the screen to be a blank white window in each interation
            self.game_screen.fill(WHITE_COLOR)
            #Draw the actual image of the background
            self.game_screen.blit(self.image,(0,0))

            #Drawing the treasure
            treasure.draw(self.game_screen)
            
            #Update player position
            player_character.move(direction, self.height)
            #Drawing player at new position
            player_character.draw(self.game_screen)

            #Update enemy position
            enemy_0.move (self.width)
            #Drawing enemy at new position
            enemy_0.draw(self.game_screen)

            if player_character.detect_collision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render('You lost!', True, BLACK_COLOR)
                self.game_screen.blit(text,(300,350))
                pygame.display.update()
                clock.tick(1)
                break

            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('You win!', True, BLACK_COLOR)
                self.game_screen.blit(text,(300,350))
                pygame.display.update()
                clock.tick(1)
                break
            
            #displays and updates all of the graphics
            pygame.display.update()
            #Updates everything within the game
            clock.tick(self.TICK_RATE)        

        if did_win:
            self.run_game_loop()
        else:
            return
#Our parent class 
class GameObject:
    def __init__(self, image_path, x, y, width, height):
        
        #Uploading the image we want to display
        object_image = pygame.image.load(image_path)
        #Changing the size of our image
        self.image = pygame.transform.scale(object_image, (width,height))

        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def draw(self, background):
        #Displays our image to the display 
        background.blit(self.image, (self.x_pos, self.y_pos))
        
# Class to represent the character controlled by the player       
class PlayerCharacter(GameObject):

    #the amount of tiles the player moves per second
    SPEED = 10
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path,x,y,width,height)

    #function will move up when direction > 0 and down when direction < 0
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        #Prevent character from going to the bottom of the screen
        if self.y_pos >= max_height -40:
            self.y_pos = max_height -40

    #Returns true if there is a collision
    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos+self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos+self.width < other_body.x_pos:
            return False
        
        return True

class enemyPlayerCharacter(GameObject):

    #the amount of tiles the player moves per second
    SPEED = 10
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path,x,y,width,height)

    #function will move up when direction > 0 and down when direction < 0
    def move(self, max_width):

        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        
        elif self.x_pos >= max_width -40:
            self.SPEED = -abs(self.SPEED)
        
        self.x_pos += self.SPEED

#need to initialize pygame before running
pygame.init()

new_game = Game('background.png',SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop()



    
# Quits pygame and the program
pygame.quit()
quit()
