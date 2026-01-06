import pygame
import random
import numpy as np

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game settings
SNAKE_BLOCK = 20
SNAKE_SPEED = 45
WIDTH, HEIGHT = 800, 600

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Q-Learning")
clock = pygame.time.Clock()

# Q-learning parameters
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 1.0
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
q_table = {}

generation = 0
high_score = 0

# ------------------------------------
# Utility Functions
# ------------------------------------
def get_random_food_position(snake):
    while True:
        x = random.randrange(0, WIDTH, SNAKE_BLOCK)
        y = random.randrange(0, HEIGHT, SNAKE_BLOCK)
        if (x, y) not in snake:
            return (x, y)

def initialize_game():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    food = get_random_food_position(snake)
    return snake, food

def get_new_position(pos, action):
    x, y = pos
    if action == "UP":
        y -= SNAKE_BLOCK
    elif action == "DOWN":
        y += SNAKE_BLOCK
    elif action == "LEFT":
        x -= SNAKE_BLOCK
    elif action == "RIGHT":
        x += SNAKE_BLOCK
    return (x, y)

def is_collision(snake):
    head = snake[0]
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False

# ------------------------------------
# Improved State Representation
# ------------------------------------
def get_state(snake, food):
    head = snake[0]

    danger_up = (head[0], head[1] - SNAKE_BLOCK) in snake or head[1] - SNAKE_BLOCK < 0
    danger_down = (head[0], head[1] + SNAKE_BLOCK) in snake or head[1] + SNAKE_BLOCK >= HEIGHT
    danger_left = (head[0] - SNAKE_BLOCK, head[1]) in snake or head[0] - SNAKE_BLOCK < 0
    danger_right = (head[0] + SNAKE_BLOCK, head[1]) in snake or head[0] + SNAKE_BLOCK >= WIDTH

    food_dir_x = 1 if food[0] > head[0] else -1 if food[0] < head[0] else 0
    food_dir_y = 1 if food[1] > head[1] else -1 if food[1] < head[1] else 0

    return (danger_up, danger_down, danger_left, danger_right, food_dir_x, food_dir_y)

def get_action(state, epsilon):
    if state not in q_table:
        q_table[state] = {a: 0 for a in ACTIONS}

    if np.random.rand() < epsilon:
        return random.choice(ACTIONS)
    return max(q_table[state], key=q_table[state].get)

def update_q(state, action, reward, next_state):
    if next_state not in q_table:
        q_table[next_state] = {a: 0 for a in ACTIONS}

    old = q_table[state][action]
    future = max(q_table[next_state].values())
    q_table[state][action] = old + ALPHA * (reward + GAMMA * future - old)

# ------------------------------------
# Main Game Loop
# ------------------------------------
def main():
    global EPSILON, generation, high_score

    while True:
        snake, food = initialize_game()
        score = 0
        last_move_time = pygame.time.get_ticks()
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            state = get_state(snake, food)
            action = get_action(state, EPSILON)

            new_head = get_new_position(snake[0], action)
            snake.insert(0, new_head)

            if is_collision(snake):
                reward = -100
                q_table[state][action] += ALPHA * (reward - q_table[state][action])
                game_over = True
                generation += 1
                break

            if new_head == food:
                food = get_random_food_position(snake)
                reward = 100
                score += 1
            else:
                snake.pop()
                reward = 1 if abs(food[0] - new_head[0]) + abs(food[1] - new_head[1]) < \
                            abs(food[0] - snake[1][0]) + abs(food[1] - snake[1][1]) else -1

            next_state = get_state(snake, food)
            update_q(state, action, reward, next_state)

            EPSILON = max(MIN_EPSILON, EPSILON * EPSILON_DECAY)

            # Drawing
            display.fill(BLACK)
            for block in snake:
                pygame.draw.rect(display, GREEN, (*block, SNAKE_BLOCK, SNAKE_BLOCK))
            pygame.draw.rect(display, RED, (*food, SNAKE_BLOCK, SNAKE_BLOCK))

            font = pygame.font.SysFont(None, 30)
            display.blit(font.render(f"Gen: {generation}", True, WHITE), (10, 10))
            display.blit(font.render(f"Score: {score}", True, WHITE), (10, 40))
            display.blit(font.render(f"High: {high_score}", True, WHITE), (10, 70))

            pygame.display.update()
            clock.tick(SNAKE_SPEED)

        high_score = max(high_score, score)

if __name__ == "__main__":
    main()
