import networkx as nx
from pathlib import Path
from nodes import *
import json

class ION_GEN:
    models:dict

    graph:nx.DiGraph
    
    def __init__(self):
        pass

    def create_graph_from_data(self, graph_data:dict):
        graph = nx.DiGraph()
        graph.graph["models"] = graph_data["models"]
        
        #add node
        for n in graph_data["nodes"]:
            print(f"Create node: {n['type']}")
            node_obj = globals()[n['type']]()
            node_obj.name = n["name"]
            if "discription" in n:
                node_obj.discription = n["discription"]
            node_obj.input_param.update(n["input"])    
            node_obj.graph = graph   
            graph.add_node(n["name"], object = node_obj)  
        graph.add_edges_from(graph_data["edges"])
        self.graph = graph

    def create_graph_from_json(self, path):
        # read json file
        path = Path(path)
        with open(path) as f:
            graph_data = json.load(f)
        self.create_graph_from_data(graph_data)
        pass

    def run(self):
        if "start" in self.graph.nodes:
            self.graph.nodes["start"]["object"].run_flow()
        else:
            first_node_name = list(self.graph.nodes)[0]
            self.graph.nodes[first_node_name]["object"].run_flow()
        
