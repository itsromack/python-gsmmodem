# ==============================================================
# Issue Category Class
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since March 12, 2016
# ==============================================================
class Category:
    id = None
    name = None
    active = None

    # expects a dictionary
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.active = data['active']
