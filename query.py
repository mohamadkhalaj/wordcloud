import re, random, requests
from stop_words import substitutions
from pxx import pox

def post_limitation(grapql_host, url_path_with_id):
	url = grapql_host + url_path_with_id
	ran = random.randrange(0, len(pox))
	j = requests.get(url).json()
	targetUser = j['data']['user']
	posts_count = targetUser['edge_owner_to_timeline_media']['count']
	if posts_count > 1000:
		return True
	return False

def start(instagramID, chat_id, message, bot, update):
	end_cursor = ''
	IGcontent = ''
	cc_count = 0
	url_host = 'https://www.instagram.com/'
	url_path = str(instagramID) + '/?__a=1'

	grapql_host = 'https://www.instagram.com/graphql/query/'
	url_path_with_id = ''

	try:
		url = url_host + url_path
		ran = random.randrange(0, len(pox))
		jsonPayload = requests.get(url).json()
		targetUserId = jsonPayload['graphql']['user']["id"]
		isPrivate = jsonPayload['graphql']['user']["is_private"]
		url_path_with_id = '?query_hash=472f257a40c653c64c666ce877d59d2b&variables={"id":"' + targetUserId + '","first":50,"after":""}'
	except Exception as Q:
		try:
			if (int(Q.getcode() / 100) == 4):
				message(chat_id = chat_id.chat_id, text = "کاربر یافت نشد!")
		except:
			message(chat_id = chat_id.chat_id, text = "مشکلی رخ داده است چند دقیقه دیگر دوباره تلاش کنید.")
		exit()
	if post_limitation(grapql_host, url_path_with_id):
		message(chat_id=chat_id.chat_id, text="صفحه مورد نظر شما بیش از 1000 پست دارد. فقط 1000 پست آخر آن استفاده می شود.")
	while 1:
		try:
			url = grapql_host + url_path_with_id
			ran = random.randrange(0, len(pox))
			j = requests.get(url).json()
			targetUser = j['data']['user']
			#print(str(targetUser))
			if isPrivate != True:
				items = targetUser['edge_owner_to_timeline_media']['edges']
				for item in items:
					edgeItems = item['node']['edge_media_to_caption']['edges']
					#print(str(edgeItems))
					for j in edgeItems:
						if 'node' in j:
							if 'text' in j['node']:
								#print(str(j['node']['text']))
								text_original = str(j['node']['text'])
								for x in substitutions:
									text_original = text_original.replace(x,substitutions[x])
								IGcontent += text_original

				#print(str(len(items)));
				if targetUser['edge_owner_to_timeline_media']['page_info']['has_next_page'] == True and cc_count <= 1000:
					end_cursor = targetUser['edge_owner_to_timeline_media']['page_info']['end_cursor']
					url_path_with_id = '?query_hash=472f257a40c653c64c666ce877d59d2b&variables={"id":"' + targetUserId + '","first":50,"after":"' + end_cursor + '"}'
					cc_count += len(items)
					stdout = '('
					stdout += str(int((cc_count) / targetUser['edge_owner_to_timeline_media']['count'] * 100))
					stdout +='%)'

					stdout += str(cc_count - 50) + ' پست '

					bot.edit_message_text(chat_id = chat_id.chat_id,
										  text = stdout,
										  message_id = update.message.message_id + 1)
					#time.sleep(5)
				else:
					bot.edit_message_text(chat_id = chat_id.chat_id,
										  text = '100%',
										  message_id = update.message.message_id + 1)

					message(chat_id = chat_id.chat_id, text = "درحال پردازش عکس...")
					return IGcontent
			else:
				message(chat_id = chat_id.chat_id, text = "این یوزر درحالت private قرار دارد برای استفاده از این ربات صفحه شما می بایست در حالت public باشد.")
				exit()
		except Exception as Q:
			print(str(Q))
			message(chat_id=chat_id.chat_id, text="مشکلی رخ داده است چند دقیقه دیگر دوباره تلاش کنید.")
			exit()
			message(chat_id = chat_id.chat_id, text = "مشکلی رخ داده است چند دقیقه دیگر دوباره تلاش کنید.")
			#time.sleep(5)

def replace(string, substitutions):

	substrings = sorted(substitutions, key=len, reverse=True)
	regex = re.compile('|'.join(map(re.escape, substrings)))
	return regex.sub(lambda match: substitutions[match.group(0)], string)