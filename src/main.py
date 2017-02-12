import os
import time


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
    previous_times = {}  # includes all precious times, key: path, value: timestamp
    while True:
        monitor(previous_times, ['C:/Users/QY/Desktop/test.txt', 'C:/Users/QY/Desktop/test'])
        time.sleep(5)


if __name__ == '__main__':
    main()
