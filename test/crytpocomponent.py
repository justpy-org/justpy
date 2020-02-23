import justpy as jp
from datetime import datetime
import asyncio
#{"data":{"base":"ETH","currency":"USD","amount":"187.005"}}
#r = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')

class CryptoQuote(jp.Div):


    def __int__(self, **kwargs):
        self.crypto = 'BTC'
        self.currency = 'USD'
        self.value = None
        super().__init__(**kwargs)
        self.quote_time = None
        jp.run_task(self.get_quote())

    async def get_quote(self):
        while True:
            r = await jp.get(f'https://api.coinbase.com/v2/prices/{self.crypto}-{self.currency}/spot')
            print(r)
            self.quote_time = datetime.now()
            await asyncio.sleep(2)



