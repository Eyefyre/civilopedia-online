import json


# def get_trans(language):
#         json_data = open(f"translations_{language}.json",encoding="utf-8")
#         json_data = json.load(json_data)
#         print(language)
#         for row in json_data:
#             json_data[row] = json_data[row].split('|')[0]
#         with open(f"translations_{language}.json", 'w', encoding="utf-8") as f:
#             json.dump(json_data, f, indent=4)
#             f.close()
          
# keyPath = "key_list.csv" #"en","zh","fr","de","it","ja","ko","pl","ru","es"
# languages = ["en","de","es","fr","it","ja","ko","pl","ru","zh"]

# for language in languages:
#     get_trans(language)


# translations = open("translations_en.json",encoding="utf-8")
# json_data = json.load(translations)
# i = 1568
# for row in json_data:
#     if row.startswith("TXT_KEY_CONGRESS_") and row.endswith("TITLE"):
#         print("{")
#         print(f"\"id\": \"item_{i}\",")
#         print(f"\"label\": \"{row}\"")
#         print("},")
#         i += 1

translations = open("structure.json",encoding="utf-8")
json_data = json.load(translations)


    

for x in range(1,10):
    items_list = json_data["categories"][3]["sections"][x]["items"]
    for item in items_list:
        result = {"item_id":item["id"],"view_id":"view_1","strings":{"image":"./assets/images/unit_icons/.png","title":item["label"],"game_info":"TXT_KEY_UNIT_HELP_" + item["label"].split("_")[-1],"historical_info":"TXT_KEY_CIV5_" + item["label"].split("_")[-1] + "_TEXT","strategy":"TXT_KEY_UNIT_" + item["label"].split("_")[-1] + "_STRATEGY","cost":"","combat_type":"","combat":"","ranged_combat":"","range":"","movement":"","civilization":[],"abilities":[],"prerequisite_techs":[],"becomes_obsolete_with":[],"upgrade_unit":[],"replaces":[]}}
        json_formatted_str = json.dumps(result, indent=4)
        print(json_formatted_str + ",")
    
