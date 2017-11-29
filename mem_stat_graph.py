#!/usr/bin/env python3

import re
import sys
import os
import yaml
from jinja2 import Template


def read_input(stdin_list, stat):
    """
    Read input lines and create plot structure

    :param stdin_list: stats slab output
    :param stat: str of the desired 'stats slabs' element
    :return: dict
    """

    data = {}
    counter = 1

    stat_line = re.compile('^STAT')
    for line in stdin_list:
        if not stat_line.match(line):
            break

        m = re.match(r".+(\d+):(.+) (\d+)", line)
        if m.group(2) == stat:
            while counter < int(m.group(1)):
                data[counter] = '0'
                counter += 1
            data[counter] = int(m.group(3))
            counter += 1

    return data


def render_graph(data, title):
    """
    Render image (plot)

    :param data: dict of the data
    :param title: title of the generated graph
    :return:
    """

    # Template plot file
    plot_template = Template("set term png crop\n\
    set output '{{ title }}.png'\n\
    set boxwidth 0.5 absolute\n\
    set style fill solid 0.25 border\n\
    set samples 25, 25\n\
    set xrange [1:]\n\
    set title '{{ title.replace(\"_\", \" \") }}'\n\
    plot '/dev/shm/" + title + ".data' using 2 title '' with boxes")

    # Write plot values
    file = open('/dev/shm/' + title + '.data', 'w')
    for key, value in data.items():
        file.write(str(key) + ' ' + str(value) + '\n')
    file.close()

    # Write plot file
    plot_file = '/dev/shm/' + title + '.plot'
    file = open(plot_file, 'w')
    file.write(plot_template.render(title=title))
    file.close()

    # Generate graph
    os.system('gnuplot -persist ' + plot_file)


def config():
    """
    Read yaml config to choose which statistics to graph

    :return: list
    """
    with open("stats.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)


if __name__ == "__main__":
    stdin_list = []
    for line in sys.stdin:
        stdin_list.append(line)

    for stat in config():
        render_graph(read_input(stdin_list, stat), stat)
