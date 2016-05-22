# ==============================================================
# Team Class
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since March 2, 2016
# ==============================================================
class Team:
    id = None
    name = None
    contact_person = None
    contact_number = None
    members = None
    members_count = None
    created_at = None
    updated_at = None
    deleted_at = None

    # expects a dictionary
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.contact_person = data['contact_person']
        self.contact_number = data['contact_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.deleted_at = data['deleted_at']

class TeamMember:
    id = None
    team_id = None
    full_name = None
    contact_number = None
    email = None
    active = None
    created_at = None
    updated_at = None
    deleted_at = None

    # expects a dictionary
    def __init__(self, data):
        self.id = data['id']
        self.team_id = data['team_id']
        self.full_name = data['full_name']
        self.contact_number = data['contact_number']
        self.email = data['email']
        self.active = data['active']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.deleted_at = data['deleted_at']
