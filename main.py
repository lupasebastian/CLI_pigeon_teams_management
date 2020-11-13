"""Main module for running the app, allows for actions defined below"""
# pylint: disable=no-member, protected-access
import argparse
from typing import List

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


from data import load_pigeons, load_teams, save_pigeons, save_teams
from models import sql_engine, Base, Pigeon, Team

Session = sessionmaker(bind=sql_engine)
session: Session = Session()
Base.metadata.create_all(bind=sql_engine)


def add_pigeons_to_db(pigeons: List[Pigeon]) -> None:
    """Function for adding pigeons loaded by load_pigeons function to database"""
    for pigeon in pigeons:
        first_name = pigeon.first_name
        last_name = pigeon.last_name
        team_id = pigeon.team_id
        session.add(Pigeon(_first_name=first_name, _last_name=last_name, _team_id=team_id))
    session.commit()


def add_teams_to_db(teams: List[Team]) -> None:
    """Function for adding teams loaded by load_pigeons function to database"""
    for team in teams:
        name = team.name
        session.add(Team(_name=name))
    session.commit()


def delete_pigeon(first_name: str, last_name: str) -> None:
    """Function for deleting pigeons from a database and subsequently from file"""
    try:
        pigeon_to_del = session.query(Pigeon).filter(Pigeon._first_name == first_name) \
            .filter(Pigeon._last_name == last_name).one()
        session.delete(pigeon_to_del)
        session.commit()
    except NoResultFound:
        print('No such pigeon in database.')


def delete_team(name: str) -> None:
    """
    Function for deleting teams from database and subsequently from file
    When a team is deleted so are all pigeons assigned to it
    """
    try:
        team_to_del = session.query(Team).filter(Team._name == name).one()
        session.delete(team_to_del)
        session.commit()
    except NoResultFound:
        print('No such team in database.')


def add_pigeon(first_name: str, last_name: str, team_name: str) -> None:
    """
    Function for adding pigeons to database, to the chosen team
    Function finds appropriate team in a database basing on the team name
    """
    try:
        team = session.query(Team).filter(Team._name == team_name).one()
        team_id = team.id
        session.add(Pigeon(_first_name=first_name, _last_name=last_name, _team_id=team_id))
        session.commit()
    except NoResultFound:
        print('Cannot add. No such team in database.')


def add_team(name: str) -> None:
    """Function for adding teams to database"""
    session.add(Team(_name=name))
    session.commit()


parser = argparse.ArgumentParser(description='data container')
parser.add_argument('-pn', '--pigeon_first_name', type=str, help='name of a pigeon')
parser.add_argument('-pl', '--pigeon_last_name', type=str, help='last name of a pigeon')
parser.add_argument('-tn', '--name_of_the_team', type=str, help='name of a team')
operation = parser.add_mutually_exclusive_group()
operation.add_argument('-ap', '--add_pigeon', action='store_true')
operation.add_argument('-dp', '--delete_pigeon', action='store_true')
operation.add_argument('-at', '--add_team', action='store_true')
operation.add_argument('-dt', '--delete_team', action='store_true')
operation.add_argument('-st', '--show_teams', action='store_true')

if __name__ == '__main__':

    add_teams_to_db(load_teams())
    add_pigeons_to_db(load_pigeons())
    args = parser.parse_args()
    if args.add_pigeon:
        add_pigeon(args.pigeon_first_name, args.pigeon_last_name, args.name_of_the_team)
    elif args.delete_pigeon:
        delete_pigeon(args.pigeon_first_name, args.pigeon_last_name)
    elif args.add_team:
        add_team(args.name_of_the_team)
    elif args.delete_team:
        delete_team(args.name_of_the_team)
    elif args.show_teams:
        print(session.query(Team).all())
    save_pigeons(session.query(Pigeon).all())
    save_teams(session.query(Team).all())
