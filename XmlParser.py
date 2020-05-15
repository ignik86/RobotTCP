import xml.etree.ElementTree as ET


class ConfigParse:
    def __init__(self, file):
        super(self.__class__, self).__init__()
        self.tree = ET.parse(file)
        self.root = self.tree.getroot()

    def ip(self):
        ret = self.tree.find('server').get('ip')
        return ret

    def port(self):
        ret = int(self.tree.find('server').get('port'))
        return ret

    def logopicture(self):
        ret = self.tree.find('logo').get('file')
        return ret

    def logotext(self):
        ret = self.tree.find('logo').get('logotext')
        return ret

