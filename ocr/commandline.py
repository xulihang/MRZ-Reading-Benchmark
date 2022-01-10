import json
import os
import zmq
import sys
sys.path.append("..")
import ocr.utils

class CommandLineReader():
    def __init__(self, config_path="dlr_path",port=5558):
        self.context = zmq.Context()
        self.process = None
        self.config_path = config_path
        self.port = port
        self.postprocessing = "mrz"
    
    def ocr(self, img_path):
        result_dict = {}
        results = []
        try:
            socket = self.context.socket(zmq.REQ)
            socket.connect("tcp://localhost:"+str(self.port))
            socket.send(bytes(img_path,"utf-8"))
            message = socket.recv()
            json_object = json.loads(message.decode("utf-8"))
            if "boxes" in json_object:
                boxes=json_object["boxes"]
            if "elapsedTime" in json_object:
                result_dict["elapsedTime"]=json_object["elapsedTime"]
        except Exception as e:
            print("decode error")
            print(e)
        result_dict["raw_boxes"] = boxes
        result_dict["boxes"] = ocr.utils.postprocess(self.postprocessing, boxes)
        return result_dict
        
if __name__ == '__main__':
    reader = CommandLineReader()
    results = reader.ocr("F:\\mrz\\costa-forum-166254d7052f6d640-passport.jpg")
    print(results)
    