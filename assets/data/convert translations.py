import csv 
import json 
import sqlite3

local_conn = sqlite3.connect("Localization-Full.db")
tran = local_conn.cursor()

def translate(language,key):
    if key == None:
        return 
    language_table = "Language_en_US"
    match language:
        case "en":
            language_table = "Language_en_US"
        case "zh":
            language_table = "Language_ZH_HANT_HK"
        case "fr":
            language_table = "Language_FR_FR"
        case "de":
            language_table = "Language_DE_DE"
        case "it":
            language_table = "Language_IT_IT"
        case "ja":
            language_table = "Language_JA_JP"
        case "ko":
            language_table = "Language_KO_KR"
        case "pl":
            language_table = "Language_PL_PL"
        case "ru":
            language_table = "Language_RU_RU"
        case "es":
            language_table = "Language_ES_ES"
    tran.execute("SELECT Text FROM " + language_table + " WHERE Tag=?",(key,))
    translation = tran.fetchall()
    if translation == []:
        return []
    return translation[0][0]

def get_trans(csvFilePath,language):
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.reader(csvf) 

        json_data = open(f"translations_{language}.json",encoding="utf-8")
        json_data = json.load(json_data)
        print(language)
        for row in csvReader:
            print(row[0])
            json_data[row[0]] = translate(language,row[0]).split('|')[0]
            print(json_data[row[0]])
        with open(f"translations_{language}.json", 'w', encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)
            f.close()
          
keyPath = "key_list.csv" #"en","zh","fr","de","it","ja","ko","pl","ru","es"
languages = ["en","de","es","fr","it","ja","ko","pl","ru","zh"]

for language in languages:
    get_trans(keyPath,language)