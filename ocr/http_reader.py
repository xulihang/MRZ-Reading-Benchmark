import json
import requests
import os
import base64


class HTTPReader():
    def __init__(self, sdk="MLKit",url="http://192.168.8.68:8888/"):
        self.url = url
        self.sdk = sdk
    
    def ocr(self, img_path):
        with open(img_path, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read())
        dic = {'base64':b64_string.decode("utf-8"),'sdk':self.sdk}
        r = requests.post(self.url, json = dic)
        result_dict = json.loads(r.text)
        lines = result_dict["results"] 
        filtered = self.filtered_result(lines)
        result_dict["boxes"] = filtered
        result_dict.pop("results")
        return result_dict
        
    def filtered_result(self, lines):
        filtered = []
        threshold = 35
        for line in lines:
            text = line["text"]
            line["text"] = self.postprocess(text)
            if len(text)>threshold:
                filtered.append(line)
        return filtered
        
    def postprocess(self,text):
        text = text.upper()
        text = text.replace(" ","")
        return text
        
if __name__ == '__main__':

    reader = HTTPReader()
    
    results = reader.ocr("0.jpg")
    print(results)
    