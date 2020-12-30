import logging

from requests import Session


class DikidiAPI:
    DIKIDI_AUTH_HOST = "auth.dikidi.ru"
    DIKIDI_API_HOST = "beauty.dikidi.ru"

    def __init__(self, login: str, password: str):
        """
        Create client for request to Dikidi API
            :param login: mobile phone
            :param password: pass phrase
        """
        self.login = login
        self.password = password
        self.session = self.create_session()

    def create_session(self) -> Session:
        """
        Create session using credentials
        :return: session instance
        """
        session = Session()
        response = session.post(
            url='https://{0}/ajax/user/auth/'.format(DikidiAPI.DIKIDI_AUTH_HOST),
            data={
                'number': self.login,
                'password': self.password
            },
            headers={
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }
        )
        if 'callback' in response.json():
            if 'sw.auth.complete()' in response.json()['callback']:
                logging.info('Auth complete')
                return session
        raise Exception('Session not created')

    def get_appointment_list(self, company_id: str, date_start: str, date_end: str, limit: int) -> list:
        """
        Get appointment list with client data
        :param company_id: numeric company id
        :param date_start: start date in format %Y-%m-%d
        :param date_end: end date in format %Y-%m-%d
        :param limit: number of records
        :return: list of active appointments
        """
        response = self.session.get(
            url="https://{0}/owner/ajax/journal/appointment_list/".format(DikidiAPI.DIKIDI_API_HOST),
            params={
                'company': company_id,
                'client': '',
                'start': date_start,
                'end': date_end,
                'date_field': '',
                'date_order': '',
                'sort_field': '',
                'sort_order': '',
                'limit': limit,
                'offset': 0,
                'first': 1
            },
            headers={
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }
        )
        self.session.close()

        records = response.json()
        if 'appointments' in records:
            return [record for record in records['appointments'] if 'time' in record
                                                                    and 'client_phone' in record
                                                                    and record['status_id'] == '1']
        elif 'error' in records:
            if records['error'] != 0:
                raise Exception("Code: {}. Message: {}".format(records['error']['code'], records['error']['message']))
        else:
            raise Exception("Request execution error")
