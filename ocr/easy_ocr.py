import easyocr
import os

class EasyOCRReader():
    def __init__(self):
        current_lang="en"
        root = os.path.dirname(__file__)
        self.reader = easyocr.Reader([current_lang],model_storage_directory=root)
        
    def ocr(self, file_path):
        result_dict = {}
        boxes = []
        result_dict["boxes"] = boxes
        result = self.reader.readtext(file_path)
        #for mrz
        result = self.filtered_result(result)
        if len(result)>=2:
            box1 = {}
            box1["text"] = result[-2][1]
            box2 = {}
            box2["text"] = result[-1][1]
            boxes.append(box1)
            boxes.append(box2)
            
        #for general purpose
        #for line in result:
        #    box = {}
        #    box["text"] = line[1]
        #    boxes.append(box)
        
        return result_dict
    
    def filtered_result(self, result):
        filtered = []
        threshold = 30
        for line in result:
            text = line[1]
            if len(text)>threshold:
                filtered.append(line)
        return filtered
        
if __name__ == "__main__":
    reader = EasyOCRReader()
    result_dict = reader.ocr("test.jpg")
    print(result_dict)