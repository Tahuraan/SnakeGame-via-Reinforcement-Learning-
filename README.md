# Snake Game with Q-learning AI 

This project implements a **Snake Game** with an AI agent powered by **Q-learning**, a reinforcement learning algorithm. The snake learns to navigate the grid to eat food while avoiding collisions with itself and the walls, gradually improving its performance through experience.

## Features
- **Q-learning Agent**: The snake uses Q-learning to learn optimal moves over generations, learning to maximize its score by balancing exploration and exploitation.
- **Reward and Penalty System**: Rewards the snake for eating food and penalizes it for collisions and revisiting previously visited positions.
- **Adaptive Exploration with Epsilon Decay**: Epsilon decay allows the agent to balance exploration and exploitation as it learns.
- **Performance Display**: Real-time display of generation count, current score, and high score.
- **Customizable Parameters**: Q-learning parameters, snake speed, and other settings can be adjusted to observe different learning behaviors.

## Installation
### Prerequisites
- **Python 3.x**
- **Pygame** and **NumPy** libraries

### Installation Steps
1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/snake-qlearning.git
   cd snake-qlearning
   ```

2. **Install dependencies**:
   ```bash
   pip install pygame numpy
   ```

3. **Run the game**:
   ```bash
   python snake_qlearning.py
   ```

## How It Works
The Q-learning algorithm enables the snake to learn an optimal policy based on its environment:
- **State Representation**: The agent's state includes the direction to food, body direction, and wall proximity.
- **Q-table**: Tracks the agent’s learned values for each state-action pair, helping the snake select actions with the highest expected rewards.
- **Rewards and Penalties**:
  - **+100** for eating food
  - **-100** for collisions
  - **+0.1** for moving to a new position
  - **-0.1** for revisiting positions

Each episode (game run) updates the Q-table, helping the snake refine its strategy with experience. Epsilon decay allows the snake to explore new actions at first, then focus on learned actions over time.

## Game Controls
The game runs on autopilot using the Q-learning agent, so no player controls are required. You can stop the game by closing the game window.

## Parameters
Customize the following Q-learning and game parameters in the code:
- `ALPHA` (learning rate): Controls how much new information overrides old.
- `GAMMA` (discount factor): Balances immediate vs. future rewards.
- `EPSILON` (exploration rate): Initial rate of random actions.
- `EPSILON_DECAY` and `MIN_EPSILON`: Control how exploration decreases over time.
- `SNAKE_SPEED`: Controls the game speed, affecting the agent's training pace.

## Code Structure
- **initialize_game**: Sets up the initial snake position, direction, and food location.
- **get_random_food_position**: Spawns food in a random, unoccupied cell.
- **get_state**: Encodes the environment’s state from the snake’s perspective.
- **get_action**: Selects the best action based on Q-values or a random action (epsilon-greedy).
- **update_q_table**: Updates Q-values based on the current state, action, and reward.
- **main**: Runs the main game loop, handling state updates, Q-learning, and rendering.

## Future Improvements
Potential enhancements for further learning:
- **Deep Q-learning**: Implementing neural networks for more complex state representation.
- **Obstacle addition**: Adding obstacles to increase challenge.
- **Adaptive rewards**: Dynamic reward adjustments based on performance.
