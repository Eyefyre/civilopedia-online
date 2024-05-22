import json

f = open('structure.json')

json_data = json.load(f)

languages = ["en","de","es","fr","it","ja","ko","pl","ru","zh"]

items = []
sections = []
highest_item_id = 0

all_items = []

for cat in json_data["categories"]:
    for sec in cat["sections"]:
        if sec["id"] in sections:
                print(f"Duplicate section {sec['id']} in category {cat['id']}")
        else:
            sections.append(sec["id"])
        for item in sec["items"]:
            if int(item["id"].split("_")[1]) > highest_item_id:
                highest_item_id = int(item["id"].split("_")[1])
            if item["id"] in items:
                print(f"Duplicate item {item['id']} from {sec['id']} in category {cat['id']}")
            else:
                items.append(item["id"])
            all_items.append(item["id"])

for extra in json_data["extras"]:
    all_items.append(extra["id"])
    if int(extra["id"].split("_")[1]) > highest_item_id:
            highest_item_id = int(extra["id"].split("_")[1])

pages = open('content.json')
page_data = json.load(pages)
pages_content = [x["item_id"] for x in page_data]

missing_content = [x for x in all_items if x not in pages_content]
for miss in missing_content:
    print(f"No content created for Item {miss} yet")
print(f"Number of pages left: {len(missing_content)}")



print(f"Highest item ID is item_{highest_item_id}")

for lang in languages:
    translations = open(f"translations_{lang}.json", encoding="utf-8")
    translations = json.load(translations)
    for cat in json_data["categories"]:
        if cat["label"] not in translations:
            print(f"{cat['label']} in {cat['id']} doesn't exist in translation_{lang}.json file") 
        for sec in cat["sections"]:
            if sec["label"] not in translations:
                print(f"{sec['label']} in {sec['id']} from {cat['id']} doesn't exist in translation_{lang}.json file") 
            for item in sec["items"]:
                if item["label"] not in translations:
                    print(f"{item['label']} in {item['id']} from {sec['id']} in {cat['id']} doesn't exist in translation_{lang}.json file") 
                    
                    


               