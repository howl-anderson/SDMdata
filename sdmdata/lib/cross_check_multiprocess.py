#!/usr/bin/env python
# -*- coding:utf-8 -*-

import multiprocessing
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

    queue = multiprocessing.Queue()
    for item in occurrence_list:
        item_data = [item.id, item.longitude, item.latitude, item.country_code]
        queue.put(item_data)

    cpu_core_count = multiprocessing.cpu_count()
    multiprocess_core = cpu_core_count - 1

    process_pool = []
    for index in range(multiprocess_core):
        process_obj = multiprocessing.Process(target=worker, args=(queue, work_dir))
        process_obj.daemon = True
        process_obj.start()
        process_pool.append(process_obj)

    for process_obj in process_pool:
        process_obj.join()

    return None