import argparse
import json

import sys
from typing import List, Any

import sinter
from sinter._csv_out import CSV_HEADER
from sinter._existing_data import ExistingData
from sinter._plotting import better_sorted_str_terms


def main_combine(*, command_line_args: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--order',
                        choices=('preserve', 'metadata', 'error'),
                        default='metadata',
                        help='Determines the order of output rows.\n'
                             '    metadata (default): sort ascending by metadata.'
                             '    preserve: match order of input rows.\n'
                             '    error: sort ascending by error rate')
    parser.add_argument('rest',
                        nargs=argparse.REMAINDER,
                        type=str,
                        help='Paths to CSV files containing sample statistics.')
    args = parser.parse_args(command_line_args)

    if args.rest:
        total = ExistingData()
        for path in args.rest:
            total += ExistingData.from_file(path)
    else:
        total = ExistingData.from_file(sys.stdin)

    if args.order == 'metadata':
        output = sorted(total.data.values(), key=lambda e: better_sorted_str_terms(json.dumps(e.json_metadata, separators=(',', ':'), sort_keys=True)))
    elif args.order == 'preserve':
        output = list(total.data.values())
    elif args.order == 'error':
        def err_rate_key(stats: sinter.TaskStats) -> Any:
            num_kept = stats.shots - stats.discards
            err_rate = 0 if num_kept == 0 else stats.errors / num_kept
            discard_rate = 0 if stats.shots == 0 else stats.discards / stats.shots
            return err_rate, discard_rate
        output = sorted(total.data.values(), key=err_rate_key)
    else:
        raise NotImplementedError(f'order={args.order}')

    print(CSV_HEADER)
    for value in output:
        print(value.to_csv_line())
