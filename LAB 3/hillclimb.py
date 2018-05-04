import sys
import math
from random import shuffle
from draw import drawTour
import graph_plot
from collections import defaultdict
import argparse
import random
import itertools

#########################################################################################################
################# Provided code #########################################################################
#########################################################################################################
cities = 0
nodeDict = {}
numberOfRuns = 5

class Node():
	def __init__(self,index, xc, yc):
		self.i = index
		self.x = xc
		self.y = yc


def generateFile(cities, seed):
	MIN = 0
	MAX = 5000   
	random.seed(seed)
	i = 1
	filename = "tsp"+str(cities)
	with open(filename, "w") as f:
		for _ in itertools.repeat(None, cities):
			f.write("{p} {p0} {p1}\n".format(p=i, p0=random.randint(MIN, MAX), p1=random.randint(MIN, MAX)))
			i = i + 1
	return filename


def takeInput(file):
	global cities
	f = open(file,'r').read().splitlines()
	cities = len(f)
	for a in f:
		m = a.split()
		i = int(m[0])
		x = float(m[1])
		y = float(m[2])
		nodeDict[i] = Node(i, x, y)
	return


def save2optNeighbours(tour):
	""" You can print the list on stdout to check if your getting correct 2opt-neighbours
		or look into 2optNeighbours.txt file in your current directory"""
	tourList = generate2optNeighbours(tour)
	print(tourList)
	filename = "2optNeighbours.txt"
	file = open(filename, 'w')
	for i in tourList:
		file.write("%s\n" % i)



def generateRandomTour(r2seed):
	global cities
	print("number of cities are ",cities)
	random.seed(r2seed)
	tour = [x for x in range(1,cities+1)]
	#print(tour)
	shuffle(tour)
	#print(tour)
	return tour

def getTourLength(tour):
	global cities
	if len(tour) == 0:
		return 0

	length = 0
	if len(tour) == 2:
		return getDistance(nodeDict[tour[0]],nodeDict[tour[1]])

	for x in range(len(tour)-1):
		length += getDistance(nodeDict[tour[x]],nodeDict[tour[x+1]]) 
	
	length += getDistance(nodeDict[tour[0]],nodeDict[tour[-1]])

	return length

def getDistance(n1, n2):
	return math.sqrt((n1.x-n2.x)*(n1.x-n2.x) + (n1.y-n2.y)*(n1.y-n2.y))

unionFind= [] 

def union(x,y):
	k1 = unionFind[x]
	k2 = unionFind[y]
	for x in range(cities+1):
		if unionFind[x] == k1:
			unionFind[x] = k2


def find(x,y):
	return unionFind[x] == unionFind[y]


#############################################################################################

def generate2optNeighbours(tour):
	global cities
	all_possible_neighbours = []

	"*** YOUR CODE HERE ***"
	for i in range(len(tour)):
		for j in range(i+1,len(tour)):
			curr_tour = tour[:]
			sublist = tour[i:j]
			sublist.reverse()
			curr_tour[i:j] = sublist
			if curr_tour not in all_possible_neighbours:
				all_possible_neighbours.append(curr_tour)

	"*** --------------  ***"
	return all_possible_neighbours


def hillClimbUtil(tour):
	all_possible_neighbours = generate2optNeighbours(tour)
	min_cost = getTourLength(tour)
	min_tour = tour[:]
	for curr_tour in all_possible_neighbours:
		curr_cost = getTourLength(curr_tour)
		if curr_cost < min_cost:
			min_cost = curr_cost
			min_tour = curr_tour[:]

	return min_tour,min_cost

def hillClimbPart(tour,lenlist):
	base_cost = getTourLength(tour)
	min_tour, min_cost = hillClimbUtil(tour)
	lenlist.append(min_cost)
	if min_cost < base_cost:
		return hillClimbPart(min_tour,lenlist)
	else:
		return min_tour,lenlist




def hillClimbFull(initial_tour):
	""" Use the given tour as initial tour, Use your generate2optNeighbours() to generate
		all possible 2opt neighbours and apply hill climbing algorithm. Store the tour lengths
		that you are getting after every hill climb step in the list tourLengthList.
		Store the minimum tour found after the hill climbing algorithms in minTour.
		Your code will return the tourLengthList and minTour.     
		You will find 'task2.png' in current directory which shows hill climb algorithm performace
		The tourLengthList will be used to generate a graph which plots tour lengths with each step.
		that is hill climb iterations against tour length"""

	global cities
	tourLengthList = []
	minTour = 0
	tourLengthList.append(getTourLength(initial_tour))
	"*** YOUR CODE HERE ***"
	minTour, tourLengthList = hillClimbPart(initial_tour,tourLengthList)
	"*** --------------  ***"
	return tourLengthList, minTour


def nearestNeighbourTour(initial_city):
	tour = []

	"*** YOUR CODE HERE ***"
	tour.append(initial_city)
	visited = [0 for i in range(len(nodeDict))]
	visited[initial_city-1] = 1
	num_visited = 1
	curr_city = initial_city
	while num_visited != len(nodeDict):
		curr_node = nodeDict[curr_city]
		min_dist = float("Inf")
		min_city = 1
		for i in range(1,len(nodeDict)+1):
			if i != curr_city and visited[i-1] == 0:
				curr_dist = getDistance(curr_node,nodeDict[i])
				if curr_dist <= min_dist:
					min_dist = curr_dist
					min_city = i
		tour.append(min_city)
		num_visited+=1
		visited[min_city-1]=1
		curr_city = min_city
	"*** --------------  ***"
	return tour



def eucledianTour(initial_city):
	global unionFind, cities, nodeDict
	edgeList = []

	"*** YOUR CODE HERE ***"
	for i in range(1,len(nodeDict)+1):
		curr_node = nodeDict[i]
		for j in range(i+1,len(nodeDict)+1):
			edgeList.append([i,j,getDistance(curr_node,nodeDict[j])])

	"*** --------------  ***"

	'''KRUSKAL's algorithm'''

	mst = []
	for x in range(cities+1):
		unionFind.append(x)
	
	edgeList.sort(key=lambda x:int(x[2]))
	for x in edgeList:
		if(find(x[0],x[1]) == False):
			mst.append((x[0],x[1]))
			union(x[0],x[1])

	'''FINISHES HERE'''



	fin_ord = finalOrder(mst, initial_city)
	return fin_ord

def prehelper(mst, initial_city, list_so_far,visited):
	list_so_far.append(initial_city)
	visited[initial_city-1] = 1
	for i in range(len(mst)):
		if mst[i][0] == initial_city and visited[mst[i][1]-1] == 0:
			list_so_far,visited = prehelper(mst,mst[i][1],list_so_far,visited)
		if mst[i][1] == initial_city and visited[mst[i][0]-1] == 0:
			list_so_far,visited = prehelper(mst,mst[i][0],list_so_far,visited)
	return list_so_far,visited


def finalOrder(mst, initial_city):
	fin_order = 0
	"*** YOUR CODE HERE ***"
	visited = [0 for i in range(len(nodeDict))]
	fin_order,visited = prehelper(mst,initial_city,[],visited)
	# print(fin_order)
	"*** --------------  ***"
	return fin_order

 
##################################################################################################
####### DO NOT CHANGE THIS CODE ###########################################################################
###########################################################################################################
def hillClimbWithNearestNeighbour(start_city):
	tour = nearestNeighbourTour(start_city)
	tourLengthList, min_tour = hillClimbFull(tour)
	return tourLengthList
	

def hillClimbWithEucledianMST(initial_city):
	tour = eucledianTour(initial_city)
	tourLengthList, minTour = hillClimbFull(tour)
	
	#drawTour(nodeDict, minTour)
	return tourLengthList



def hillClimbWithRandomTour(tour):
	tourLengthList = []
	tourLengthList, minTour = hillClimbFull(tour)
	return tourLengthList

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', '-f', action='store', dest='file', help="Provide a file name (if file given then no need to provide city and random seed option that is -n and -r)")
	parser.add_argument('--cities', '-n', action='store', type=int, dest='cities', help="Provide number of cities in a tour")
	parser.add_argument('--r1seed', action='store', type=int, dest='r1seed', default=1, help="random seed")
	parser.add_argument('--r2seed', action='store', type=int, dest='r2seed', default=1, help="random seed")
	parser.add_argument('--task', '-t', action='store', type=int, dest="task", help="task to execute")
	parser.add_argument('--start_city', '-i', action='store', type=int, default=1, dest='start_city', help="Initial city")
	parser.add_argument('--submit', action='store_true', help="final submission")

	args = parser.parse_args()

	if args.submit:
		takeInput("data/st70.tsp");
	elif args.file:
		takeInput(args.file)
	elif args.cities:
		file = generateFile(args.cities, args.r1seed)
		takeInput(file)
	else:
		print("Please provide either a file or combination of number of cities and random seed")
		sys.exit()

	if not args.task:
		print("Please provide task number to execute")
		sys.exit()


	if args.task == 1:
		tour = generateRandomTour(args.r2seed)
		save2optNeighbours(tour)

	if not args.submit:
		if args.task == 2:
			tour = generateRandomTour(args.r2seed)
			tourLengthList = hillClimbWithRandomTour(tour)
			graph_plot.generateGraph(tourLengthList, "task2.png")
		

		if args.task == 3:
			tourLengthList = hillClimbWithNearestNeighbour(args.start_city)
			graph_plot.generateGraph(tourLengthList, "task3.png")


		if args.task == 4:
			tourLengthList = hillClimbWithEucledianMST(args.start_city)
			graph_plot.generateGraph(tourLengthList, "task4.png")

	else:
		if args.task == 2:
			data = []
			for i in range(1, numberOfRuns+1):
				random_seed = i
				tour = generateRandomTour(random_seed)
				tourLengthList = hillClimbWithRandomTour(tour)
				data.append(tourLengthList)

			graph_plot.generateFinalGraph(data, "task2_submit.png", 2)

		if args.task == 3:
			data = []
			for i in range(1, numberOfRuns+1):
				start_city = i
				tourLengthList = hillClimbWithNearestNeighbour(start_city)
				data.append(tourLengthList)

			graph_plot.generateFinalGraph(data, "task3_submit.png", 3)

		if args.task == 4:
			tourLengthList = hillClimbWithEucledianMST(args.start_city)
			graph_plot.generateGraph(tourLengthList, "task4_submit.png")
###################################################################################

