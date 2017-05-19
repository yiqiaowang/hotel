from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from util import log

class Scraper():
    url = 'https://ssl.omnihotels.com/Omni?pagesrc=RR&pagedst=RR1_2&Phoenix_state=clear&language=en&hotelCode=BOSPAR&SBrand=OM'
    data = dict()
    start_date = None
    end_date = None

    def __init__(self, start_date, end_date, debug=False):
        self.start_date = start_date
        self.end_date = end_date

        # set headless options
        self.options = webdriver.ChromeOptions()

        if not debug:
            self.options.add_argument('headless')
            self.options.add_argument('disable-gpu')
            self.options.add_argument('window-size=1200x600')

        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.get(self.url)
        self.arrival_input = self.driver.find_element_by_id('reservationsArrival')
        self.departure_input = self.driver.find_element_by_id('reservationsDeparture')
        self.form = self.driver.find_element_by_id('navFormRR')

        self.driver.execute_script("arguments[0].value = '{}';".format(start_date), self.arrival_input)
        self.driver.execute_script("arguments[0].value = '{}';".format(end_date), self.departure_input)
        self.form.submit()


    def crawl_room(self, room_type, log_file):

        p_daBARs = None
        p_CRP1F1 = None
        p_FTDAY = None

        try:
            daBARs = room_type.find_element_by_xpath('*//div[@data-filter-criterion = "daBARs"]')
            p_daBARs = daBARs.get_attribute('data-lowest-rate')
            log(log_file, '{} for {} priced at {}. Checkin date:{} Checkout date:{}.'.format('Best Available Rate', self.get_room_name(room_type), p_daBARs, self.start_date, self.end_date))
        except NoSuchElementException:
            log(log_file, 'WARN: {} for {} price not found. Checkin date:{} Checkout date:{}.'.format('Best Available Rate', self.get_room_name(room_type), self.start_date, self.end_date))

        try:
            CRP1F1 = room_type.find_element_by_xpath('*//div[@data-filter-criterion = "CRP1F1"]')
            p_CRP1F1 = CRP1F1.get_attribute('data-lowest-rate')
            log(log_file, '{} for {} priced at {}. Checkin date:{} Checkout date:{}.'.format('Step Into Summer...', self.get_room_name(room_type), p_CRP1F1, self.start_date, self.end_date))
        except NoSuchElementException:
            log(log_file, 'WARN: {} for {} price not found. Checkin date:{} Checkout date:{}.'.format('Step Into Summer 1 Night', self.get_room_name(room_type), self.start_date, self.end_date))

        try:
            FTDAY = room_type.find_element_by_xpath('*//div[@data-filter-criterion = "14DAY"]')
            p_FTDAY = FTDAY.get_attribute('data-lowest-rate')
            log(log_file, '{} for {} priced at {}. Checkin date:{} Checkout date:{}.'.format('Advance Purchase Promotion', self.get_room_name(room_type), p_FTDAY, self.start_date, self.end_date))
        except NoSuchElementException:
            log(log_file, 'WARN: {} for {} price not found. Checkin date:{} Checkout date:{}.'.format('Advance Purchase Promotion', self.get_room_name(room_type), self.start_date, self.end_date))

        return {
            'price_bar': p_daBARs,
            'price_summer': p_CRP1F1,
            'price_adv': p_FTDAY
            }

    def crawl(self, log_file):
        # navigate to the room types tab
        try:
            self.driver.find_element_by_css_selector('#myTab > li:nth-child(4) > a').click()
        except NoSuchElementException as err:
            try:
                msg = self.driver.find_element_by_css_selector('#navFormRR > div:nth-child(5) > p:nth-child(1)')
                if 'NO AVAILABILITY' in msg.text:
                    log(log_file, 'WARN: No availability on. Checkin date:{} Checkout date:{}'.format(self.start_date, self.end_date))
                    return
                else:
                    log(log_file, 'CRITICAL: {}'.format(err))
                    return
            except:
                pass

        room_type_container = self.driver.find_element_by_id('byroomtype')
        room_types = room_type_container.find_elements_by_class_name('grouping-row')

        for room in room_types:
            room_name = self.get_room_name(room)
            room_data = self.crawl_room(room, log_file)
            self.data[room_name] = room_data

        return self.data

    def get_room_name(self, room_type):
        return room_type.find_element_by_css_selector('.panel-collapse-header > a').text

    def clean(self):
        self.driver.close()
