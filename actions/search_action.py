from actions.actions import Action


class SearchAction(Action):
    def perform(self):
        hidden_entities = self.get_hidden_entities(self.entity.x, self.entity.y)
        for e in hidden_entities:
            # Unhide the entity
            e.rm_comp("hidden")
            # Msg
            self.msg += f"You find a {e.name}! "

    def get_hidden_entities(self, x, y):
        _map = self.entity.gamemap

        # Look at all the squares immediately surrounding the player
        tiles_around = _map.tiles_around(x, y, 1)

        hidden_entities = []
        for x, y in tiles_around:
            entities = _map.get_entities_at(x, y)
            for e in entities:
                if "hidden" in e:
                    hidden_entities.append(e)

        # If any entities are hidden, it will unhide them and reveal a message.
        return hidden_entities
