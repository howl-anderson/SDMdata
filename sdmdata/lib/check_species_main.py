#!/usr/bin/env python
# -*-coding:utf-8-*-

from .species_match import species_match

from .db import Species
from .db import create_session
from . import Exceptions


def check_species_data():
    session = create_session()
    species_name_list = session.query(Species.species_name).filter(Species.name_correct == None).all()
    for species_obj in species_name_list:
        species_name = species_obj.species_name

        try:
            species_data = species_match(species_name)
        except Exceptions.NetworkError as e:
            continue
        species_obj = session.query(Species).filter(Species.species_name == species_name).one()

        if "speciesKey" not in species_data.keys():
            species_obj.name_correct = False
            session.commit()
            continue

        species_obj.name_correct = True
        species_obj.species_key = species_data.get("speciesKey")
        species_obj.kingdom = species_data.get("kingdom")
        species_obj.phylum = species_data.get("phylum")
        species_obj.clazz = species_data.get("class")
        species_obj.order = species_data.get("order")
        species_obj.superfamily = species_data.get("superfamily")
        species_obj.family = species_data.get("family")
        species_obj.genus = species_data.get("genus")
        species_obj.species = species_data.get("scientificName")
        species_obj.infraspecific = species_data.get("infraspecific")

        session.commit()

    return None