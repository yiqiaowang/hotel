import datetime
import csv


def get_current_date():
    return datetime.date.today()


def offset_current_date(offset):
    current_date = get_current_date()
    offset_start = current_date + datetime.timedelta(offset)
    offset_end = offset_start + datetime.timedelta(1)
    return tuple(map(lambda x: x.strftime('%m/%d/%Y'), (offset_start, offset_end)))


def get_date_pairs():
    return [offset_current_date(n) for n in range(0, 60)]


def append_row(file_name, row):
    with open(file_name, 'a', newline='') as csvfile:
        data_writer = csv.writer(csvfile)
        data_writer.writerow(row)


def create_csv(file_name):
    with open(file_name, 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile)
        data_writer.writerow(['Arrival Date',
                              'Departure Date',
                              'Room Type',
                              'Best Available Rate',
                              'Step Into Summer 1 Night',
                              'Advance Purchase Promotion'])


def log(log_file, log_data):

    log_data = '{} - {}'.format(datetime.datetime.now().isoformat(), log_data)
    print(log_data)
    with open(log_file, 'a') as logfile:
        logfile.write(log_data)
