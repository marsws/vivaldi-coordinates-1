#!/usr/bin/python

from Graph import Graph
from Configuration import Configuration
from Vivaldi import Vivaldi

import sys
from pylab import *

def buildgraph(rows):
	g = Graph(len(rows))
	for node in range(len(rows)):
		arr = rows[node].strip().split(" ")
		rtts = [float(x) for x in arr if len(x) > 0]
		for neighbor in range(len(rtts)):
			g.addVertex(node,neighbor,rtts[neighbor])
	
	return g
	
	
if __name__== "__main__":
	if len(sys.argv) != 2:
		print "Usage: %s <rtt_file>"%sys.argv[0]
		sys.exit(0)
	
	rttfile = sys.argv[1]
	infile = open(rttfile, 'r')
	rows = infile.readlines()
	num_nodes = len(rows)
	infile.close()
	
	# These parameters are part of the Configuration.
	# Modify them according to your need.
	#num_neighbors = 10
	#num_iterations = 200
	num_neighbors = 10
	num_iterations = 200

	num_dimension = 2
	
	# build a configuration and load the matrix into the graph
	c = Configuration(num_nodes, num_neighbors, num_iterations, num_dimension)
	init_graph = buildgraph(rows)

	print "Running Vivaldi on a %d size matrix" % num_nodes
	print "Num dimensions = %d " % num_dimension
	print "Num neighbors = %d " % num_neighbors 
	print "Num iterations = %d " % num_iterations
	
	# run vivaldi: here, only the CDF of the relative error is retrieved. 
	# Modify to retrieve what's requested.
	v = Vivaldi(init_graph, c)
	
	v.run()
	
	predicted = v.getRTTGraph()
	rerr = v.getRelativeError(predicted)
	
	print sum(rerr) / float(len(rerr))

	# Example (using pylab plotting function):
	x,y = v.computeCDF(rerr)
	plot(x,y)
	show()
