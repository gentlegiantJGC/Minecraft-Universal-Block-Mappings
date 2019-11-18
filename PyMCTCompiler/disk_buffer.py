import os
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Union, Tuple, Set, TYPE_CHECKING

import PyMCTCompiler
if TYPE_CHECKING:
	from PyMCTCompiler.translation_functions import FunctionList
from PyMCTCompiler.helpers import log_to_file


def save_json_file(path, data):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w') as f:
		json.dump(data, f, indent=4)


class DiskBuffer:
	def __init__(self):
		self._specification: Dict[Tuple[str, str, str, str, str, str], dict] = {}
		self._translations: Dict[str, Dict[Tuple[str, str, str, str, str, str], 'FunctionList']] = {
			"to_universal": {},
			"from_universal": {}
		}

		# self._translations = {}

		# stores the primitive names converting to the hash of those primitive names (or a slight variant if a duplicate is found)
		self._nested_translations: Dict[Union[Tuple[str, ...], Tuple[Tuple[str, ...], ...]], str] = {}
		# stores the inverse of the above
		self._nested_translations_inverse: Set[str] = set()

		self._files_to_save: Dict[tuple, Union[list, dict]] = {}

	def add_specification(self, version_name: str, object_type: str, version_format: str, namespace: str, group_name: str, base_name: str, data: dict):
		"""add a specification file to the disk buffer to be saved at the end
		:param version_name: 'bedrock_1_13_0'
		:param object_type: 'block' or 'entity'
		:param version_format: 'numerical' or 'blockstate'
		:param namespace:
		:param group_name:
		:param base_name:
		:param data:
		:return:
		"""
		self.save_json_object(('versions', version_name, object_type, version_format, "specification", namespace, group_name, base_name), data)

	def has_specification(self, version_name: str, object_type: str, version_format: str, namespace: str, group_name: str, base_name: str) -> bool:
		return ('versions', version_name, object_type, version_format, "specification", namespace, group_name, base_name) in self._files_to_save

	def add_translation_to_universal(self, version_name: str, object_type: str, version_format: str, namespace: str, group_name: str, base_name: str, data: 'FunctionList'):
		"""add a translation file from version to universal format to the disk buffer to be saved at the end"""
		self._translations["to_universal"][(version_name, object_type, version_format, namespace, group_name, base_name)] = data
		
	def has_translation_to_universal(self, version_name: str, object_type: str, version_format: str, namespace: str, group_name: str, base_name: str) -> bool:
		return (version_name, object_type, version_format, namespace, group_name, base_name) in self._translations["to_universal"]

	def add_translation_from_universal(self, version_name: str, object_type: str, version_format: str, namespace: str, group_name: str, base_name: str, data: 'FunctionList'):
		"""add a translation file from universal to version format to the disk buffer to be saved at the end.
		If something already exists here it will be merged.
		:param version_name: 'bedrock_1_13_0'
		:param object_type: 'block' or 'entity'
		:param version_format: 'numerical' or 'blockstate'
		:param namespace:
		:param group_name:
		:param base_name:
		:param data:
		:return:
		"""
		if (version_name, object_type, version_format, namespace, group_name, base_name) in self._translations["from_universal"]:
			self._translations["from_universal"][(version_name, object_type, version_format, namespace, group_name, base_name)].extend(data, [])
		else:
			self._translations["from_universal"][(version_name, object_type, version_format, namespace, group_name, base_name)] = data

	def save_nested_translation(self, primitive_group: Union[Tuple[str, ...], Tuple[Tuple[str, ...], ...]], data: list):
		"""This method should only be used by internal code.
		Used at the end during the saving process to add a nested primitive file for saving."""
		key = self.nested_translation_key(primitive_group)
		if ('nested_translations', key) not in self._files_to_save:
			self.save_json_object(('nested_translations', key), data)

	def nested_translation_key(self, primitive_group: Tuple[Tuple[str, ...], ...]) -> str:
		"""Used to retrieve or create a key a nested primitive is stored under."""
		if primitive_group in self._nested_translations:
			return self._nested_translations[primitive_group]
		else:
			key = hash(primitive_group)
			while str(key) in self._nested_translations_inverse:
				# we have a duplicate hash
				key += 1

			self._nested_translations_inverse.add(str(key))
			self._nested_translations[primitive_group] = str(key)
			return str(key)

	def save_json_object(self, tuple_path: tuple, data: Union[dict, list]):
		assert isinstance(data, (dict, list))
		self._files_to_save[tuple_path] = data

	def save(self):
		log_to_file('Saving to disk')
		for direction in self._translations:
			for path, data in self._translations[direction].items():
				data.commit(None, [])  # validate the translation
				self.save_json_object(('versions',) + path[:3] + (direction,) + path[3:], data.save([]))  # add the file to the dictionary to be saved

		with ThreadPoolExecutor(max_workers=1000) as executor:
			for path, data in self._files_to_save.items():
				path = os.path.join(PyMCTCompiler.compiled_dir, *path) + '.json'
				executor.submit(save_json_file, path, data)


disk_buffer = DiskBuffer()
