from typing import List, Optional, Callable, Tuple
from random import choices, randint, randrange, random
from collections import namedtuple
from functools import partial
import time

genetics = List[int]
Pop = List[genetics]
FitnessFunc = Callable[[genetics], int]
PopulateFunc = Callable[[] , Pop]
SelectionFunc = Callable[[Pop, FitnessFunc], Tuple[genetics, genetics]]
CrossoverFunc = Callable[[genetics,genetics], Tuple[genetics,genetics]]
MutationFunc = Callable[[genetics], genetics]
Things = namedtuple('Thing' , [ 'name' , 'value', 'weight' ])

things = [
	Things('Notebook', 500, 2200),
	Things('Headphones', 150, 160),
	Things('Dog', 600, 2100),
	Things('Wallet', 400, 150),
	Things('Phone', 450, 300),
	Things('Clothes', 200, 150),
	Things('Moisturizer', 300, 100),
	Things('Sunscreen', 500, 200),
	Things('Glasses', 300, 100),
	Things('Card', 200, 50),
	Things('Esquenta', 500, 105),
	Things('Nintendo', 1000, 300),
	Things('Casaco', 500, 500),
	Things('Computador', 700,400),
	Things('Tenis', 600, 100),
	Things('iPad', 300, 300),
	Things('Book', 150, 500),
	Things('Jenga', 200, 350)
]

def generate_genetics(lenght: int) -> genetics:
	return choices([0,1], k = lenght)

def generate_pop(size: int, genetics_len: int) -> Pop:
	return [generate_genetics(genetics_len) for _ in range(size)]

def fitness(genetics: genetics, things: [Things], weight_max: int) -> int:
	if len(genetics) != len(things):
		error = "Genetics and things must be the same length!"
		print(error)
		return -1
	weight = 0
	fitness_level = 0

	for i, thing in enumerate(things):
		if genetics[i] == 1:
			
			weight += thing.weight
			fitness_level += thing.value


		if weight > weight_max:
			return 0

	return fitness_level

def select_pair(pop: Pop, fitness_func: FitnessFunc):
	return choices(
		population=pop,
		weights=[fitness_func(genetics) for genetics in pop],
		k=2
	)

def cross_gens(a: genetics,b: genetics) -> Tuple[genetics,genetics]:
	if len(a) != len(b):
		error = "Genetics must have the same length"
		print(error)
		return -1

	length = len(a)
	if length < 2:
		return a,b

	p = randint(1 , length - 1)
	return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genetics: genetics, num: int = 1, probability: float = 0.5) -> genetics:
	for _ in range(num):
		index = randrange(len(genetics))
		if (random() > probability):
			genetics[index] = genetics[index]
		else:
			genetics[index] = abs(genetics[index] - 1)
	return genetics

def genetics_to_string(genetics: genetics) -> str:
    return "".join(map(str, genetics))
	
def run_evolution(
	generate_pop: PopulateFunc, 
	fitness_func: FitnessFunc, 
	selection_func: SelectionFunc = select_pair, 
	crossover_func: CrossoverFunc = cross_gens, 
	mutation_func: MutationFunc = mutation, 
	generation_limit: int = 100
) -> Tuple[Pop, int]:
	pop = generate_pop()

	for i in range(generation_limit):
		pop = sorted(pop,key =lambda genetics: fitness_func(genetics),reverse = True)

		next_gen = pop[0:2]

		for j in range(int(len(pop) / 2) - 1):
			parents = selection_func(pop,fitness_func)
			cross_a, cross_b = crossover_func(parents[0], parents[1])
			cross_a = mutation_func(cross_a)
			cross_b = mutation_func(cross_b)
			next_gen += [cross_a, cross_b]

		pop = next_gen
	
	pop = sorted(pop,key =lambda genetics: fitness_func(genetics),reverse = True)

	return pop

start = time.time()

population = run_evolution(
		generate_pop = partial(generate_pop, size = 100, genetics_len = len(things)),
		fitness_func = partial(fitness, things = things, weight_max = 3000),
		generation_limit = 100)

end = time.time()


x = int(len(population))

timecount = end - start


print(f"Best solution found - " + genetics_to_string(population[0]))

print(f"Time took to run algorithm - {timecount}s")

print(f"Things to carry in your backpack to get max fitness level:")

z = 0
things_list = []
for j in population[0]:
	if j == 1:
		things_list += [things[z].name]
	z += 1

print(things_list)

		
	
	