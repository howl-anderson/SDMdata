#!/usr/bin/env python
# -*-coding:utf-8-*-
# TODO: not finished, may remove

import json
import Queue
import threading

from occurrence_search import OccurrenceSearch
from db import Species, Occurrence
from db import create_session


class ThreadWorker(threading.Thread):
    def __init__(self, work_queue, db_session):
        threading.Thread.__init__(self)
        self.queue = work_queue
        self.db_session = db_session

    def run(self):
        db_session = self.db_session
        while True:
            work_data = self.queue.get()
            species_name = work_data[0]
            species_key = work_data[1]

            obj = OccurrenceSearch()
            data, no_data = obj.search(taxon_key=species_key)
            species_obj = db_session.query(Species).filter(Species.species_name == species_name).one()
            species_obj.in_process = True
            db_session.commit()

            if len(no_data):
                species_obj.have_un_coordinate_data = True
                species_obj.un_coordinate_data = json.dumps(no_data)
                db_session.commit()

            if len(data):
                for item in data:
                    longitude = item[0]
                    latitude = item[1]
                    country_code = item[2]
                    occurrence_obj = Occurrence(species_name=species_name,
                                                longitude=longitude,
                                                latitude=latitude,
                                                country_code=country_code)
                    db_session.add(occurrence_obj)
                    db_session.commit()
            else:
                species_obj.no_data = True
                db_session.commit()

            self.queue.task_done()


def check_species_data():
    db_session = create_session()
    species_name_list = db_session.query(Species).filter(Species.in_process == False,
                                                         Species.name_correct == True).all()
    work_queue = Queue.Queue()

    for i in range(10):
        t = ThreadWorker(work_queue, db_session)
        t.setDaemon(True)
        t.start()

    for species_obj in species_name_list:
        species_name = species_obj.species_name
        species_key = species_obj.species_key
        work_data = [species_name, species_key]
        work_queue.put(work_data)

    #wait on the queue until everything has been processed
    work_queue.join()

    return None