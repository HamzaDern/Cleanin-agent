class Room:
    """
    Represents a single room in the environment.
    
    Attributes:
        dirtiness (int): 0 if clean, 1-5 if dirty
    """
    def __init__(self, dirtiness: int = 0):
        self.dirtiness = dirtiness
    
    def is_clean(self) -> bool:
        return self.dirtiness == 0
    
    def clean(self) -> int:
        """
        Clean the room and return the energy cost (original dirtiness level).
        """
        cost = self.dirtiness
        self.dirtiness = 0
        return cost
    
    def make_dirty(self, dirtiness_level: int):
        """
        Make the room dirty with specified dirtiness level.
        """
        self.dirtiness = dirtiness_level


class Environment:
    """
    Represents the linear environment containing N rooms.
    
    Attributes:
        rooms (list[Room]): List of Room objects
        size (int): Number of rooms in the environment
    """
    def __init__(self, size: int, initial_dirtiness: list = None):
        self.size = size
        if initial_dirtiness is None:
            self.rooms = [Room(0) for _ in range(size)]
        else:
            assert len(initial_dirtiness) == size, "Initial dirtiness list must match environment size"
            for dirt in initial_dirtiness:
                assert 0 <= dirt <= 5, "Dirtiness must be between 0-5"
            self.rooms = [Room(dirt) for dirt in initial_dirtiness]
    
    def get_room_state(self, room_index: int) -> tuple:
        """
        Get the state of a room at given index.
        Returns: (is_clean: bool, dirtiness: int)
        """
        room = self.rooms[room_index]
        return (room.is_clean(), room.dirtiness)
    
    def clean_room(self, room_index: int) -> int:
        """Clean the room at given index and return energy cost."""
        return self.rooms[room_index].clean()
    
    def make_room_dirty(self, room_index: int, dirtiness_level: int):
        """Make a specific room dirty with given dirtiness level."""
        self.rooms[room_index].make_dirty(dirtiness_level)
    
    def get_all_rooms_clean(self) -> bool:
        """Check if all rooms are clean."""
        return all(room.is_clean() for room in self.rooms)
    
    def get_room_dirtiness_levels(self) -> list:
        """Get dirtiness levels of all rooms for output."""
        return [room.dirtiness for room in self.rooms]