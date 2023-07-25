import telebot
import requests
token = "6001141946:AAGMm3RTtAh2vbc_HoCm6fDDWNp66z2heZE"
bot = telebot.TeleBot(token)

keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'йена': 'JPY',
    'лира': 'TRY',
    'рубль': 'RUB'
}
names = {
    'доллар': 'долларов',
    'евро': 'евро',
    'йена': 'йен',
    'лира': 'лир',
    'рубль': 'рублей'

}


class ConvertException(Exception):
    pass


class Com:
    def __init__(self, com_name, text_of_com):
        self.com_name = com_name
        self.text_of_com = text_of_com

    def set_com(self, com_name, text_of_com):
        self.com_name = com_name
        self.text_of_com = text_of_com

    def get_name(self):
        return self.com_name

    def get_text(self):
        return self.text_of_com

    def stat_of_com(self):
        @bot.message_handler(commands=[f'{self.get_name()}'])
        def enter_com(message: telebot.types.Message):
            bot.reply_to(message, self.get_text())


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    val = message.text.split(' ')
    quote, base, amount = val
    if len(val) != 3:
        raise ConvertException('Неверное количество вводимых данных')
    try:
        keys_ticker_base = keys[base]
    except KeyError:
        raise ConvertException(f'Невозможно перевести валюту {base}')
    try:
        keys_ticker_quote = keys[quote]
    except KeyError:
        raise ConvertException(f'Невозможно перевести валюту {quote}')
    r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym="
                     f"{keys_ticker_quote}&tsyms={keys_ticker_base}").json()
    t = r[keys[base].upper()] * int(amount)
    bot.send_message(message.chat.id, f"{str(t)} {names[base]}")


start = Com('start', 'приветствуем вас в нашем конвертируещем валюты боте.\n Для того что-бы начать работу, '
                     'введите данные в формате\n <валюта которую хотим перевести> <в какую хотим перевести> '
                     '<количество переводимой валюты>\n для того чтобы узнать список валют введите /values')

bot.polling(none_stop=True)
