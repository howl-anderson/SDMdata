#!/usr/bin/env python
# -*- coding:utf-8 -*-
# TODO: not finished, may remove

import Queue
import threading

from species_match import species_match

from db import Species
from db import create_session


class ThreadWorker(threading.Thread):
    def __init__(self, work_queue, db_session):
        threading.Thread.__init__(self)
        self.queue = work_queue
        self.db_session = db_session

    def run(self):
        db_session = self.db_session
        while True:
            species_name = self.queue.get()
            print(species_name)

            # species_data = species_match(species_name)
            # species_obj = db_session.query(Species).filter(Species.species_name == species_name).one()
            #
            # if not "speciesKey" in species_data.keys():
            #     species_obj.name_correct = False
            #     db_session.commit()
            #     continue
            #
            # species_obj.name_correct = True
            # species_obj.species_key = species_data.get("speciesKey")
            # species_obj.kingdom = species_data.get("kingdom")
            # species_obj.phylum = species_data.get("phylum")
            # species_obj.clazz = species_data.get("class")
            # species_obj.order = species_data.get("order")
            # species_obj.superfamily = species_data.get("superfamily")
            # species_obj.family = species_data.get("family")
            # species_obj.genus = species_data.get("genus")
            # species_obj.species = species_data.get("scientificName")
            # species_obj.infraspecific = species_data.get("infraspecific")
            #
            # db_session.commit()

            self.queue.task_done()


def check_species_data():
    db_session = create_session()
    species_name_list = db_session.query(Species.species_name).filter(Species.name_correct == None).all()
    work_queue = Queue.Queue()

    for i in range(10):
        t = ThreadWorker(work_queue, db_session)
        t.setDaemon(True)
        t.start()

    for species_obj in species_name_list:
        species_name = species_obj.species_name
        work_queue.put(species_name)

    # wait on the queue until everything has been processed
    work_queue.join()

    return None