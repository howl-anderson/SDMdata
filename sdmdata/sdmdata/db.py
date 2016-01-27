#!/usr/bin/env python
# -*- coding;utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db_config import DATABASE_URI
from .db_config import DATABASE_HOST_URI

database_base = declarative_base()


class Species(database_base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True)
    species_name = Column(String(255), unique=True)
    in_process = Column(Boolean, nullable=False, default=False)
    data_source = Column(String(255), nullable=False, default="GBIF")
    name_correct = Column(Boolean, nullable=True, default=None)

    # taxonomic classification
    kingdom = Column(String(255), nullable=True, default=None)
    phylum = Column(String(255), nullable=True, default=None)
    clazz = Column(String(255), nullable=True, default=None)
    order = Column(String(255), nullable=True, default=None)
    superfamily = Column(String(255), nullable=True, default=None)
    family = Column(String(255), nullable=True, default=None)
    genus = Column(String(255), nullable=True, default=None)
    species = Column(String(255), nullable=True, default=None)
    infraspecific = Column(String(255), nullable=True, default=None)

    # species taxon key
    species_key = Column(String(255), nullable=True, default=None)

    # no occurrence data?
    no_data = Column(Boolean, nullable=True, default=None)
    # have un-coordinate data?
    have_un_coordinate_data = Column(Boolean, nullable=True, default=None)
    # store un-coordinate data
    un_coordinate_data = Column(Text, nullable=True, default=None)


class Occurrence(database_base):
    __tablename__ = "occurrence"

    id = Column(Integer, primary_key=True)
    species_name = Column(String(255))
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    country_code = Column(String(255), nullable=True)
    cross_check = Column(Integer, nullable=True)


class State(database_base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True)
    species_name = Column(String(255), unique=True)
    correct = Column(Integer, nullable=True, default=None)
    incorrect = Column(Integer, nullable=True, default=None)
    unknown_country = Column(Integer, nullable=True, default=None)


class User(database_base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    login_name = Column(String(64), unique=True)
    real_name = Column(String(255))
    password = Column(String(255))
    email = Column(String(120))
    current_project_id = Column(Integer)


def create_session():
    db_source = DATABASE_URI
    engine = create_engine(db_source, encoding="utf-8", echo=False)
    database_base.metadata.create_all(engine)

    session_object = sessionmaker(bind=engine)
    session_object.configure(bind=engine)
    species_session = session_object()
    return species_session


def create_connect():
    db_source = DATABASE_HOST_URI
    engine = create_engine(db_source, encoding="utf-8", echo=False)
    connect = engine.connect()
    
    return connect
