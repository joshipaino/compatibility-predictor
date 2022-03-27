#! /usr/bin/env python3

# Datahouse Take-Home Project / Coding Assessment
# Joshua Paino
# This program takes as input a JSON file and calculates a score for the included applicants.  The output is then printed out in JSON.

import sys
import json
from statistics import median

# retrieve input and load its data
with open(sys.argv[1]) as input:
    data = json.load(input)

# set variables which will be used to store the team's stats and compute average as well median
teamInt = []
teamStr = []
teamEnd = []
teamSpc = []
totalTeamInt = 0
totalTeamStr = 0
totalTeamEnd = 0
totalTeamSpc = 0
teamMemberCount = len(data['team'])

# iterate through the team array to gather the sum of each attribute
for teamMember in data['team']:
    teamInt.append(teamMember['attributes']['intelligence'])
    teamStr.append(teamMember['attributes']['strength'])
    teamEnd.append(teamMember['attributes']['endurance'])
    teamSpc.append(teamMember['attributes']['spicyFoodTolerance'])
    totalTeamInt += teamMember['attributes']['intelligence']
    totalTeamStr += teamMember['attributes']['strength']
    totalTeamEnd += teamMember['attributes']['endurance']
    totalTeamSpc += teamMember['attributes']['spicyFoodTolerance']

# compute average of each stat within the team
avgTeamInt = totalTeamInt / teamMemberCount
avgTeamStr = totalTeamStr / teamMemberCount
avgTeamEnd = totalTeamEnd / teamMemberCount
avgTeamSpc = totalTeamSpc / teamMemberCount

# class that will be used to compute score of each applicant
class applicantAttributes:
    def __init__(self, name, int, str, end, spc):
        self.name = name
        self.int = int
        self.str = str
        self.end = end
        self.spc = spc
        self.teamMembersPlusApplicant = len(data['team']) + 1

    def compute(self):
        score = 0

        totalTeamIntPlusApplicant = totalTeamInt + self.int
        avgTeamIntPlusApplicant = totalTeamIntPlusApplicant / self.teamMembersPlusApplicant

        totalTeamStrPlusApplicant = totalTeamStr + self.str
        avgTeamStrPlusApplicant = totalTeamStrPlusApplicant / self.teamMembersPlusApplicant

        totalTeamEndPlusApplicant = totalTeamEnd + self.end
        avgTeamEndPlusApplicant = totalTeamEndPlusApplicant / self.teamMembersPlusApplicant

        totalTeamSpcPlusApplicant = totalTeamSpc + self.spc
        avgTeamSpcPlusApplicant = totalTeamSpcPlusApplicant / self.teamMembersPlusApplicant

        # If the new applicant's attribute increases the team's 
        # average or is greater than or equal to team's median value, add to the score where 
        # each attribute has different weights based on relavency in contributing to innovative 
        # technological projects.  

        if (avgTeamIntPlusApplicant >= avgTeamInt or self.int >= median(teamInt)):
            score += 0.4

        if (avgTeamStrPlusApplicant >= avgTeamStr or self.str >= median(teamStr)):
            score += 0.2

        if (avgTeamEndPlusApplicant >= avgTeamEnd or self.end >= median(teamEnd)):
            score += 0.3

        if (avgTeamSpcPlusApplicant >= avgTeamSpc or self.spc >= median(teamSpc)):
            score += 0.1

        return score

# Initialize object that will hold the applicants and their scores
computedApplicants = {
    "scoredApplicants": []
}

# iterate through the array containing the applicants and compute their scores
for applicant in data['applicants']:
    applicantInfo = applicantAttributes(
        applicant['name'],
        applicant['attributes']['intelligence'],
        applicant['attributes']['strength'],
        applicant['attributes']['endurance'], 
        applicant['attributes']['spicyFoodTolerance'])
    calculatedScore = applicantInfo.compute()
    output = {
        "name": applicant['name'],
        "score": round(calculatedScore, 2)
    }
    computedApplicants['scoredApplicants'].append(output)

# output the computed score in JSON format
print(json.dumps(computedApplicants, indent=2))
