def postprocess(kind, lines):
    if kind == "mrz":
        return postprocess_for_mrz(lines)
    return lines

def postprocess_for_mrz(lines):
    filtered = []
    threshold = 35
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