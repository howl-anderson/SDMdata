#!/usr/bin/env python
#-*- coding:utf-8 -*-

from multiprocessing import Process, Queue
from osgeo import ogr


from db import Occurrence
from db import create_session
from cross_check_process_worker import worker


# TODO: write this to other gdal script
ogr.UseExceptions()


def cross_check(work_dir="."):
    session = create_session()

    occurrence_list = session.query(Occurrence).filter(Occurrence.cross_check == None).all()
    session.close()

    queue = Queue()
    for item in occurrence_list:
        item_data = [item.id, item.longitude, item.latitude, item.country_code]
        queue.put(item_data)

    process_pool = []
    for index in range(7):
        process_obj = Process(target=worker, args=(queue, work_dir))
        process_obj.daemon = True
        process_obj.start()
        process_pool.append(process_obj)

    for process_obj in process_pool:
        process_obj.join()

    return None