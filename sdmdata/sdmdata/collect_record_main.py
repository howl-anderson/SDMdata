#!/usr/bin/env python
# -*-coding:utf-8-*-

import json
import os
from occurrence_search import OccurrenceSearch
from db import Species, Occurrence
from db import create_session


def collect_record_data(root_dir):
    session = create_session()
    species_name_list = session.query(Species).filter(Species.in_process == False, Species.name_correct == True).all()

    for species_obj in species_name_list:
        species_name = species_obj.species_name
        species_key = species_obj.species_key

        obj = OccurrenceSearch()
        data, no_data = obj.search(taxon_key=species_key)
        species_obj = session.query(Species).filter(Species.species_name == species_name).one()
        species_obj.in_process = True
        session.commit()

        if len(no_data):
            species_obj.have_un_coordinate_data = True
            session.commit()
            # species_obj.un_coordinate_data = json.dumps(no_data)
            store_dir = "un-occurrence-data"
            species_file = species_name.replace(" ", "_") + ".json"
            file_name = os.path.join(root_dir, store_dir, species_file)
            fd = open(file_name, "w")
            fd.write(json.dumps(no_data))
            fd.close()

        if len(data):
            for item in data:
                longitude = item[0]
                latitude = item[1]
                country_code = item[2]
                occurrence_obj = Occurrence(species_name=species_name,
                                            longitude=longitude,
                                            latitude=latitude,
                                            country_code=country_code)
                session.add(occurrence_obj)
                session.commit()
        else:
            species_obj.no_data = True
            session.commit()
    return None