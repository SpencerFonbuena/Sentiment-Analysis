import asyncio
import pandas as pd
from twscrape import API, gather
from twscrape.logger import set_log_level

async def main():
    search_queries = [
        'venture capital'
    ]
    
    db_url = '/Users/spencerfonbuena/Documents/Python/FO/Sentiment Analysis/accounts.db'
    api = API(db_url)  # or API("path-to.db") - default is `accounts.db`
    #await api.pool.add_account('SFonbuena7734', 'Justg0tt@try', 'schfonbuena@gmail.com', 'sp3nc3rp00')
    #await api.pool.add_account('FonSpence26', 'Justg0tt@try', 'spencer@om.com', 'Th3g!ver1stime')
    #await api.pool.add_account('ClarkHeato24311', 'Justg0tt@try', 'procurement@om.com', 'Omspend159')
    
    await api.pool.login_all()
    data = pd.DataFrame()
    # search (latest tab)
    for ele in search_queries:
        test = await gather(api.search(ele, limit=1, kv={"product": "Top"}))
        pd_test = pd.DataFrame(test)
        data = pd.concat((data, pd_test))
    data.to_csv('test_output.csv', index=False)
    
if __name__ == "__main__":
    asyncio.run(main())