from paddleocr import PaddleOCR
import sys
import cv2
sys.path.append("..")
import ocr.utils

class PaddleOCRReader():
    def __init__(self):
        self.current_lang="en"
        self.reader = PaddleOCR(lang=self.current_lang,det_db_thresh=0.9,det_db_box_thresh=0.6)
        self.postprocessing = "mrz"
        
    def ocr(self, file_path):
        result_dict = {}
        result = self.reader.ocr(file_path)
        lines=[]
        for line in result:
            new_line={}
            index=1
            for coord in line[0]:
                new_line["x"+str(index)]=int(coord[0])
                new_line["y"+str(index)]=int(coord[1])
                index=index+1
            new_line["text"]=line[1][0]
            lines.append(new_line)
            
        result_dict["raw_boxes"] = lines
        result_dict["boxes"] = ocr.utils.postprocess(self.postprocessing, lines)
        return result_dict
        
if __name__ == "__main__":
    reader = PaddleOCRReader()
    result_dict = reader.ocr("test.png")
    print(result_dict)