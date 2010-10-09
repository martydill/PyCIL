
class Variable(object):

    def __init__(self, value = None, type = None, alias = None):
        self.name = 'unnamed'
        self.value = value
        self.type = type
        self.alias = alias
        
    def __str__(self):
        return str(self.value) + ' - ' + str(self.type)


