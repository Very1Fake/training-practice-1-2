# Copyright 2020 Timur Israpilov
# Licensed under the Apache License, Version 2.0
import json
import os
import sys
import time
from collections import Counter


if __name__ == '__main__':
    print('Starting')

    if len(sys.argv) > 1 and sys.argv[1]:  # Check for first argument (path)
        path = sys.argv[1]
    else:
        path = './TASK_1_Israpilov.txt'  # Default path

    while True:
        try:  # Get lines count from user (with validation)
            count = int(input('How much lines you want to save? : '))

            if count < 1:
                print('Line count cannot be less then 1')
            else:
                break
        except ValueError:
            print('Wrong line count\nTry again (count must be positive integer)')

    print('Saving lines')

    archive_path = f'{os.path.expanduser("~")}/ARCHIVE'  # Generating ARCHIVE/ path (in user directory)

    if os.path.isfile(path):  # Check for text file existence
        with open(path) as f:
            if not os.path.isdir(archive_path):  # Check for ARCHIVE/ existence
                os.makedirs(archive_path)  # Create ARCHIVE/ if not exists

            for number, line in enumerate(f):  # Enumerate text file lines
                if number <= count - 1:  # Check if line is correct
                    # Save line to S_{line}.txt in ARCHIVE/
                    with open(f'{archive_path}/S_{number + 1}.txt', 'w+') as lf:
                        print(f'Saving {number+1} line in S_{number + 1}.txt ({line})')
                        lf.write(line)
                else:
                    break
    else:
        print(f'File on this path ("{path}") does not exist')
        exit(0)

    print('Lines saved')
    print('Saving stats')

    stats: dict = {'files': {}, 'time': time.time()}  # Dict with file stats, system time and biggest file
    biggest_size = -1  # Biggest file size
    biggest_name = ''  # Biggest file name

    for i in range(count):
        stat = os.stat(f'{archive_path}/S_{i+1}.txt')  # File stat

        # Save file stat to stats (with representing as dict)
        stats['files'][f'S_{i+1}.txt'] = dict(zip('mode ino dev nlink uid gid size atime mtime ctime'.split(), stat))

        if stat.st_size > biggest_size:  # Compare file with biggest
            biggest_size = stat.st_size
            biggest_name = f'S_{i+1}.txt'

    stats['biggest'] = {'name': biggest_name, 'size': biggest_size}  # Save biggest file info to stats

    json.dump(stats, open(f'{archive_path}/INFO.json', 'w+'), indent=4)  # Save stats to ARCHIVE/INFO.json

    print('Stats saved')
    print(f'Scanning home directory ({os.path.expanduser("~")}) for .mp4 files')

    paths: list[str] = []

    for path, dirs, files in os.walk(os.path.expanduser("~")):  # Walk all directories in home directory
        for file in files:  # Check files in directory
            if file.split('.')[-1:][0] == 'mp4':  # Check for .mp4
                paths.append(f'{path}/{file}')

    print('Scan complete')
    print(f'{len(paths)} files found in home directory ({os.path.expanduser("~")})')

    for i in paths:
        print(f'\t"{i}"')

    duplicates: dict[str, int] = {k: v for k, v in Counter((i.split('/')[-1:][0] for i in paths)).items() if v > 1}

    print(f'{len(duplicates)} duplicates of .mp4 files found')

    for k, v in duplicates.items():
        print(f'\t"{k}" - {v} duplicates')
