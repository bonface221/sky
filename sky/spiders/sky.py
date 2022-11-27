import scrapy
from scrapy.utils.response import open_in_browser
from scrapy_splash import SplashRequest
from datetime import date
from datetime import date


# div> xpath => //*[@class="BpkTicket_bpk-ticket__NTM0M"]

# lua_script = """
# function main(splash, args)
#     assert(splash:go(args.url))

#   while not splash:select('#app-root > div.FlightsDayView_row__NjQyZ > div > div > div > div:nth-child(1) > button') do
#     splash:wait(0.1)
#     print('waiting...')
#   end
#   return 
# end
# """
# {html=splash:html()}

lua_script = """
function main(splash, args)
    assert(splash:go(args.url))

  while not splash:select('#app-root > div.FlightsDayView_row__NjQyZ > div > div > div > div:nth-child(1) > button') do
    splash:wait(0.1)
    print('waiting...')
  end
  return {html=splash:html()}
end
"""


class MiamiSpider(scrapy.Spider):
    # This is the spider name
    name = 'sky'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'


    def start_requests(self):
        today = date.today()

        date_obj= '{}{}{}'.format(
            str(today.year)[2:],
            str(today.month),
            str(today.day)
        )

        data_payload = {
            'from': 'saoa',
            'to': 'fln',
            'today_date':date_obj,
            'adults': '1',
            'adultsv2': '1',
            'cabinclass': 'economy',
            'children': '0',
            'childrenv2': '',
            'destinationentityid': '27541670',
            'inboundaltsenabled': 'false',
            'infants': '0',
            'originentityid': '27539772',
            'outboundaltsenabled': 'false',
            'preferdirects': 'false',
            'ref': 'home',
            'rtn': '0',
            'currency': 'USD'

        }
        
        url_with_parameters = 'https://www.skyscanner.com/transport/flights/{}/{}/{}/?adults={}&adultsv2={}&cabinclass={}&children={}&childrenv2={}&currency={}&destinationentityid={}&inboundaltsenabled={}&infants={}&originentityid={}&outboundaltsenabled={}&preferdirects={}&ref={}&rtn={}/'.format(
            data_payload['from'],
            data_payload['to'],
            data_payload['today_date'],
            data_payload['adults'],
            data_payload['adultsv2'],
            data_payload['cabinclass'],
            data_payload['children'],
            data_payload['childrenv2'],
            data_payload['currency'],
            data_payload['destinationentityid'],
            data_payload['inboundaltsenabled'],
            data_payload['infants'],
            data_payload['originentityid'],
            data_payload['outboundaltsenabled'],
            data_payload['preferdirects'],
            data_payload['ref'],
            data_payload['rtn'],


        )

        
        yield SplashRequest(
            url_with_parameters,
            method='GET',
            endpoint='execute',
            
            args={
                'wait': 6, 
                'lua_source': lua_script,
                'url':url_with_parameters,
                'timeout':90,
                  }
        )
        

    def parse(self, response):
        open_in_browser(response)


    # def get_flights_data(self,response):
        # soup3 = bs(response.body, 'html.parser')
        # print(soup3.prettify())

        # open_in_browser(response)


