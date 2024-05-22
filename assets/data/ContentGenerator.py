import json
import sqlite3

debug_connection = sqlite3.connect("Civ5DebugDatabase.db")
cur = debug_connection.cursor()

item = open('structure2.json')
items = json.load(item)
translations = open("structure.json",encoding="utf-8")
json_data = json.load(translations)

local_conn = sqlite3.connect("Localization-Full.db")
tran = local_conn.cursor()

def translate(key):
    tran.execute("SELECT Text FROM Language_en_US WHERE Tag=?",(key,))
    translation = tran.fetchone()
    if translation == None:
        return None
    return translation[0]

def get_unit_info(unit_type):
    cur.execute("SELECT Civilopedia,Strategy,Help,Combat,Cost,FaithCost,Moves,RangedCombat,Range,CombatClass,PrereqTech,ObsoleteTech,GoodyHutUpgradeUnitClass,Type FROM Units WHERE Description=?",(unit_type,))
    unit = cur.fetchone()

    cur.execute("SELECT PromotionType FROM Unit_FreePromotions WHERE UnitType=?",(unit[13],))
    abilities = cur.fetchall()
    ability_names = []
    for ability in abilities:
        cur.execute("SELECT Description FROM UnitPromotions WHERE Type=?",(ability[0],))
        ability_names.append(cur.fetchone()[0])
        
    
    cur.execute("SELECT ResourceType FROM Unit_ResourceQuantityRequirements WHERE UnitType=?",(unit[13],))
    req_resources = cur.fetchall()
    resource_names = []
    for resource in req_resources:
        cur.execute("SELECT Description FROM Resources WHERE Type=?",(resource[0],))
        resource_names.append(cur.fetchone()[0])
        
    cur.execute("SELECT UnitClassType,CivilizationType FROM Civilization_UnitClassOverrides WHERE UnitType=?",(unit[13],))
    civ_override = cur.fetchone()
    civ_override_unit = None
    civilization = None
    if civ_override != None:
        cur.execute("SELECT Description FROM Units WHERE Class=?",(civ_override[0],))
        civ_override_unit = cur.fetchone()[0]
    
    if civ_override != None:
        cur.execute("SELECT ShortDescription FROM Civilizations WHERE Type=?",(civ_override[1],))
        civilization = cur.fetchone()[0]
    unit_template = {}
    
    unit_template["image"] = "./assets/images/unit_icons/.png"
    unit_template["title"] = unit_type
    if unit[2] != None:
        unit_template["game_info"] = unit[2]
    if unit[0] != None:
        unit_template["historical_info"] = unit[0]
    if unit[1] != None:
        unit_template["strategy"] = unit[1]
    if unit[4] != 0:
        unit_template["cost"] = f"{unit[4]} [ICON_PRODUCTION]"
    if unit[5] != 0:
        unit_template["cost"] = f"{unit_template['cost']} or {unit[5]} [ICON_PEACE]"
    if unit[9] != None:
        unit_template["combat_type"] = f"TXT_KEY_{unit[9]}"
    if unit[3] != 0:
        unit_template["combat"] = f"{unit[3]} [ICON_STRENGTH]"
    if unit[7] != 0:
        unit_template["ranged_combat"] = f"{unit[7]} [ICON_RANGED_STRENGTH]"
    if unit[8] != 0:
        unit_template["ranged"] = str(unit[8])
    if unit[6] != 0:
        unit_template["movement"] = f"{unit[6]} [ICON_MOVES]"
    if civilization != None:
        for option in items["cat_10"]["sections"]:
            for item in items["cat_10"]["sections"][option]["items"]:
                if civilization == items["cat_10"]["sections"][option]["items"][item]:
                    unit_template["civilization"] = [item]
    if abilities != []:
        unit_abilities = []
        for ability in ability_names:
            for option in items["cat_5"]["sections"]:
                for item in items["cat_5"]["sections"][option]["items"]:
                    if ability == items["cat_5"]["sections"][option]["items"][item]:
                        unit_abilities.append(item)
        unit_template["abilities"] = unit_abilities
    if req_resources != []:
        unit_resources = []
        for resource in resource_names:
            for option in items["cat_13"]["sections"]:
                for item in items["cat_13"]["sections"][option]["items"]:
                    if resource == items["cat_13"]["sections"][option]["items"][item]:
                        unit_resources.append(item)
        unit_template["required_resources"] = unit_resources
    if unit[10] != None:
        cur.execute("SELECT Description FROM Technologies WHERE Type=?",(unit[10],))
        tech_name = cur.fetchone()[0]
        for option in items["cat_3"]["sections"]:
            for item in items["cat_3"]["sections"][option]["items"]:
                if tech_name == items["cat_3"]["sections"][option]["items"][item] and item != "item_1029":
                    unit_template["prerequisite_techs"] = [item]
    if unit[11] != None:
        cur.execute("SELECT Description FROM Technologies WHERE Type=?",(unit[11],))
        tech_name = cur.fetchone()[0]
        for option in items["cat_3"]["sections"]:
            for item in items["cat_3"]["sections"][option]["items"]:
                if tech_name == items["cat_3"]["sections"][option]["items"][item]:
                    unit_template["becomes_obsolete_with"] = [item]
    if unit[12] != None:
        cur.execute("SELECT Description FROM Units WHERE Class=?",(unit[12],))
        civ_upgrade_unit = cur.fetchone()[0]
        for option in items["cat_4"]["sections"]:
            for item in items["cat_4"]["sections"][option]["items"]:
                if civ_upgrade_unit == items["cat_4"]["sections"][option]["items"][item]:
                    unit_template["upgrade_unit"] = [item]
    if civ_override_unit != None:
        for option in items["cat_4"]["sections"]:
            for item in items["cat_4"]["sections"][option]["items"]:
                if civ_override_unit == items["cat_4"]["sections"][option]["items"][item]:
                    unit_template["replaces"] = [item]
        

    return(unit_template)

def get_tech_info(tech_type):
    cur.execute("SELECT Type,Civilopedia,Help,Cost,Quote FROM Technologies WHERE Description=?",(tech_type,))
    tech = cur.fetchone()
    
    cur.execute("SELECT PrereqTech FROM Technology_PrereqTechs WHERE TechType=?",(tech[0],))
    prereq_techs = cur.fetchall()
    prereq_techs_names = []
    for ptech in prereq_techs:
        cur.execute("SELECT Description FROM Technologies WHERE Type=?",(ptech[0],))
        prereq_techs_names.append(cur.fetchone()[0])
    
    #leads_to_tech
    cur.execute("SELECT TechType FROM Technology_PrereqTechs where PrereqTech=?",(tech[0],))
    leads_to_tech = cur.fetchall()
    leads_to_tech_names = []
    for ltech in leads_to_tech:
        cur.execute("SELECT Description FROM Technologies WHERE Type=?",(ltech[0],))
        leads_to_tech_names.append(cur.fetchone()[0])
    
    cur.execute("SELECT Description from Units WHERE PrereqTech=?",(tech[0],))
    units_unlocked = cur.fetchall()
        
    cur.execute("SELECT Description from Projects WHERE TechPrereq=?",(tech[0],))
    projects_unlocked = cur.fetchall()
    
    cur.execute("SELECT Description from Resources WHERE TechReveal=?",(tech[0],))
    res_reveal = cur.fetchall()
    
    cur.execute("SELECT Description from Buildings WHERE PrereqTech=?",(tech[0],))
    buildings_unlocked = cur.fetchall()
    
    cur.execute("SELECT Description from Builds WHERE PrereqTech=?",(tech[0],))
    worker_actions = cur.fetchall()
    
    tech_template = {}
    
    tech_template["image"] = f"./assets/images/unit_icons/{translate(tech_type).lower().replace(' ','_')}.png"
    tech_template["title"] = tech_type
    tech_template["game_info"] = tech[2]
    tech_template["historical_info"] = tech[1]
    tech_template["quote"] = tech[4]
    tech_template["cost"] = f"{tech[3]} [ICON_RESEARCH]"
    
    if prereq_techs != []:
        prereq_technos = []
        for techs in prereq_techs_names:
            for option in items["cat_3"]["sections"]:
                for item in items["cat_3"]["sections"][option]["items"]:
                    if techs == items["cat_3"]["sections"][option]["items"][item]:
                        prereq_technos.append(item)
        tech_template["prerequisite_techs"] = prereq_technos
    if leads_to_tech != []:
        lead_technos = []
        for techs in leads_to_tech_names:
            for option in items["cat_3"]["sections"]:
                for item in items["cat_3"]["sections"][option]["items"]:
                    if techs == items["cat_3"]["sections"][option]["items"][item]:
                        lead_technos.append(item)
        tech_template["leads_to_techs"] = lead_technos
    if units_unlocked != []:
        units_un = []
        for unitss in units_unlocked:
            for option in items["cat_4"]["sections"]:
                for item in items["cat_4"]["sections"][option]["items"]:
                    if unitss[0] == items["cat_4"]["sections"][option]["items"][item]:
                        units_un.append(item)
        tech_template["units_unlocked"] = units_un
    if res_reveal != []:
        res_rev = []
        for ress in res_reveal:
            for option in items["cat_13"]["sections"]:
                for item in items["cat_13"]["sections"][option]["items"]:
                    if ress[0] == items["cat_13"]["sections"][option]["items"][item]:
                        res_rev.append(item)
        tech_template["resources_revealed"] = res_rev
    if buildings_unlocked != []:
        build_un = []
        for builds in buildings_unlocked:
            for option in items["cat_6"]["sections"]:
                for item in items["cat_6"]["sections"][option]["items"]:
                    if builds[0] == items["cat_6"]["sections"][option]["items"][item]:
                        build_un.append(item)
        tech_template["buildings_unlocked"] = build_un
    if worker_actions != []:
        action_un = []
        for actions in worker_actions:
            for option in items["extras"]:
                if actions[0] == items["extras"][option]:
                    action_un.append(option)
        tech_template["worker_actions_allowed"] = action_un
    if projects_unlocked != []:
        proje_un = []
        for projects in projects_unlocked:
            for option in items["cat_7"]["sections"]:
                for item in items["cat_7"]["sections"][option]["items"]:
                    if projects[0] == items["cat_7"]["sections"][option]["items"][item]:
                        proje_un.append(item)
        tech_template["projects_unlocked"] = proje_un
    
    return tech_template
    
def get_wonder_info(wonder_type):
    
    building_template = {}
    building_template["image"] = f"./assets/images/wonder_icons/{translate(wonder_type).lower().replace(' ','_')}.png"
    building_template["title"] = wonder_type
    cur.execute("SELECT Type,Civilopedia,Help,Strategy,Quote,Cost,PrereqTech,SpecialistType,GreatPeopleRateChange,UnmoddedHappiness,GreatWorkSlotType,GreatWorkCount,Defense FROM Buildings WHERE Description=?",(wonder_type,))
    wonder = cur.fetchone()
   
    if wonder != None: 
        
        if wonder[5] == 0:
            building_template["cost"] = "TXT_KEY_FREE"
        elif wonder[5] == -1:
            building_template["cost"] = "850 [ICON_PRODUCTION]"
        else:
            building_template["cost"] = f"{wonder[5]} [ICON_PRODUCTION]"
        if wonder[2] != None:
            building_template["game_info"] = wonder[2]
        if wonder[1] != None:
            building_template["historical_info"] = wonder[1]
        if wonder[3] != None:
            building_template["strategy"] = wonder[3]
        if wonder[4] != None:
            building_template["quote"] = wonder[4]
        if wonder[6] != None:
            prereq_techs_names = []
            cur.execute("SELECT Description FROM Technologies WHERE Type=?",(wonder[6],))
            prereq_techs_names.append(cur.fetchone()[0])
            pretechs = []
            for reqtech in prereq_techs_names:
                for option in items["cat_3"]["sections"]:
                    for item in items["cat_3"]["sections"][option]["items"]:
                        if reqtech == items["cat_3"]["sections"][option]["items"][item]:
                            pretechs.append(item)
            building_template["prerequisite_techs"] = pretechs
            
        if building[8] != None:
            if building[8] == "SPECIALIST_ENGINEER":
                building_template["great_engineer_points"] = f"{building[9]} [ICON_GREAT_PEOPLE]"
            if building[8] == "SPECIALIST_MERCHANT":
                building_template["great_merchant_points"] = f"{building[9]} [ICON_GREAT_PEOPLE]"
            if building[8] == "SPECIALIST_SCIENTIST":
                building_template["great_scientist_points"] = f"{building[9]} [ICON_GREAT_PEOPLE]"
            if building[8] == "SPECIALIST_WRITER":
                building_template["great_writer_points"] = f"{building[9]} [ICON_GREAT_PEOPLE]"
            if building[8] == "SPECIALIST_ARTIST":
                building_template["great_artist_points"] = f"{building[9]} [ICON_GREAT_PEOPLE]"
            if building[8] == "SPECIALIST_MUSICIAN":
                building_template["great_musician_points"] = f"{building[9]} [ICON_GREAT_PEOPLE]"
                
        if wonder[9] != 0:
            building_template["happiness"] = f"{wonder[9]} [ICON_HAPPINESS_1]"
            
        if wonder[10] != None:
            if wonder[10] == "GREAT_WORK_SLOT_ART_ARTIFACT":
                building_template["great_works"] = ["item_1582" for x in range(wonder[11])]
            if wonder[10] == "GREAT_WORK_SLOT_LITERATURE":
                building_template["great_works"] = ["item_1581" for x in range(wonder[11])]
            if wonder[10] == "GREAT_WORK_SLOT_MUSIC":
                building_template["great_works"] = ["item_1580" for x in range(wonder[11])]
                
        if wonder[12] != 0:
            building_template["defense"] = f"{float(wonder[12])/100} [ICON_STRENGTH]"
        
        cur.execute("SELECT YieldType,Yield from Building_YieldChanges WHERE BuildingType=?",(wonder[0],))
        wonder_yield_changes = cur.fetchall()
        
        if wonder_yield_changes != []:
            for yield_change in wonder_yield_changes:
                if yield_change[0] == "YIELD_CULTURE":
                    building_template["culture"] = f"{yield_change[1]} [ICON_CULTURE]"
                if yield_change[0] == "YIELD_SCIENCE":
                    building_template["science"] = f"+{yield_change[1]} [ICON_RESEARCH]"
                if yield_change[0] == "YIELD_PRODUCTION":
                    building_template["production"] = f"+{yield_change[1]} [ICON_PRODUCTION]"
                if yield_change[0] == "YIELD_GOLD":
                    building_template["gold"] = f"+{yield_change[1]} [ICON_GOLD]"
                if yield_change[0] == "YIELD_FAITH":
                    building_template["faith"] = f"+{yield_change[1]} [ICON_PEACE]"
                if yield_change[0] == "YIELD_FOOD":
                    building_template["food"] = f"+{yield_change[1]} [ICON_FOOD]"
        
        cur.execute("SELECT BuildingClassType from Building_PrereqBuildingClasses WHERE BuildingType=?",(wonder[0],))
        build_prereqs = cur.fetchall()
        if build_prereqs != []:
            required_building_names = []
            for buildingclass in build_prereqs:
                cur.execute("SELECT Description from Buildings WHERE BuildingClass=?",(buildingclass[0],))
                required_building_names.append(cur.fetchone()[0])
            wonder_builds = []
            for reqbuild in required_building_names:
                for option in items["cat_7"]["sections"]:
                    for item in items["cat_7"]["sections"][option]["items"]:
                        if reqbuild == items["cat_7"]["sections"][option]["items"][item]:
                            wonder_builds.append(item)
                for option in items["cat_6"]["sections"]:
                    for item in items["cat_6"]["sections"][option]["items"]:
                        if reqbuild == items["cat_6"]["sections"][option]["items"][item]:
                            wonder_builds.append(item)
            building_template["required_buildings"] = wonder_builds
    else:
        cur.execute("SELECT Type,Civilopedia,Strategy,Help,Cost,TechPrereq from Projects WHERE Description=?",(wonder_type,))
        project = cur.fetchone()
        building_template["cost"] = f"{project[4]} [ICON_PRODUCTION]"
        building_template["game_info"] = project[3]
        building_template["strategy"] = project[2]
        building_template["historical_info"] = project[1]
        
        prereq_techs_names = []
        cur.execute("SELECT Description FROM Technologies WHERE Type=?",(project[5],))
        prereq_techs_names.append(cur.fetchone()[0])
        pretechs = []
        for reqtech in prereq_techs_names:
            for option in items["cat_3"]["sections"]:
                for item in items["cat_3"]["sections"][option]["items"]:
                    if reqtech == items["cat_3"]["sections"][option]["items"][item]:
                        pretechs.append(item)
        building_template["prerequisite_techs"] = pretechs
    
    return building_template
   
   
def get_building_info(building_type):
    
    building_template = {}
    building_template["image"] = f"./assets/images/building_icons/{translate(building_type).lower().replace(' ','_')}.png"
    building_template["title"] = building_type
    cur.execute("SELECT Type,Civilopedia,Help,Strategy,Cost,FaithCost,PrereqTech,GoldMaintenance,SpecialistType,SpecialistCount,GreatPeopleRateChange,UnmoddedHappiness,GreatWorkSlotType,GreatWorkCount,Defense,BuildingClass FROM Buildings WHERE Description=?",(building_type,))
    building = cur.fetchone()

    cur.execute("SELECT YieldType,Yield from Building_YieldChanges WHERE BuildingType=?",(building[0],))
    building_yield_changes = cur.fetchall()
    
    if building_yield_changes != []:
        for yield_change in building_yield_changes:
            if yield_change[0] == "YIELD_CULTURE":
                building_template["culture"] = f"{yield_change[1]} [ICON_CULTURE]"
            if yield_change[0] == "YIELD_SCIENCE":
                building_template["science"] = f"+{yield_change[1]} [ICON_RESEARCH]"
            if yield_change[0] == "YIELD_PRODUCTION":
                building_template["production"] = f"+{yield_change[1]} [ICON_PRODUCTION]"
            if yield_change[0] == "YIELD_GOLD":
                building_template["gold"] = f"+{yield_change[1]} [ICON_GOLD]"
            if yield_change[0] == "YIELD_FAITH":
                building_template["faith"] = f"+{yield_change[1]} [ICON_PEACE]"
            if yield_change[0] == "YIELD_FOOD":
                building_template["food"] = f"+{yield_change[1]} [ICON_FOOD]"
                
    if building[12] != None:
        if building[12] == "GREAT_WORK_SLOT_ART_ARTIFACT":
            building_template["great_works"] = ["item_1582" for x in range(building[13])]
        if building[12] == "GREAT_WORK_SLOT_LITERATURE":
            building_template["great_works"] = ["item_1581" for x in range(building[13])]
        if building[12] == "GREAT_WORK_SLOT_MUSIC":
            building_template["great_works"] = ["item_1580" for x in range(building[13])]
            
    if building[4] == 0 or building[4] == -1:
        building_template["cost"] = f"{building[5]} [ICON_PEACE]"
    elif building[5] == 0:
        building_template["cost"] = f"{building[4]} [ICON_PRODUCTION]"
    else:
        building_template["cost"] = f"{building[4]} [ICON_PRODUCTION] or {building[5]} [ICON_PEACE]"
        
    if building[2] != None:
        building_template["game_info"] = building[2]
    if building[1] != None:
        building_template["historical_info"] = building[1]
    if building[3] != None:
        building_template["strategy"] = building[3]
        
    if building[7] != 0:
        building_template["maintenance"] = f"{building[7]} [ICON_GOLD]"
    if building[11] != 0:
        building_template["happiness"] = f"{building[11]} [ICON_HAPPINESS_1]"
        
    if building[6] != None:
        prereq_techs_names = []
        cur.execute("SELECT Description FROM Technologies WHERE Type=?",(building[6],))
        prereq_techs_names.append(cur.fetchone()[0])
        pretechs = []
        for reqtech in prereq_techs_names:
            for option in items["cat_3"]["sections"]:
                for item in items["cat_3"]["sections"][option]["items"]:
                    if reqtech == items["cat_3"]["sections"][option]["items"][item]:
                        pretechs.append(item)
        building_template["prerequisite_techs"] = pretechs
    cur.execute("SELECT CivilizationType FROM Civilization_BuildingClassOverrides WHERE BuildingType=?",(building[0],))
    if cur.fetchall() != []:
        cur.execute("SELECT ShortDescription from Civilizations WHERE Type=?",(cur.execute("SELECT CivilizationType FROM Civilization_BuildingClassOverrides WHERE BuildingType=?",(building[0],)).fetchone()[0],))
        civilization_name = cur.fetchone()[0]
        civs = []
        for option in items["cat_10"]["sections"]:
            for item in items["cat_10"]["sections"][option]["items"]:
                if civilization_name == items["cat_10"]["sections"][option]["items"][item]:
                    civs.append(item)
        building_template["civilization"] = civs
    
    cur.execute("SELECT Description from BuildingClasses WHERE Type=?",(building[15],))
    replace_building = cur.fetchone()
    replacements = []
    for option in items["cat_6"]["sections"]:
        for item in items["cat_6"]["sections"][option]["items"]:
            if replace_building[0] == items["cat_6"]["sections"][option]["items"][item]:
                replacements.append(item)
    building_template["replaces"] = replacements
    
    cur.execute("SELECT BuildingClassType from Building_PrereqBuildingClasses WHERE BuildingType=?",(building[0],))
    build_prereqs = cur.fetchall()
    if build_prereqs != []:
        required_building_names = []
        for buildingclass in build_prereqs:
            cur.execute("SELECT Description from Buildings WHERE BuildingClass=?",(buildingclass[0],))
            required_building_names.append(cur.fetchone()[0])
        wonder_builds = []
        for reqbuild in required_building_names:
            for option in items["cat_7"]["sections"]:
                for item in items["cat_7"]["sections"][option]["items"]:
                    if reqbuild == items["cat_7"]["sections"][option]["items"][item]:
                        wonder_builds.append(item)
            for option in items["cat_6"]["sections"]:
                for item in items["cat_6"]["sections"][option]["items"]:
                    if reqbuild == items["cat_6"]["sections"][option]["items"][item]:
                        wonder_builds.append(item)
        building_template["required_buildings"] = wonder_builds
        
    if building[8] != None:
        if building[8] == "SPECIALIST_ENGINEER":
            building_template["specialists"] = ["item_336" for x in range(building[9])]
        if building[8] == "SPECIALIST_MERCHANT":
            building_template["specialists"] = ["item_337" for x in range(building[9])]
        if building[8] == "SPECIALIST_SCIENTIST":
            building_template["specialists"] = ["item_339" for x in range(building[9])]
        if building[8] == "SPECIALIST_WRITER":
            building_template["specialists"] = ["item_341" for x in range(building[9])]
        if building[8] == "SPECIALIST_ARTIST":
            building_template["specialists"] = ["item_335" for x in range(building[9])]
        if building[8] == "SPECIALIST_MUSICIAN":
            building_template["specialists"] = ["item_338" for x in range(building[9])]
            
            
    if building[8] != None:
        if building[8] == "SPECIALIST_ENGINEER":
            building_template["great_engineer_points"] = f"{building[10]} [ICON_GREAT_PEOPLE]"
        if building[8] == "SPECIALIST_MERCHANT":
            building_template["great_merchant_points"] = f"{building[10]} [ICON_GREAT_PEOPLE]"
        if building[8] == "SPECIALIST_SCIENTIST":
            building_template["great_scientist_points"] = f"{building[10]} [ICON_GREAT_PEOPLE]"
        if building[8] == "SPECIALIST_WRITER":
            building_template["great_writer_points"] = f"{building[10]} [ICON_GREAT_PEOPLE]"
        if building[8] == "SPECIALIST_ARTIST":
            building_template["great_artist_points"] = f"{building[10]} [ICON_GREAT_PEOPLE]"
        if building[8] == "SPECIALIST_MUSICIAN":
            building_template["great_musician_points"] = f"{building[10]} [ICON_GREAT_PEOPLE]"
                
    if building[14] != 0:
        building_template["defense"] = f"{float(building[14])/100} [ICON_STRENGTH]"
        
    cur.execute("SELECT ResourceType FROM Building_ResourceQuantityRequirements WHERE BuildingType=?",(building[0],))
    req_resources = cur.fetchall()
    resource_names = []
    for resource in req_resources:
        cur.execute("SELECT Description FROM Resources WHERE Type=?",(resource[0],))
        resource_names.append(cur.fetchone()[0])
    if req_resources != []:
        unit_resources = []
        for resource in resource_names:
            for option in items["cat_13"]["sections"]:
                for item in items["cat_13"]["sections"][option]["items"]:
                    if resource == items["cat_13"]["sections"][option]["items"][item]:
                        unit_resources.append(item)
        building_template["required_resources"] = unit_resources
        
    return building_template
        
def get_civ_info(civ_type):
    
    civ_template = {}
    civ_template["image"] = f"./assets/images/building_icons/{translate(civ_type).lower().replace(' ','_')}.png"
    civ_template["title"] = civ_type
    cur.execute("SELECT Type,CivilopediaTag from Civilizations WHERE ShortDescription=?",(civ_type,))
    civ = cur.fetchone()
    tran.execute("SELECT Tag FROM Language_en_US WHERE Tag LIKE ?",(f"%{civ[1]}%",))
    civ_paras = tran.fetchall()
    heading_list = []
    text_list = []
    for paras in civ_paras:
        if "HEADING" in paras[0]:
            heading_list.append(paras[0])
        elif "TEXT" in paras[0]:
            text_list.append(paras[0])
    #print(len(heading_list), len(text_list))
    
    civ_template["heading"] = heading_list
    civ_template["texts"] = text_list
    # for heading in heading_list:
    #     print(heading)
    # for text in text_list:
    #     print(text)
    
    cur.execute("SELECT LeaderheadType from Civilization_Leaders WHERE CivilizationType=?",(civ[0],))
    civ_leader = cur.fetchone()
    cur.execute("SELECT Description from Leaders WHERE Type=?",(civ_leader[0],))
    civ_leader = cur.fetchone()[0]
    leaders = []
    for option in items["cat_10"]["sections"]:
        for item in items["cat_10"]["sections"][option]["items"]:
            if civ_leader == items["cat_10"]["sections"][option]["items"][item]:
                leaders.append(item)
    civ_template["leaders"] = leaders
    
    cur.execute("SELECT UnitType from Civilization_UnitClassOverrides WHERE CivilizationType=?",(civ[0],))
    unique_units = cur.fetchall()
    if unique_units != []:
        uni_units = []
        for unit in unique_units:
            cur.execute("SELECT Description from Units WHERE Type=?",(unit[0],))
            unit_name = cur.fetchone()[0]
            for option in items["cat_4"]["sections"]:
                for item in items["cat_4"]["sections"][option]["items"]:
                    if unit_name == items["cat_4"]["sections"][option]["items"][item]:
                        uni_units.append(item)   
        civ_template["unique_units"] = uni_units
    
    cur.execute("SELECT BuildingType from Civilization_BuildingClassOverrides WHERE CivilizationType=?",(civ[0],))
    unique_buildings = cur.fetchall()
    if unique_buildings != []:
        uni_buildings = []
        for building in unique_buildings:
            cur.execute("SELECT Description from Buildings WHERE Type=?",(building[0],))
            building_name = cur.fetchone()[0]
            for option in items["cat_6"]["sections"]:
                for item in items["cat_6"]["sections"][option]["items"]:
                    if building_name == items["cat_6"]["sections"][option]["items"][item]:
                        uni_buildings.append(item)   
        civ_template["unique_buildings"] = uni_buildings
        
    cur.execute("SELECT Description from Improvements WHERE CivilizationType=?",(civ[0],))
    unique_improvements = cur.fetchall()
    if unique_improvements != []:
        uni_improves = []
        for improve in unique_improvements:
            for option in items["cat_14"]["sections"]:
                for item in items["cat_14"]["sections"][option]["items"]:
                    if improve[0] == items["cat_14"]["sections"][option]["items"][item]:
                        uni_improves.append(item)   
        civ_template["unique_improvements"] = uni_improves
        
    return civ_template
    
    
def get_leader_info(leader_type):
    leader_template = {}
    leader_template["image"] = f"./assets/images/leader_icons/{translate(leader_type).lower().replace(' ','_')}.png"
    leader_template["title"] = leader_type
    
    cur.execute("SELECT Type,CivilopediaTag FROM Leaders where Description=?",(leader_type,))
    leader = cur.fetchone()
    
    leader_template["subtitle"] = f"{leader[1]}_SUBTITLE"
    leader_template["lived"] = f"{leader[1]}_LIVED"
    
    cur.execute("SELECT ShortDescription from Civilizations WHERE Type=?",(cur.execute("SELECT CivilizationType FROM Civilization_Leaders WHERE LeaderheadType=?",(leader[0],)).fetchone()[0],))
    civilization_name = cur.fetchone()[0]
    civs = []
    for option in items["cat_10"]["sections"]:
        for item in items["cat_10"]["sections"][option]["items"]:
            if civilization_name == items["cat_10"]["sections"][option]["items"][item]:
                civs.append(item)
    leader_template["civilization"] = civs
    
    tran.execute("SELECT Tag FROM Language_en_US WHERE Tag LIKE ?",(f"%{leader[1]}%",))
    leader_paras = tran.fetchall()
    heading_list = []
    text_list = []
    titles = ""
    for x,paras in enumerate(leader_paras):
        if "HEADING" in paras[0]:
            heading_list.append(paras[0])
        elif "TEXT" in paras[0]:
            text_list.append(paras[0])
        elif "TITLES" in paras[0]:
            if "TITLES_1" not in paras[0]:
                titles += "[NEWLINE]"
            titles += paras[0]
    
    leader_template["heading"] = heading_list
    leader_template["texts"] = text_list
    leader_template["titles"] = titles
    
    
    
    
    return leader_template

for x in range(1,10):
    items_list = json_data["categories"][5]["sections"][x]["items"]
    for item in items_list:
        response_strings = get_building_info(item['label'])
        item_final = {"item_id":item["id"],"view_id":"view_1","strings":response_strings}
        print(f"{json.dumps(item_final, indent=4)},")
