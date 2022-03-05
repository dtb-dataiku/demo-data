import random
import datetime
from dataclasses import dataclass, field
from faker import Faker


@dataclass
class User:
    '''
    Defines a fake website user
    '''
    
    email: str = None
    uuid = str = None
    ip_address: str = None
    os_name: str = None
    os_version: str = None
    browser_name: str = None
    browser_user_agent: str = None
    user_league_favorite: str = None
    user_subscriber: str = None
        
    def to_dict(self) -> dict:
        '''
        Return user attributes as a dictionary
        '''
        
        return dict(
            email=self.email,
            uuid=self.uuid,
            ip_address=self.ip_address,
            os_name=self.os_name,
            os_version=self.os_version,
            browser_name=self.browser_name,
            browser_user_agent=self.browser_user_agent,
            user_league_favorite=self.user_league_favorite,
            user_subscriber=self.user_subscriber
        )


@dataclass
class UserMaker(Faker):
    '''
    Class that creates a fake website user
    '''
    
    settings: dict = field(default_factory=dict, repr=False)
    
    def __init__(self):
        super().__init__(['en_US'])
        self.settings = {
            'operating_systems': {
                'Windows': 0.15,
                'MacOS': 0.10,
                'Linux': 0.05,
                'Android': 0.30,
                'iOS': 0.40
            },
            'browsers': {
                'Windows': {
                    'Chrome': 0.75,
                    'Safari': 0.02,
                    'InternetExplorer': 0.12,
                    'Firefox': 0.08,
                    'Opera': 0.03
                },
                'MacOS': {
                    'Chrome': 0.25,
                    'Safari': 0.70,
                    'Firefox': 0.03,
                    'Opera': 0.02
                },
                'Linux': {
                    'Chrome': 0.80,
                    'Firefox': 0.15,
                    'Opera': 0.05
                },
                'Android': {
                    'Chrome': 0.95,
                    'Firefox': 0.04,
                    'Opera': 0.01
                },
                'iOS': {
                    'Chrome': 0.05,
                    'Safari': 0.95
                }
            },
            'league_favorite': {
                'nfl': 0.38,
                'nba': 0.25,
                'ufc': 0.20,
                'mlb': 0.12,
                'mls': 0.05
            },
            'subscriber': {
                'y': 0.10,
                'n': 0.90
            }
        }
        
    def __pick_os__(self) -> str:
        '''
        Randomly pick an operating systems
        '''
        
        systems = list(self.settings.get('operating_systems').keys())
        weights = list(self.settings.get('operating_systems').values())
        
        return random.choices(systems, weights=weights)[0]

    def __pick_os_version__(self, os: str) -> str:
        '''
        Randomly pick the os version based for a given operating system
        '''
        
        os_versions = {
            'Windows': self.windows_platform_token(),
            'MacOS': self.mac_platform_token(),
            'Linux': self.linux_platform_token(),
            'Android': self.android_platform_token(),
            'iOS': self.ios_platform_token()
        }
        
        return os_versions.get(os)
    
    def __pick_browser__(self, os: str) -> str:
        '''
        Randomly pick the browser based for a given operating system
        '''
        
        browsers = list(self.settings.get('browsers').get(os).keys())
        weights = list(self.settings.get('browsers').get(os).values())

        return random.choices(browsers, weights=weights)[0]

    def __pick_browser_user_agent__(self, browser: str) -> str:
        '''
        Randomly pick the browser user agent for a given browser
        '''
        
        browser_versions = {
            'Chrome': self.chrome(),
            'Safari': self.safari(),
            'InternetExplorer': self.internet_explorer(),
            'Firefox': self.firefox(),
            'Opera': self.opera()
        }
        
        return browser_versions.get(browser)

    def __pick_league_favorite__(self) -> str:
        '''
        Randomly pick an operating systems
        '''
        
        favorites = list(self.settings.get('league_favorite').keys())
        weights = list(self.settings.get('league_favorite').values())
        
        return random.choices(favorites, weights=weights)[0]
    
    def __pick_subscriber__(self) -> str:
        '''
        Randomly pick an operating systems
        '''
        
        subscribers = list(self.settings.get('subscriber').keys())
        weights = list(self.settings.get('subscriber').values())
        
        return random.choices(subscribers, weights=weights)[0]
    
    def get_users(self, count) -> list:
        '''
        Return a list of generated users
        '''
        
        users = []
        for _ in range(count):
            user = User()
            
            user.email = self.ascii_free_email()
            user.uuid = self.uuid4()
            user.ip_address = self.ipv4_public()
            user.os_name = self.__pick_os__()
            user.os_version = self.__pick_os_version__(user.os_name)
            user.browser_name = self.__pick_browser__(user.os_name)
            user.browser_user_agent = self.__pick_browser_user_agent__(user.browser_name)
            user.user_league_favorite = self.__pick_league_favorite__()
            user.user_subscriber = self.__pick_subscriber__()
            
            users.append(user.to_dict())
            
        return users
    
    
@dataclass
class Event:
    '''
    Creates events and keep track of sessions
    '''
    
    user: dict
    current_timestamp: datetime
    session_id: str = None
    previous_page: str = None
    current_page: str = None
    is_new_page: bool = True
    test_id: str = None
    test_group: str = None
    test_groups: dict = field(default_factory=dict, repr=False)
    landing_pages: dict = field(default_factory=dict, repr=False)
    pages: dict = field(default_factory=dict, repr=False)
    
    
    def __init__(self, user: dict, current_timestamp: datetime):
        self.user = user
        self.current_timestamp = self.__randomize_timestamp__(current_timestamp, range_minutes=60, method='uniform')
        
        faker = Faker()
        self.session_id = faker.ean13()
        
        test_prefix = 'test_sidebar'
        test_date = self.current_timestamp.date()
        test_date = test_date.strftime('%Y%m%d')
        self.test_id = f'{test_prefix}_{test_date}'
        
        self.test_groups = {
            'Control': 0.70,
            'Recommendation': 0.15,
            'Trending': 0.15
        }
        self.test_group = self.__pick_test_group__()
        
        self.landing_pages = dict(
            home=0.60,
            nfl=0.15,
            nba=0.10,
            ufc=0.08,
            mlb=0.05,
            mls=0.02
        )
        
        self.pages = {
            'Control': {
                'home': dict(home=0.10, nfl=0.25, nba=0.15, ufc=0.05, mlb=0.03, mls=0.02, end=0.40),
                'nfl': dict(home=0.02, nfl=0.16, nba=0.08, ufc=0.07, mlb=0.04, mls=0.03, end=0.60),
                'nba': dict(home=0.02, nfl=0.08, nba=0.16, ufc=0.07, mlb=0.04, mls=0.03, end=0.60),
                'ufc': dict(home=0.02, nfl=0.08, nba=0.07, ufc=0.21, mlb=0.01, mls=0.01, end=0.60),
                'mlb': dict(home=0.02, nfl=0.03, nba=0.03, ufc=0.01, mlb=0.30, mls=0.01, end=0.60),
                'mls': dict(home=0.02, nfl=0.02, nba=0.04, ufc=0.01, mlb=0.01, mls=0.30, end=0.60)
            },
            'Recommendation': {
                'home': dict(home=0.10, nfl=0.25, nba=0.15, ufc=0.05, mlb=0.03, mls=0.02, end=0.40),
                'nfl': dict(home=0.02, nfl=0.32, nba=0.16, ufc=0.13, mlb=0.04, mls=0.03, end=0.30),
                'nba': dict(home=0.02, nfl=0.16, nba=0.32, ufc=0.13, mlb=0.04, mls=0.03, end=0.30),
                'ufc': dict(home=0.02, nfl=0.16, nba=0.14, ufc=0.36, mlb=0.01, mls=0.01, end=0.30),
                'mlb': dict(home=0.02, nfl=0.10, nba=0.10, ufc=0.01, mlb=0.46, mls=0.01, end=0.30),
                'mls': dict(home=0.02, nfl=0.09, nba=0.11, ufc=0.01, mlb=0.01, mls=0.46, end=0.30)
            },
            'Trending': {
                'home': dict(home=0.10, nfl=0.25, nba=0.15, ufc=0.05, mlb=0.03, mls=0.02, end=0.40),
                'nfl': dict(home=0.02, nfl=0.16, nba=0.08, ufc=0.07, mlb=0.04, mls=0.03, end=0.60),
                'nba': dict(home=0.02, nfl=0.08, nba=0.16, ufc=0.07, mlb=0.04, mls=0.03, end=0.60),
                'ufc': dict(home=0.02, nfl=0.09, nba=0.08, ufc=0.21, mlb=0.01, mls=0.01, end=0.58),
                'mlb': dict(home=0.02, nfl=0.04, nba=0.04, ufc=0.01, mlb=0.30, mls=0.01, end=0.58),
                'mls': dict(home=0.02, nfl=0.03, nba=0.05, ufc=0.01, mlb=0.01, mls=0.30, end=0.58)
            }
        }
        
        self.current_page = self.__pick_landing_page__()

    def __randomize_timestamp__(self, timestamp: datetime, range_minutes: int=2, method: str='uniform') -> datetime:
        '''
        Randomize timestamp
        '''
        
        if method not in ['uniform', 'normal']:
            method = 'uniform'
        
        if method == 'uniform':
            random_interval = random.randrange(0, range_minutes)
        elif method == 'normal':
            random_interval = random.gauss(range_minutes, range_minutes * 0.25)
        
        return timestamp + datetime.timedelta(minutes=random_interval)
    
    def __pick_landing_page__(self) -> str:
        '''
        Randomly pick a landing page
        '''
        
        landing_pages = list(self.landing_pages.keys())
        weights = list(self.landing_pages.values())
        
        return random.choices(landing_pages, weights=weights)[0]
    
    def __pick_test_group__(self) -> str:
        '''
        Randomly pick a test group for the user
        '''
        
        test_groups = list(self.test_groups.keys())
        weights = list(self.test_groups.values())
        
        return random.choices(test_groups, weights=weights)[0]

    def get_pageview(self) -> dict:
        '''
        Return event information as dictionary
        '''
        
        return dict(
            visitor_id=self.user.get('uuid'),
            visitor_ip_address=self.user.get('ip_address'),
            visitor_os_name=self.user.get('os_name'),
            visitor_os_version=self.user.get('os_version'),
            visitor_browser_name=self.user.get('browser_name'),
            visitor_browser_user_agent=self.user.get('browser_user_agent'),
            session_id=self.session_id,
            event_timestamp=self.current_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            event_type='pageview',
            page_url=f'http://www.espntheocho.com/{self.current_page}',
            test_id=self.test_id,
            test_group=self.test_group
        )
    
    def is_active(self) -> bool:
        '''
        Check if session is currently active
        '''

        return self.current_page != 'end'
    
    def go_next_page(self) -> str:
        '''
        Go to another page (or stay or end session)
        '''
        
        pages = list(self.pages.get(self.test_group).get(self.current_page).keys())
        weights = list(self.pages.get(self.test_group).get(self.current_page).values())
        self.current_page = random.choices(pages, weights=weights)[0]
        
        return self.current_page
    
    def update(self) -> bool:
        '''
        Update (click to new page, stay on current page, or end the session)
        '''
        
        if self.is_active():
            self.current_timestamp = self.__randomize_timestamp__(self.current_timestamp, method='normal')
            self.previous_page = self.current_page
            self.go_next_page()
            self.is_new_page = self.current_page != self.previous_page
            
            return self.is_new_page


@dataclass
class Simulation:
    '''
    Track a simulation
    '''
    
    user_pool_size: int = 30000
    sessions_per_day: int = 10000
    current_timestamp: datetime = datetime.datetime.now()
    user_pool: list = field(default_factory=list, repr=False)
    users: list = field(default_factory=list, repr=False)
    events: list = field(default_factory=list, repr=False)
    pct_sessions_per_hour: dict = field(default_factory=dict, repr=False)
        
    def __init__(self):
        self.pct_sessions_per_hour = {
            0: 0.0273,
            1: 0.0185,
            2: 0.0108,
            3: 0.0107,
            4: 0.0050,
            5: 0.0105,
            6: 0.0192,
            7: 0.0297,
            8: 0.0382,
            9: 0.0426,
            10: 0.0549,
            11: 0.0583,
            12: 0.0646,
            13: 0.0627,
            14: 0.0572,
            15: 0.0521,
            16: 0.0590,
            17: 0.0667,
            18: 0.0718,
            19: 0.0662,
            20: 0.0696,
            21: 0.0428,
            22: 0.0329,
            23: 0.0287
        }
        
    def initialize(self, timestamp: datetime=None):
        '''
        Initialize/reset the simulation
        '''
        
        if timestamp != None:
            self.current_timestamp = timestamp
            
        min_user_pool_size = int(max(self.pct_sessions_per_hour.values()) * self.sessions_per_day)
        user_pool_size = max([min_user_pool_size, self.user_pool_size])
        
        user_maker = UserMaker()
        self.user_pool = user_maker.get_users(user_pool_size)
        self.users = list()
        self.events = list()

    def run(self, days=1):
        '''
        Run the simualation
        '''
        
        year = self.current_timestamp.year
        month = self.current_timestamp.month
        day = self.current_timestamp.day
        timestamp = datetime.datetime(year, month, day)
        
        for d in range(days):            
            new_day = 0 if d == 0 else 1
            timestamp = timestamp + datetime.timedelta(days=new_day)
            sessions_per_day_rnd = random.normalvariate(self.sessions_per_day, 0.1 * self.sessions_per_day)
            
            for h in range(24):
                timestamp = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, h)
                
                session_count_adjustment = int(sessions_per_day_rnd * min(self.pct_sessions_per_hour.values()) * 0.5)
                session_count_adjustment = max([1, session_count_adjustment])
                
                session_count = \
                    int(self.pct_sessions_per_hour.get(h) * self.sessions_per_day) + \
                    int(random.randrange(-session_count_adjustment, session_count_adjustment))
                    
                current_users = random.choices(self.user_pool, k=session_count)
                
                for user in current_users:
                    self.users.append(user)
                    
                    event = Event(user, timestamp)
                    self.events.append(event.get_pageview())
                    while (event.is_active()):
                        event.update()
                        self.events.append(event.get_pageview())
