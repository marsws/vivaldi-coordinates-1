#!/usr/bin/python
# Basic Vivaldi implementation

import random
from Graph import Graph
from Configuration import Configuration
from math import sqrt
#from operator import sub
import operator

class Vivaldi():
	def __init__(self, graph, conf):
		self.graph = graph
		self.conf = conf
		self.nodes = [[random.uniform(-50, 50) for _i in range(conf.num_dimension)] for _j in range(conf.num_nodes)]
	
	# Core of the Vivaldi algorithm
	def run(self):
		#TODO: Vivaldi run
		# for each iteration
		# for each node pick up K random neighbors
		# check how much the node has to "move" in terms of RTT towards/away his neighbors
		# compute the new coordinates following the Vivaldi algorithm
		for _iteration in xrange(self.conf.num_interations):
			for node_i in xrange(self.conf.num_nodes):
				node = self.nodes[node_i]
				for _neighbour in xrange(self.conf.num_neighbors):
					neighbor_i = random.randint(0, self.conf.num_nodes-1)
					while node_i == neighbor_i: 	# Dont select yourself as a neigbour
						neighbor_i = random.randint(0, self.conf.num_nodes-1)
					neighbor = self.nodes[neighbor_i]
					rtt = self.graph.getRTT(node_i, neighbor_i)
					dist = getNorm(getVet(node, neighbor))
					u = getDirection(neighbor, node)
					new_coords = map(lambda old, ud: old + self.conf.delta * (rtt - dist) * ud, node, u)
					node = new_coords
				self.nodes[node_i] = node
	
	# get the predicted RTT graph following Vivaldi.
	def oldgetRTTGraph(self):
		al = {}
		for i in xrange(self.conf.num_nodes):
			a = self.nodes[i]
			for j in xrange(self.conf.num_nodes):
				if i == j:
					continue
				b = self.nodes[j]
				rtt = getNorm(getVet(a, b))
				if i not in al.keys():
					al[i] = [(j,rtt)]
				else:
					al[i].append((j,rtt))
		return al

	def getRTTGraph(self):
		graph = Graph(self.conf.getNumNodes());
		for i, node1 in enumerate(self.nodes):
			for j, node2 in enumerate(self.nodes):
				rtt = getNorm(getVet(node1, node2))
				graph.addVertex(i, j, rtt)
		return graph

	# get the position of a node 
	def getPositions(self, node):
		return self.nodes[node]
	
	# Relative error of the predicted graph wrt real RTT graph
	def getRelativeError(self, predicted_graph):
		out = []
		for i in xrange(self.conf.num_nodes):
			for j in xrange(self.conf.num_nodes):
				#print self.graph.getRTT(i,j), predicted_graph.getRTT(i, j), self.graph.getRTT(i,j) - predicted_graph.getRTT(i, j)
				#out.append((self.graph.getRTT(i,j) - predicted_graph.getRTT(i, j))**2)
				real = self.graph.getRTT(i,j)
				approx = predicted_graph.getRTT(i, j)
				out.append(0 if real == 0 else abs((real - approx) / real))
				#print real, approx, 0 if real == 0 else abs((real - approx) / real)
		return out
	
	# basic CDF computation
	def computeCDF(self, input_):
		x = sorted(input_)
		y = map(lambda x: x / float((len(input_) + 1)), range(len(input_)))
		return x,y
	
#def get2DNorm(x, y):
#	return math.sqrt(x*x + y*y)

def getVet(a,b):
	return map(operator.sub, b, a)

def getNorm(vPos):
	norm = 0
	for i in range(len(vPos)):
		norm += (vPos[i])**2
	return sqrt(norm)

def getDirection(a, b):
	v = getVet(a, b)
	l = getNorm(v)
	return map(lambda x: x/l, v)
	