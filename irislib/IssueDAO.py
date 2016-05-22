# ==============================================================
# Issue Data Access Object
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since February 27, 2016
# ==============================================================
from Issue import Issue
from datetime import date
import _mysql

class IssueDAO:
    db = False

    def __init__(self, db):
        self.db = db

    def result_to_issues(self, result):
        issues = []
        for row in result:
            issue = Issue(row)
            issues.append(issue)
        return issues

    # expects a Issue object
    def create(self, issueObject=None):
        if issueObject != None:
            sql = 'INSERT INTO issues ' \
                  'SET category = %d' % issueObject.category
            if issueObject.location != None: sql = '%s, location = "%s"' % (sql, _mysql.escape_string(issueObject.location))
            if issueObject.date_happened != None: sql = '%s, date_happened = "%s"' % (sql, _mysql.escape_string(issueObject.date_happened))
            if issueObject.details != None: sql = '%s, details = "%s"' % (sql, _mysql.escape_string(issueObject.details))
            if issueObject.full_name != None: sql = '%s, full_name = "%s"' % (sql, _mysql.escape_string(issueObject.full_name))
            if issueObject.email != None: sql = '%s, email = "%s"' % (sql, _mysql.escape_string(issueObject.email))
            if issueObject.user_id != None: sql = '%s, user_id = "%s"' % (sql, _mysql.escape_string(issueObject.user_id))
            if issueObject.contact_number != None: sql = '%s, contact_number = "%s"' % (sql, _mysql.escape_string(issueObject.contact_number))
            if issueObject.source != None: sql = '%s, source = "%s"' % (sql, _mysql.escape_string(issueObject.source))
            self.db.cursor.execute(sql)
            # create issue_status record
            issueObject.id = self.db.cursor.lastrowid
            self.set_status(issueObject)
            return issueObject
        return False

    def create_from_sms(self, detail, sender):
        sql = 'INSERT INTO issues SET ' \
              'details = "%s", ' \
              'contact_number = "%s", ' \
              'source="sms",' \
              'category=4' % (detail, sender)
        self.db.cursor.execute(sql)
        issue_id = self.db.cursor.lastrowid
        sql = 'INSERT INTO issue_statuses ' \
              'SET issue_id=%d' % issue_id
        self.db.cursor.execute(sql)
        return True

    def update(self, issueObject=None):
        if issueObject != None:
            now = date.today()
            issueObject.updated_at = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE issues SET ' \
                  ' category = %d, ' \
                  ' location = "%s", ' \
                  ' date_happened = "%s", ' \
                  ' details = "%s", ' \
                  ' full_name = "%s", ' \
                  ' email = "%s", ' \
                  ' contact_number = "%s", ' \
                  ' user_id = %d, ' \
                  ' source = "%s"' \
                  'WHERE id = %d' % (
                issueObject['category'],
                _mysql.escape_string(issueObject['location']),
                issueObject['date_happened'],
                _mysql.escape_string(issueObject['details']),
                _mysql.escape_string(issueObject['full_name']),
                _mysql.escape_string(issueObject['email']),
                _mysql.escape_string(issueObject['contact_number']),
                issueObject['user_id'],
                _mysql.escape_string(issueObject['source']),
                issueObject['id']
            )
            self.db.cursor.execute(sql)
            return True
        return False

    def update_status(self, status):
        if self.has_issue_status(status.issue_id) != False:
            if status.priority == None:
                sql = 'UPDATE issue_statuses ' \
                      'SET status = "%s" ' \
                      'WHERE issue_id = %d' % (status.status, status.issue_id)
                if status.assigned_team != None:
                    sql = 'UPDATE issue_statuses ' \
                          'SET status = "%s", ' \
                          ' assigned_team = %d ' \
                          'WHERE issue_id = %d' % (status.status, status.assigned_team, status.issue_id)
            else:
                sql = 'UPDATE issue_statuses ' \
                      'SET status = "%s", ' \
                      ' priority = "%s" ' \
                      'WHERE issue_id = %d' % (status.status, status.priority, status.issue_id)
                if status.assigned_team != None:
                    sql = 'UPDATE issue_statuses ' \
                          'SET status = "%s", ' \
                          ' priority = "%s", ' \
                          ' assigned_team = %d ' \
                          'WHERE issue_id = %d' % (status.status, status.priority, status.assigned_team, status.issue_id)
            self.db.cursor.execute(sql)
            return True
        else:
            return self.set_status(status)

    def set_status(self, status):
        status.priority = str(status.priority)
        status.assigned_team = int(status.assigned_team)
        # Only NEW issue_ids are
        if self.has_issue_status(status.id) != False:
            return self.update_status(status)
        # Insert now
        if status.priority == None:
            sql = 'INSERT INTO issue_statuses ' \
                  'SET issue_id = %d' % status.id
            if status.assigned_team != None:
                sql = 'INSERT INTO issue_statuses ' \
                      'SET assigned_responder = %d, ' \
                      ' issue_id = %d' % (status.assigned_team, status.id)
        else:
            sql = 'INSERT INTO issue_statuses ' \
                  'SET priority = "%s", ' \
                  ' issue_id = %d' % (status.priority, status.id)
            if status.assigned_team != None:
                sql = 'INSERT INTO issue_statuses ' \
                      'SET priority = "%s", ' \
                      ' assigned_responder = %d, ' \
                      ' issue_id = %d ' % (status.priority, status.assigned_team, status.id)
        self.db.cursor.execute(sql)
        return True

    def has_issue_status(self, issue_id):
        sql = 'SELECT * FROM issue_statuses WHERE issue_id = %d AND deleted_at IS NULL' % issue_id
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return True
        return False

    def delete(self, issue_id=None):
        if issue_id != None:
            now = date.today()
            updated_at = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE issues ' \
                  'SET deleted_at = "%s" ' \
                  'WHERE id = %d' % (updated_at, issue_id)
            self.db.cursor.execute(sql)
            return True
        return False

    def all(self, scope=None):
        sql = 'SELECT i.*,' \
              ' c.name AS category_name,' \
              ' s.status,' \
              ' s.priority, ' \
              ' t.id AS team_id, ' \
              ' t.name AS assigned_team ' \
              'FROM issues i ' \
              'JOIN issue_statuses s ON (i.id=s.issue_id) ' \
              'JOIN categories c ON (i.category=c.id) ' \
              'LEFT JOIN response_teams AS t ON (t.id=s.assigned_responder) ' \
              'WHERE i.deleted_at IS NULL '
        if scope != None:
            if scope == 'today':
                sql = '%s AND i.date_happened LIKE CONCAT(CURDATE(), "%%") ' % sql
            elif scope == 'week':
                sql = '%s AND WEEK(CURDATE()) = WEEK(i.date_happened) ' % sql
            elif scope == 'month':
                sql = '%s AND MONTH(CURDATE()) = MONTH(i.date_happened) ' % sql
            elif scope == 'year':
                sql = '%s AND YEAR(CURDATE()) = YEAR(i.date_happened) ' % sql
            elif scope == 'new':
                sql = '%s AND s.status = "new" ' % sql
            elif scope == 'in_progress':
                sql = '%s AND s.status = "in_progress" ' % sql
            elif scope == 'complete':
                sql = '%s AND s.status = "complete" ' % sql
            elif scope == 'fraud':
                sql = '%s AND s.status = "fraud" ' % sql
            elif scope == 'duplicate':
                sql = '%s AND s.status = "duplicate" ' % sql
            elif scope == 'all issues':
                print 'all issues'
        sql = '%s ORDER BY i.date_happened DESC' % sql
        print sql
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_by_id(self, id):
        sql = 'SELECT * FROM issues WHERE id = %d AND deleted_at IS NULL' % id
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return Issue(row)
        return False

    def get_by_category_name(self, category_name):
        sql = 'SELECT i.* FROM issues i ' \
              'JOIN categories c ON (i.category=c.id) ' \
              'WHERE c.name = "%s" ' \
              ' AND active = 1 ' \
              ' AND i.deleted_at IS NULL' % category_name
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_by_date_happened(self, date_happpened):
        sql = 'SELECT * FROM issues WHERE date_happened = "%s" AND deleted_at IS NULL' % date_happpened
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_by_full_name(self, full_name):
        sql = 'SELECT * FROM issues WHERE full_name = "%s" AND deleted_at IS NULL' % full_name
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_by_email(self, email):
        sql = 'SELECT * FROM issues WHERE email = "%s" AND deleted_at IS NULL' % email
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_by_contact_number(self, contact_number):
        sql = 'SELECT * FROM issues WHERE contact_number = "%s" AND deleted_at IS NULL' % contact_number
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_by_user_id(self, user_id):
        sql = 'SELECT * FROM issues WHERE user_id = %d AND deleted_at IS NULL' % user_id
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_by_source(self, source):
        sql = 'SELECT * FROM issues WHERE source = "%s" AND deleted_at IS NULL' % source
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_by_status(self, status):
        sql = 'SELECT i.* FROM issues i' \
              'JOIN issue_statuses s ON (i.id=s.issue_id) ' \
              'WHERE s.status = "%s" ' \
              ' AND i.deleted_at IS NULL' % status
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        return self.result_to_issues(result)

    def get_stats(self):
        stats = dict()
        stats['today'] = self.count_issues_today()
        stats['new_issues'] = self.count_new_issues()
        stats['in_progress_issues'] = self.count_in_progress_issues()
        stats['complete_issues'] = self.count_complete_issues()
        stats['fraud_issues'] = self.count_fraud_issues()
        stats['duplicate_issues'] = self.count_duplicate_issues()
        stats['week'] = self.count_issues_this_week()
        stats['month'] = self.count_issues_this_month()
        stats['year'] = self.count_issues_this_year()
        return stats

    def count_issues_today(self):
        sql = 'SELECT COUNT(id) issues_count FROM issues ' \
              'WHERE date_happened LIKE CONCAT(CURDATE(), "%") ' \
              ' AND deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']

    def count_new_issues(self):
        sql = 'SELECT COUNT(i.id) issues_count FROM issues i ' \
              'JOIN issue_statuses s ON (i.id=s.issue_id) ' \
              'WHERE s.status = "new" ' \
              ' AND i.deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']

    def count_in_progress_issues(self):
        sql = 'SELECT COUNT(i.id) issues_count FROM issues i ' \
              'JOIN issue_statuses s ON (i.id=s.issue_id) ' \
              'WHERE s.status = "in progress" ' \
              ' AND i.deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']

    def count_complete_issues(self):
        sql = 'SELECT COUNT(i.id) issues_count FROM issues i ' \
              'JOIN issue_statuses s ON (i.id=s.issue_id) ' \
              'WHERE s.status = "complete" ' \
              ' AND i.deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']

    def count_fraud_issues(self):
        sql = 'SELECT COUNT(i.id) issues_count FROM issues i ' \
              'JOIN issue_statuses s ON (i.id=s.issue_id) ' \
              'WHERE s.status = "fraud" ' \
              ' AND i.deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']

    def count_duplicate_issues(self):
        sql = 'SELECT COUNT(i.id) issues_count FROM issues i ' \
              'JOIN issue_statuses s ON (i.id=s.issue_id) ' \
              'WHERE s.status = "duplicate" ' \
              ' AND i.deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']

    def count_issues_this_week(self):
        sql = 'SELECT COUNT(id) issues_count FROM issues ' \
              'WHERE WEEK(CURDATE()) = WEEK(date_happened) ' \
              ' AND deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']

    def count_issues_this_month(self):
        sql = 'SELECT COUNT(id) issues_count FROM issues ' \
              'WHERE MONTH(CURDATE()) = MONTH(date_happened) ' \
              ' AND deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']

    def count_issues_this_year(self):
        sql = 'SELECT COUNT(id) issues_count FROM issues ' \
              'WHERE YEAR(CURDATE()) = YEAR(date_happened) ' \
              ' AND deleted_at IS NULL'
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        return row['issues_count']
