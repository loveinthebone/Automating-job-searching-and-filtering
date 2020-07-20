# -*- coding: utf-8 -*-
"""
Created on Thursday Jul 16 2020

@author: kingson
"""
# Job Posts Screening

# In[] Import required libraries
import re
import string
import csv
from datetime import datetime

# In[] open the job posts csv file, save posts information to a list
def unpack_file(file_abs_path, date_string):
    data_list = []

    with open(file_abs_path, newline='', encoding="utf-8") as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row[2] != date_string:
                continue
            else:
                data_list.append(row)
    return data_list

# # Test:
# file_path = r'e:/Python3732/Scripts/web_scraping/daily_job_scraping_Kingson.csv'
# dateString = datetime.strftime(datetime.now(), '%Y_%m_%d') # date of today
# # print(dateString)
# date_string = dateString
# test = unpack_file(file_path,dateString)[0:3]


# In[] Compare the description string with the word cloud string, output score
def compare(post, word_cloud):
    description = post[4]
   
    # Convert all strings to lowercase
    text = description.lower()
    # Remove numbers
    text = re.sub(r'\d+','',text)
    # Remove punctuation
    text = text.translate(str.maketrans('','',string.punctuation))

    title = post[0]
    title = re.sub(r'\d+','',title)
    title_text = title.lower().translate(str.maketrans('','',string.punctuation))

    # Initialize a scores list and variables to save scores for different area
    scores =[]
    soft_skills = 0
    Mechanical_engineer = 0
    researcher = 0
    simulation = 0
    best = 0
    impossible = 0 # impossible words are those I don't want to have in the job post

    # Obtain the scores for each area
    for area in word_cloud.keys():
            
        if area == 'soft skills':
            for word in word_cloud[area]:
                if word in text:
                    soft_skills +=1
            scores.append(soft_skills)
            
        elif area == 'mechanical':
            for word in word_cloud[area]:
                if word in text:
                    Mechanical_engineer +=1
            scores.append(Mechanical_engineer)
            
        elif area == 'researcher':
            for word in word_cloud[area]:
                if word in text:
                    researcher +=1
            scores.append(researcher)
            
        elif area == 'simulation':
            for word in word_cloud[area]:
                if word in text:
                    simulation +=1
            scores.append(simulation)
            
        elif area == 'best':
            for word in word_cloud[area]:
                if word in text:
                    best +=10
            scores.append(best)
            
        else:
            for word in word_cloud[area]:
                if word in title_text:
                    impossible -= 100
            scores.append(impossible)

    # Also add a column of total scores    
    score_sum = sum([impossible, best, simulation, researcher, Mechanical_engineer, soft_skills])
    scores.append(score_sum)

    return scores

# # Test:
# description = """How will your job look as Team Lead / Mechatronics Designer?

# In our product development projects at R&D you and your team take responsibility for a unit or module in our products. You are focusing with your team on mechatronic topics like accurate positioning, media handling, fast and accurate motion or thermal control.


# Together with architects you specify and agree on requirements based on customer’s demands. After this you and your team to come up with technical designs and concepts that meet these objectives, properly balancing time, quality, performance, interdisciplinary interactions and taking cost into account.


# Within the project you collaborate with colleagues from other disciplines than mechanics and electronics, like embedded software and also chemistry and physics, who are mainly responsible for the ink and print head development. Together you review the ideas and jointly develop smart creative solutions that meet the overall project objectives. You test and review your model based design(s) by building prototypes to proof the feasibility of the routes you have identified.

# """
# test1 = compare(description, word_me())

# In[] Score descriptions according to the word cloud, and extend it to the list:
def update_list(data_list, word_cloud):
    for post in data_list:
        score = compare(post, word_cloud) # score is single number list, or a list of scores in different domain, and their sum
        post.extend(score)
    return data_list

# In[] Build a word cloud representing me
def word_me():

    word_cloud = {
            'soft skills':['creativity','innovation','concept','think outside the box','creative','proactive',
                                'organized', 'planning','plan','independent','listener','analytical','innovative','improvement',
                                'result-driven','enthusiasm','supportive','quality','optimize'
                                ],      
            
            'mechanical':['solidworks','inventor','autocad','machine','device',
                                    'machinery','maintenance','manufacture','machining','mechanics','precision',
                                    'mechanical','production','design',
                                    'concept','process','material','strength','fatigue','failure analysis',
                                    'stamp','punching','sensor','electronics','microcontroller','arduino','driver',
                                    'motor','coil','vibration','acoustic','strength','motion', 'piezo','piezoelectric','electric',
                                    'root cause', 'actuator','prototypes','equipment','mechanical engineer','project engineer',
                                    'desugn engineer','system','tolerance','technician', 'drawings','feasibility','product','products','testing',
                                    '3d modeling','automation','handson','testing','testing','testing','pwm','pid','technology'],
            
            'researcher':['photoacoustic','optics','light','interferometers','interferometer','interferometry',
                            'technology','photonic','optical','spectroscopy','equipment','development','research',
                            'sensor','sensors', 'data analysis','python', 'theory','proposal',
                            'matlab','comsol','labview','acoustic','sensitive','stability',
                            'response time','linearity','sensing','temperature','pressure','fiber','laser',
                            'near infrared','power transformer','co2','iot','device',
                            'material','validation','prototypes','data processing','physical ','feasibility ','measurement',
                            'setup','theoretical','boundary','applied physics', 'phd','experiments','literature','publication',
                            'conference','characterization','analysis','absorption','experiment','nir','wavelength',# NIR
                            'modulation','intensity','amplifier','signal','rd' # R&D
                            ,'noise','techniques','microscope','metrology','measurements','scientist', 'complex','postdoc',
                            'modeling', 'academic','thermal','scientific','gas','calibration'],
            
            'simulation':['comsol','finite element analysis','fea','fem','acoustic','simulation',
                                'modeling','thermal','vibration','amplitude','deformation','strength','modeling',
                                'python'],

            'best':['gas','sensor','photoacoustic','power transformer', 'absorption','spectroscopy','miniaturized','fiber optics','comsol'],
            
            'impossible':['phd','professor','internship']
            }
    return word_cloud

# In[] execution
word_cloud = word_me()
file_abs_path = r'e:/Python3732/Scripts/web_scraping/daily_job_scraping_Kingson.csv'
date_string = datetime.strftime(datetime.now(), '%Y_%m_%d') # date of today
data_list = unpack_file(file_abs_path, date_string)
updated_list = update_list(data_list, word_cloud)

# # Test:
# print(updated_list[0][1])
updated_list.sort(key=lambda x:-x[-1]) #sort by the total score descend.

new_file_path = r'e:/Python3732/Scripts/web_scraping/daily_job_scraping_Kingson_scored.csv'
with open(new_file_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(updated_list)
print("job posts sorting finished!")
    
#In[] open the top job posts in browser
import webbrowser
import time

for i in range(3):
    # os.startfile(updated_list[i][3])
    webbrowser.open(updated_list[i][3], new=1)
    time.sleep(1)
