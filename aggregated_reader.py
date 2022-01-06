import time

class AggregatedReader():
    def __init__(self, engine="dynamsoft"):
        self.reader = None
        self.engine = engine
        self.init_reader()
        
    def init_reader(self):
        if self.engine == "PassportEye":
            from ocr.passport_eye import PassportReader
            self.reader = PassportReader()
    
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