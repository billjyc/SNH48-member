# coding=utf-8

class Helper:
    def __init__(self):
        print 'helper'

    def process_item_team(self, team):
        team = team.strip()
        print team
        if team == 'SNH48  S队（TEAM SII）'.strip():
            return 1
        elif team == 'SNH48  N队（TEAM NII）'.strip():
            return 2
        elif team == 'SNH48  H队（TEAM HII）'.strip():
            return 3
        elif team == 'SNH48  X队（TEAM X）'.strip():
            return 4
        elif team == 'SNH48 XII队（TEAM XII）'.strip():
            return 5
        return 0
