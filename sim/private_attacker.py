
from .block import Block
from .node import Node
import sim.network as network


class PrivateAttacker(Node):
    # this attacker differs from the dumb attacker in that it does not broadcast the block it mines
    # and that it resets its mining target if the honest chain is longer than its own

    def __init__(self, genesis: Block, mining_rate: float, network: network.Network) -> None:
        super().__init__(genesis, mining_rate, bandwidth=0, header_delay=0, network=network)
        self._tip = genesis

    def mine_block(self) -> Block:
        block = super().mine_block()
        self._mining_target = block
        self._tip = block
        return block

    def receive_header(self, block: Block) -> None:
        super().receive_header(block)
        if block.height > self._tip.height:
            self._tip = block
        self._mining_target = self._tip

    def download_complete(self, block: Block) -> None:
        super().download_complete(block)
        self._mining_target = self._tip

    def download_interrupted(self, block: Block, fraction_downloaded: float) -> None:
        super().download_interrupted(block, fraction_downloaded)
        self._mining_target = self._tip
