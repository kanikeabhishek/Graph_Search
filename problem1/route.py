#!/usr/bin/env python

import sys
import time
from heapq import heappush, heapify, heappop
import pickle
from math import sin, cos, sqrt, atan2, radians


def successors(city):
	return graph[city]['neighbour'].keys()

def solve(search_type, start_city, end_city):
	index = 0
	fringe = [(start_city, 0, 0)]
	while len(fringe) > 0:
		next_city = fringe.pop(search_type)
		index += 1
		if next_city[0] == start_city:
			graph[next_city[0]]['parent'] = 'start'
		for s in successors( next_city[0] ):
			if graph[s]['parent'] != 'null':
				continue
			distance = next_city[1] + graph[next_city[0]]['neighbour'][s][0]
			time = next_city[2] + (graph[next_city[0]]['neighbour'][s][0] / float(graph[next_city[0]]['neighbour'][s][1]))
			graph[s]['parent'] = next_city[0]
			if s == end_city:
				return distance, time
			fringe.append((s, distance, time))
	return False

def minheap(start_city, end_city, cost_function):
	fringe = []
	heapify(fringe)
	heappush(fringe, (0, 0, 0, start_city))
	visited = []
	distance = 0
	time  = 0
	graph[start_city]['parent'] = 'start'
	while len(fringe) > 0:
		next_city = heappop(fringe)
		visited.append(next_city[3])
		if next_city[3] == end_city:
			return next_city[1], next_city[2]

		for s in successors( next_city[3] ):
			if s in visited:
				continue
			continue_successor = False
			if cost_function == 'distance':
				neighbour_cost = graph[next_city[3]]['neighbour'][s][0] + next_city[1]
				distance = neighbour_cost
				time = graph[next_city[3]]['neighbour'][s][0] / float(graph[next_city[3]]['neighbour'][s][1]) + next_city[2]
			elif cost_function == 'time':
				neighbour_cost = (graph[next_city[3]]['neighbour'][s][0] / float(graph[next_city[3]]['neighbour'][s][1])) + next_city[2]
				distance = graph[next_city[3]]['neighbour'][s][0] + next_city[1]
				time = neighbour_cost
			elif cost_function == 'segment':
				neighbour_cost = 1 + next_city[0]
				distance = graph[next_city[3]]['neighbour'][s][0] + next_city[1]
				time = graph[next_city[3]]['neighbour'][s][0] / float(graph[next_city[3]]['neighbour'][s][1]) + next_city[2]

			for i , (j, k, l, m) in zip(range(len(fringe)), fringe):
				if m == s:
					if j < neighbour_cost:
						continue_successor = True
						break
					else:
						del fringe[i]
			if continue_successor:
				continue
			graph[s]['parent'] = next_city[3]
			heappush(fringe, (neighbour_cost, distance, time, s))
	return False

def haversine(start_city, goal_city):
	if graph[start_city]['lat'] == 0.0:
		return 0.0
	R = 6373.0
	start_city_latitude = radians(graph[start_city]['lat'])
	start_city_longitude = radians(graph[start_city]['long'])
	goal_city_latitude = radians(graph[goal_city]['lat'])
	goal_city_longitude = radians(graph[goal_city]['long'])
	delta_longitude = goal_city_longitude - start_city_longitude
	delta_latitude = goal_city_latitude - start_city_latitude
	a = sin(delta_latitude / 2)**2 + cos(start_city_latitude) * cos(goal_city_latitude) * sin(delta_longitude / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	return R * c * 0.621371

def astar(start_city, end_city, cost_function):
	fringe = []
	heapify(fringe)
	heappush(fringe, (0, 0, 0, start_city, 0))
	graph[start_city]['parent'] = 'start'
	visited = []
	while len(fringe) > 0:
		next_city = heappop(fringe)

		visited.append(next_city[3])
		if next_city[3] == end_city:
			return next_city[1], next_city[2]

		for s in successors( next_city[3] ):
			if s in visited:
				continue
			continue_successor = False

			heuristic_cost = haversine(s, end_city)

			if cost_function == 'distance':
				neighbour_cost = next_city[1] + graph[next_city[3]]['neighbour'][s][0]
				distance = neighbour_cost
				time = graph[next_city[3]]['neighbour'][s][0] / float(graph[next_city[3]]['neighbour'][s][1]) + next_city[2]

			elif cost_function == 'segment':
				neighbour_cost = next_city[4] + 1
				if heuristic_cost:
					heuristic_cost = min_distance / heuristic_cost
				distance = graph[next_city[3]]['neighbour'][s][0] + next_city[1]
				time = graph[next_city[3]]['neighbour'][s][0] / float(graph[next_city[3]]['neighbour'][s][1]) + next_city[2]

			elif cost_function == 'time':
				neighbour_cost = (graph[next_city[3]]['neighbour'][s][0] / float(graph[next_city[3]]['neighbour'][s][1])) + next_city[2]
				heuristic_cost /= max_speed
				distance = graph[next_city[3]]['neighbour'][s][0] + next_city[1]
				time = neighbour_cost

			for i , (j, k, l, m, n) in zip(range(len(fringe)), fringe):
				if m == s:
					if j < neighbour_cost + heuristic_cost:
						continue_successor = True
						break
					else:
						del fringe[i]
			if continue_successor == True:
				continue
			graph[s]['parent'] = next_city[3]
			heappush(fringe, (neighbour_cost + heuristic_cost, distance, time, s, neighbour_cost))
	return False

def populate_graph():
	global min_distance
	global max_speed
	city_gps = open("city-gps.txt", "r")
	road_segments = open("road-segments.txt", "r")
	city_data = city_gps.readline().split()
	min_distance = 9999
	# Populate city data
	while city_data:
		graph[city_data[0]] = {}
		graph[city_data[0]].update({'lat' : float(city_data[1])})
		graph[city_data[0]].update({'long' : float(city_data[2])})
		graph[city_data[0]].update({'neighbour': {}})
		city_data = city_gps.readline().split()

	# Populate route data
	route_data = road_segments.readline().split()
	while route_data:
		for city in range(0,2):
			if not route_data[city] in graph:
				graph[route_data[city]] = {'lat' : 0.0, 'long' : 0.0, 'neighbour': {}}

		if len(route_data) == 4:
			route_data.insert(3, 40)
		if int(route_data[2]) == 0:
			route_data[2] = 40
		if int(route_data[3]) == 0:
			route_data[3] = 40

		neighbour_data = {route_data[1]: [int(route_data[2]), int(route_data[3]), route_data[4]]}
		graph[route_data[0]]['neighbour'].update(neighbour_data)

		neighbour_data = {route_data[0]: [int(route_data[2]), int(route_data[3]), route_data[4]]}
		graph[route_data[1]]['neighbour'].update(neighbour_data)

		if int(route_data[3]) > max_speed:
			max_speed = int(route_data[3])
		if min_distance > int(route_data[2]):
			min_distance = int(route_data[2])

		route_data = road_segments.readline().split()

	for node in graph:
		if not 'parent' in node:
			graph[node].update({'parent' : 'null'})

graph = {}
min_distance = 0
max_speed = 0


def print_solution(start_city, end_city, distance, time):
	path = []
	print distance, time,
	parent_city = graph[end_city]['parent']
	path.insert(0, end_city)
	while parent_city != 'start':
		path.insert(0, parent_city)
		parent_city = graph[parent_city]['parent']
	for node in path:
		print node,
	print "\n"

def main():
	start_city = sys.argv[1]
	end_city = sys.argv[2]
	routing_algorithm = sys.argv[3]
	cost_function = sys.argv[4]

	populate_graph()

	if routing_algorithm == 'bfs':
		distance, time = solve(0, start_city, end_city)
		if distance and time:
			print_solution(start_city, end_city, distance, time)
		else:
			print 'didnt find the solution'

	elif routing_algorithm == 'uniform':
		distance, time = minheap(start_city, end_city, cost_function)
		if distance and time:
			print_solution(start_city, end_city, distance, time)
		else:
			print 'didnt find the solution'

	elif routing_algorithm == 'dfs':
		distance, time = solve(-1, start_city, end_city)
		if distance and time:
			print_solution(start_city, end_city, distance, time)
		else:
			print 'didnt find the solution'

	elif routing_algorithm == 'astar':
		distance, time = astar(start_city, end_city, cost_function)
		if distance and time:
			print_solution(start_city, end_city, distance, time)
		else:
			print 'didnt find the solution'

if __name__ == '__main__':
	main()