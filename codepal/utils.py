import os


def get_conf(conf_filepath):
    """Returns the config values either based on the provided filepath"""

    config_file_path = os.path.expanduser(conf_filepath)

    if not os.path.isfile(config_file_path):
        print("Config file not found")
        return None

    conf = {}

    with open(config_file_path, 'r') as f:
        for line in f:
            if '=' not in line:
                return None

            key, value = line.strip().split('=')
            conf[key] = value

    if not conf:
        print("Config file does not have proper format or values")
        return None

    return conf


def load_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()
