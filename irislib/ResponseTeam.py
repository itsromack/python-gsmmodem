# ==============================================================
# ResponseTeam Class
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since February 27, 2016
# ==============================================================
class ResponseTeam:
    id = None
    name = None
    created_at = None
    updated_at = None
    deleted_at = None

    # expects a dictionary
    def __init__(self, data):
        self.id = data['id']
        self.name = data['level']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.deleted_at = data['deleted_at']
