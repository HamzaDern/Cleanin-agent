import random
from environment import Environment
from agent import Agent


class Simulation:
    """Manages the simulation of the intelligent cleaning agent."""
    
    def __init__(self, environment_size: int, max_steps: int, initial_dirtiness: list = None):
        self.environment = Environment(environment_size, initial_dirtiness)
        self.agent = Agent(environment_size)
        self.max_steps = max_steps
        self.current_step = 0
        self.simulation_ended = False
        self.termination_reason = ""
    
    def step(self) -> bool:
        """Execute one step of the simulation."""
        if self.current_step >= self.max_steps:
            self.termination_reason = "Maximum steps reached"
            return False
        
        action = self.agent.decide_action(self.environment)
        if action is None:
            self.termination_reason = "No valid actions possible"
            return False
        
        success = self.agent.perform_action(self.environment, action)
        if not success:
            self.termination_reason = "Action failed due to insufficient energy"
            return False
        
        self._apply_re_dirtying()
        
        if self.agent.energy <= 0 and not self.agent.has_meaningful_actions(self.environment):
            self.termination_reason = "No energy for meaningful actions"
            return False
        
        if self.environment.get_all_rooms_clean() and not self.agent.has_meaningful_actions(self.environment):
            self.termination_reason = "All rooms clean and no meaningful actions"
            return False
        
        self.current_step += 1
        return True
    
    def _apply_re_dirtying(self):
        """Apply 10% chance re-dirtying to all clean rooms."""
        for i in range(self.environment.size):
            is_clean, _ = self.environment.get_room_state(i)
            if is_clean and random.random() < 0.1:
                dirtiness_level = random.randint(1, 5)
                self.environment.make_room_dirty(i, dirtiness_level)
    
    def run(self):
        """Run the complete simulation until termination."""
        while self.step():
            pass
    
    def get_results(self) -> dict:
        """Get simulation results for output."""
        return {
            'final_room_states': self.environment.get_room_dirtiness_levels(),
            'rooms_cleaned': self.agent.rooms_cleaned,
            'total_energy_consumed': self.agent.total_energy_consumed,
            'final_remaining_energy': self.agent.energy,
            'action_sequence': self.agent.actions_sequence,
            'steps_executed': self.current_step,
            'termination_reason': self.termination_reason
        }