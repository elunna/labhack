from src import settings


class Door:
    """Defines door for a room in a map. """
    def __init__(self, room, x, y):
        if not room.valid_door_loc(x, y):
            raise ValueError('Invalid coordinates supplied for Door!')

        self.room = room
        self.x, self.y = x, y
        self.facing = room.direction_facing(self.x, self.y)

    def facing_other(self, other):
        """ Tells us if this door indirectly faces another door.
        The two cases are:
            Vertically facing: The lower door faces North and the higher door faces South
            Horizontally facing: The western door faces east and the eastern door faces west.

        If one door faces North and one faces East, they do not face eachother.
        :param other: A different door to compare against.
        :return: True if the doors face eachother, False otherwise.
        """
        faces = {self.facing, other.facing}
        MIN_FACING_SPACE = 1

        # See if the doors are facing vertically
        if faces == {'N', 'S'}:
            # Check which door is lower.
            if self.y - other.y >= MIN_FACING_SPACE:
                # This door is to the south of the other
                return self.facing == 'N'
            elif other.y - self.y >= MIN_FACING_SPACE:
                # This door is to the north of the other
                return self.facing == 'S'

        # See if the doors are facing horizontally
        if faces == {'E', 'W'}:
            # Check which door is east/west
            if self.x - other.x >= MIN_FACING_SPACE:
                # This door is to east of the other
                return self.facing == 'W'
            elif other.x - self.x >= MIN_FACING_SPACE:
                # This door is to west of the other
                return self.facing == 'E'

        return False

    def closet(self):
        """ Returns the coordinates of the "closet" space outside of the door where the door
        immediately faces.

        :return: x, y coordinates
        """
        dx, dy = settings.CARDINAL_DIR[self.facing]
        return self.x + dx, self.y + dy
