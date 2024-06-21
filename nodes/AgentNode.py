from BaseNode import BaseNode 
import requests
import copy

class AgentNode(BaseNode):
    # this set of parameter user to discribe the node
    input_param:dict
    output_param:dict 
    
    def __init__(self):
        self.input_param =  {"model":"","system":"","user":"","messages":[]}
        self.output_param = {"last_response":"","messages":[]}
        pass

    def main(self,**kwargs):
        
        model = self.graph.graph["models"][self.input_param["model"]]
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + model["api_key"],
        }

        messages = [{"role":"system","content":kwargs["system"]}]
        if len(kwargs["messages"]) >0 :
            messages.append(kwargs["messages"])
        if len(kwargs["user"]) >0 :
            messages.append({"role":"user","content":kwargs["user"]})
        print(f"AgentNode {self.name} messages: {messages}")
        json_data = {
            'messages': messages,
            'model': model["model"],
            'temperature': model["temperature"],
            'max_tokens': 1024,
            'top_p': 1,
            'stream': False,
            'stop': None,
        }
        #remove system prompt from messages
        self.output_param["messages"] = copy.copy(messages)
        for m in self.output_param["messages"]:
            if m["role"] == "system":
                self.output_param["messages"].remove(m)


        self.response = requests.post(model["endpoint"], headers=headers, json=json_data).json()
        if "choices" in self.response and len(self.response["choices"]) > 0:
            self.output_param["last_response"] = self.response["choices"][0]["message"]["content"]
            self.output_param["messages"].append(self.response["choices"][0]["message"])
        print(f"AgentNode response: {self.output_param['last_response']}")
        return self.output_param['last_response']
