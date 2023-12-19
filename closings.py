import urllib.request
import xml.etree.ElementTree as ET
import configparser
import argparse
import os


def create_config_if_not_exists():
    """
    Creates a config.ini file with default settings if it does not exist.

    :return: None
    """
    config_file = 'config.ini'
    if not os.path.exists(config_file):
        config = configparser.ConfigParser()
        config['SCHOOL_NAMES'] = {'names': ''}
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        print(f"'{config_file}' created with default settings.")


def read_config(section, key):
    """
    Read a config value from a given section and key.

    :param section: The section name in the config file.
    :param key: The key name within the section.
    :return: A list of lowercased, stripped strings from the config value.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return [name.strip().lower() for name in config.get(section, key).split(',')]


def write_config(section, key, school_names):
    """
    Write the given school names to the specified section and key in the configuration file.

    :param section: The section in the configuration file.
    :param key: The key within the section in the configuration file.
    :param school_names: The list of school names to be written to the configuration file.
    :return: None

    Example usage:
        write_config('General', 'Schools', ['School A', 'School B', 'School C'])
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set(section, key, ', '.join(school_names))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def add_school(school_name):
    """
    Adds a school to the list of school names.

    :param school_name: The name of the school to add.
    :type school_name: str
    :return: None
    """
    school_names = read_config('SCHOOL_NAMES', 'names')
    school_names.append(school_name.lower())
    write_config('SCHOOL_NAMES', 'names', school_names)


def remove_school(school_name):
    """
    Remove a school from the list of school names.

    :param school_name: The name of the school to remove.
    :type school_name: str
    :return: None
    :rtype: None
    """
    school_names = read_config('SCHOOL_NAMES', 'names')
    school_names = [name for name in school_names if name != school_name.lower()]
    write_config('SCHOOL_NAMES', 'names', school_names)


def show_schools():
    """
    Shows the current schools in the configuration.

    :return: None
    """
    school_names = read_config('SCHOOL_NAMES', 'names')
    print("Current schools in config:")
    for name in school_names:
        print(f" - {name}")


def show_all_schools():
    """
    Retrieves and displays information about all schools from a given XML feed.

    :return: None
    """
    url = "https://assets1.cbsnewsstatic.com/Integrations/SchoolClosings/PRODUCTION/CBS/kdka/NEWSROOM/KDKAclosings.xml"
    with urllib.request.urlopen(url) as response:
        content = response.read()
    root = ET.fromstring(content)
    print("All schools from the feed:")
    for record in root.findall('.//RECORD'):
        org_name = record.find('FORCED_ORGANIZATION_NAME').text
        status_name = record.find('FORCED_STATUS_NAME').text
        print(f"{org_name} - {status_name}")


def main():
    """
    Main

    This method manages school names in the config and fetches their status from a specified feed.

    Args:
        None

    Returns:
        None

    Example Usage:
        To add a school name to the config:
        main --add <school_name>

        To remove a school name from the config:
        main --remove <school_name>

        To show current school names in the config:
        main --show

        To show all schools from the feed:
        main --all
    """
    create_config_if_not_exists()
    parser = argparse.ArgumentParser(description='Manage school names in config and fetch status.')
    parser.add_argument('--add', help='Add a school name to config')
    parser.add_argument('--remove', help='Remove a school name from config')
    parser.add_argument('--show', action='store_true', help='Show current school names in config')
    parser.add_argument('--all', action='store_true', help='Show all schools from the feed')
    args = parser.parse_args()

    if args.add:
        add_school(args.add)
        print(f"Added '{args.add}' to config.")
    elif args.remove:
        remove_school(args.remove)
        print(f"Removed '{args.remove}' from config.")
    elif args.show:
        show_schools()
    elif args.all:
        show_all_schools()
    else:
        found_closing = False
        school_names = read_config('SCHOOL_NAMES', 'names')
        url = "https://assets1.cbsnewsstatic.com/Integrations/SchoolClosings/PRODUCTION/CBS/kdka/NEWSROOM/KDKAclosings.xml"
        with urllib.request.urlopen(url) as response:
            content = response.read()
        root = ET.fromstring(content)
        updated_at = root.find('RUN_DATE').text
        for record in root.findall('.//RECORD'):
            org_name = record.find('FORCED_ORGANIZATION_NAME').text
            status_name = record.find('FORCED_STATUS_NAME').text
            if any(school_name in org_name.lower() for school_name in school_names):
                print(f"{org_name} - {status_name}")
                found_closing = True
        if not found_closing:
            print(f"No Closings for you today! - {updated_at}")


if __name__ == "__main__":
    main()
