from PyMCTCompiler.compilers import nbt_blockstate_compiler

init = {
	"block_format": "nbt-blockstate",
	"block_entity_format": "str-id",
	"block_entity_coord_format": "xyz-int",
	"entity_format": "namespace-str-id",
	"entity_coord_format": "Pos-list-float",
	"platform": "bedrock",
	"version": [1, 13, 0]
}
compiler = nbt_blockstate_compiler.main

