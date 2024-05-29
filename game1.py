import pygame
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình
screen = pygame.display.set_mode((432, 768))
pygame.display.set_caption("Pygame Flappy Bird")

# Tải hình nền
bg = pygame.image.load(r"assets/bg.png")
bg = pygame.transform.scale(bg, (432, 768))

# Tải logo game
logo = pygame.image.load(r"assets/logo.png")
logo = pygame.transform.scale(logo, (250, 100))

# Tải hình ảnh sàn
floor = pygame.image.load(r"assets/floor.png")
floor = pygame.transform.scale(floor, (432, 80))

# Tải hình ảnh chim
bird = pygame.image.load(r"assets/chim1.png").convert_alpha()
bird = pygame.transform.scale(bird, (70, 70))
bird_rect = bird.get_rect(center=(100, 384))

# Tạo ống
pipe_surface = pygame.image.load('assets/ong.png')
pipe_list = []

# Tạo thời gian ống để tạo ống mới
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1000)

# Tạo chiều cao cho ống
pipe_height = [400, 500, 600]

# Định nghĩa màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Thiết lập font chữ
font = pygame.font.Font(r'font/04B_19.TTF', 40)

# Hàm tạo nút
def draw_button(text, x, y, width, height, color, screen):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)

# Lấy kích thước của màn hình
screen_width, screen_height = screen.get_size()

# Lấy kích thước của logo
logo_width, logo_height = logo.get_size()

# Tính toán vị trí để đặt logo ở giữa màn hình theo chiều ngang
logo_x = (screen_width - logo_width) // 2

# Tính toán vị trí đặt logo ở giữa màn hình theo chiều dọc
logo_y = (screen_height - logo_height) // 2 - 100

# Trạng thái màn hình
MENU = 'menu'
GAME = 'game'
state = MENU

# Biến toàn cục cho sàn di chuyển
floor_x = 0
floor_speed = 1  # Giảm tốc độ chạy của sàn

# Trọng lực cho chim
gravity = 0.5  # Tăng giá trị của gravity để giảm tốc độ rơi của chim
bird_movement = 0
game_active = True

# Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(600, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(600, random_pipe_pos - 300))  # Giảm khoảng cách giữa ống trên và ống dưới
    return bottom_pipe, top_pipe

# Hàm di chuyển ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Hàm vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Hàm kiểm tra va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

# Hàm xoay chim
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

# Hàm hiển thị màn hình menu
def show_menu():
    global state  # Sử dụng biến toàn cục
    global floor_x  # Sử dụng biến toàn cục
    floor_x = 0
    running = True
    while running and state == MENU: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    state = GAME
                    running = False
                if score_button.collidepoint(event.pos):
                    print("Hiển thị bảng xếp hạng")
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        screen.fill(BLACK)
        screen.blit(bg, (0, 0))
        screen.blit(logo, (logo_x, logo_y))
        floor_x -= 1
        screen.blit(floor, (floor_x, 650))
        screen.blit(floor, (floor_x + 432, 650))
        if floor_x <= -432:
            floor_x = 0
        play_button = draw_button("Play", 116, 400, 200, 50, WHITE, screen)
        score_button = draw_button("Score", 50, 500, 150, 50, WHITE, screen)
        quit_button = draw_button("Quit", 232, 500, 150, 50, WHITE, screen)
        pygame.display.update()

# Hàm hiển thị màn hình chơi game
def show_game():
    global state
    global floor_x
    global floor_speed
    global bird_movement  # Khai báo bird_movement là toàn cục
    global pipe_list  # Thêm global ở đây
    global game_active  # Khai báo game_active là toàn cục
    floor_x = 0
    bird_movement = 0
    pipe_list.clear()  # Xóa danh sách ống cũ khi bắt đầu trò chơi mới
    clock = pygame.time.Clock() 
    running = True
    while running and state == GAME:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = MENU
                    running = False
                if event.key == pygame.K_SPACE:
                    bird_movement = -11  # Chỉ gán giá trị khi phím SPACE được nhấn
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    bird_rect.center = (100, 384)
                    bird_movement = 0
                    pipe_list.clear()
            if event.type == spawnpipe:
                pipe_list.extend(create_pipe())

        screen.blit(bg, (0, 0))
        if game_active:
            screen.blit(floor, (floor_x, 650))
            screen.blit(floor, (floor_x + 432, 650))
            
            bird_movement += gravity 
            bird_rect.centery += bird_movement 
            
            rotated_bird = rotate_bird(bird)  # Xoay chim
            screen.blit(rotated_bird, bird_rect)  # Vẽ chim đã xoay

            pipe_list = move_pipe(pipe_list)  # Di chuyển ống
            draw_pipe(pipe_list)  # Vẽ ống
            game_active = check_collision(pipe_list)

        # Nếu sàn di chuyển quá xa bên trái, reset vị trí của nó
        if floor_x <= -432:
            floor_x = 0
        floor_speed += 0.001  # Tăng tốc độ chạy của sàn sau mỗi vòng lặp

        pygame.display.update()

# Vòng lặp chính
while True:
    if state == MENU:
        show_menu()
    elif state == GAME:
        show_game()
