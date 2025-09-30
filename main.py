import random
import argparse
from simulation import Simulation


def parse_arguments():
    parser = argparse.ArgumentParser(description='Intelligent Cleaning Agent Simulation')
    parser.add_argument('--rooms', type=int, default=10, 
                       help='Number of rooms in the environment (default: 10)')
    parser.add_argument('--steps', type=int, default=100,
                       help='Maximum number of simulation steps (default: 100)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility (default: None)')
    parser.add_argument('--initial-dirtiness', type=int, nargs='*',
                       help='Initial dirtiness levels for rooms (0-5, 0=clean)')
    return parser.parse_args()


def generate_random_initial_dirtiness(size: int) -> list:
    """Generate random initial dirtiness (50% chance dirty, level 1-5)."""
    return [random.randint(1, 5) if random.random() < 0.5 else 0 for _ in range(size)]


def print_results(results: dict):
    print("\n" + "="*60)
    print("SIMULATION RESULTS")
    print("="*60)
    print(f"Final room states (0=clean, 1-5=dirty): {results['final_room_states']}")
    print(f"Number of rooms cleaned: {results['rooms_cleaned']}")
    print(f"Total energy consumed: {results['total_energy_consumed']:.1f}")
    print(f"Final remaining energy: {results['final_remaining_energy']:.1f}")
    print(f"Steps executed: {results['steps_executed']}")
    print(f"Termination reason: {results['termination_reason']}")
    print(f"\nAction sequence ({len(results['action_sequence'])} actions):")
    seq = results['action_sequence']
    if len(seq) <= 50:
        print(" -> ".join(seq))
    else:
        print(" -> ".join(seq[:25]) + " -> ... -> " + " -> ".join(seq[-25:]))


def main():
    args = parse_arguments()
    
    if args.seed is not None:
        random.seed(args.seed)
    
    if args.rooms <= 0:
        print("Error: Number of rooms must be positive")
        return
    
    if args.initial_dirtiness is not None:
        if len(args.initial_dirtiness) != args.rooms:
            print(f"Error: Initial dirtiness list must have exactly {args.rooms} values")
            return
        for dirt in args.initial_dirtiness:
            if not (0 <= dirt <= 5):
                print("Error: Dirtiness levels must be between 0 and 5")
                return
        initial_dirtiness = args.initial_dirtiness
    else:
        initial_dirtiness = generate_random_initial_dirtiness(args.rooms)
    
    print(f"Starting simulation with {args.rooms} rooms and max {args.steps} steps")
    print(f"Initial dirtiness: {initial_dirtiness}")
    print(f"Initial energy: {2.5 * args.rooms}")
    
    sim = Simulation(args.rooms, args.steps, initial_dirtiness)
    sim.run()
    print_results(sim.get_results())


if __name__ == "__main__":
    main() 
