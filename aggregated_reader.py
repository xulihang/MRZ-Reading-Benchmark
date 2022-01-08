import time
import os

class AggregatedReader():
    def __init__(self, engine="DLR"):
        self.reader = None
        self.engine = engine
        self.init_reader()
        
    def init_reader(self):
        if self.engine == "DLR":
            from ocr.commandline import CommandLineReader
            root = os.path.dirname(__file__)
            self.reader = CommandLineReader(config_path=os.path.join(root, "dlr_path"))
        elif self.engine == "PassportEye":
            from ocr.passport_eye import PassportReader
            self.reader = PassportReader()
        elif self.engine == "EasyOCR":
            from ocr.easy_ocr import EasyOCRReader
            self.reader = EasyOCRReader()
        elif self.engine == "MLKit":
            from ocr.easy_ocr import EasyOCRReader
            self.reader = EasyOCRReader() 
            
    
    def ocr(self, file_path):
        start_time = time.time()
        result_dict = self.reader.ocr(file_path)
        end_time = time.time()
        elapsedTime = int((end_time - start_time) * 1000)
        if "elapsedTime" not in result_dict:
            result_dict["elapsedTime"] = elapsedTime
        return result_dict

if __name__ == "__main__":
    reader = AggregatedReader(engine="PassportEye")
    print(reader.ocr("test.jpg"))