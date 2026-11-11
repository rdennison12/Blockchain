import time

import pytest

from blockchain.backend.blockchain.block import Block, GENESIS_DATA
from blockchain.backend.config import MINE_RATE, SECONDS
from blockchain.backend.utils.hex_to_binary import hex_to_binary


def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_quickly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty + 1


def test_slowly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1():
    last_block = Block(
        time.time_ns(),
        "test_last_hash",
        "test_hash",
        "test_data",
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')
    assert mined_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis()


@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test_data')


def test_is_block_valid(last_block, block):
    Block.is_block_valid(last_block, block)


def test_is_block_valid_bad_last_hash(last_block, block):
    block.last_hash = 'test_data'

    with pytest.raises(Exception, match='must have the proper last_hash reference'):
        Block.is_block_valid(last_block, block)


#
def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = 'fff'
    with pytest.raises(Exception, match='must meet the proof of work requirement'):
        Block.is_block_valid(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block, block):
    jumped_difficulty = 100
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}111abc'

    with pytest.raises(Exception, match='difficulty must only adjust by 1'):
        Block.is_block_valid(last_block, block)


def test_is_block_valid_bad_block_hash(last_block, block):
    block.hash = '0000000000000000bbbabc'

    with pytest.raises(Exception, match='block hash must be correct'):
        Block.is_block_valid(last_block, block)
