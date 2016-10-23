# Author:
# Patrick O'Boyle
# Shane Fay

import csv
import os
from shutil import copyfile
from os import remove
import copy
import sys
import Tree
import Node
import calculate_routing_tables

def create_list_state_routing_table():
    ports, tables = calculate_routing_tables.create_routing_tables()
    
    for port, table in zip(ports,tables):
        file_path = "tables/" + port + ".csv"
        print file_path
        
        with open(file_path, "w+") as routing_table:
            writer = csv.writer(routing_table, delimiter=',')
        
            for row in table:
                print row
                writer.writerow(row)

    
# check if a router has not already been added to the map
# returns False if it has, True otherwise
def is_router_not_in_map(router_port, map_path):
    with open(map_path, "r") as network_map:
        reader = csv.reader(network_map, delimiter=',')
        
        for row in reader:
            if(row[0] == router_port):
                return False
        return True

# create the network map CSV
def create_network_map(router_list):
    file_path = "config/network_map.csv"
    
    # create empty CSV
    # check if open for writing later is better (probably is :( )
    network_map = open(file_path, "w+")
    network_map.close
    
    router_maps = []
    
    # create a list of all router-maps
    for router in router_list:
        router_maps.append(router.file_path)
    
    # ensure all paths are correct (they are)
    for router_map in router_maps:
        with open(router_map, "r") as mapping_file:
            reader = csv.reader(mapping_file, delimiter=',')
            
            for row in reader:
                router = row[0]

                if( is_router_not_in_map(router, file_path) ):
                    connections = row[1]
                    with open(file_path, "a+") as network_map:
                        writer = csv.writer(network_map, delimiter=',')
                        writer.writerow([router, connections])
        # delete mapping of this router                
        os.remove(router_map)

# Returns a list of router nodes, where node is a tuple - (router_port, direct connections)
def get_router_nodes(network_map_path):
    # list of all nodes
    router_nodes = []
    
    with open(network_map_path, "r") as network_map:
        # get a list of all routers and connections, IE - Create nodes
        reader = csv.reader(network_map, delimiter=',')
        
        for row in reader:
            router_node = (row[0], row[1])
            router_nodes.append(router_node)
            
    return router_nodes

def convert_csv_to_list(file_path):
    lookup_table = []
        
    with open(file_path, 'r') as table:
        reader = csv.reader(table, delimiter=',')
            
        for row in reader:
            row_data = []
                
            for item in row:
                row_data.append(item)

            lookup_table.append(row_data)
    return lookup_table

def write_list_to_csv(file_path, lookup_table):
    with open(file_path, "w+") as table:
        writer = csv.writer(table, delimiter=',')
        
        for row in lookup_table:
            writer.writerow(row)
            
def get_next_hop(router_port, dest):
    dvr_table_path = "tables/" + str(router_port) + ".csv"
    dvr_table = convert_csv_to_list(dvr_table_path)
    
    num_columns = len( dvr_table[0] )
    
    for row in xrange(1):
        port_number = dvr_table[row][0]
        
        if port_number == dest:
            next_hop = dvr_table[row][1]
            return next_hop