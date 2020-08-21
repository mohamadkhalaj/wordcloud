#!/usr/bin/env python3
import re, query
from wordcloud_fa import WordCloudFa

def removeWeirdChars(text):
		weridPatterns = re.compile("["
									u"\U0001F600-\U0001F64F"  # emoticons
									u"\U0001F300-\U0001F5FF"  # symbols & pictographs
									u"\U0001F680-\U0001F6FF"  # transport & map symbols
									u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
									u"\U00002702-\U000027B0"
									u"\U000024C2-\U0001F251"
									u"\U0001f926-\U0001f937"
									u'\U00010000-\U0010ffff'
									u"\u200d"
									u"\u2640-\u2642"
									u"\u2600-\u2B55"
									u"\u23cf"
									u"\u23e9"
									u"\u231a"
									u"\u3030"
									u"\ufe0f"
									u"\u2069"
									u"\u2066"
									u"\u200c"
									u"\u2068"
									u"\u2067"
									"]+", flags=re.UNICODE)
		return weridPatterns.sub(r'', text)

def get_image(UserID, chat_id, message, bot, update):
	if len(UserID)<2:
		message(chat_id = chat_id.chat_id, text = "آی دی نامعتبر است!")
	else:
		message(chat_id = chat_id.chat_id, text = "در حال اتصال به اینستاگرام...")
		allword=query.start(UserID, chat_id, message, bot, update)
		allword_edited = removeWeirdChars(allword)
		my_wordcloud=WordCloudFa(font_path="Sahel.ttf",background_color="white",width=720, height=1280, margin=2).generate(allword_edited)

		image = my_wordcloud.to_image()
		saved_dir = 'analysis/' + str(UserID) + '.jpg'
		image.save(saved_dir)
		message(chat_id = chat_id.chat_id, text = "درحال ارسال عکس...")
		return saved_dir