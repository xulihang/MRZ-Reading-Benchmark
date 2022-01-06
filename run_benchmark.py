import json
import argparse
import os
import conf
import editdistance
from aggregated_reader import AggregatedReader

engines = conf.engines
parser = argparse.ArgumentParser()
parser.add_argument("--path", help="path of data.json")
parser.add_argument("--engine", help="engine name")
parser.add_argument("--calculate", help="calculate score only (pass any value to enable)")
parser.add_argument("--enabled_engines", help="enabled engines list")
args = parser.parse_args()


def load_engines(conf_path):
    global engines
    engines = []
    with open(conf_path,"r") as f:
        for line in f.readlines():
            engines.append(line.strip())

def read_images_data(path):
    with open(path,"r") as f:
        images = json.loads(f.read())["images"]
    return images
    
def ocr_and_save_result(reader, image):
    filename = image["filename"]
    result_dict = reader.ocr(filename)
    engine = reader.engine
    
    print(result_dict)
    print(image)
    result_dict["score"] = get_similarity(get_total_text_of_boxes(result_dict["boxes"]), get_total_text_of_boxes(image["boxes"]))
    
    with open(get_engine_json_name(filename, engine), "w") as f:
        f.write(json.dumps(result_dict))

def get_engine_json_name(filename, engine):
    name, ext = os.path.splitext(filename)
    return name + "-" + engine + ".json"

def save_overall_statistics(result):
    with open("statistics.json","w") as f:
        f.write(json.dumps(result))

def get_overall_statistics(images):
    result = {}
    for engine in engines:
        engine_result = {}
        total_score = 0
        for image in images:
            ocr_result = get_ocr_result_from_json(engine, image)
            ground_truth = get_total_text_of_boxes(image["boxes"])
            total_score = total_score + get_similarity(ocr_result, ground_truth)
        engine_result["score"] = total_score/len(images)
        result[engine] = engine_result
    return result

def get_ocr_result_from_json(engine, image):
    json_name = get_engine_json_name(image["filename"], engine)
    with open(json_name, "r") as f:
        result_dict = json.loads(f.read())
        return get_total_text_of_boxes(result_dict["boxes"])
    
def get_total_text_of_boxes(boxes):
    text = ""
    for box in boxes:
        text = text + box["text"]
    return text

def get_similarity(text, ground_truth):
    distance = editdistance.eval(text, ground_truth)
    return 1 - distance/max(len(text),len(ground_truth))

def ocr_all_images(images):
    for engine in engines:
        reader = AggregatedReader(engine)
        for image in images:
            ocr_and_save_result(reader, image)
        
def run():
    if args.engine:
        global engines
        engines = []
        engines.append(args.engine)
    else:
        if args.enabled_engines:
            load_engines(args.enabled_engines)
    if os.path.exists(args.path) == False:
        print("path does not exist")
        return
    parent_path = os.path.abspath(os.path.dirname(args.path))
    print(parent_path)
    os.chdir(parent_path)
    images = read_images_data(args.path)
    
    if args.calculate:
        result = get_overall_statistics(images)
        save_overall_statistics(result)
    else:
        ocr_all_images(images)
        result = get_overall_statistics(images)
        save_overall_statistics(result)
    
run()
    
    
    