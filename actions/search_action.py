from actions.actions import Action


class SearchAction(Action):
    def perform(self):
        hidden_entities = self.get_hidden_entities(self.entity.x, self.entity.y)

        for e in hidden_entities:
            # Unhide the entity
            e.rm_comp("hidden")
            self.msg += f"You find a {e.name}! "

            # This might be too specific, but if we something more general we can add a
            # "remove on found" component.
            if e.name == "hidden corridor":
                self.entity.gamemap.rm_entity(e)
            if e.name == "hidden door":
                e.consumable.activate(self)  # Change the tile back to a door
                # It consumes itself
                self.entity.gamemap.rm_entity(e)

    def get_hidden_entities(self, x, y):
        _map = self.entity.gamemap

        # Look at all the squares immediately surrounding the player
        tiles_around = _map.tiles_around(x, y, 1)

        hidden_entities = []
        for x, y in tiles_around:
            entities = _map.filter(x=x, y=y)
            for e in entities:
                if "hidden" in e:
                    hidden_entities.append(e)

        # If any entities are hidden, it will unhide them and reveal a message.
        return hidden_entities
