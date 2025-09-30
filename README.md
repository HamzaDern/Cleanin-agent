# Intelligent Cleaning Agent Simulation

A Python-based simulation of an autonomous agent that cleans rooms in a linear environment while managing a limited energy budget and adapting to dynamic changes.

## Overview

The agent operates in a row of N rooms (indexed 0 to N−1), where each room is either clean or dirty with a dirtiness level from 1 to 5. Starting at room 0, the agent must decide when to clean or move while respecting strict energy constraints:

- **Initial energy**: 2.5 × N  
- **Move cost**: 2 energy units per move (left or right)  
- **Clean cost**: Equal to the room’s current dirtiness level  

The environment is dynamic: after every agent action, each clean room has a 10% chance to become dirty again with a random dirtiness level (1–5). The simulation runs for a maximum of T steps and ends early if all rooms are clean with no useful actions left, or if the agent runs out of usable energy.

## Features

- Fully configurable number of rooms, step limit, and initial dirtiness
- Realistic energy accounting and action costs
- Stochastic re-dirtying to simulate real-world dynamics
- Comprehensive output: final room states, rooms cleaned, energy used, action sequence
- Reproducible runs with random seed support
- Modular, clean codebase with no external dependencies

## Usage

### Requirements
- Python 3.6 or higher

### Quick Start
1. Clone or download this repository
2. Open a terminal in the project folder
3. Run the simulation:

```bash
python main.py
```

### Command-Line Options

| Option                | Description                                                               | Default                   |
|-----------------------|---------------------------------------------------------------------------|---------------------------|
| `--rooms`             | Number of rooms in the environment                                        | `10`                      |
| `--steps`             | Maximum number of simulation steps                                        | `100`                     |
| `--seed`              | Random seed for reproducible results                                      | *None*                    |
| `--initial-dirtiness` | Space-separated list of initial dirtiness levels (0 = clean, 1–5 = dirty) | Random (50% chance dirty) |

### Examples

```bash
# Run with default settings
python main.py

# Small environment, limited steps
python main.py --rooms 5 --steps 30

# Reproducible run
python main.py --rooms 8 --steps 150 --seed 42

# Custom starting state
python main.py --rooms 4 --steps 80 --initial-dirtiness 3 0 2 5
```

## Output

After completion, the program displays:

- Final dirtiness level of each room
- Total number of unique rooms cleaned
- Total energy consumed and remaining energy
- Number of steps executed
- Termination reason
- Full sequence of actions taken (`Suck`, `MoveLeft`, `MoveRight`)

## Project Structure

- `main.py` – Entry point and command-line interface  
- `agent.py` – Intelligent agent logic and decision-making  
- `environment.py` – Room and world state management  
- `simulation.py` – Simulation loop and environmental dynamics  

## Extending the Agent

The baseline agent uses a simple reactive strategy (clean if dirty, otherwise move right). This provides a solid foundation for enhancements such as:

- Memory of previously seen dirty rooms
- Energy-efficient path planning
- Prioritization of high-dirtiness rooms
- Adaptive sweep patterns to counter re-dirtying

Modify the `decide_action` method in `agent.py` to implement advanced behaviors.

## License

This project is open source and available under the MIT License.
