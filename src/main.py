import os
import time
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
    while True:
        monitor(previous_times, ['C:/Users/QY/Desktop/test.txt', 'C:/Users/QY/Desktop/test'])
        with open('previous_times.json', 'w') as fout:
            fout.write(json.dumps(previous_times))
        time.sleep(5)


if __name__ == '__main__':
    main()
