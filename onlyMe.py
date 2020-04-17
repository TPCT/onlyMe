class onlyMe:
    def __init__(self, username, password):
        from robobrowser import RoboBrowser
        from requests import Session
        from warnings import simplefilter
        simplefilter('ignore', UserWarning)
        self.username = username
        self.password = password
        self.browser = RoboBrowser
        self.Session = Session
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        self.Browser = None
        self.session = None
        self.login()

    def login(self):
        self.session = self.Session()
        headers = '''Host: m.facebook.com
                     User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
                     Accept-Language: en-US,en;q=0.5
                     Connection: keep-alive
                     TE: Trailers'''
        for header in headers.split('\n'):
            header = header.split(': ')
            self.session.headers[header[0].strip()] = header[1].strip()
        self.Browser = self.browser(session=self.session,
                                    user_agent=self.userAgent,
                                    cache=True)
        self.Browser.open('https://m.facebook.com/login')
        loginForm = self.Browser.get_form('login_form')
        loginForm['email'].value = self.username
        loginForm['pass'].value = self.password
        self.Browser.submit_form(loginForm, submit=loginForm['login'])
        self.Browser.open('https://m.facebook.com/login/save-device/cancel/'
                          '?flow=interstitial_nux&nux_source=regular_login')
        if self.Browser.get_form('mbasic-composer-form'):
            return True
        return False

    def makePostOnlyMe(self):
        self.Browser.open('https://m.facebook.com/profile.php')
        seeMore = self.Browser.find('div', {'id': 'u_0_2'})
        composer = self.Browser.find('div', {'id': 'structured_composer_async_container'})
        while seeMore:
            for article in composer.find_all('article'):
                privacyUrl = article.find('footer')
                if privacyUrl and 'Privacy' in privacyUrl.text:
                    if 'Only me' not in privacyUrl.text:
                        print('changing Post privacy to only me: %s ' %
                              (eval(article['data-ft'].strip('"'))["mf_story_key"]))
                        self.Browser.open('https://m.facebook.com' + privacyUrl.find('a')['href'])
                        seeMore = [x for x in self.Browser.find_all('a') if 'see_all' in x['href']][0]
                        self.Browser.open('https://m.facebook.com' + seeMore['href'])
                        onlyMeUrl = self.Browser.find('a', {'aria-label': 'Only me'})
                        self.Browser.open('https://m.facebook.com' + onlyMeUrl['href'])
                    else:
                        print('Post privacy is only me: %s ' %
                              (eval(article['data-ft'].strip('"'))["mf_story_key"]))
            seeMore = seeMore.find('a')
            self.Browser.open('https://m.facebook.com' + seeMore['href'])
            seeMore = self.Browser.find('div', {'id': 'u_0_0'})
