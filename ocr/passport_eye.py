from passporteye.mrz.image import MRZPipeline
import sys
sys.path.append("..")
import ocr.utils

class PassportReader():
    def __init__(self):
        pass
        
    def ocr(self, file_path):
        result_dict = {}
        boxes = []
        result_dict["boxes"] = boxes
        
        p = MRZPipeline(file_path)
        mrz = p.result
        
        
        text = p["text"]
        if text != None:
            x = p["boxes"][0].cx
            y = p["boxes"][0].cy
            width = p["boxes"][0].width
            height = p["boxes"][0].height
            x1, x2, x3, x4, y1, y2, y3, y4 = ocr.utils.corner_points_from_rect(x, y, width, height)
            box = {}
            box["text"] = text
            box["x1"] = x1
            box["y1"] = y1
            box["x2"] = x2
            box["y2"] = y2
            box["x3"] = x3
            box["y3"] = y3
            box["x4"] = x4
            box["y4"] = y4
            boxes.append(box)
        
        return result_dict
        
        
        
if __name__ == "__main__":
    reader = PassportReader()
    result_dict = reader.ocr("./test.png")
    print(result_dict)