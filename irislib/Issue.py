# ==============================================================
# Issue Class
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since February 27, 2016
# ==============================================================
class Issue:
    id = None
    category = None
    category_name = None
    location = None
    date_happened = None
    details = None
    full_name = None
    email = None
    contact_number = None
    user_id = None
    source = None
    created_at = None
    updated_at = None
    deleted_at = None
    status = None
    priority = None
    assigned_team = None

    # expects a dictionary
    def __init__(self, data):
        self.id = data['id']
        self.category = data['category']
        self.category_name = data['category_name']
        self.location = data['location']
        self.date_happened = data['date_happened']
        self.details = data['details']
        self.full_name = data['full_name']
        self.email = data['email']
        self.contact_number = data['contact_number']
        self.user_id = data['user_id']
        self.source = data['source']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.deleted_at = data['deleted_at']
        self.status = data['status']
        self.priority = data['priority']
        self.assigned_team = data['assigned_team']
        self.team_id = data['team_id']

