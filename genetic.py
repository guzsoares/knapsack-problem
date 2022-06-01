from typing import list
from random import choices

genetics = List[int]
pop = List[genetics]
Things = namedtuple('Thing' , [ 'name' , 'value', 'weight' ])

def generate_genetics(lenght):
	return choices([0,1], k = lenght)

def generate_pop(size, genetics_len):
	return [generate_genetics(genetics_len) for _ in range(size)]

def fitness(genetics, things, weight_max):
	if len(genetics) != len(things):
		error = "Genetics and things must be the same lenght!"
		print(error)
		return -1
	weight = 0
	fitness_level = 0

	for i, thing in enumerate(things):
		if genome[i] == 1:
			
			weight += thing.weight
			fitness_level += thing.value


		if weight > weight_max:
			return 0

	return fitness_level