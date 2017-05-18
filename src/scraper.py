from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from util import log

class Scraper():
    url = 'https://ssl.omnihotels.com/Omni?pagesrc=RR&pagedst=RR1_2&Phoenix_state=clear&language=en&hotelCode=BOSPAR&SBrand=OM'
    data = dict()
    start_date = None
    end_date = None

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

        # set headless options
        self.options = webdriver.ChromeOptions()
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

        # navigate to the room types tab
        self.driver.find_element_by_css_selector('#myTab > li:nth-child(4) > a').click()

    def crawl_room(self, room_type):

        p_daBARs = None
        p_CRP1F1 = None
        p_FTDAY = None

        try:
            daBARs = room_type.find_element_by_xpath('*//div[@data-filter-criterion = "daBARs"]')
            p_daBARs = daBARs.get_attribute('data-lowest-rate')
            log('{} priced at {}. Checkin date:{} Checkout date:{}.'.format('Best Available Rate', p_daBARs, self.start_date, self.end_date))
        except NoSuchElementException:
            log('WARN: {} price not found. Checkin date:{} Checkout date:{}.'.format('Best Available Rate', self.start_date, self.end_date))

        try:
            CRP1F1 = room_type.find_element_by_xpath('*//div[@data-filter-criterion = "CRP1F1"]')
            p_CRP1F1 = CRP1F1.get_attribute('data-lowest-rate')
            log('{} priced at {}. Checkin date:{} Checkout date:{}.'.format('Step Into Summer...', p_CRP1F1, self.start_date, self.end_date))
        except NoSuchElementException:
            log('WARN: {} price not found. Checkin date:{} Checkout date:{}.'.format('Step Into Summer 1 Night', self.start_date, self.end_date))

        try:
            FTDAY = room_type.find_element_by_xpath('*//div[@data-filter-criterion = "14DAY"]')
            p_FTDAY = FTDAY.get_attribute('data-lowest-rate')
            log('{} priced at {}. Checkin date:{} Checkout date:{}.'.format('Advance Purchase Promotion', p_FTDAY, self.start_date, self.end_date))
        except NoSuchElementException:
            log('WARN: {} price not found. Checkin date:{} Checkout date:{}.'.format('Advance Purchase Promotion', self.start_date, self.end_date))

        return {
            'price_bar': p_daBARs,
            'price_summer': p_CRP1F1,
            'price_adv': p_FTDAY
            }

    def crawl(self):
        room_type_container = self.driver.find_element_by_id('byroomtype')

        room_types = room_type_container.find_elements_by_class_name('grouping-row')
        for room in room_types:
            room_name = room.find_element_by_css_selector('.panel-collapse-header > a').text
            room_data = self.crawl_room(room)

            self.data[room_name] = room_data

    def clean(self):
        self.driver.close()
