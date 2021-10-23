import requests
import time

PAGE = 'https://howrare.is/' 



class Agent:
    def __init__(self, collection, querries: list or str) -> None:
        collection = collection\
            .replace(PAGE, '')\
            .split('/')[0]

        collection_url = PAGE + collection + '/'

        if querries:
            if type(querries) is str:
                collection_url += querries

        self.page_url = PAGE
        self.collection_url = PAGE + collection


    # REQUESTING
    def evaluate_request(self, status_code: int, type = 'Collection') -> bool:
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
        Checks if page is valid then collection page \n
        returns string - empty if collection is not valid
        '''
        # TODO: group these into function
        try:
            page_response = requests.get(self.page_url)
            page_valid = self.evaluate_request(page_response.status_code, 'Page')
        except:
            page_valid = self.evaluate_request(0, 'page')
        if not page_valid: 
            return ''
        
        try:
            collection_response = requests.get(url)
            collection_valid = self.evaluate_request(collection_response.status_code)
        except:
            collection_valid = self.evaluate_request(0)
        if not collection_valid:
            return ''

        return collection_response.text


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
        a_split[-1], _ = a_split[-1].split('</a>')

        start = time.time_ns()
        print(f'[PARSING] Html to objects')

        nft_list = []
        for raw_data_block in a_split:
            raw_data_block = '<a' + raw_data_block
            raw_data_block = raw_data_block.replace('    ', '')
            raw_data_block = raw_data_block.replace(' ', '')

            nft = NFT(raw_data_block)
            nft_list.append(nft)

        end = time.time_ns()
        print(f'[PARSING] Parsing done {(end - start) / 1e6}ms')



class NFT:
    def __init__(self, raw_data) -> None:
        '''
        Parses given raw_data(string) to object
        '''
        # TODO: can be extended to page parsing, 
        #   I would takde data about this NFT from it's detail page
        self.m_raw_data = raw_data

        # Formating text, for easier manipulation
        data = NFT.format_data(raw_data)

        #split to individual lines
        lines = data.split(';--;\n')

        args, args_html = [], []
        #region Parsing args
        def parse_arg(new_list, condition, func):
            for line in lines:
                if condition(line):
                    new_list.append(func(line))

        # args without html tag
        parse_arg(
            args, 
            lambda x : not '<' in x, 
            lambda x: x.replace('\"', '').split(':') if not '<' in x else x
        )

        # extract args from html tag
        parse_arg(
            args_html, 
            lambda x : '<' in x, 
            lambda x : x.replace('<', '').replace('=', '').split('\"')[:2] if '<' in x else x, 
        )
        #endregion
        
        #region Implement args as attributes
        for attrib in args:
            if len(attrib) == 1: 
                continue

            setattr(self, attrib[0], attrib[1])

        # implement html_args as member attribs
        for attrib in args_html:
            if len(attrib) == 1: 
                continue

            setattr(self, 'm_'+attrib[0], attrib[1])
        #endregion

    @staticmethod
    def format_data(raw_data):
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



#region Console

#endregion



# a = Agent('solsnatchers')
# raw_html = a.request_collection(a.collection_url)
# a.parse_NFTs(raw_html)
