"""
Module for saving and loading objects for an app
Implements very useful external library - jsonpickle, that can serialize
and save pretty much every object
"""
import jsonpickle

PIGEON_FILE = r'C:\Users\Sebastian\PycharmProjects\CLI_db_management_pigeons\pigeons.txt'
TEAM_FILE = r'C:\Users\Sebastian\PycharmProjects\CLI_db_management_pigeons\teams.txt'


def save_pigeons(pigeons_to_save):
    """
    Function for saving Pigeon objects queried from database
    when the app is closing
    """
    with open(PIGEON_FILE, 'w') as file:
        file.write(jsonpickle.encode(pigeons_to_save))


def save_teams(teams_to_save):
    """
    Function for saving Team objects queried from database
    when the app is closing
    """
    with open(TEAM_FILE, 'w') as file:
        file.write(jsonpickle.encode(teams_to_save))


def load_teams():
    """Function for loading Team objects at start-up"""
    try:
        with open(TEAM_FILE, 'r') as file:
            teams = jsonpickle.decode(file.read())
    except EOFError:
        pass
    except FileNotFoundError:
        print('Can\'t load pigeons.')
    return teams


def load_pigeons():
    """Function for loading Pigeon objects at start-up """
    try:
        with open(PIGEON_FILE, 'r') as file:
            pigeons = jsonpickle.decode(file.read())
    except EOFError:
        pass
    except FileNotFoundError:
        print('Can\'t load pigeons.')
    return pigeons
