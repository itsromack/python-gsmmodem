# ==============================================================
# User Data Access Object
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since February 27, 2016
# ==============================================================
from ResponseTeam import ResponseTeam
from datetime import date

class ResponseTeamDAO:
    db = False

    def __init__(self, db):
        self.db = db

    def result_to_teams(self, result):
        teams = []
        for row in result:
            team = ResponseTeam(row)
            teams.append(team)
        return teams

    # expects a ResponseTeam object
    def create(self, teamObject=None):
        if teamObject != None:
            sql = 'INSERT INTO response_teams ' \
                  'SET name = "%s"' % (
                teamObject['name']
            )
            self.db.cursor.execute(sql)
            return True
        return False

    def update(self, teamObject=None):
        if teamObject != None:
            now = date.today()
            teamObject['updated_at'] = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE response_teams ' \
                  'SET name = "%s", ' \
                  'updated_at = "%s"' % (
                teamObject['level'],
                teamObject['updated_at']
            )
            return True
        return False

    def delete(self, user_id=None):
        if user_id != None:
            now = date.today()
            updated_at = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE response_teams SET deleted_at = "%s" WHERE id = %d' % (updated_at, user_id)
            self.db.cursor.execute(sql)
            return True
        return False

    def all(self):
        sql = 'SELECT * FROM response_teams WHERE deleted_at IS NULL'
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_teams(result)

    def get_by_id(self, id):
        sql = 'SELECT * FROM response_teams WHERE id = %d AND deleted_at IS NULL' % id
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return ResponseTeam(row)
        return False

    def get_by_name(self, name):
        sql = 'SELECT * FROM response_teams WHERE name = "%s" AND deleted_at IS NULL LIMIT 1' % name
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return ResponseTeam(row)
        return False

    def get_members(self, team_id):
        sql = 'SELECT m.full_name, m.contact_number, m.email, m.active ' \
              'FROM response_teams t ' \
              'JOIN response_team_members m ON (t.id=m.response_team_id)' \
              'WHERE t.id = %d ' \
              'AND t.deleted_at IS NULL ' \
              'AND m.deleted_at IS NULL' % (team_id)