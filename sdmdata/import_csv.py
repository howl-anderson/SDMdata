#!/usr/bin/env python
#-*- coding:utf-8 -*-

import click
from sdmdata.import_species_csv import import_species_csv

@click.command()
@click.argument('csv_file', type=click.Path(exists=False))
@click.argument("col_index", default=0, type=int)
def main(csv_file, col_index):
    imported_name_list, error_name_list = import_species_csv(csv_file, col_index=col_index)
    imported_species_count = len(imported_name_list)
    error_species_count = len(error_name_list)
    all_species_count = len(imported_name_list) + len(error_name_list)
    click.echo("All species number in CSV file: %s" % all_species_count)
    click.echo("Imported species count: %s" % imported_species_count)
    click.echo("Error species name count: %s" % error_species_count)

if __name__ == "__main__":
    main()