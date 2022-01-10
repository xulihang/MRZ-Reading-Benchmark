def postprocess(kind, lines):
    if kind == "mrz":
        return postprocess_for_mrz(lines)
    return lines

def postprocess_for_mrz(lines):
    filtered = []
    threshold = 40
    for line in lines:
        text = line["text"]
        text = text.upper()
        text = text.replace(" ","")
        line["text"] = text
        if len(text)>threshold:
            filtered.append(line)
            
    if len(filtered)>2:
        filtered = filtered[-2:]
    return filtered
    
def corner_points_from_rect(x, y ,width, height):
    x1 = x
    x2 = x + width
    x3 = x + width
    x4 = x
    y1 = y
    y2 = y
    y3 = y + height 
    y4 = y + height
    return x1, x2, x3, x4, y1, y2, y3, y4
    