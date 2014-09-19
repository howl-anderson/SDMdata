#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv

from db import Species
from db import create_session


def import_species_csv(csv_file, col_index=0, delimiter=',', quote_char='"'):
    session = create_session()
    species_name_list = []
    with open(csv_file, 'rb') as csv_file:
        data_list = csv.reader(csv_file, delimiter=delimiter, quotechar=quote_char)
        for row in data_list:
            species_name = row[col_index]
            species_name_list.append(species_name)

    import collections

    duplicate_list = [x for x, y in collections.Counter(species_name_list).items() if y > 1]
    unique_list = list(set(species_name_list))

    for species_name in unique_list:
        species_obj = Species(species_name=species_name)
        session.add(species_obj)
    session.commit()

    return unique_list, duplicate_list