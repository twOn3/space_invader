import pygame
import random
from time import sleep

# 화면 크기
WIDTH = 400
HEIGHT = 700

# 색깔
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

backgroundImage = pygame.image.load("images/galaxy2.jpeg")
backgroundImage = pygame.transform.scale(backgroundImage, (WIDTH, HEIGHT))
spaceshipImage = pygame.image.load("images/ship.png")
bulletImage = pygame.image.load("images/bullet.png")
bombImage = pygame.image.load("images/bomb.png")
enemyImage = pygame.image.load("images/enemy.png")
fireImage = pygame.image.load("images/fire.png")
gameOverImage = pygame.image.load("images/gameover.jpg")
gameOverImage = pygame.transform.scale(gameOverImage, (WIDTH, HEIGHT))


gameOver = False
score = 0
stage = 1

spaceshipStartPosition = {
    "x": WIDTH // 2 - 32,
    "y": HEIGHT - 64,
}

spaceshipX = spaceshipStartPosition["x"]
spaceshipY = spaceshipStartPosition["y"]

bulletList = []
bombList = []
enemyList = []

class Bullet:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.type = t

    def update(self):
        self.y -= 7

        if self.type == 2:
            self.x -= 0.5
        elif self.type == 3:
            self.x += 0.5
        elif self.type == 4:
            self.x -= 1
        elif self.type == 5:
            self.x += 1

        if self.y <= 0:
            self.destroy()

    def checkCollision(self, enemy):
        return self.y <= enemy.y and self.x >= enemy.x and self.x <= enemy.x + 64

    def destroy(self):
        if self in bulletList:
            bulletList.remove(self)


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.m = 0

    def update(self):
        self.y -= 1
        self.m += 1

        if self.m >= 50:
            createBullet(self.x, self.y - 5, 1)
            createBullet(self.x - 20, self.y, 2)
            createBullet(self.x + 20, self.y, 3)
            createBullet(self.x - 40, self.y + 5, 4)
            createBullet(self.x + 40, self.y + 5, 5)
            self.destroy()

    def destroy(self):
        if self in bombList:
            bombList.remove(self)

class Enemy:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.isHit = False
        self.hitCount = 0
        self.hitTimer = 0

    def init(self):
        self.y = 0
        self.x = random.randint(0, WIDTH - 48)

    def update(self):
        if self.isHit:
            self.y += 1
            self.hitTimer -= self.hitCount
            if self.hitTimer <= 0:
                self.destroy()
        else:
            self.y += stage

        if self.y >= HEIGHT - 64:
            global gameOver
            gameOver = True
            print("gameover!")

    def destroy(self):
        if self in enemyList:
            enemyList.remove(self)

    def hit(self):
        if not self.isHit:
            self.hitTimer = 60
        self.isHit = True
        self.hitCount += 1

def randomInt(min, max):
    return random.randint(min, max)

def createBullet(x, y, t=1):
    bullet = Bullet(x + 25, y - 15, t)
    bulletList.append(bullet)

def createBomb():
    bomb = Bomb(spaceshipX + 15, spaceshipY - 20)
    bombList.append(bomb)

def createEnemy():
    enemy = Enemy()
    enemy.init()
    enemyList.append(enemy)

def update():
    global spaceshipX, spaceshipY, score, stage, gameOver

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Check the arrow keys and move the spaceship accordingly
    if keys[pygame.K_LEFT]:
        spaceshipX -= 5
    if keys[pygame.K_RIGHT]:
        spaceshipX += 5

    # Handle other events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                createBullet(spaceshipX, spaceshipY)
            elif event.key == pygame.K_b:
                createBomb()
        elif event.type == pygame.USEREVENT:  # Enemy 생성 타이머 이벤트
            createEnemy()

    spaceshipX = max(0, min(spaceshipX, WIDTH - 64))

    for bullet in bulletList:
        bullet.update()

        for enemy in enemyList:
            if bullet.checkCollision(enemy):
                enemy.hit()
                bullet.destroy()
                score += stage

                if score >= stage * stage * 10:
                    stage += 1
                    print(f"level up, score={score}, stage={stage}")

    for bomb in bombList:
        bomb.update()

    for enemy in enemyList:
        enemy.update()

def render():
    screen.blit(backgroundImage, (0, 0))
    screen.blit(spaceshipImage, (spaceshipX, spaceshipY))
    font = pygame.font.Font(None, 20)
    scoreText = font.render(f"Score: {score}", True, WHITE)
    stageText = font.render(f"Stage: {stage}", True, WHITE)
    screen.blit(scoreText, (20, 20))
    screen.blit(stageText, (300, 20))

    for bullet in bulletList:
        screen.blit(bulletImage, (bullet.x, bullet.y))

    for bomb in bombList:
        screen.blit(bombImage, (bomb.x, bomb.y))

    for enemy in enemyList:
        screen.blit(enemyImage, (enemy.x, enemy.y))

        if enemy.isHit:
            screen.blit(fireImage, (enemy.x, enemy.y))
            if enemy.hitCount >= 2:
                screen.blit(fireImage, (enemy.x + 15, enemy.y + 5))
            if enemy.hitCount >= 3:
                screen.blit(fireImage, (enemy.x + 7, enemy.y - 8))

    pygame.display.flip()

def main():
    global gameOver

    pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1초마다 Enemy 생성 타이머 이벤트 발생

    while not gameOver:
        update()
        render()
        clock.tick(60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
def main():
    global gameOver

    pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1초마다 Enemy 생성 타이머 이벤트 발생

    while not gameOver:
        update()
        render()
        clock.tick(60)

    screen.blit(gameOverImage, (10, 100))
    pygame.display.flip()

main()
sleep(5)
pygame.quit()
