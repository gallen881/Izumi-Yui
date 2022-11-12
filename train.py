from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import function
langs = ['english', 'chinese', 'japanese']
chatbot = {}
for lang in langs:
    chatbot[lang] = ChatBot(lang, database_uri=f'sqlite:///cmds/talk_data/{lang}.database')
    ChatterBotCorpusTrainer(chatbot[lang]).train(f'chatterbot.corpus.{lang}')
    function.print_time(f'Training {lang} done')