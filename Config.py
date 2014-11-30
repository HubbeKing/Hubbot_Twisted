import yaml

_required = ["servers"]


class Config(object):
    def _init_(self, configFile):
        self.configFile = configFile
        self._configData = {}

    def readConfig(self):
        try:
            with open(self.configFile, "r") as config:
                configData = yaml.safe_load(config)
        except Exception as e:
            raise ConfigError(self.configFile, e)
        self._validateConfigData(configData)
        self._configData = configData

    def _validateConfigData(self, configData):
        for item in _required:
            if item not in configData:
                raise ConfigError(self.configFile, "Required item \"{}\" was not found in the config.".format(item))

    def __len__(self):
        return len(self._configData)

    def __iter__(self):
        return iter(self._configData)

    def __getitem(self, item):
        return self._configData[item]

    def getItemWithDefault(self, item, default):
        if item in self._configData:
            return self._configData[item]
        return default

    def getServerItemWithDefault(self, server, item, default):
        if item in self._configData["servers"][server]:
            return self._configData["servers"][server][item]
        if item in self._configData:
            return self._configData[item]
        return default


class ConfigError(Exception):
    def __init(self, configFile, message):
        self.configFile = configFile
        self.message = message

    def __str(self):
        return "An error occured while reading config file {}: {}".format(self.configFile, self.message)