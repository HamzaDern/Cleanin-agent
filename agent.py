from typing import Optional


class Agent:
    """
    Intelligent cleaning agent that operates in a linear environment.
    Basic behavior: clean if dirty, otherwise move right (or left at boundary).
    """
    
    def __init__(self, environment_size: int):
        self.position = 0
        self.energy = 2.5 * environment_size
        self.initial_energy = self.energy
        self.environment_size = environment_size
        self.actions_sequence = []
        self.rooms_cleaned = 0
        self.total_energy_consumed = 0
        self.cleaned_rooms_set = set()
    
    def get_percepts(self, environment) -> dict:
        """Get current percepts from the environment."""
        is_clean, dirtiness = environment.get_room_state(self.position)
        return {
            'current_room': self.position,
            'is_clean': is_clean,
            'dirtiness': dirtiness,
            'remaining_energy': self.energy
        }
    
    def can_perform_action(self, action: str, dirtiness: int = 0) -> bool:
        """Check if the agent can perform a given action with current energy."""
        if action == 'Suck':
            return self.energy >= dirtiness and dirtiness > 0
        elif action in ['MoveLeft', 'MoveRight']:
            return self.energy >= 2
        return False
    
    def perform_action(self, environment, action: str) -> bool:
        """Perform the specified action and update agent state."""
        percepts = self.get_percepts(environment)
        
        if action == 'Suck':
            if self.can_perform_action('Suck', percepts['dirtiness']):
                energy_cost = environment.clean_room(self.position)
                self.energy -= energy_cost
                self.total_energy_consumed += energy_cost
                self.actions_sequence.append('Suck')
                if self.position not in self.cleaned_rooms_set:
                    self.cleaned_rooms_set.add(self.position)
                    self.rooms_cleaned += 1
                return True
            return False
            
        elif action == 'MoveRight':
            if self.can_perform_action('MoveRight') and self.position < self.environment_size - 1:
                self.position += 1
                self.energy -= 2
                self.total_energy_consumed += 2
                self.actions_sequence.append('MoveRight')
                return True
            return False
            
        elif action == 'MoveLeft':
            if self.can_perform_action('MoveLeft') and self.position > 0:
                self.position -= 1
                self.energy -= 2
                self.total_energy_consumed += 2
                self.actions_sequence.append('MoveLeft')
                return True
            return False
        
        return False
    
    def decide_action(self, environment) -> Optional[str]:
        """Decide the next action based on basic agent behavior."""
        percepts = self.get_percepts(environment)
        
        if not percepts['is_clean'] and self.can_perform_action('Suck', percepts['dirtiness']):
            return 'Suck'
        
        if self.position < self.environment_size - 1:
            if self.can_perform_action('MoveRight'):
                return 'MoveRight'
        elif self.position > 0:
            if self.can_perform_action('MoveLeft'):
                return 'MoveLeft'
        
        return None
    
    def has_meaningful_actions(self, environment) -> bool:
        """Check if the agent has any meaningful actions left."""
        if environment.get_all_rooms_clean():
            return False
        
        if self.energy < 2:
            _, dirtiness = environment.get_room_state(self.position)
            if dirtiness > 0 and self.energy >= dirtiness:
                return True
            return False
        
        return True