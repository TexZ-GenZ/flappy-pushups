import pygame
import random
import cv2
import mediapipe as mp
import numpy as np

# Initialize Pygame
pygame.init()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

video_cam = cv2.VideoCapture(1)

if not video_cam.isOpened():
    print("Cannot access the camera")
    exit()

# Get camera resolution
SCREEN_WIDTH = int(video_cam.get(cv2.CAP_PROP_FRAME_WIDTH))
SCREEN_HEIGHT = int(video_cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up the display with camera resolution
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Pygame")

# Constants
PIPE_WIDTH = 50
PIPE_SPEED = 15
BIRD_HEIGHT_PERCENT_TO_SCREEN = 0.05
BIRD_X_POS = SCREEN_WIDTH // 4

# Colors
WHITE = (255, 255, 255)

# Load images
bird_image = pygame.image.load('./assests/redbird-upflap.png').convert_alpha()
pipe_image = pygame.image.load('./assests/pipe-green.png').convert_alpha()
base_image = pygame.image.load('./assests/base.png').convert_alpha()

# Scale images
bird_image = pygame.transform.scale(bird_image, (50, int(SCREEN_HEIGHT * BIRD_HEIGHT_PERCENT_TO_SCREEN)))
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, SCREEN_HEIGHT))
base_image = pygame.transform.scale(base_image, (SCREEN_WIDTH, int(SCREEN_HEIGHT * 0.1)))

# Class Bird
class Bird:
    def __init__(self):
        self.x = BIRD_X_POS
        self.y = SCREEN_HEIGHT // 2
        self.target_y = self.y
        self.y_history = [self.y] * 3
        self.dead_zone = 5
        self.max_speed = 30

    def update(self, frame):
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe Hands
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the y-coordinate of the index finger tip
                index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                
                # Convert the y-coordinate to pixel position
                self.target_y = int(index_finger_y * SCREEN_HEIGHT)

        # Apply dead zone
        if abs(self.target_y - self.y) > self.dead_zone:
            # Calculate direction and apply max speed
            direction = 1 if self.target_y > self.y else -1
            move_amount = min(abs(self.target_y - self.y), self.max_speed)
            new_y = self.y + direction * move_amount
            
            # Update position history
            self.y_history.pop(0)
            self.y_history.append(new_y)
            
            # Set new position with weighted average (more weight to recent positions)
            self.y = int((self.y_history[0] + 2*self.y_history[1] + 3*self.y_history[2]) / 6)

    def draw(self, screen):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.6))

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        # Draw top pipe
        screen.blit(pipe_image, (self.x, self.height - SCREEN_HEIGHT))
        # Draw bottom pipe
        screen.blit(pipe_image, (self.x, self.height + int(3.5 * BIRD_HEIGHT_PERCENT_TO_SCREEN * SCREEN_HEIGHT)))

    def is_offscreen(self):
        return self.x < -PIPE_WIDTH

    def collide(self, bird):
        within_pipe_x_bounds = bird.x + 50 > self.x and bird.x < self.x + PIPE_WIDTH
        
        within_top_pipe_y_bounds = bird.y - 25 >= 0 and bird.y < self.height
        
        within_bottom_pipe_y_bounds = bird.y - 25 + int(SCREEN_HEIGHT * BIRD_HEIGHT_PERCENT_TO_SCREEN) > self.height + int(3.5 * BIRD_HEIGHT_PERCENT_TO_SCREEN * SCREEN_HEIGHT) and bird.y <= SCREEN_HEIGHT
        
        return within_pipe_x_bounds and (within_top_pipe_y_bounds or within_bottom_pipe_y_bounds)

# Game Manager class
class GameManager:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.is_game_over = False

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.is_game_over = False

    def update(self, frame):
        if not self.is_game_over:
            self.bird.update(frame)

            if len(self.pipes) == 0 or self.pipes[-1].x < SCREEN_WIDTH // 2:
                self.pipes.append(Pipe())

            for pipe in self.pipes:
                pipe.update()
                if pipe.is_offscreen():
                    self.pipes.remove(pipe)
                    self.score += 1
                if pipe.collide(self.bird):
                    self.is_game_over = True

    def draw(self, screen):
        self.bird.draw(screen)
        for pipe in self.pipes:
            pipe.draw(screen)
        screen.blit(base_image, (0, SCREEN_HEIGHT - int(SCREEN_HEIGHT * 0.1)))

        # Draw score
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.score), 1, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2, 50))

# Game loop
game = GameManager()
clock = pygame.time.Clock()

running = True
while running:
    ret, frame = video_cam.read()
    if ret:
        # Rotate the frame 90 degrees clockwise if needed
        frame_render = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        frame_surface = pygame.surfarray.make_surface(cv2.cvtColor(frame_render, cv2.COLOR_BGR2RGB))
        screen.blit(frame_surface, (0, 0))  # Draw the webcam feed as background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update(frame)  # Update game state with the current frame
        game.draw(screen)  # Draw the game elements

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Maintain 30 FPS

        if game.is_game_over:
            print("Game Over! Final Score:", game.score)
            pygame.time.wait(2000)  # Wait for 2 seconds before resetting
            game.reset()

video_cam.release()
cv2.destroyAllWindows()
pygame.quit()