def default(namespace: str, block_name: str) -> dict:
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					"0": {
						"new_block": f"{namespace}:{block_name}"
					}
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"new_properties": {
					"block_data": "0"
				}
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{namespace}:{block_name}"
		},
		"blockstate_from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}"
			}
		}
	}


def liquid(namespace: str, block_name: str, flowing_: bool) -> dict:
	flowing_str = "true" if flowing_ else "false"
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{namespace}:{block_name}",
						"new_properties": {
							"level": {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}[data & 7],
							"falling": {0: "false", 8: "true"}[data & 8],
							"flowing": flowing_str
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"map_properties": {
					"flowing": {
						flowing_str: {
							"map_properties": {
								"falling": {
									falling: {
										"map_properties": {
											"level": {
												level: {
													"new_block": f"{namespace}:{'flowing_' if flowing_ else ''}{block_name}",
													"new_properties": {
														"block_data": str(data8 + data7)
													}
												} for data7, level in {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7"}.items()
											}
										}
									} for data8, falling in {0: "false", 8: "true"}.items()
								}
							}
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"level": [
					"0",
					"1",
					"2",
					"3",
					"4",
					"5",
					"6",
					"7"
				],
				"falling": [
					"false",
					"true"
				]
			},
			"defaults": {
				"level": "0",
				"falling": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{namespace}:{block_name}",
			"carry_properties": {
				"level": [
					"0",
					"1",
					"2",
					"3",
					"4",
					"5",
					"6",
					"7"
				],
				"falling": [
					"false",
					"true"
				]
			},
			"new_properties": {
				"flowing": flowing_str
			}
		},
		"blockstate_from_universal": {
			f"{namespace}:{block_name}": {
				"carry_properties": {
					"level": [
						"0",
						"1",
						"2",
						"3",
						"4",
						"5",
						"6",
						"7"
					],
					"falling": [
						"false",
						"true"
					]
				},
				"map_properties": {
					"flowing": {
						flowing_str: {
							"new_block": f"{namespace}:{'flowing_' if flowing_ else ''}{block_name}"
						}
					}
				}
			}
		}
	}


def leaves(namespace: str, block_name: str, platform: str, to_namespace: str = "minecraft", to_block_name: str = "leaves") -> dict:
	if platform == 'bedrock':
		property8 = "decayable"
		property4 = "check_decay"
	elif platform == 'java':
		property8 = "check_decay"
		property4 = "decayable"
	else:
		raise Exception(f'Platform "{platform}" is not known')

	if block_name == "leaves":
		material_pallet = {0: "oak", 1: "spruce", 2: "birch", 3: "jungle"}
	elif block_name == "leaves2":
		material_pallet = {0: "acacia", 1: "dark_oak"}
	else:
		raise Exception(f'Block name "{block_name}" is not known')

	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{to_namespace}:{to_block_name}",
						"new_properties": {
							"material": material_pallet[data & 3],
							property4: {0: "true", 4: "false"}[data & 4],
							property8: {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 3 in material_pallet
				}
			}
		},
		"from_universal": {
			f"{to_namespace}:{to_block_name}": {
				"map_properties": {
					property8: {
						val8: {
							"map_properties": {
								property4: {
									val4: {
										"map_properties": {
											"material": {
												material: {
													"new_block": f"{namespace}:{block_name}",
													"new_properties": {
														"block_data": str(data3 + data4 + data8)
													}
												} for data3, material in material_pallet.items()
											}
										}
									} for data4, val4 in {0: "true", 4: "false"}.items()
								}
							}
						} for data8, val8 in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": list(material_pallet.values()),
				"decayable": [
					"true",
					"false"
				],
				"check_decay": [
					"true",
					"false"
				]
			},
			"defaults": {
				"material": material_pallet[0],
				"decayable": "true",
				"check_decay": "true"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{to_namespace}:{to_block_name}",
			"carry_properties": {
				"material": list(material_pallet.values()),
				"decayable": [
					"true",
					"false"
				],
				"check_decay": [
					"true",
					"false"
				]
			}
		},
		"blockstate_from_universal": {
			f"{to_namespace}:{to_block_name}": {
				"carry_properties": {
					"material": list(material_pallet.values()),
					"decayable": [
						"true",
						"false"
					],
					"check_decay": [
						"true",
						"false"
					]
				},
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{namespace}:{block_name}"
						} for material in material_pallet.values()
					}
				}
			}
		}
	}


def log(namespace: str, block_name: str, to_namespace: str = "minecraft", to_block_name: str = "log") -> dict:
	if block_name == "log":
		material_pallet = {0: "oak", 1: "spruce", 2: "birch", 3: "jungle"}
	elif block_name == "log2":
		material_pallet = {0: "acacia", 1: "dark_oak"}
	else:
		raise Exception(f'Block name "{block_name}" is not known')

	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{to_namespace}:{to_block_name}",
						"new_properties": {
							"material": material_pallet[data & 3],
							"axis": {0: "y", 4: "x", 8: "z"}[data & 12],
						}
					} if data <= 11 else {
						"new_block": "minecraft:wood",
						"new_properties": {
							"material": material_pallet[data & 3]
						}
					} for data in range(16) if data & 3 in material_pallet
				}
			}
		},
		"from_universal": {
			f"{to_namespace}:{to_block_name}": {
				"map_properties": {
					"axis": {
						axis: {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{namespace}:{block_name}",
										"new_properties": {
											"block_data": str(data12 + data3)
										}
									} for data3, material in material_pallet.items()
								}
							}
						} for data12, axis in {0: "y", 4: "x", 8: "z"}.items()
					}
				}
			},
			"minecraft:wood": {
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{namespace}:{block_name}",
							"new_properties": {
								"block_data": str(12 + data3)
							}
						} for data3, material in material_pallet.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": list(material_pallet.values()),
				"axis": [
					"x",
					"y",
					"z",
					"all"
				]
			},
			"defaults": {
				"material": material_pallet[0],
				"axis": "y"
			}
		},
		"blockstate_to_universal": {
			"carry_properties": {
				"material": list(material_pallet.values()),
				"axis": [
					"x",
					"y",
					"z"
				]
			},
			"map_properties": {
				"axis": {
					"x": {
						"new_block": "minecraft:log"
					},
					"y": {
						"new_block": "minecraft:log"
					},
					"z": {
						"new_block": "minecraft:log"
					},
					"all": {
						"new_block": "minecraft:wood",
						"new_properties": {
							"axis": "y"
						}
					}
				}
			}
		},
		"blockstate_from_universal": {
			"minecraft:log": {
				"carry_properties": {
					"material": list(material_pallet.values()),
					"axis": [
						"x",
						"y",
						"z"
					]
				},
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{namespace}:{block_name}"
						} for material in material_pallet.values()
					}
				}
			},
			"minecraft:wood": {
				"carry_properties": {
					"material": list(material_pallet.values())
				},
				"map_properties": {
					"material": {
						material: {
							"new_block": f"{namespace}:{block_name}"
						} for material in material_pallet.values()
					}
				}
			}
		}
	}


def dispenser(namespace: str, block_name: str) -> dict:
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{namespace}:{block_name}",
						"new_properties": {
							"facing": {0: "down", 1: "up", 2: "north", 3: "south", 4: "west", 5: "east"}[data & 7],
							"triggered": {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 7 <= 5
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"map_properties": {
					"triggered": {
						triggered: {
							"map_properties": {
								"facing": {
									facing: {
										"new_block": f"{namespace}:{block_name}",
										"new_properties": {
											"block_data": str(data8 + data7)
										}
									} for data7, facing in {0: "down", 1: "up", 2: "north", 3: "south", 4: "west", 5: "east"}.items()
								}
							}
						} for data8, triggered in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				],
				"triggered": [
					"true",
					"false"
				]
			},
			"defaults": {
				"facing": "north",
				"triggered": "false"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{namespace}:{block_name}",
			"carry_properties": {
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				],
				"triggered": [
					"true",
					"false"
				]
			}
		},
		"blockstate_from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"carry_properties": {
					"facing": [
						"north",
						"east",
						"south",
						"west",
						"up",
						"down"
					],
					"triggered": [
						"true",
						"false"
					]
				}
			}
		}
	}


def sandstone(namespace: str, block_name: str, level: int = 1) -> dict:
	variants = {var: {0: "normal", 1: "chiseled", 2: "cut", 3: "smooth"}[var] for var in range(level)}
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{namespace}:{block_name}",
						"new_properties": {
							"variant": var
						}
					} for data, var in variants.items()
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"map_properties": {
					"variant": {
						variant: {
							"new_block": f"{namespace}:{block_name}",
							"new_properties": {
								"block_data": str(data)
							}
						} for data, variant in variants.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"variant": list(variants.values())
			},
			"defaults": {
				"variant": variants[0]
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{namespace}:{block_name}",
			"carry_properties": {
				"variant": list(variants.values())
			}
		},
		"blockstate_from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"carry_properties": {
					"variant": list(variants.values())
				}
			}
		}
	}


def rail(namespace: str, block_name: str) -> dict:
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{namespace}:{block_name}",
						"new_properties": {
							"shape": {
								0: "north_south", 1: "east_west", 2: "ascending_east", 3: "ascending_west", 4: "ascending_north", 5: "ascending_south", 6: "south_east", 7: "south_west", 8: "north_west", 9: "north_east"
							}[data]
						}
					} for data in range(10)
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"map_properties": {
					"shape": {
						shape: {
							"new_block": f"{namespace}:{block_name}",
							"new_properties": {
								"block_data": str(data)
							}
						} for data, shape in {0: "north_south", 1: "east_west", 2: "ascending_east", 3: "ascending_west", 4: "ascending_north", 5: "ascending_south", 6: "south_east", 7: "south_west", 8: "north_west", 9: "north_east"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"shape": [
					"north_south",
					"east_west",
					"ascending_east",
					"ascending_west",
					"ascending_north",
					"ascending_south",
					"south_east",
					"south_west",
					"north_west",
					"north_east"
				]
			},
			"defaults": {
				"shape": "north_south"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{namespace}:{block_name}",
			"carry_properties": {
				"shape": [
					"north_south",
					"east_west",
					"ascending_east",
					"ascending_west",
					"ascending_north",
					"ascending_south",
					"south_east",
					"south_west",
					"north_west",
					"north_east"
				]
			}
		},
		"blockstate_from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"carry_properties": {
					"shape": [
						"north_south",
						"east_west",
						"ascending_east",
						"ascending_west",
						"ascending_north",
						"ascending_south",
						"south_east",
						"south_west",
						"north_west",
						"north_east"
					]
				}
			}
		}
	}


def rail2(namespace: str, block_name: str) -> dict:
	return {
		"to_universal": {
			"map_properties": {
				"block_data": {
					str(data): {
						"new_block": f"{namespace}:{block_name}",
						"new_properties": {
							"shape": {
								0: "north_south", 1: "east_west", 2: "ascending_east", 3: "ascending_west", 4: "ascending_north", 5: "ascending_south"
							}[data & 5],
							"powered": {0: "false", 8: "true"}[data & 8]
						}
					} for data in range(16) if data & 7 <= 5
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"map_properties": {
					"powered": {
						powered: {
							"map_properties": {
								"shape": {
									shape: {
										"new_block": f"{namespace}:{block_name}",
										"new_properties": {
											"block_data": str(data8 + data7)
										}
									} for data7, shape in {0: "north_south", 1: "east_west", 2: "ascending_east", 3: "ascending_west", 4: "ascending_north", 5: "ascending_south"}.items()
								}
							}
						} for data8, powered in {0: "false", 8: "true"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"powered": [
					"true",
					"false"
				],
				"shape": [
					"north_south",
					"east_west",
					"ascending_east",
					"ascending_west",
					"ascending_north",
					"ascending_south"
				]
			},
			"defaults": {
				"powered": "false",
				"shape": "north_south"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{namespace}:{block_name}",
			"carry_properties": {
				"powered": [
					"true",
					"false"
				],
				"shape": [
					"north_south",
					"east_west",
					"ascending_east",
					"ascending_west",
					"ascending_north",
					"ascending_south"
				]
			}
		},
		"blockstate_from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"carry_properties": {
					"powered": [
						"true",
						"false"
					],
					"shape": [
						"north_south",
						"east_west",
						"ascending_east",
						"ascending_west",
						"ascending_north",
						"ascending_south"
					]
				}
			}
		}
	}


def bed_color(platform: str) -> dict:
	return {
		"specification": {
			"properties": {
				"block_data": [str(data) for data in range(16)]
			},
			"defaults": {
				"block_data": "0"
			},
			"nbt": {
				"color": {
					"name": "color",
					"type": {"bedrock": "byte", "java": "int"}[platform],
					"options": [str(data) for data in range(16)],
					"default": "14"
				}
			},
		},
		"to_universal": {
			"new_block": "minecraft:bed",
			"map_properties": {
				"block_data": {
					str(data): {
						"new_properties": {
							"facing": {0: "south", 1: "west", 2: "north", 3: "east"}[data & 3],
							"occupied": {0: "false", 4: "true"}[data & 4],
							"part": {0: "foot", 8: "head"}[data & 8]
						}
					} for data in range(16)
				}
			},
			"map_nbt": {
				"color": {
					num: {
						"new_properties": {
							"color": color
						}
					} for num, color in {
						"0": "white",
						"1": "orange",
						"2": "magenta",
						"3": "light_blue",
						"4": "yellow",
						"5": "lime",
						"6": "pink",
						"7": "gray",
						"8": "light_gray",
						"9": "cyan",
						"10": "purple",
						"11": "blue",
						"12": "brown",
						"13": "green",
						"14": "red",
						"15": "black"
					}.items()
				}
			}
		},
		"from_universal": {
			"minecraft:bed": {
				"new_block": "minecraft:bed",
				"map_properties": {
					"part": {
						part: {
							"map_properties": {
								"occupied": {
									occupied: {
										"map_properties": {
											"facing": {
												facing: {
													"new_properties": {
														"block_data": str(data8 + data4 + data3)
													}
												} for data3, facing in {0: "south", 1: "west", 2: "north", 3: "east"}.items()
											}
										}
									} for data4, occupied in {0: "false", 4: "true"}.items()
								}
							}
						} for data8, part in {0: "foot", 8: "head"}.items()
					},
					"color": {
						color: {
							"new_nbt": {
								"color": num
							}
						} for num, color in {
							"0": "white",
							"1": "orange",
							"2": "magenta",
							"3": "light_blue",
							"4": "yellow",
							"5": "lime",
							"6": "pink",
							"7": "gray",
							"8": "light_gray",
							"9": "cyan",
							"10": "purple",
							"11": "blue",
							"12": "brown",
							"13": "green",
							"14": "red",
							"15": "black"
						}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"east",
					"north",
					"south",
					"west"
				],
				"occupied": [
					"true",
					"false"
				],
				"part": [
					"foot",
					"head"
				],
				"color": [
					"white",
					"orange",
					"magenta",
					"light_blue",
					"yellow",
					"lime",
					"pink",
					"gray",
					"light_gray",
					"cyan",
					"purple",
					"blue",
					"brown",
					"green",
					"red",
					"black"
				]
			},
			"defaults": {
				"facing": "north",
				"occupied": "false",
				"part": "foot",
				"color": "red"
			}
		},
		"blockstate_to_universal": {
			"new_block": "minecraft:bed",
			"carry_properties": {
				"facing": [
					"east",
					"north",
					"south",
					"west"
				],
				"occupied": [
					"true",
					"false"
				],
				"part": [
					"foot",
					"head"
				],
				"color": [
					"white",
					"orange",
					"magenta",
					"light_blue",
					"yellow",
					"lime",
					"pink",
					"gray",
					"light_gray",
					"cyan",
					"purple",
					"blue",
					"brown",
					"green",
					"red",
					"black"
				]
			}
		},
		"blockstate_from_universal": {
			"minecraft:bed": {
				"new_block": "minecraft:bed",
				"carry_properties": {
					"facing": [
						"east",
						"north",
						"south",
						"west"
					],
					"occupied": [
						"true",
						"false"
					],
					"part": [
						"foot",
						"head"
					],
					"color": [
						"white",
						"orange",
						"magenta",
						"light_blue",
						"yellow",
						"lime",
						"pink",
						"gray",
						"light_gray",
						"cyan",
						"purple",
						"blue",
						"brown",
						"green",
						"red",
						"black"
					]
				}
			}
		}
	}


def piston_bedrock(namespace: str, block_name: str) -> dict:
	return {
		"comment": "There is also a tile entity here that contains more data",
		"to_universal": {
			"new_block": f"{namespace}:{block_name}",
			"map_properties": {
				"block_data": {
					str(data): {
						"new_properties": {
							"facing": {0: "down", 1: "up", 2: "south", 3: "north", 4: "east", 5: "west"}[data]
						}
					} for data in range(6)
				}
			}
		},
		"from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"map_properties": {
					"facing": {
						facing: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, facing in {0: "down", 1: "up", 2: "south", 3: "north", 4: "east", 5: "west"}.items()
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				]
			},
			"defaults": {
				"facing": "north"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{namespace}:{block_name}",
			"carry_properties": {
				"facing": [
					"north",
					"east",
					"south",
					"west",
					"up",
					"down"
				]
			}
		},
		"blockstate_from_universal": {
			f"{namespace}:{block_name}": {
				"new_block": f"{namespace}:{block_name}",
				"carry_properties": {
					"facing": [
						"north",
						"east",
						"south",
						"west",
						"up",
						"down"
					]
				}
			}
		}
	}


def colour(input_namespace: str, input_block_name: str, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"map_properties": {
				"block_data": {
					str(data): {
						"new_properties": {
							"color": ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"][data]
						}
					} for data in range(16)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"map_properties": {
					"color": {
						color: {
							"new_properties": {
								"block_data": str(data)
							}
						} for data, color in enumerate(["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"])
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"color": [
					"white",
					"orange",
					"magenta",
					"light_blue",
					"yellow",
					"lime",
					"pink",
					"gray",
					"light_gray",
					"cyan",
					"purple",
					"blue",
					"brown",
					"green",
					"red",
					"black"
				]
			},
			"defaults": {
				"color": "white"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"color": [
					"white",
					"orange",
					"magenta",
					"light_blue",
					"yellow",
					"lime",
					"pink",
					"gray",
					"light_gray",
					"cyan",
					"purple",
					"blue",
					"brown",
					"green",
					"red",
					"black"
				]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"new_block": f"{input_namespace}:{input_block_name}",
				"carry_properties": {
					"color": [
						"white",
						"orange",
						"magenta",
						"light_blue",
						"yellow",
						"lime",
						"pink",
						"gray",
						"light_gray",
						"cyan",
						"purple",
						"blue",
						"brown",
						"green",
						"red",
						"black"
					]
				}
			}
		}
	}


def double_slab(input_namespace: str, input_block_name: str, block_types: list, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"map_properties": {
				"block_data": {
					str(data): {
						"new_properties": {
							"material": material,
							"type": "double"
						}
					} for data, material in enumerate(block_types)
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"type": {
						"double": {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"block_data": str(data)
										}
									} for data, material in enumerate(block_types)
								}
							}
						}
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": block_types
			},
			"defaults": {
				"material": block_types[0]
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"material": block_types
			},
			"new_properties": {
				"type": "double"
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"type": {
						"double": {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"material": material
										}
									} for material in block_types
								}
							}
						}
					}
				}
			}
		}
	}


def slab(input_namespace: str, input_block_name: str, block_types: list, universal_namespace: str = None, universal_block_name: str = None) -> dict:
	if universal_namespace is None:
		universal_namespace = input_namespace
	if universal_block_name is None:
		universal_block_name = input_block_name
	return {
		"to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"map_properties": {
				"block_data": {
					str(data): {
						"new_properties": {
							"material": block,
							"type": position
						}
					} for data, (block, position) in {data + data8 * 8: [material, position] for data8, position in enumerate(["bottom", "top"]) for data, material in enumerate(block_types)}.items()
				}
			}
		},
		"from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"type": {
						position: {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"block_data": str(data + data8 * 8)
										}
									} for data, material in enumerate(block_types)
								}
							}
						} for data8, position in enumerate(["bottom", "top"])
					}
				}
			}
		},
		"blockstate_specification": {
			"properties": {
				"material": block_types,
				"type": ["bottom", "top"]
			},
			"defaults": {
				"material": block_types[0],
				"type": "bottom"
			}
		},
		"blockstate_to_universal": {
			"new_block": f"{universal_namespace}:{universal_block_name}",
			"carry_properties": {
				"material": block_types,
				"type": ["bottom", "top"]
			}
		},
		"blockstate_from_universal": {
			f"{universal_namespace}:{universal_block_name}": {
				"map_properties": {
					"type": {
						position: {
							"map_properties": {
								"material": {
									material: {
										"new_block": f"{input_namespace}:{input_block_name}",
										"new_properties": {
											"material": material,
											"type": position
										}
									} for material in block_types
								}
							}
						} for position in ["bottom", "top"]
					}
				}
			}
		}
	}
