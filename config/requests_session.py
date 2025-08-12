from logging import exception
import traceback
import requests
from config.logger_message import record_log


class RequestsSession(object):
    def __init__(self, base_data):
        log_name = base_data['spider_name']
        self.logger = record_log(log_name)
        self.session = requests.Session()
        self.proxies = None
        self.session_id = base_data['session_id']

    def get(self, url, headers=None, cookies=None, proxy_ip=None, timeout=5, clean_cookie=False, **kwargs):
        res = None
        # data = kwargs['params'] if 'params' in kwargs else None
        try:
            proxies = None if proxy_ip is None else {'http': proxy_ip, 'https': proxy_ip}
            if clean_cookie:
                self.session.cookies.clear()
            res = self.session.get(url=url, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout,
                                   **kwargs)
            self.logger.info('session_id: {}, url: {}, statue_code: {}'.format(self.session_id, url, res.status_code))
        except:
            self.logger.error('session_id: {}, error is: {}'.format(self.session_id, traceback.format_exc()))
        return res

    def post(self, url, data=None, headers=None, json=None, cookies=None, proxy_ip=None, clean_cookie=False, timeout=5,
             **kwargs):
        res = None
        try:
            proxies = None if proxy_ip is None else {'http': proxy_ip, 'https': proxy_ip}
            if clean_cookie:
                self.session.cookies.clear()
            if json is None:
                res = self.session.post(url=url, data=data, headers=headers, cookies=cookies, proxies=proxies,
                                        timeout=timeout, **kwargs)
            else:
                res = self.session.post(url=url, json=json, headers=headers, cookies=cookies, proxies=proxies,
                                        timeout=timeout, **kwargs)
            self.logger.info('session_id: {} url: {}, status_code: {}'.format(self.session_id, url, res.status_code))
        except:
            self.logger.error('session_id: {}, error is: {}'.format(self.session_id, traceback.format_exc()))
        return res

    def put(self, url, data=None, json=None, headers=None, cookies=None, proxy_ip=None, clean_cookie=False, timeout=5,
            **kwargs):
        res = None
        try:
            proxies = None if proxy_ip is None else {'http': proxy_ip, 'https': proxy_ip}
            if clean_cookie:
                self.session.cookies.clear()
            if json is None:
                res = self.session.put(url=url, data=data, headers=headers, cookies=cookies, proxies=proxies,
                                   timeout=timeout, **kwargs)
            else:
                res = self.session.put(url=url, json=json, headers=headers, cookies=cookies, proxies=proxies,
                                   timeout=timeout, **kwargs)
            self.logger.info('session_id: {} url: {}, status_code: {}'.format(self.session_id, url, res.status_code))
        except:
            self.logger.error('session_id: {}, error is: {}'.format(self.session_id, traceback.format_exc()))
        return res

    def delete(self, url, headers=None, cookies=None, proxy_ip=None, clean_cookie=False, timeout=5, **kwargs):
        res = None
        try:
            proxies = None if proxy_ip is None else {'http': proxy_ip, 'https': proxy_ip}
            if clean_cookie:
                self.session.cookies.clear()
            res = self.session.delete(url=url, headers=headers, cookies=cookies, proxies=proxies,
                                      timeout=timeout, **kwargs)
            self.logger.info('session_id: {} url: {}, status_code: {}'.format(self.session_id, url, res.status_code))
        except:
            self.logger.error('session_id: {}, error is: {}'.format(self.session_id, traceback.format_exc()))
        return res

    def patch(self, url, data=None,json=None, headers=None, cookies=None, proxy_ip=None, clean_cookie=False, timeout=5, **kwargs):
        res = None
        try:
            proxies = None if proxy_ip is None else {'http': proxy_ip, 'https': proxy_ip}
            if clean_cookie:
                self.session.cookies.clear()
            if json is None:
                res = self.session.patch(url=url, data=data, headers=headers, cookies=cookies, proxies=proxies,
                                     timeout=timeout, **kwargs)
            else:
                res = self.session.patch(url=url, json=json, headers=headers, cookies=cookies, proxies=proxies,
                                     timeout=timeout, **kwargs)
            self.logger.info('session_id: {} url: {}, status_code: {}'.format(self.session_id, url, res.status_code))
        except:
            self.logger.error('session_id: {}, error is: {}'.format(self.session_id, traceback.format_exc()))
        return res