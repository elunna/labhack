import pytest
from components.component import Component
from components.material import MaterialComponent


def test_init__is_Component():
    m = MaterialComponent('PLASTIC', 'MELT')
    assert isinstance(m, Component)


def test_init__material():
    m = MaterialComponent('PLASTIC', 'MELT')
    assert m.material == 'PLASTIC'


def test_init__vulnerabilities__single_tuple():
    m = MaterialComponent('PLASTIC', 'MELT')
    assert m.erosion == {'MELT': 0}


def test_init__vulnerabilities__tuple():
    m = MaterialComponent('PLASTIC', 'MELT', 'BURN')
    assert m.erosion == {'MELT': 0, 'BURN': 0}


def test_init__invalid_material():
    with pytest.raises(ValueError):
        MaterialComponent('RUG', 'melt')


def test_init__invalid_vulnerabilities():
    with pytest.raises(ValueError):
        MaterialComponent('CLOTH', 'LAUGH')


def test_add_erosion__success_returns_True():
    m = MaterialComponent('PLASTIC', 'MELT')
    assert m.add_erosion("MELT")


def test_add_erosion__fail_returns_False():
    m = MaterialComponent('PLASTIC', 'MELT')
    assert m.add_erosion("ROT") is False


def test_add_erosion__0_to_1():
    m = MaterialComponent('PLASTIC', 'MELT')
    assert m.erosion['MELT'] == 0
    m.add_erosion("MELT")
    assert m.erosion['MELT'] == 1


def test_add_erosion__level_3__returns_False():
    m = MaterialComponent('PLASTIC', 'MELT')
    m.erosion['MELT'] = 3
    assert m.add_erosion("MELT") is False
    assert m.erosion['MELT'] == 3


def test_burn__burnable_returns_True():
    m = MaterialComponent('WOOD', 'BURN')
    assert m.burn()


def test_burn__burnable_calls_add_erosion(mocker):
    mocker.patch('components.material.MaterialComponent.add_erosion')
    m = MaterialComponent('WOOD', 'BURN')
    m.burn()
    m.add_erosion.assert_called_once()


def test_burn__nonburnable_returns_False():
    m = MaterialComponent('IRON', 'RUST')
    assert m.burn() is False


def test_rot__rottable_returns_True():
    m = MaterialComponent('WOOD', 'ROT')
    assert m.rot()


def test_rot__rottable_calls_add_erosion(mocker):
    mocker.patch('components.material.MaterialComponent.add_erosion')
    m = MaterialComponent('WOOD', 'ROT')
    m.rot()
    m.add_erosion.assert_called_once()


def test_rot__nonrottable_returns_False():
    m = MaterialComponent('IRON', 'RUST')
    assert m.rot() is False


def test_melt__meltable_returns_True():
    m = MaterialComponent('PLASTIC', 'MELT')
    assert m.melt()


def test_melt__meltable_calls_add_erosion(mocker):
    mocker.patch('components.material.MaterialComponent.add_erosion')
    m = MaterialComponent('PLASTIC', 'MELT')
    m.melt()
    m.add_erosion.assert_called_once()


def test_melt__nonmeltable_returns_False():
    m = MaterialComponent('WOOD', 'BURN')
    assert m.melt() is False


def test_rust__rustable_returns_True():
    m = MaterialComponent('IRON', 'RUST')
    assert m.rust()


def test_rust__rustable_calls_add_erosion(mocker):
    mocker.patch('components.material.MaterialComponent.add_erosion')
    m = MaterialComponent('IRON', 'RUST')
    m.rust()
    m.add_erosion.assert_called_once()


def test_rust__nonrustable_returns_False():
    m = MaterialComponent('WOOD', 'BURN')
    assert m.rust() is False


def test_corrode__corrodable_returns_True():
    m = MaterialComponent('IRON', 'RUST', 'CORRODE')
    assert m.corrode()


def test_corrode__corrodable_calls_add_erosion(mocker):
    mocker.patch('components.material.MaterialComponent.add_erosion')
    m = MaterialComponent('IRON', 'RUST')  # No corrode, means always calls add_erosion
    m.corrode()
    m.add_erosion.assert_called_once()


def test_corrode__noncorrodable_returns_False():
    m = MaterialComponent('WOOD', 'BURN')
    assert m.corrode() is False
