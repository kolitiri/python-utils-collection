# Standard library imports
import ast
import configparser
import sys


def get_list_cfg(config_file, section, config_item):
    """ Utility proc that uses configparser package
        to parse a list config from a file.

        A list config is a sequence of comma separated items

        Args:
            config_file: The configuration file
            section:     The section of the config item
            config_item: The config item

        Returns:
            config_item: A config item list
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    config_item = config.get(section, config_item)
    # This is a string with comma separated items.
    # Convert to a list
    config_item = config_item.split(',')
    # Filter any empty values from the list
    config_item = list(filter(None, config_item))
    # Strip spaces in case of multiline values
    config_item = [item.strip() for item in config_item]

    return config_item

def get_dict_cfg(config_file, section, config_item):
    """ Utility proc that uses configparser package
        to parse a dictionary config from a file.

        Args:
            config_file: The configuration file
            section:     The section of the config item
            config_item: The config item

        Returns:
            config_item: A config item dictionary
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        config_item = ast.literal_eval(config.get(section, config_item))
    except configparser.NoOptionError:
        print(config_item, 'item not found in', config_file)
        sys.exit(0)

    return config_item

def get_str_cfg(config_file, section, config_item):
    """ Utility proc that uses configparser package
        to parse a string config from a file.

        A string config is a sequence of characters.
        (Should not contain commas as it will be
        parsed as a list)

        Args:
            config_file: The configuration file
            section:     The section of the config item
            config_item: The config item

        Returns:
            config_item: A config item string
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    config_item = config.get(section, config_item)

    return config_item


# dict_value = get_dict_cfg('sample_conf.ini', 'PARAMS', 'dict_value')
# print(dict_value)

# list_value = get_list_cfg('sample_conf.ini', 'PARAMS', 'list_value')
# print(list_value)

# str_value = get_str_cfg('sample_conf.ini', 'PARAMS', 'str_value')
# print(str_value)
