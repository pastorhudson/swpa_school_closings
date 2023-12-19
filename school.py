import urllib.request
import xml.etree.ElementTree as ET
import configparser
import argparse

def read_config(section, key):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return [name.strip().lower() for name in config.get(section, key).split(',')]

def write_config(section, key, school_names):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set(section, key, ', '.join(school_names))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def add_school(school_name):
    school_names = read_config('SCHOOL_NAMES', 'names')
    school_names.append(school_name.lower())
    write_config('SCHOOL_NAMES', 'names', school_names)

def remove_school(school_name):
    school_names = read_config('SCHOOL_NAMES', 'names')
    school_names = [name for name in school_names if name != school_name.lower()]
    write_config('SCHOOL_NAMES', 'names', school_names)

def show_schools():
    school_names = read_config('SCHOOL_NAMES', 'names')
    print("Current schools in config:")
    for name in school_names:
        print(f" - {name}")

def show_all_schools():
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
