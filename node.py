
from typing import Set, ClassVar, Optional
from block import Block


class Node:

    __next_id: ClassVar[int] = 0

    def __init__(self, mining_power: float, bandwidth: float) -> None:
        self.__mining_power = mining_power
        self.__bandwidth = bandwidth

        self.__known_headers: Set[Block] = set()
        self.__downloaded_blocks: Set[Block] = set()

        #set a unique id:
        self.__id = Node.__next_id
        Node.__next_id += 1

        #honest node behavior:
        self.__longest_header_tip: Optional[Block] = None
        self.__longest_known_chain: Optional[Block] = None

    def receive_header(self, block: Block) -> None:
        if not self.__longest_header_tip or self.__longest_header_tip.height < block.height:
            self.__longest_header_tip = block
            

    def mine_block(self) -> None:
        block = Block(self.__longest_known_chain)
        self.__longest_known_chain = block
        self.receive_header(block) 
