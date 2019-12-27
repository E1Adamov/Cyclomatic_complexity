#!python3

import os
import sys
import json
import argparse
from typing import *
from collections import defaultdict
from datetime import datetime as dt

import lizard


def parse_args():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument('--path', '-p', action='store', dest='path', required=False,
                             help="Path to what you want to analyze. Can be a directory or file")

    args_parser.add_argument('--recursive', '-r', action='store', dest='recursive', required=False,
                             type=lambda x: eval(x), choices=(True, False), default=True,
                             help="Analyze directories inside path? Defaults to True")

    args_parser.add_argument('--do_save_report', '-s', action='store', dest='do_save_report', required=False,
                             type=lambda x: eval(x), choices=(True, False), default=True,
                             help="Save output to file")

    args, _ = args_parser.parse_known_args()

    return args.path or sys.argv[1], args.recursive, args.do_save_report


def get_file_complexity(file_path: str) -> Dict:
    """
    :return: dict(function mame: function complexity)
    """
    complexity = dict()

    analysis_result = lizard.analyze_file(file_path)

    for function in analysis_result.function_list:
        func_name = function.__dict__['name']
        cyclomatic_complexity = function.__dict__['cyclomatic_complexity']
        complexity[func_name] = cyclomatic_complexity

    return complexity


def parse_path(path: str) -> Tuple[str, str]:
    if os.path.isabs(path):
        file_name = os.path.split(path)[1]
        full_path = path
    else:
        file_name = path
        full_path = os.path.join(os.getcwd(), path)

    return file_name, full_path


def save_report(results: str):
    """
    Saves the report to the current working directory
    :param results: dumped to string json
    """
    # later, when parsing the report, the timestamp can be reversed back to the
    # datetime format: date_time = datetime.datetime.fromtimestamp(timestamp)
    timestamp = dt.now().timestamp()
    file_path = os.path.join(os.getcwd(), f"cc_{timestamp}.json")
    with open(file_path, 'w') as report:
        report.write(results)


def analyze(path: str, recursive: bool = True) -> Dict:
    rel_path, abs_path = parse_path(path)
    results = defaultdict(dict)

    if os.path.isfile(abs_path):
        return get_file_complexity(abs_path)

    for i in os.listdir(abs_path):
        full_path = os.path.join(abs_path, i)
        if os.path.isfile(full_path):
            results[i] = analyze(full_path, recursive)
        else:
            if recursive:
                results[i] = analyze(full_path, recursive)

    return results


def main():
    path, recursive, do_save_report = parse_args()

    results: Dict = analyze(path, recursive)
    results = {path: results}
    results_json_str = json.dumps(results, indent=2)

    print(results_json_str)

    if do_save_report:
        save_report(results_json_str)


if __name__ == '__main__':
    main()
