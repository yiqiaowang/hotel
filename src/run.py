import scraper
import util


def run_scraper(debug=False):
    date = util.get_current_date()

    # create the csv file
    csv_name = '{}_data.csv'.format(date)
    log_file = '{}_log.txt'.format(date)
    util.create_csv(csv_name)

    for date_pair in util.get_date_pairs():
        worker = scraper.Scraper(date_pair[0], date_pair[1], debug)
        data = worker.crawl(log_file)

        if not data:
            data_row = [date_pair[0], date_pair[1], None, None, None, None]
            util.append_row(csv_name, data_row)
        else:
            for room_type in sorted(data):
                room_data = data[room_type]
                data_row = [date_pair[0], date_pair[1], room_type, room_data['price_bar'], room_data['price_summer'], room_data['price_adv']]
                util.append_row(csv_name, data_row)
        worker.clean()
