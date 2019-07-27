from compiler.compilers import java_blockstate_compiler

init = {
	"block_format": "blockstate",
	"block_entity_format": "namespace-str-id",
	"block_entity_coord_format": "xyz-int",
	"entity_format": "namespace-str-id",
	"entity_coord_format": "Pos-list-float",
	"platform": "java",
	"version": [1, 13, 2]
}
compiler = java_blockstate_compiler.main
