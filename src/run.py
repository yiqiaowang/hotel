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

                # Merge the accomodation data

                for accom_type in sorted(room_data['price_bar']):
                    m_price = merge(room_data, accom_type)
                    data_row = [date_pair[0], date_pair[1],
                                room_type,
                                accom_type,
                                m_price['p_bar'],
                                m_price['p_sum'],
                                m_price['p_adv']
                                ]
                    util.append_row(csv_name, data_row)

                for accom_type in sorted(room_data['price_summer']):
                    m_price = merge(room_data, accom_type)
                    data_row = [date_pair[0], date_pair[1],
                                room_type,
                                accom_type,
                                m_price['p_bar'],
                                m_price['p_sum'],
                                m_price['p_adv']
                                ]
                    util.append_row(csv_name, data_row)
                for accom_type in sorted(room_data['price_adv']):
                    m_price = merge(room_data, accom_type)
                    data_row = [date_pair[0], date_pair[1],
                                room_type,
                                accom_type,
                                m_price['p_bar'],
                                m_price['p_sum'],
                                m_price['p_adv']
                                ]
                    util.append_row(csv_name, data_row)
        worker.clean()


# Takes in a room_data structure and an accom_type
def merge(room_data, accom_type):

    merged = {
        'p_bar': None,
        'p_sum': None,
        'p_adv': None
    }

    if accom_type in room_data['price_bar']:
        merged['p_bar'] = room_data['price_bar'][accom_type]
        del(room_data['price_bar'][accom_type])

    if accom_type in room_data['price_summer']:
        merged['p_sum'] = room_data['price_summer'][accom_type]
        del(room_data['price_summer'][accom_type])

    if accom_type in room_data['price_adv']:
        merged['p_adv'] = room_data['price_adv'][accom_type]
        del(room_data['price_adv'][accom_type])

    return merged
