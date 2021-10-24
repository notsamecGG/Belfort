import requests
import time

from datetime import datetime

PAGE = 'https://howrare.is/' 
TIME_FMT = '%S:%M:%H,%d-%m-%Y'


class Timer:
    def __init__(self) -> None:
        self.start = time.time_ns()

    @property
    def stop(self) -> int():
        '''returns time(int) ns'''
        now = time.time_ns()

        return now - self.start



class Agent:
    def __init__(self, *args) -> None:
        self.snapshots = []
        self.filtered_snapshots = []
        self.nft_list = []
        self.filtered_nft_list = []

        self.url = self._args_handler(args)


    def _args_handler(self, args) -> str:
        '''
        Inputed arguments are convereted to url string \n
        reutrns url string
        '''
        def add_slash(string: str) -> str:
            last_char = string[-1]

            if not last_char == '/':
                string + '/'

            #return string[:]

        len_ = len(args)
        url = ''

        if len_ > 1:
            page_url, options = args[0], args[1:]
            options_string = "&".join(options)

            add_slash(page_url)
            url = f'{page_url}?{options_string}'
        else:
            url = args[0]

        return url


    # REQUESTING
    #region
    def _evaluate_request(self, status_code: int, type = 'Collection') -> bool:
        '''
        Checks validity of given response(or status_code), then logs result \n
        returns bool
        '''

        validity = status_code == 200

        if validity:
            print(f'[EVALUATING] {type}, ✔ valid')
        else:
            print(f'[EVALUATING] {type}, ❌ NOT valid')

        return validity


    def request_collection(self, url: str) -> str:
        '''
        Requests url, evaluates result \n
        returns html_body(string) else empty(string)
        '''
        try:
            collection_response = requests.get(url)
            collection_valid = self._evaluate_request(collection_response.status_code)
        except:
            collection_valid = self._evaluate_request(0)
        if not collection_valid:
            return ''

        return collection_response.text
    #endregion

    # SNAPSHOT Manipulation 
    #region
    def _append_snaphsot(self, snapshot: list=[]):
        print('[APPENDING]')
        if not snapshot:
            self.snapshots.append(self.nft_list)
        else:
            self.snapshots.append(snapshot)
        

    def filter_snapshot(self, snapshot: list = [], **kwargs):
        last_snap = None

        if len(self.snapshots):
            last_snap = self.snapshots[-1]
        elif self.nft_list:
            last_snap = self.nft_list
        else:
            return

        if not snapshot:
            snapshot = self.nft_list

        last_time = last_snap[-1]
        last_snap = last_snap[:-1]

        snap_time = snapshot[-1]
        snap = snapshot[:-1]

        last_time = datetime.strptime(last_time, TIME_FMT)
        snap_time = datetime.strptime(snap_time, TIME_FMT)

        f_time = last_time - snap_time

        filtered_snapshot = []

        for nft in snap:
            nft_dict = nft.__dict__
            nft_keys = nft.__dict__.keys()

            condition = True

            for key, value in kwargs.items():
                if key in nft_keys:
                    condition = condition and int(nft_dict[key]) < value

            if condition:
                filtered_snapshot.append(nft)
        
        if len(filtered_snapshot):
            filtered_snapshot.append(f_time)

            self.filtered_nft_list = filtered_snapshot
            self.filtered_snapshots.append(filtered_snapshot)
    #endregion

    # REQUEST PARSING
    def parse_NFTs(self, raw_page: str) -> list:
        '''
        Takes in raw html of the page \n
        returns list/array of NFT objects
        '''
        
        if not raw_page:
            return

        a_split = raw_page.split('<a')
        a_split.pop(0)
        a_split.pop(-1)
        
        # only divs of NFTS do have this filter, yeah its quiet ugly
        a_split = list(filter(lambda x : 'class=\"m-2\" style=\"display: block;\"' in x, a_split))
        a_split[-1] = a_split[-1].split('</a>')[0]

        timer = Timer()
        print(f'[PARSING] Html to objects')

        # actual parsing
        nft_list = []
        for raw_data_block in a_split:
            raw_data_block = '<a' + raw_data_block
            raw_data_block = raw_data_block.replace('    ', '')
            raw_data_block = raw_data_block.replace(' ', '')

            nft = NFT(raw_data_block)
            nft_list.append(nft)
        nft_list.append(datetime.now().strftime(TIME_FMT))

        print(f'[PARSING] Parsing done {timer.stop / 1e6}ms')

        # saving
        self._append_snaphsot(nft_list)
        self.nft_list = nft_list
        return nft_list



class NFT:
    def __init__(self, raw_data) -> None:
        '''
        Parses given raw_data(string) to object
        '''
        # TODO: can be extended to page parsing, 
        #   I would takde data about this NFT from it's detail page
        self.m_raw_data = raw_data

        self.format_data()
        

    def format_data(self):
        '''
        !(Required: self.m_raw_data) \n
        Parses NFT from raw data to attributes \n
            attributes are then implemented as \
            member_variables to this object
        '''
        # Formating text, for easier manipulation
        if not self.m_raw_data:
            print(f'There are no raw data in {self}')

        data = NFT.remove_spaces(self.m_raw_data)
        lines = data.split(';--;\n')

        attribs = NFT._parse_attbribs(lambda x : not '<' in x, lambda x: x.replace('\"', '').split(':'), lines)
        attribs_html = NFT._parse_attbribs(lambda x : '<' in x, lambda x : x.replace('<', '').replace('=', '').split('\"')[:2], lines)

        self._implement_attribs(attribs)
        self._implement_attribs(attribs_html, 'm_')


    def _implement_attribs(self, attribs: list, prefix=''):
        for attrib in attribs:
            if len(attrib) == 1: 
                continue

            setattr(self, prefix+attrib[0], attrib[1])


    @staticmethod
    def _parse_attbribs(condition, func, lines: list) -> list:
        output_list = []

        for line in lines:
            if condition(line):
                output_list.append(func(line))

        return output_list

    @staticmethod
    def remove_spaces(raw_data):
        data = raw_data.replace('<divclass="nft-token-listrounded">', '')
        data = data.replace('<divclass="nft-details">', '')
        data = data.replace('<strong>', '\"').replace('</strong>', '\"')
        data = data.replace('</a>', '')\
            .replace('</div>', '').replace('<div>', '')\
            .replace('</p>', '').replace('<p>', '')
        data = data.replace('\n\n', '\n')
        data = data.replace('\n\n', '')
        data = data.replace('\"Price:\n', '\"\nPrice:')
        data = data.replace('Rank', 'Rank:')
        data = data.replace('\n', ';--;\n')
        data = data.replace('<h3>', 'Name:')
        data = data.replace('</h3>', '')

        return data



url = 'https://howrare.is/solsnatchers/?for_sale=on&sort_by=price'
a = Agent(url)
raw_html = a.request_collection(url)
a.parse_NFTs(raw_html)
a.filter_snapshot(Rank=1500)
