import json
import math
import os
import docx
import random

import pandas as pd

random.seed(42)

def get_prompt():
    prompt_path = 'student_prompt.docx'
    file = docx.Document(prompt_path)
    texts = []
    for para in file.paragraphs:
        texts.append(para.text)
    texts = [t for t in texts if t != '']
    prompt = '\n'.join(texts)
    return prompt


def set_student_profile(profile_num=3,prior_know=None):
    names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Charles", "Sarah", "Thomas", "Karen"]

    majors = {
        0: 'Computer Science',
        1: 'Psychology',
        2: 'Biology',
        3: 'Chemistry',
        4: 'Physics',
        5: 'Mathematics',
        6: 'History',
        7: 'Literature',
        8: 'Political Science',
        9: 'Economics',
        10: 'Sociology',
        11: 'Business Administration',
        12: 'Engineering',
        13: 'Environmental Science',
        14: 'Nursing'
    }

    styles = {
        0: 'Encouraging: This style involves affirming others’ contributions to boost morale and foster a positive atmosphere.',
        1: 'Critical: This style focuses on evaluating ideas rigorously, asking tough questions and providing constructive feedback.',
        2: 'Analytical: This approach emphasizes data and logical reasoning, focusing on evidence to support arguments.',
        3: 'Narrative: This style involves telling stories or sharing personal experiences to illustrate points and engage the audience.',
        4: 'Suggestive: This style offers ideas and alternatives for consideration, encouraging exploration of different options.',
        5: 'Inquisitive: This approach involves asking open-ended questions to stimulate discussion and invite participation.',
        6: 'Summarizing: This style distills key points from the discussion to ensure clarity and understanding among participants.',
        7: 'Collaborative: This approach focuses on building consensus and fostering teamwork among group members.',
        8: 'Humorous: This style uses humor to lighten the mood and create a more relaxed and engaging environment.',
        9: 'Emotional: This approach connects with participants on a personal level, expressing feelings and values related to the topic.'
    }

    Virtual_Student = {
        'age': {0: '12-18', 1: '18-24', 2: '25-31', 3: '32-38', 4: '> 39'},
        'gender': {0: 'female', 1: 'male', 2: 'others'},
        'majors': majors,
        'education': {0: 'high school', 1: 'undergraduate', 2: 'master', 3: 'doctor'},
        'attitude': {0: 'very motivated', 1: 'not motivated'},
        'exam': {0: 'high GPA', 1: 'low GPA'},
        'focus': {0: 'focused', 1: 'absent-minded'},
        'curiosity': {0: 'curious', 1: 'not curious'},
        'interest': {0: 'interested', 1: 'not interested'},
        'compliance': {0: 'well-behaved', 1: 'struggling'},
        'smartness': {0: 'smart', 1: 'not smart'},
        'family': {0: 'strong academic', 1: 'not care about education'},
        'goal commitment': {0: 'high', 1: 'medium', 2: 'low'},
        'self-efficacy': {0: 'high', 1: 'medium', 2: 'low'},
        'social pressure': {0: 'high', 1: 'medium', 2: 'low'},
        'sentiment': {0: 'positive', 1: 'neutral', 2: 'negative'},
        'speaking style': styles,
        'prior knowledge to this topic': ''
    }

    name_record = []
    profile_record = []
    profiles = {}
    for profile_id in range(profile_num):
        student_prompt = get_prompt()
        random_name = random.choice(names)

        ##剔除相同的name
        while random_name in name_record:
            random_name = random.choice(names)

        name_record.append(random_name)
        student_prompt = student_prompt.replace('{name}', random_name)

        main_traits = {}
        for trait,trait_options in Virtual_Student.items():
            ## only one option
            if trait == 'prior knowledge to this topic':
                # random_flag = random.randint(0,1)
                # if random_flag == 0: ## support
                #     options_list = prior_know['support_list']
                # elif random_flag == 1:
                #     options_list = prior_know['attack_list']
                # selected_options = random.choices(options_list,k=math.floor(len(options_list)/2))
                # main_traits[trait] = selected_options
                main_traits[trait] = ''
            elif trait == 'majors':
                random_number = random.randint(0, len(trait_options) - 1)
                options = random.choices(list(range(len(trait_options))), k=random_number)
                majors_temp = {}
                for opt in options:
                    majors_temp[opt] = majors[opt]
                main_traits[trait] = majors_temp
            else:
                random_number = random.randint(0, len(trait_options)-1)
                main_traits[trait] = {random_number: trait_options[random_number]}

        main_traits.pop('prior knowledge to this topic')
        main_traits_str = json.dumps(main_traits).replace('},', '},\n')

        ## 剔除相同的profile
        while main_traits_str in profile_record:
            for trait, trait_options in Virtual_Student.items():
                ## only one option
                if trait != 'majors':
                    random_number = random.randint(0, len(trait_options) - 1)
                    main_traits[trait] = {random_number: trait_options[random_number]}
                else:
                    random_number = random.randint(0, len(trait_options) - 1)
                    options = random.choices(list(range(len(trait_options))), k=random_number)
                    majors_temp = {}
                    for opt in options:
                        majors_temp[opt] = majors[opt]
                    main_traits[trait] = majors_temp

        profile_record.append(main_traits_str)
        main_traits_str = json.dumps(main_traits).replace('},', '},\n')
        student_prompt = student_prompt.replace('{profile}', main_traits_str)
        profiles[profile_id] = student_prompt

    # 添加先验态度和知识
    for pro_id,profile in profiles.items():
        random_flag = random.randint(0, 1)
        if random_flag == 0: ## support
            options_list = prior_know['support_list']
            prior_att = 'support'
        elif random_flag == 1:
            options_list = prior_know['attack_list']
            prior_att = 'attack'
        selected_options = random.choices(options_list,k=math.floor(len(options_list)/2))
        profiles[pro_id] = profiles[pro_id].replace('{*attitude*}', prior_att)
        profiles[pro_id] = profiles[pro_id].replace('{*prior knowledge list*}', str(selected_options))

    return profiles

if __name__ == '__main__':
    questions_json = json.load(open('new_questions.json','r',encoding='utf-8'))

    row = 0
    multi_agent_interaction_recording = pd.DataFrame(columns=['room_id','topic','person_num','role_0','role_1','role_2','role_3','role_4'])
    for i,d_json in enumerate(questions_json):
        que = d_json['question']
        if que.strip() != '':
            person_num = random.randint(2,5)
            profiles = set_student_profile(profile_num=person_num,prior_know=d_json)
            multi_agent_interaction_recording.at[row,'room_id'] = row
            multi_agent_interaction_recording.at[row,'topic'] = que
            multi_agent_interaction_recording.at[row,'person_num'] = person_num
            for role_id, profile in profiles.items():
                multi_agent_interaction_recording.at[row,f'role_{role_id}'] = profile
            row = row + 1

        # if row == 9:
        #     break

    multi_agent_interaction_recording['label'] = 'testing'
    multi_agent_interaction_recording.to_excel('multi_agent_interaction_testing.xlsx',index=False)