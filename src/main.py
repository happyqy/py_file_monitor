import os
import json
import time
import Tkinter as tk

is_snooze = False


def monitor(previous_times, paths):
    result = []
    for path in paths:
        current_time = os.path.getmtime(path)
        if os.path.isdir(path):
            # folder
            if path in previous_times and previous_times[path] != current_time:
                result.append('Folder %s changed' % path)
            files = [path + '/' + p for p in os.listdir(path)]
            result += monitor(previous_times, files)
        else:
            # file
            if path in previous_times and previous_times[path] != current_time:
                result.append('File %s changed' % path)
        previous_times[path] = current_time
    return result


def get_json_file(filename, default):
    """
    If exists, get the specified file. Otherwise create file with default, return default.
    :param filename:
    :param default:
    :return:
    """
    if os.path.exists(filename):
        with open(filename) as fin:
            return json.loads(fin.read())
    else:
        with open(filename, 'w') as fout:
            fout.write(json.dumps(default))
        return default


def create_message(result):
    def snooze_with_close_callback():
        snooze_callback()
        master.destroy()

    master = tk.Tk()
    master.title('File Change Notice')
    update_result = '\n'.join(result)
    msg = tk.Message(master, text=update_result, width=500).pack()
    snooze_button = tk.Button(master, text="Snooze", command=snooze_with_close_callback).pack()
    tk.mainloop()


def snooze_callback():
    global is_snooze
    is_snooze = True


def main():
    global is_snooze
    previous_times = get_json_file('previous_times.json', {})
    paths = get_json_file('monitor_list.json',
                          {
                              'current': [],
                              'all': []
                          })

    while True:
        previous_times_new = previous_times.copy()
        result = monitor(previous_times_new, paths['current'])
        is_snooze = False

        if result:
            # there are updates
            create_message(result)

        if not is_snooze:
            previous_times = previous_times_new
            with open('previous_times.json', 'w') as fout:
                fout.write(json.dumps(previous_times))

        time.sleep(5)


if __name__ == '__main__':
    print 'Start'
    main()
