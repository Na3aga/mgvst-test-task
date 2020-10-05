import os
import aiohttp
import asyncio
import json


class API:
    ''' Basic functionality '''

    def __init__(self, firstname_lastname, count = 100):
        '''
        sets firstname_lastname for API calls and reads json file
        '''
        self.count = count # number of non-changes to stop making requests
        self.API_URL = f"https://www.magetic.com/c/test?api=1&name={firstname_lastname}"
        # constant to get cross-platform relational path to the file
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.games_file = os.path.join(THIS_FOLDER, 'data.txt')
        with open(self.games_file) as json_file:
            data = json.load(json_file)
            # make a names set from dictionary formatted elements 
            game_list = [dic["gamename"] for dic in data]
            self.game_names = set(game_list)
        print(self.game_names)

    async def get_games_names_async(self):
        '''
        stores len of game names set and compares after each asynchronous request
        if there was no change in the length => stop  
        '''
        prev_len = len(self.game_names)
        nogame = 0    
        async with aiohttp.ClientSession() as session:
            while (nogame < 50):
                async with session.get(self.API_URL) as resp:
                    txt = await resp.text()
                    # stop iteration after error
                    if(txt.split(';')[0] == 'Error 501'):
                        continue
                    else:
                        # update the set with names from response
                        new_set = txt.split(';')
                        self.game_names.update(new_set)
                        if(len(self.game_names) > prev_len):
                            nogame = 0
                            prev_len = len(self.game_names)
                            print(txt)
                        else: 
                            # increment if no changes in length
                            nogame +=1
        print(len(self.game_names))

    def get_games_names(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_games_names_async())

    def build_json(self):
        # make dictionary formatted elements of names from the names set 
        games_list = [{"gamename": game, "number": i+1} for i, game in enumerate(list(self.game_names))]
        with open(self.games_file, 'w') as outfile:
            json.dump(games_list, outfile)

    def print_json(self):
        ''' builds json before reading and printing json file'''
        self.build_json()
        with open(self.games_file) as json_file:
            data = json.load(json_file)
            print(data)
            return data


if __name__ == "__main__":
    ap = API('nazar_havryliuk')
    ap.get_games_names()
    ap.print_json()