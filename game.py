import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 400
screen_height = 400

# Create the Pygame window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Idle and Directional Animation with Falling Balls")

# Load the background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))  # Scale to screen size

# Load the sprite sheets for idle and running animations
idle_sprite_sheet = pygame.image.load("Pink_Monster_Idle_4.png")
run_sprite_sheet = pygame.image.load("Pink_Monster_Run_6.png")

# Define sprite properties
sprite_width = 32
sprite_height = 32

# Load idle animation frames
idle_frames = [
    idle_sprite_sheet.subsurface(pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height))
    for i in range(4)  # 4 frames for idle
]

# Load running animation frames
run_frames = [
    run_sprite_sheet.subsurface(pygame.Rect(i * sprite_width, 0, sprite_width, sprite_height))
    for i in range(6)  # 6 frames for running
]

# Create mirrored frames for running left
run_frames_left = [pygame.transform.flip(frame, True, False) for frame in run_frames]

# Initial position of the character
x, y = 150, 175

# Movement speed (pixels per frame)
speed = 2

# Animation variables
frame_index = 0
frame_timer = 0
frame_delay = 150  # Milliseconds between frames

# Direction and state flags
moving_right = False
moving_left = False
is_idle = True
last_key = None  # To track the last key pressed

# Ball properties
ball_radius = 15
ball_color = (255, 0, 0)  # Red color

# Ball list to store multiple balls with random fall speeds (no speed of 1)
balls = [
    {"x": random.randint(0, screen_width), "y": -ball_radius, "speed": random.randint(2, 5)}  # Speed now between 2 and 5
    for _ in range(3)
]

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states (for continuous movement)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] and last_key != pygame.K_d:
        # Start moving right if 'D' is pressed
        moving_right = True
        moving_left = False
        is_idle = False
        last_key = pygame.K_d
        frame_index = 0  # Reset frame index for run animation

    elif keys[pygame.K_a] and last_key != pygame.K_a:
        # Start moving left if 'A' is pressed
        moving_left = True
        moving_right = False
        is_idle = False
        last_key = pygame.K_a
        frame_index = 0  # Reset frame index for run animation

    elif not keys[pygame.K_a] and not keys[pygame.K_d]:
        # If no movement keys are pressed, go idle
        moving_left = False
        moving_right = False
        is_idle = True
        last_key = None

    # Handle horizontal movement
    if moving_right:
        x += speed
    if moving_left:
        x -= speed

    # Prevent character from going off-screen
    x = max(0, min(screen_width - sprite_width, x))  # Keep within horizontal bounds
    y = max(0, min(screen_height - sprite_height, y))  # Keep within vertical bounds

    # Update falling logic for all balls
    for ball in balls:
        ball["y"] += ball["speed"]  # Ball falls at its own speed
        # If the ball hits the ground, respawn it at the top
        if ball["y"] >= screen_height - ball_radius:
            ball["y"] = -ball_radius  # Respawn at the top with a random x position
            ball["x"] = random.randint(0, screen_width)
            ball["speed"] = random.randint(2, 5)  # Give it a new random speed when it respawns
            score += 1  # Increase score when ball hits the ground

    # Collision Detection (pink monster vs. red balls)
    monster_rect = pygame.Rect(x, y, sprite_width, sprite_height)

    for ball in balls:
        ball_rect = pygame.Rect(ball["x"] - ball_radius, ball["y"] - ball_radius, ball_radius * 2, ball_radius * 2)
        if monster_rect.colliderect(ball_rect):
            # If the monster touches any ball, quit the game
            print("Collision detected! Game over.")
            running = False

    # Update animation frame on each new key press (not continuously)
    frame_timer += clock.get_time()
    if frame_timer >= frame_delay:
        frame_timer = 0
        if is_idle:
            # Ensure frame_index is within bounds for idle frames
            frame_index = (frame_index + 1) % len(idle_frames)  # Wrap index correctly
        else:
            # Ensure frame_index is within bounds for running frames
            frame_index = (frame_index + 1) % len(run_frames)  # Wrap index correctly

    # Ensure frame_index is within bounds for the animation frames
    frame_index = max(0, min(frame_index, len(idle_frames) - 1 if is_idle else len(run_frames) - 1))

    # Clear screen (draw the background first)
    screen.blit(background, (0, 0))  # Draw the background image

    # Draw the red balls
    for ball in balls:
        pygame.draw.circle(screen, ball_color, (ball["x"], ball["y"]), ball_radius)

    # Draw the appropriate animation
    if is_idle:
        # Play idle animation
        screen.blit(idle_frames[frame_index], (x, y))
    elif moving_right:
        # Play running right animation
        screen.blit(run_frames[frame_index], (x, y))
    elif moving_left:
        # Play running left animation
        screen.blit(run_frames_left[frame_index], (x, y))

    # Draw the score at the top right
    score_text = font.render(f"Score: {score}", True, (0, 0, 255))  # Blue score
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

