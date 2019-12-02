from PyMCTCompiler.primitives.scripts.nbt import NBTRemapHelper, EmptyNBT, merge
from .common import java_custom_name, java_items_27, java_str_lock, java_loot_table, \
    bedrock_items_27, bedrock_is_movable

"""
Default
J113    "minecraft:chest"		"{Items: [], Lock: \"\"}"

B113	"Chest"		"{Findable: 0b, Items: [], isMovable: 1b}"


Trapped Default
J113    "minecraft:trapped_chest"		"{Items: [], Lock: \"\"}"
"""

_B113 = NBTRemapHelper(
    [
        (
            ("Findable", "byte", []),
            ("Findable", "byte", [("utags", "compound")])
        )
    ],
    "{Findable: 0b}"
)

j113 = merge(
    [EmptyNBT('minecraft:chest'), java_custom_name, java_items_27, java_str_lock, java_loot_table],
    ['universal_minecraft:chest']
)

trapped_j113 = merge(
    [EmptyNBT('minecraft:trapped_chest'), java_custom_name, java_items_27, java_str_lock, java_loot_table],
    ['universal_minecraft:trapped_chest']
)

b113 = merge(
    [EmptyNBT('minecraft:chest'), _B113, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:chest']
)

trapped_b113 = merge(
    [EmptyNBT('minecraft:chest'), _B113, bedrock_items_27, bedrock_is_movable],
    ['universal_minecraft:trapped_chest']
)