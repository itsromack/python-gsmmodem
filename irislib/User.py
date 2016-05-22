# ==============================================================
# User Class
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since February 27, 2016
# ==============================================================
class User:
    id = None
    level = None
    full_name = None
    login = None
    password = None
    contact_number = None
    created_at = None
    updated_at = None
    deleted_at = None

    # expects a dictionary
    def __init__(self, data):
        self.id = data['id']
        self.level = data['level']
        self.full_name = data['full_name']
        self.login = data['login']
        self.password = data['password']
        self.contact_number = data['contact_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.deleted_at = data['deleted_at']
