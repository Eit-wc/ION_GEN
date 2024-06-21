from BaseNode import BaseNode

class InputNode(BaseNode):
    # this set of parameter user to discribe the node
    input_param:dict
    output_param:dict 
    
    def __init__(self):
        self.input_param = {}
        self.output_param = {"text":""}
        pass

    def main(self,**kwargs):
        userInput = input()
        self.output_param["text"] = userInput
