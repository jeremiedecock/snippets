def parse_property(property_dict):

    if property_dict["type"] == "rollup":
        value = set()
        for ms in property_dict["rollup"]["array"]:
            for ms2 in ms["multi_select"]:
                value.add(ms2["name"])
        value = list(value)

    elif property_dict["type"] == "multi_select":
        value = set()
        for ms in property_dict["multi_select"]:
            value.add(ms["name"])
        value = list(value)

    elif property_dict["type"] == "select":
        value = None
        if property_dict["select"] is not None:
            value = property_dict["select"]["name"]
    
    elif property_dict["type"] == "rich_text":
        value = ""
        for line in property_dict["rich_text"]:
            value += line['plain_text']
    
    elif property_dict["type"] == "number":
        value =  property_dict["number"]
    
    elif property_dict["type"] == "people":
        value = set()
        for ms in property_dict["people"]:
            value.add(ms["name"])
        value = list(value)
    
    elif property_dict["type"] == "url":
        value =  property_dict["url"]
    
    elif property_dict["type"] == "relation":
        value = set()
        for ms in property_dict["relation"]:
            page_id = ms["id"]
            sub_resp = requests.get(f"https://api.notion.com/v1/pages/{page_id}", headers=HEADER_DICT)

            for k, v in sub_resp.json()["properties"].items():
                if v["type"] == "title":
                    title = ""
                    for line in v["title"]:
                        title += line['plain_text']
                    value.add(title)
        value = list(value)
    
    elif property_dict["type"] == "title":
        value = ""
        for line in property_dict["title"]:
            value += line['plain_text']

    return value