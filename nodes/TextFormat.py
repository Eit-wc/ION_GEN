from BaseNode import BaseNode

class TextFormat(BaseNode):
    # this set of parameter user to discribe the node
    input_param:dict
    output_param:dict 
    
    def __init__(self):
        self.input_param = {"format":""}
        self.output_param = {"text":""}
        pass

    def main(self,**kwargs):
        self.output_param["text"] = kwargs["format"].format(**kwargs)
