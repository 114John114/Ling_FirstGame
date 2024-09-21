import pygame
import random
import os

os.chdir("E:\Tabletop\软件工程作业\Homework_2")

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH = 600 # 窗口大小
HEIGHT = 600 # 窗口大小
TILE_SIZE = 100 # 图案大小
ROWS = 10 # 行数和列数
COLS = 10 # 行数和列数
FPS = 30 # 帧率
START_LEVEL = 4 # 开始关卡
MESSAGE_DURATION = 3  # 消息显示时长（秒）

# 设置字体
font_path = 'SimHei.otf'  # 字体文件路径
font_size = 36
font = pygame.font.Font(font_path, font_size)  # 使用支持汉字的字体

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("羊了个羊小游戏") 

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 加载游戏背景图片
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# 初始化游戏状态
level = 1  # 当前关卡
board = None  # 游戏板
selected = []  # 选中的方块
board_num = 36
message_displayed = False
message_time = 0

def draw_text(text, font, color, surface, x, y):
    """绘制文本"""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


# 创建开始界面
def show_menu():
    """显示开始菜单"""
    menu_running = True
    while menu_running:
        screen.blit(background, (0, 0))  # 绘制背景图像
        draw_text("羊了个羊小游戏", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 3)
        draw_text("开始游戏", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2)
        draw_text("退出", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 + 100)
        pygame.display.flip() # 更新屏幕显示

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit() 
                exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if HEIGHT // 2 - 50 < y < HEIGHT // 2 + 50:
                    return "start"
                elif HEIGHT // 2 + 100 - 50 < y < HEIGHT // 2 + 100 + 50:
                    pygame.quit()
                    exit()

# 显示开始界面
show_menu()

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

def check_match():
    global board_num
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if r1 == r2 and c1 == c2:
            board[r1][c1] = None
            board_num -= 1
            selected.clear()
            return
        if board[r1][c1] == board[r2][c2]:
            board[r1][c1] = None
            board[r2][c2] = None
            board_num -= 2
        selected.clear()

# 定义关卡
def generate_board(level):
    global board_num
    board_num = 36
    """根据关卡生成不同难度的游戏板"""
    num_patterns = START_LEVEL + level  # 随着关卡增加，增加图案种类
    patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, num_patterns + 1)]
    patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]
    return [[random.choice(patterns) for _ in range(COLS)] for _ in range(ROWS)]

# 在每次关卡完成后更新游戏板
board = generate_board(level)


# 在屏幕上显示消息
def draw_message(message, duration):
    """在屏幕上显示消息"""
    text = font.render(message, True, (255, 255, 255))  # 创建文本对象
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 获取文本的矩形区域
    screen.blit(text, text_rect)  # 绘制文本
    pygame.display.flip()
    pygame.time.wait(duration * 1000)  # 等待指定的秒数

# 主游戏循环
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // TILE_SIZE, y // TILE_SIZE
            if board[row][col] is not None:
                selected.append((row, col))
            if len(selected) == 2:
                check_match()
            
    screen.blit(background, (0, 0))
    draw_board()
    pygame.display.flip()

    # 游戏逻辑示例：检查是否完成当前关卡
    if all(board_num == 0 for row in board):
        level += 1
        # 在第三关结束游戏
        if level == 4:
            draw_message("游戏结束!", MESSAGE_DURATION)
            running = False
        else:
            draw_message(f"恭喜你完成了第{level-1}关！", MESSAGE_DURATION)
            board = generate_board(level)
            selected = []
    

pygame.quit()