import configparser


class ConfigParserInstance:
    obj = None

    @staticmethod
    def getInstance():
        if not ConfigParserInstance.obj:
            ConfigParserInstance.obj = configparser.RawConfigParser()
        return ConfigParserInstance.obj


class SaveLoadMixin:
    def getParser(self):
        return ConfigParserInstance.getInstance()

    def save(self, **kwargs):
        raise NotImplementedError("Save method is not implemented")
