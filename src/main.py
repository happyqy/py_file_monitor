import os
import json


def monitor(previous_times, paths):
    for path in paths:
        current_time = os.path.getmtime(path)
        if os.path.isdir(path):
            # folder
            if path in previous_times and previous_times[path] != current_time:
                print 'Folder %s changed' % path
            files = [path + '/' + p for p in os.listdir(path)]
            monitor(previous_times, files)
        else:
            # file
            if path in previous_times and previous_times[path] != current_time:
                print 'File %s changed' % path
        previous_times[path] = current_time


def main():
    if os.path.exists('previous_times.json'):
        with open('previous_times.json') as fin:
            previous_times = json.loads(fin.read())  # includes all precious times, key: path, value: timestamp
    else:
        previous_times = {}

    if os.path.exists('monitor_list.json'):
        with open('monitor_list.json') as fin:
            paths = json.loads(fin.read())  # includes all precious times, key: path, value: timestamp
    else:
        paths = {
            'current': [],
            'all': []
        }

    monitor(previous_times, paths['current'])
    with open('previous_times.json', 'w') as fout:
        fout.write(json.dumps(previous_times))

    print 'Check finished'

if __name__ == '__main__':
    main()
