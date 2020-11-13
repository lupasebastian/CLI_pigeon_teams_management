"""
Module storing classes for objects to be created from
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

sql_engine = create_engine("sqlite:///:memory:")
Base = declarative_base()


class Pigeon(Base):
    """class Pigeon, pigeons can be assigned to Teams"""
    __tablename__ = 'pigeons'

    id = Column(Integer, primary_key=True)
    _first_name = Column(String(20), nullable=False)
    _last_name = Column(String(30), nullable=False, unique=True)
    _team_id = Column(Integer, ForeignKey('teams.id'))

    team = relationship('Team', back_populates='pigeons')

    def __repr__(self):
        return f'Pigeon named {self.first_name} {self.last_name}'

    @property
    def first_name(self):
        """Property for getting pigeons' first name"""
        return self._first_name

    @property
    def last_name(self):
        """Property for getting pigeons' last name"""
        return self._last_name

    @property
    def team_id(self):
        """Property for getting id of a team the pigeon is assigned to"""
        return self._team_id


class Team(Base):
    """
    class Team, teams can be listed from main menu,
    with list of pigeons assigned to it
    """
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    _name = Column(String(50), nullable=False, unique=True)

    pigeons = relationship(Pigeon, back_populates='team', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'Team {self.name}, pigeons {self.pigeons}'

    @property
    def name(self):
        """Property for getting teams' name"""
        return self._name
