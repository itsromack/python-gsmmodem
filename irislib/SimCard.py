class SimCard:
    """ SimCard Class  """
    number = ''
    network_name = ''
    active = False

    def __init__(self, number, network_name):
        self.number = number
        self.network_name = network_name

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
