import hashes as rh


GRADES = {
    12.9: 'S+',
    10.5: 'S',
    9.3: 'S-',
    6.5: 'A+',
    6.1: 'A',
    5.8: 'A-',
    5.1: 'B+',
    4.5: 'B',
    3.9: 'B-',
    3.5: 'C+',
    3.3: "C",
    3: "C-",
    2.3: "D+",
    1.7:"D",
}


score_mapping = {
        'cleared': 0.13,
        'trio boss': 0.04,
        'trio full': 0.27,
        'trio flawless': 0.33,
        'duo boss': 0.23,
        'duo full': 0.2,
        'duo flawless': 0.35,
        'solo boss': 0.3,
        'solo full': 0.9,
}


restrictions = {
    'VOG': ['solo full', 'solo boss'],
    'LW': ["duo full", "duo flawless", "solo boss", "solo full"],
    'GOS': ['duo full', 'duo flawless', 'solo full'],
    'DSC': ['solo boss', 'solo full'],
    'VOD': ['duo boss', 'duo full', 'duo flawless', 'solo boss', 'solo full'],
    "KF": ['duo full', "duo flawless", "solo full", "solo boss"],
    "RON": []
}


time_thresholds = {
    'DSC': 1079,   # Time threshold in minutes for the DSC raid
    'KF': 1572,    # Time threshold in minutes for the KF raid
    'VOD': 1784,   # Time threshold in minutes for the VOD raid
    'LW': 612,    # Time threshold in minutes for the LW raid
    'RON': 1102,  # Time threshold in minutes for the RON raid
    'GOS': 893,  # Time threshold in minutes for the GOS raid
    'VOG': 1355,   # Time threshold in minutes for the VOG raid
}


def get_raid_achievements(json_dump):
    all_achievements = {}
    for ite in json_dump['activities']:
        if 'activityHash' in ite and ite['activityHash'] in rh.raidHashes and ite['activityHash'] not in [1681562271, 4217492330, 2964135793, 2918919505]:
            data = ite
            raidHash = ite["activityHash"]
            raid = {
                "raidHash": raidHash,
                'values': {
                    'raidName': rh.raidHashes[raidHash],
                    'cleared': False,
                    'trio boss': False,
                    'trio full': False,
                    'trio flawless': False,
                    'duo boss': False,
                    'duo full': False,
                    'duo flawless': False,
                    'solo boss': False,
                    'solo full': False,
                    'time': None
                }
            }

            for activity in data['values']:
                if not raid["values"]['cleared'] and activity == 'fullClears' and data['values']['fullClears'] > 0:
                    raid["values"]['cleared'] = True
                    raid["values"]["time"] = data['values']["fastestFullClear"]['value']

                if isinstance(data['values'][activity], dict) or isinstance(data['values'][activity], list):
                    if activity == "flawlessActivities":
                    
                        for flawless in data['values'][activity]:
                            #check for duo flawless
                            if flawless['accountCount'] == 2 and (flawless["fresh"] or flawless['fresh'] is None):
                                raid["values"]["duo flawless"] = True
                                raid["values"]["duo boss"] = True
                                raid["values"]["duo full"] = True
                                raid["values"]["trio flawless"] = True
                                raid["values"]['trio full'] = True
                                raid["values"]["trio boss"] = True
                                break
                            
                            #check for trio flawless
                            if not raid["values"]['trio flawless'] and flawless['accountCount'] == 3 and (flawless["fresh"] or flawless['fresh'] is None):
                                raid["values"]["trio flawless"] = True
                                raid["values"]["trio boss"] = True
                                raid["values"]['trio full'] = True
                                continue
                            
                    if activity == "lowAccountCountActivities":
                        for LMC in data['values'][activity]:
                            #check for solo
                            if not raid["values"]['solo full'] and LMC['accountCount'] == 1:
                                raid["values"]["solo boss"] = True
                                raid["values"]["duo boss"] = True
                                raid["values"]['trio boss'] = True

                                #check for solo fresh
                                if LMC['fresh'] or LMC['fresh'] is None:
                                    raid["values"]["solo full"] = True
                                    raid["values"]["duo full"] = True
                                    raid["values"]["trio full"] = True
                                continue
                            
                            #check for duo
                            if not raid["values"]['duo full'] and LMC['accountCount'] == 2:
                                raid["values"]["duo boss"] = True
                                raid["values"]['trio boss'] = True

                                #check for duo fresh
                                if LMC['fresh'] or LMC['fresh'] is None:
                                    raid["values"]["duo full"] = True
                                    raid["values"]["trio full"] = True
                                continue
                            
                            #check for trio
                            if not raid["values"]['trio full'] and LMC['accountCount'] == 3:
                                if (LMC["fresh"] or LMC['fresh'] is None):
                                    raid['values']['trio full'] = True
                                raid["values"]['trio boss'] = True
            all_achievements[rh.raidHashes[raidHash]] = raid

    # UNCOMMENT TO PRINT A READABLE RAID DATA    
    #formatted_output = json.dumps(all_achievements, indent=4)
    #print(formatted_output)

    return all_achievements



def suggest_easiest_activities(raid_data):
    # Define the sorted achievements in ascending difficulty
    sorted_achievements = [
        'cleared',
        'trio boss',
        'trio full',
        'trio flawless',
        'time',
        'duo boss',
        'duo full',
        'duo flawless',
        'solo boss',
        'solo full'
    ]

    # Get a list of activities the user has not completed yet
    not_completed_activities = {raid_name: [key for key, value in data['values'].items() if value is False] for raid_name, data in raid_data.items()}

    # Filter out the restricted achievements
    for key, items_to_remove in restrictions.items():
        if key in not_completed_activities:
            not_completed_activities[key] = [item for item in not_completed_activities[key] if item not in items_to_remove] 

    suggested_activities = []
    # Iterate through the sorted achievements and find the first three available achievements
    for a in sorted_achievements:
        for r in not_completed_activities:
            if a in not_completed_activities[r]:
                suggested_activities.append((r, a))
                if len(suggested_activities) >= 3:
                    break  # We found three suggestions, no need to continue searching

    return suggested_activities[:3]



def get_grade(score):
    for threshold in GRADES:
        if score/threshold >= 1:
            return GRADES[threshold]
    return 'D-'



def get_score(jsonDump):
    raid_data = get_raid_achievements(jsonDump)

    total_score = 0
    for raid in raid_data.values():
        raid_name = raid["values"]['raidName']
        values = raid['values']
        for key, value in values.items():
            if value and key in score_mapping:
                if raid_name in restrictions and key in restrictions[raid_name]:
                    continue  # Skip this achievement if it's restricted
                total_score += score_mapping[key]

        if 'time' in values:
            if raid_name in time_thresholds and values['time'] <= time_thresholds[raid_name]:
                total_score += 0.35

    return (get_grade(total_score), suggest_easiest_activities(raid_data))