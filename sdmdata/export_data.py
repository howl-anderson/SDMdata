#!/usr/bin/env python
#-*- coding:utf-8 -*-

import click
from sdmdata.export_data_main import export_data

@click.command()
@click.argument('target_dir', type=click.Path(exists=True))
@click.option('--output_format', type=click.Choice(['csv', 'shp']), default="csv")
def main(target_dir, output_format):
    export_data(target_dir, output_format)

if __name__ == "__main__":
    main()