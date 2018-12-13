import json


def read(input_blockstate: dict, mappings: dict, output_dir):
	"""
	A demonstration function on how to read the json files to convert into or out of the numerical format
	You should implement something along these lines into you own code if you want to read them.

	:param input_blockstate: the blockstate put into the converter eg {"block_name": "minecraft:log", "properties": {"block_data": "0"}}
	:param mappings: the mapping file for that block
	:param output_dir: The directory where the specification files are found for the format being converted to (used to load default properties)
	:return: The conerterd blockstate
	"""
	
	output_blockstate = {"block_name": None, "properties": {}}
	if "new_block" in mappings:
		if isinstance(mappings["new_block"], str):
			output_blockstate["block_name"] = mappings["new_block"]
			namespace, block_name = output_blockstate["block_name"].split(':')
			with open(f'{output_dir}/{namespace}/vanilla/{block_name}.json') as f:
				output_blockstate["properties"] = json.load(f).get("defaults", {})
		else:
			raise Exception(f'Expected string for new_block but got {type(mappings["new_block"])}')

	if "map_properties" in mappings:
		for key in mappings["map_properties"]:
			if key in input_blockstate["properties"]:
				val = input_blockstate["properties"][key]
				if val in mappings["map_properties"][key]:
					temp_blockstate = read(input_blockstate, mappings["map_properties"][key][val], output_dir)
					if temp_blockstate["block_name"] is not None:
						output_blockstate["block_name"] = temp_blockstate["block_name"]
					for key2, val2 in temp_blockstate["properties"].items():
						output_blockstate["properties"][key2] = val2
				else:
					raise Exception(f'Value "{val}" for property "{key}" is not present in the mappings')
			else:
				raise Exception(f'Property "{key}" is not present in the input blockstate')

	if "new_properties" in mappings:
		for key, val in mappings["new_properties"].items():
			output_blockstate["properties"][key] = val

	if "carry_properties" in mappings:
		for key in mappings["carry_properties"]:
			if key in input_blockstate["properties"]:
				val = input_blockstate["properties"][key]
				if val in mappings["carry_properties"][key]:
					output_blockstate["properties"][key] = val
			else:
				raise Exception(f'Property "{key}" is not present in the input blockstate')

	return output_blockstate


if __name__ == "__main__":
	for data in range(16):
		print(data, read(
			{"block_name": "minecraft:log", "properties": {"block_data": str(data)}},
			json.load(open('../Versions/java_1.12.2/numerical/minecraft/vanilla/to_universal/log.json')),
			'../Versions/Universal'
		))
