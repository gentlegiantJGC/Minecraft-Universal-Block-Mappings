from typing import Union, Tuple
from .helpers.objects import Block, BlockEntity, Entity
from .data_version_handler import SubVersion


def convert(level, object_input: Union[Block, Entity], input_spec: dict, mappings: dict, output_version: SubVersion, location: Tuple[int, int, int] = None) -> Tuple[Union[Block, Entity], Union[BlockEntity, None], bool, bool]:
	"""
		A demonstration function on how to read the json files to convert into or out of the numerical block_format
		You should implement something along these lines into you own code if you want to read them.

		:param level: a view into the level to access additional data
		:param object_input: the Block or Entity object to be converted
		:param input_spec: the specification for the object_input from the input block_format
		:param mappings: the mapping file for the input_object
		:param output_version: A way for the function to look at the specification being converted to. (used to load default properties)
		:param location: (x, y, z) only used for Blocks if data beyond the object_input is needed
		:return: output, extra_output, extra_needed, cacheable
			extra_needed: a bool to specify if more data is needed beyond the object_input
			cacheable: a bool to specify if the result can be cached to reduce future processing
			Block, None, bool, bool
			Block, BlockEntity, bool, bool
			Entity, None, bool, bool
	"""

	extra_input = None

	if isinstance(object_input, Block):
		if 'nbt' in input_spec and location is not None:
			# TODO: create blockentity from the nbt spec
			extra_input = BlockEntity()
	# TODO: overwrite with the data loaded from the world if present

	elif isinstance(object_input, Entity):
		raise NotImplemented

	# TODO: rework the NBT system
	# if location is None:
	# 	return object_input, None, True
	# else:
	# 	nbt = get_nbt(level, location)
	# 	input_blockstate['nbt'] = {}
	# 	for key in input_spec['nbt']:
	# 		_nbt = nbt
	# 		path = input_spec['nbt'][key].get('path', []) + [input_spec['nbt'][key]['name'], input_spec['nbt'][key]['type']]
	# 		try:
	# 			assert _nbt.__class__.__name__ == 'TAG_Compound'
	# 			for path_key, dtype in path:
	# 				_nbt = _nbt[path_key]
	# 				assert _nbt.__class__.__name__ == {
	# 					'compound': 'TAG_Compound',
	# 					'list': 'TAG_List',
	# 					'byte': 'TAG_Byte',
	# 					'short': 'TAG_Short',
	# 					'int': 'TAG_Int',
	# 					'long': 'TAG_Long',
	# 					'float': 'TAG_Float',
	# 					'double': 'TAG_Double',
	# 					'string': 'TAG_String'
	# 				}[dtype]
	# 			input_blockstate['nbt'][key] = str(_nbt.value)
	# 		except:
	# 			input_blockstate['nbt'][key] = input_spec['nbt'][key]['default']

	if isinstance(object_input, Block):
		block_input = object_input
		if extra_input is not None:
			assert isinstance(extra_input, BlockEntity)
			nbt_input = extra_input
		else:
			nbt_input = None
	elif isinstance(object_input, Entity):
		block_input = None
		nbt_input = object_input
		raise NotImplemented
	else:
		raise Exception

	block_output, nbt_output, new, extra_needed, cacheable = _convert(level, block_input, nbt_input, mappings, output_version, location)
	if isinstance(block_output, dict):
		properties = block_output['properties']
		for key, val in new['properties'].items():
			properties[key] = val
		namespace, base_name = block_output['block_name'].split(':', 1)
		output = Block(None, namespace, base_name, properties)
		extra_output = None
		if extra_input is not None:
			assert isinstance(nbt_output, dict)
	# TODO: merge new['nbt'] into nbt_output and convert to a block entity

	elif block_output is None:
		assert isinstance(nbt_output, dict)
		# TODO: merge new['nbt'] into nbt_output and convert to an entity
		output, extra_output = nbt_output, None
		raise NotImplemented
	else:
		raise Exception
	return output, extra_output, extra_needed, cacheable


def _convert(level, block_input: Union[Block, None], nbt_input: Union[Entity, BlockEntity], mappings: dict, output_version: SubVersion, location: Tuple[int, int, int] = None) -> Tuple[Union[dict, None], Union[dict, None], dict, bool, bool]:
	block_output = None
	nbt_output = None
	new = {'properties': {}, 'nbt': {}}  # There could be multiple 'new_block' functions in the mappings so new properties are put in here and merged at the very end
	extra_needed = False  # used to determine if extra data is required (and thus to do block by block)
	cacheable = True
	if 'new_block' in mappings:
		assert isinstance(mappings['new_block'], str)
		namespace, block_name = mappings['new_block'].split(':', 1)
		spec = output_version.get_specification('block', namespace, block_name)
		block_output = {
			'block_name': mappings['new_block'],
			'properties': spec.get('defaults', {})
		}
		if 'nbt' in spec:
			pass
	# TODO: implement NBT

	if 'new_properties' in mappings:
		for key, val in mappings['new_properties'].items():
			new['properties'][key] = val

	if 'new_nbt' in mappings:
		# TODO: rework for the new NBT system
		for key, val in mappings['new_nbt'].items():
			new['nbt'][key] = val

	if 'carry_properties' in mappings:
		assert isinstance(block_input, Block), 'The block input is not a block'
		for key in mappings['carry_properties']:
			if key in block_input.properties:
				val = block_input.properties[key]
				if str(val) in mappings['carry_properties'][key]:
					new['properties'][key] = val

	if 'multiblock' in mappings:
		cacheable = False
		if location is None:
			extra_needed = True
	# TODO: multiblock code
	# else:
	# 	if 'multiblock' is a dictionary:
	# 		get the block at 'location' in the input format
	# 		call self._convert on this new blockstate
	# 	elif 'multiblock' is a list:
	# 		do the above but on every dictionary in the list

	if 'map_properties' in mappings:
		assert isinstance(block_input, Block), 'The block input is not a block'
		for key in mappings['map_properties']:
			if key in block_input.properties:
				val = block_input.properties[key]
				if val in mappings['map_properties'][key]:
					block_output_, nbt_output_, new_, extra_needed_, cacheable_ = _convert(level, block_input, nbt_input, mappings['map_properties'][key][val], output_version, location)
					if cacheable and not cacheable_:
						cacheable = False
					if not extra_needed and extra_needed_:
						extra_needed = True
					if isinstance(block_output_, dict):
						block_output = block_output_
					if isinstance(nbt_output_, dict):
						nbt_output = nbt_output_
					for key2, val2 in new_['properties'].items():
						new['properties'][key2] = val2
			# TODO: carry over nbt

	if 'map_block_name' in mappings:
		assert isinstance(block_input, Block)
		pass
	# TODO: map block name code

	if 'map_nbt' in mappings:
		cacheable = False
		if location is None:
			extra_needed = True
		else:
			pass
	# TODO: map nbt code

	return block_output, nbt_output, new, extra_needed, cacheable
