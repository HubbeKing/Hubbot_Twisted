import toml

_required = ["address"]


class Config(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self._config_data = {}

    def read_config(self):
        try:
            config_data = toml.load(self.config_file)
        except Exception as e:
            raise ConfigError(self.config_file, e)
        self._validate_config(config_data)
        self._config_data = config_data

    def _validate_config(self, config_data):
        for item in _required:
            if item not in config_data:
                raise ConfigError(self.config_file, "Required item {!r} was not found in the config.".format(item))

    def __len__(self):
        return len(self._config_data)

    def __iter__(self):
        return iter(self._config_data)

    def __getitem__(self, item):
        return self._config_data[item]

    def item_with_default(self, item, default):
        if item in self._config_data:
            return self._config_data[item]
        return default


class ConfigError(Exception):
    def __init(self, config_file, message):
        self.config_file = config_file
        self.message = message

    def __str(self):
        return "An error occurred while reading config file {}: {}".format(self.config_file, self.message)
