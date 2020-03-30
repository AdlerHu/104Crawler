import os

path = './skill'

# To get each skill txt
file_list = os.listdir(path)

skills_list = []

# To get all skills from skill's txt
for file_name in file_list:
    with open(path + '/' + file_name, 'r', encoding='utf-8') as f:

        for skill in f.read().split(','):
            if skill != '':
                skills_list.append(skill)

# create a dictionary for skills
skills_dict = {}
for skill in skills_list:

    if skill in skills_dict:
        skills_dict[skill] += 1
    else:
        skills_dict[skill] = 1

# sort the dictionary
tmp_list = []
for i in skills_dict:
    tmp_list.append((i, skills_dict[i]))

tmp_list.sort(key=lambda x: x[1], reverse=True)
print(tmp_list)