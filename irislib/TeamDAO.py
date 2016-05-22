# ==============================================================
# Team Data Access Object
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since February 27, 2016
# ==============================================================
from Team import Team, TeamMember
from datetime import date
from flask import Response, json
import _mysql

class TeamDAO:
    db = False

    def __init__(self, db):
        self.db = db

    def result_to_teams(self, result):
        teams = []
        for row in result:
            team = Team(row)
            team.members = self.get_members(team.id)
            team.members_count = len(team.members)
            teams.append(team)
        return teams

    def result_to_team_members(self, result):
        members = []
        for row in result:
            member = TeamMember(row)
            members.append(member)
        return members

    # expects a Team object
    def create(self, teamObject=None):
        if teamObject != None:
            sql = 'INSERT INTO response_teams ' \
                  'SET name = "%s", ' \
                  'contact_person = "%s", ' \
                  'contact_number = "%s"' % (
                _mysql.escape_string(teamObject.name),
                _mysql.escape_string(teamObject.contact_person),
                _mysql.escape_string(teamObject.contact_number)
            )
            self.db.cursor.execute(sql)
            # if teamObject['members'] != None:
            #     self.add_team_members(teamObject['members'])
            return True
        return False

    def update(self, teamObject=None):
        if teamObject != None:
            sql = 'UPDATE response_teams SET ' \
                  ' name = "%s", ' \
                  ' contact_person = "%s", ' \
                  ' contact_number = "%s", ' \
                  ' updated_at = "%s" ' \
                  'WHERE id = %d' % (
                      teamObject.name,
                      teamObject.contact_person,
                      teamObject.contact_number,
                      teamObject.updated_at,
                      teamObject.id
                  )
            # print sql
            # if teamObject['members'] != None:
            #     self.update_members(teamObject['members'])
            self.db.cursor.execute(sql)
            return True
        return False

    def add_team_member(self, memberObject=None):
        print memberObject.full_name
        if memberObject != None:
            sql = 'INSERT INTO response_team_members SET ' \
                  ' full_name = "%s", ' \
                  ' contact_number = "%s", ' \
                  ' email = "%s",' \
                  ' team_id = %d' % (
                _mysql.escape_string(memberObject.full_name),
                _mysql.escape_string(memberObject.contact_number),
                _mysql.escape_string(memberObject.email),
                memberObject.team_id
            )
            self.db.cursor.execute(sql)
            return True
        return False

    def update_members(self, members):
        for member in members:
            self.update_member(member)

    def update_member(self, member):
        now = date.today()
        member.updated_at = now.strftime('%Y-%m-%d %H:%M:%S')
        sql = 'UPDATE response_team_members SET ' \
              ' full_name = "%s", ' \
              ' contact_number = "%s", ' \
              ' email = "%s", ' \
              ' active = %d, ' \
              ' updated_at = "%s" ' \
              'WHERE id = %d' % (member.full_name, member.contact_number, member.email, member.active, member.updated_at, member.id)

    def delete(self, team_id=None):
        if team_id != None:
            now = date.today()
            updated_at = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE response_teams SET deleted_at = "%s" WHERE id = %d' % (updated_at, team_id)
            self.db.cursor.execute(sql)
            self.delete_team_members(team_id)
            return True
        return False

    def delete_team_members(self, team_id=None):
        if team_id != None:
            now = date.today()
            updated_at = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE response_team_members SET deleted_at = "%s" ' \
                  'WHERE team_id = "%s"' % (now, team_id)
            self.db.cursor.execute(sql)
            return True
        return False

    def all(self):
        sql = 'SELECT t.*, COUNT(m.id) as number_of_members ' \
              'FROM response_teams t ' \
              'LEFT JOIN response_team_members m ON (t.id=m.team_id) ' \
              'WHERE t.deleted_at IS NULL ' \
              'GROUP BY t.id '
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_teams(result)

    def teams(self):
        sql = 'SELECT * FROM response_teams WHERE deleted_at IS NULL'
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_teams(result)

    def get_by_id(self, id):
        sql = 'SELECT * FROM teams WHERE id = %d AND deleted_at IS NULL' % id
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            team = Team(row)
            team.members = self.get_members(team.id)
            return team
        return False

    def get_by_name(self, name):
        sql = 'SELECT * FROM response_teams WHERE name = "%s" AND deleted_at IS NULL LIMIT 1' % name
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            team = Team(row)
            team.members = self.get_members(team.id)
            return team
        return False

    def get_members(self, team_id):
        sql = 'SELECT m.* ' \
              'FROM response_teams t ' \
              'JOIN response_team_members m ON (t.id=m.team_id) ' \
              'WHERE t.id = %d ' \
              ' AND t.deleted_at IS NULL ' \
              ' AND m.deleted_at IS NULL' % (team_id)
        # print sql
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return result
