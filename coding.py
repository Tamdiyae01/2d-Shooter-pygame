import pygame
from random import randint

pygame.init()

win = pygame.display.set_mode((800, 480))


pygame.display.set_caption('2d Shooter Game')

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')

pygame.mixer.music.set_volume(0.4)
music = pygame.mixer.music.load('gradius.mp3')
pygame.mixer.music.play(-1)

kills = 0
amountOfBullets = 0


# Player character
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x  # attributes of the class
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.health = 10
        self.visible = True
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.xMax = 800
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)  # x y width height

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[round(self.walkCount // 3)], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[round(self.walkCount // 3)], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # displays characters dimensions

        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('monserrat', 75)
        text = font1.render('You have been hit!', 1, (255, 255, 100))
        win.blit(text, (400 - round(text.get_width() / 2), 80))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

        if self.health > 0:
            self.health -= 5
            print("Health :", self.health)
        elif self.health <= 0:
            pygame.quit()
            print("Player lost!")
        print('Player hit!')


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.velocity = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.velocity > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            pygame.draw.rect(win, (255,0,0),self.hitbox, 2) # displays characters dimensions

    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walkCount = 0
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            print("player lost")
        print('hit enemy!')


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Kills: ' + str(kills), 1, (0, 0, 0))
    bulletText = font.render('Ammo: ' + str(amountOfBullets), 1, (0, 0, 0))
    pygame.draw.rect(win, (0,0,0), (647, 10, 45, 25), 2)

    pauseText = font.render('esc - Pause', 1, (0, 0, 0))


    win.blit(text, (10, 10))
    win.blit(bulletText, (10, 35))
    win.blit(pauseText, (650, 12.5))


    man.draw(win)
    goblin.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


# mainloop
font = pygame.font.SysFont('monserrat', 30, True)
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
bullets = []
shootLoop = 0
run = True
pause = False

while run:
    clock.tick(30)  # FPS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                font1 = pygame.font.SysFont('monserrat', 100)
                text = font1.render('PAUSED!', 1, (255, 0, 0))
                win.blit(text, (400 - (text.get_width() / 2), 200))
                pygame.display.update()
                pause = not pause
    if pause == True:
        continue

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[
                2]:  # man hit by enemy
                man.hit()

    if goblin.health == 0:
        CheckIfSpawnPointIsValid = True
        # checking if spawn point is too close to player
        while CheckIfSpawnPointIsValid:

            spawnPointX = randint(0, 700)
            if man.x - 70 > spawnPointX or man.x + 70 < spawnPointX:
                print(man.x)
                print(spawnPointX)
                CheckIfSpawnPointIsValid = False
                goblin = enemy(spawnPointX, 410, 64, 64, 700)
                kills += 1
                goblin.health = 10

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
        amountOfBullets += 1
        print(amountOfBullets)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                    goblin.hitbox[2]:
                goblin.hit()

                if goblin.visible:
                    hitSound.play()

                bullets.pop(bullets.index(bullet))

        if 800 > bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.remove(bullet)  # remove element

    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:  # lenght of bullets
            bullets.append(
                projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.velocity
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < man.xMax - man.width:
        man.x += man.velocity
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindow()

pygame.quit()
