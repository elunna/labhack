from actions.actions import Action


class SearchAction(Action):
    def perform(self):
        hidden_entities = self.get_hidden_entities(self.entity.x, self.entity.y)

        for e in hidden_entities:
            # Unhide the entity
            e.rm_comp("hidden")
            # Msg
            self.msg += f"You find a {e.name}! "

            # This might be too specific, but if we something more general we can add a
            # "remove on found" component.
            if e.name == "hidden corridor":
                print(f"removing hidden corridor at ({e.x}, {e.y})")
                # e.transparent = True  # Set this to make it transparent
                # Ideally we just remove it...
                result = self.entity.gamemap.rm_entity(e)
                print(f"success: {result}")

                # We have to manually set the tiles to transparent and explored
                self.entity.gamemap.tiles['transparent'][e.x, e.y] = True
                self.entity.gamemap.explored[e.x, e.y] = True
                self.entity.gamemap.visible[e.x, e.y] = True
                print(f"transparent: {self.entity.gamemap.tiles['transparent'][e.x, e.y]}")
                print(f"explored: {self.entity.gamemap.explored[e.x, e.y]}")
                print(f"visible: {self.entity.gamemap.visible[e.x, e.y]}")

                # self.entity.gamemap.tiles["transparent"][e.x, e.y] = True

        # self.recompute_fov = True

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
