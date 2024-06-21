import networkx as nx

class BaseNode:
    # this set of parameter user to discribe the node
    input_param:dict
    output_param:dict
    name:str
    discription:str

    # this set of parameter user to control the node flow
    # user have to connect to the next node by adding the name of the next node into goto_nodes
    graph:nx.DiGraph

    def __init__(self):
        pass

    def main(self,**kwargs):
        pass

    def run_node(self):
        #retrive data from input_param
        kwargs = {}
        for k in self.input_param:
            if type(self.input_param[k]) is tuple:
                target_object = self.graph.nodes[self.input_param[k][0]]["object"]
                kwargs[k] = getattr( target_object, "output_param")[self.input_param[k][1]]
            else:
                kwargs[k] = self.input_param[k]
        
        return self.main(**kwargs)

    
    def run_flow(self):
        return_val = self.run_node()
        if self.graph is None:
            return
        
        next_node = None
        edges = self.graph[self.name]
        if len(edges) == 0:
            print("End!!")
            return
        elif len(edges) == 1:
            next_node =  self.graph.nodes[list(edges)[0]]["object"]
        elif len(edges) > 1:
            for edge in edges:
                if return_val.lower() == edges[edge]["condition"].lower():
                    next_node = self.graph.nodes[edge]["object"]
                    break


        if isinstance(next_node,BaseNode):
            print(f"goto node: {next_node.name}")
            next_node.run_flow()
        elif next_node is None:
            print("next_node none End!!")
        return