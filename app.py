import pygame, sys, random

def draw_floor():
    screen.blit(bg_base,(floor_x_position, 450 ))
    screen.blit(bg_base,(floor_x_position+288, 450 ))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(400,random_pipe_pos))
    upper_pipe = pipe_surface.get_rect(midbottom =(400,random_pipe_pos - 170))
    return bottom_pipe, upper_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if  pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False,True )
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >= 450:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1) 
    return new_bird

def bird_animation():
    new_bird = bird_frame[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

pygame.init()
screen = pygame.display.set_mode((288,512 ))
clock = pygame.time.Clock()

#game var
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/sprites/background-day.png').convert()
bg_base = pygame.image.load('assets/sprites/base.png').convert()
floor_x_position = 0

bird_downflap = pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
bird_frame = [bird_downflap,bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frame[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))

BIRDFLAP = pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/sprites/pipe-green.png')
pipe_list = []
pipe_height = [200, 320, 400]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0 
        
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()
            

    screen.blit(bg_surface,(0,0))

    if game_active:
        #bird

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        #pipes 

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)


    

    #floor 

    floor_x_position -= 1
    draw_floor()
    if floor_x_position < -288:
        floor_x_position = 0
        
    
    
    
    pygame.display.update()
    clock.tick(120)
