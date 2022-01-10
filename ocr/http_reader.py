import json
import requests
import os
import base64
import sys
sys.path.append("..")
import ocr.utils



class HTTPReader():
    def __init__(self, sdk="MLKit",url="http://192.168.8.68:8888/"):
        self.url = url
        self.sdk = sdk
        self.postprocessing = "mrz"
        self.need_sort = True
    
    def ocr(self, img_path):
        with open(img_path, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        dic = {'base64':b64_string.decode("utf-8"),'sdk':self.sdk}
        r = requests.post(self.url, json = dic)
        result_dict = json.loads(r.text)
        lines = result_dict["results"]
        if self.need_sort:
            lines = ocr.utils.sort_boxes(lines)
        result_dict["raw_boxes"] = lines
        result_dict["boxes"] = ocr.utils.postprocess(self.postprocessing,lines)
        
        result_dict.pop("results")
        return result_dict
                
        
if __name__ == '__main__':

    reader = HTTPReader()
    
    results = reader.ocr("test.jpg")
    print(results)
    