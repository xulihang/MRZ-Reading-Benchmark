from passporteye.mrz.image import MRZPipeline


class PassportReader():
    def __init__(self):
        pass
        
    def ocr(self, file_path):
        result_dict = {}
        boxes = []
        result_dict["boxes"] = boxes
        
        p = MRZPipeline(file_path)
        mrz = p.result
        
        box = {}
        text = p["text"]
        if text == None:
            text = ""
        box["text"] = text
        boxes.append(box)
        
        return result_dict
        
        
        
if __name__ == "__main__":
    reader = PassportReader()
    result_dict = reader.ocr("./test.jpg")
    print(result_dict)