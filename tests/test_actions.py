""" Tests for actions.py """

from src import actions
from src import exceptions
from src import factory
import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def player():
    return toolkit.cp_player()


@pytest.fixture
def testengine():
    m = toolkit.test_map()
    p = m.get_player()
    e = engine.Engine(p)
    e.game_map = m


def test_Action_init(player):
    a = actions.Action(player)
    assert a.entity == player
    assert a.msg == ''


def test_Action_engine(test_map):
    player = test_map.get_player()
    a = actions.Action(player)
    result = a.engine
    assert result is None


def test_Action_perform__not_implemented(player):
    a = actions.Action(player)
    with pytest.raises(NotImplementedError):
        a.perform()


def test_ActionWithDirection_is_Action(test_map):
    player = test_map.get_player()
    a = actions.ActionWithDirection(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_ActionWithDirection_init(test_map):
    player = test_map.get_player()
    a = actions.ActionWithDirection(entity=player, dx=1, dy=-1)
    assert a.entity == player
    assert a.dx == 1
    assert a.dy == -1
    assert a.msg == ''


def test_ActionWithDirection_dest_xy(test_map):
    player = test_map.get_player()
    dx, dy = 1, -1
    a = actions.ActionWithDirection(entity=player, dx=dx, dy=dy)
    assert a.dest_xy == (player.x + dx, player.y + dy)


def test_ActionWithDirection_blocking_entity(player):
    testmap = toolkit.test_map()
    player.place(1, 2, testmap)
    # Blocked by a wall, not an entity
    a = actions.ActionWithDirection(entity=player, dx=0, dy=-1)
    assert a.blocking_entity is None


def test_ActionWithDirection__target_actor(player):
    testmap = toolkit.test_map()
    player.place(2, 4, testmap)
    a = actions.ActionWithDirection(entity=player, dx=0, dy=1)
    assert a.target_actor.name == "Grid Bug"


def test_ActionWithDirection__perform(player):
    testmap = toolkit.test_map()
    player.place(2, 4, testmap)
    a = actions.ActionWithDirection(entity=player, dx=0, dy=1)
    with pytest.raises(NotImplementedError):
        a.perform()


def test_BumpAction_is_Action(test_map):
    player = test_map.get_player()
    a = actions.BumpAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_BumpAction_is_ActionWithDirection(test_map):
    player = test_map.get_player()
    a = actions.BumpAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.ActionWithDirection)


def test_BumpAction_init(test_map):
    player = test_map.get_player()
    a = actions.BumpAction(entity=player, dx=1, dy=-1)
    assert a.entity == player
    assert a.dx == 1
    assert a.dy == -1
    assert a.msg == ''


def test_BumpAction_perform__Move(test_map):
    player = test_map.get_player()
    a = actions.BumpAction(entity=player, dx=1, dy=1)
    result = a.perform()
    assert isinstance(result, actions.MovementAction)


def test_BumpAction_perform__Move(test_map):
    # We'll attack the Grid Bug at (2, 5)
    player = test_map.get_player()
    player.place(2, 4, test_map)
    a = actions.BumpAction(entity=player, dx=0, dy=1)
    result = a.perform()
    assert isinstance(result, actions.MeleeAction)


def test_ItemAction_is_Action(test_map):
    player = test_map.get_player()
    potion = factory.health_potion
    a = actions.ItemAction(entity=player, item=potion)
    assert isinstance(a, actions.Action)


def test_ItemAction_init(test_map):
    player = test_map.get_player()
    potion = factory.health_potion
    a = actions.ItemAction(entity=player, item=potion)
    assert a.item == potion
    assert a.entity == player


def test_ItemAction_init__default_targetxy_is_playersxy(test_map):
    player = test_map.get_player()
    potion = factory.health_potion
    a = actions.ItemAction(entity=player, item=potion)
    assert a.target_xy == (player.x, player.y)


def test_ItemAction_init__with_target_xy(test_map):
    player = test_map.get_player()
    potion = factory.health_potion
    a = actions.ItemAction(entity=player, item=potion, target_xy=(1, 1))
    assert a.target_xy == (1, 1)


def test_ItemAction_target_actor(test_map):
    player = test_map.get_player()
    potion = factory.health_potion
    # We'll target the grid bug
    a = actions.ItemAction(entity=player, item=potion, target_xy=(2, 5))
    result = a.target_actor
    assert result.name == "Grid Bug"


# perform
# perform with a consumable item
# perform with a non-consumable item
# perform with a reuseable/chargeable item?


def test_DropItem_is_Action(test_map):
    player = test_map.get_player()
    potion = factory.health_potion
    a = actions.DropItem(entity=player, item=potion)
    assert isinstance(a, actions.Action)


def test_DropItem_is_ItemAction(test_map):
    player = test_map.get_player()
    potion = factory.health_potion
    a = actions.DropItem(entity=player, item=potion)
    assert isinstance(a, actions.ItemAction)


def test_DropItem_init(test_map):
    player = test_map.get_player()
    potion = factory.health_potion
    a = actions.DropItem(entity=player, item=potion)
    assert a.entity == player
    assert a.item == potion


def test_DropItem_perform__item_leaves_inventory(test_map):
    player = test_map.get_player()
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "Dagger"

    a = actions.DropItem(entity=player, item=item)
    result = a.perform()
    assert item not in player.inventory.items


def test_DropItem_perform__item_appears_on_map(test_map):
    player = test_map.get_player()
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "Dagger"

    a = actions.DropItem(entity=player, item=item)
    result = a.perform()
    assert item in test_map.get_items_at(player.x, player.y)


def test_DropItem_perform__msg(test_map):
    player = test_map.get_player()
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "Dagger"

    a = actions.DropItem(entity=player, item=item)
    result = a.perform()
    assert a.msg == f"You dropped the {item.name}."


def test_DropItem_perform__invalid_item_raises_Impossible(test_map):
    player = test_map.get_player()
    a = actions.DropItem(entity=player, item=factory.sword)

    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_DropItem_perform__equipped_item(test_map):
    player = test_map.get_player()
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "Dagger"
    player.equipment.toggle_equip(item)
    assert player.equipment.item_is_equipped(item)

    a = actions.DropItem(entity=player, item=item)
    result = a.perform()

    assert not player.equipment.item_is_equipped(item)


def test_EquipAction_is_Action(test_map):
    player = test_map.get_player()
    armor = factory.leather_armor
    a = actions.EquipAction(entity=player, item=armor)
    assert isinstance(a, actions.Action)


def test_EquipAction_init(test_map):
    player = test_map.get_player()
    armor = factory.leather_armor
    a = actions.EquipAction(entity=player, item=armor)
    assert a.entity == player
    assert a.item == armor


def test_EquipAction_perform(test_map):
    player = test_map.get_player()
    armor = factory.leather_armor
    assert not player.equipment.item_is_equipped(armor)

    a = actions.EquipAction(entity=player, item=armor)
    a.perform()
    assert player.equipment.item_is_equipped(armor)


def test_MeleeAction_is_Action(test_map):
    player = test_map.get_player()
    a = actions.MeleeAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_MeleeAction_is_ActionWithDirection(test_map):
    player = test_map.get_player()
    a = actions.MeleeAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.ActionWithDirection)


def test_MeleeAction_is_ActionWithDirection(test_map):
    player = test_map.get_player()
    a = actions.MeleeAction(entity=player, dx=1, dy=-1)
    assert a.dx == 1
    assert a.dy == -1
    assert a.entity == player


def test_MeleeAction_perform__no_target__raises_Impossible(test_map):
    player = test_map.get_player()
    a = actions.MeleeAction(entity=player, dx=-1, dy=-1)
    with pytest.raises(exceptions.Impossible):
        a.perform()

# perform-Case: no target
# perform-Case: miss, calls miss
# perform-Case: hit w weapon, calls hit_with_weapon
# perform-Case: hit w hands, calls hit_withhands_

def test_MeleeAction_calc_target_number(test_map):
    player = test_map.get_player()
    a = actions.MeleeAction(entity=player, dx=-1, dy=-1)

    target = factory.orc
    assert target.level.current_level == 1
    assert target.fighter.ac == 7

    result = a.calc_target_number(target)
    expected = 10 + target.fighter.ac + target.level.current_level
    assert result == expected


def test_MeleeAction_roll_hit_die(test_map):
    player = test_map.get_player()
    a = actions.MeleeAction(entity=player, dx=-1, dy=-1)
    result = a.roll_hit_die()
    # Just testing that the random number is between 1 and the sides (usually
    # 20)
    assert result >= 1
    assert result <= a.die


def test_MeleeAction_hit_with_weapon__returns_dmg(test_map):
    player = test_map.get_player()
    dagger = player.inventory.items.get('a')
    assert player.equipment.toggle_equip(dagger)

    a = actions.MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.hit_with_weapon(target)
    attack_max = player.equipment.weapon.equippable.attack.die_sides
    assert result >= 1
    assert result <= attack_max


def test_MeleeAction_hit_with_weapon__msg(test_map):
    player = test_map.get_player()
    dagger = player.inventory.items.get('a')
    assert player.equipment.toggle_equip(dagger)

    a = actions.MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.hit_with_weapon(target)
    assert a.msg == f"The Player hits the Orc with a Dagger for {result}! "


def test_MeleeAction_hit_with_barehands__returns_dmg(test_map):
    player = test_map.get_player()
    assert not player.equipment.weapon

    a = actions.MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.hit_with_barehands(target)
    attack_max = player.fighter.attacks.die_sides
    assert result >= 1
    assert result <= attack_max


def test_MeleeAction_hit_with_barehands__msg(test_map):
    player = test_map.get_player()

    a = actions.MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.hit_with_barehands(target)
    assert a.msg == f"The Player hits the Orc for {result}! "


def test_MeleeAction_miss(test_map):
    player = test_map.get_player()
    a = actions.MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.miss(target)
    assert a.msg == f"The Player misses the Orc. "


def test_MovementAction_is_Action(test_map):
    player = test_map.get_player()
    a = actions.MovementAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_MovementAction_is_ActionWithDirection(test_map):
    player = test_map.get_player()
    a = actions.MovementAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.ActionWithDirection)


def test_MovementAction_init(test_map):
    player = test_map.get_player()
    a = actions.MovementAction(entity=player, dx=1, dy=-1)
    assert a.dx == 1
    assert a.dy == -1
    assert a.entity == player


def test_MovementAction_perform__success(test_map):
    player = test_map.get_player()
    a = actions.MovementAction(entity=player, dx=-1, dy=0)
    a.perform()
    assert player.x == 4
    assert player.y == 5


def test_MovementAction_perform__out_of_bounds__raises_Impossible(test_map):
    player = test_map.get_player()
    # Try to move out of the map bounds (we're at 5, 5)
    a = actions.MovementAction(entity=player, dx=1, dy=1)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_MovementAction_perform__blocked_by_wall__raises_Impossible(test_map):
    player = test_map.get_player()
    # Try to move into wall
    a = actions.MovementAction(entity=player, dx=-1, dy=-1)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_MovementAction_perform__blocked_by_actor__raises_Impossible(test_map):
    player = test_map.get_player()
    # Try to move into orc
    a = actions.MovementAction(entity=player, dx=0, dy=-1)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_PickupAction_is_Action(test_map):
    player = test_map.get_player()
    a = actions.PickupAction(entity=player)
    assert isinstance(a, actions.Action)


def test_PickupAction_init(test_map):
    player = test_map.get_player()
    a = actions.PickupAction(entity=player)
    assert a.entity == player


def test_PickupAction_perform__no_items__raises_Impossible(test_map):
    player = test_map.get_player()
    a = actions.PickupAction(entity=player)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_PickupAction_perform__single_item(test_map):
    player = test_map.get_player()
    # Put a scroll at player location
    factory.lightning_scroll.spawn(test_map, player.x, player.y)
    a = actions.PickupAction(entity=player)
    a.perform()
    assert a.msg == "You picked up the Lightning Scroll. "


@pytest.mark.skip(reason='Pickup for piles of items not yet supported')
def test_PickupAction_perform__multiple_items(test_map):
    player = test_map.get_player()
    # Put 2 scrolls at player location
    factory.lightning_scroll.spawn(test_map, player.x, player.y)
    factory.fireball_scroll.spawn(test_map, player.x, player.y)

    a = actions.PickupAction(entity=player)
    a.perform()

    # How do we know which item to pickup?
    assert a.msg == "You picked up the Lightning Scroll. "


def test_TakeStairsAction_is_Action(test_map):
    player = test_map.get_player()
    a = actions.TakeStairsAction(entity=player)
    assert isinstance(a, actions.Action)


def test_TakeStairsAction_init(test_map):
    player = test_map.get_player()
    a = actions.TakeStairsAction(entity=player)
    assert a.entity == player


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__player_removed_from_old_map(testengine):
    player = testengine.game_map.get_player()
    a = actions.TakeStairsAction(entity=player)
    a.perform


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__level_changed(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__player_added_to_new_map(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__player_on_upstair(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__msg(test_map):
    player = test_map.get_player()
    a = actions.TakeStairsAction(entity=player)
    assert a.msg == "You descend the stairs"


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__no_stairs__raises_Impossible(test_map):
    player = test_map.get_player()
    a = actions.TakeStairsAction(entity=player)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_WaitAction_is_Action(test_map):
    player = test_map.get_player()
    a = actions.WaitAction(entity=player)
    assert isinstance(a, actions.Action)


def test_WaitAction_init(test_map):
    player = test_map.get_player()
    a = actions.WaitAction(entity=player)
    assert a.entity == player


def test_WaitAction_init(test_map):
    player = test_map.get_player()
    a = actions.WaitAction(entity=player)
    assert a.perform() is None
    assert a.msg == ''


