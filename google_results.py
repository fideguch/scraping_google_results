#実行するとデスクトップのresult_csvに保存される

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import sys

def get_google_result(kw):
	word = kw

	target_url = ('https://www.google.co.jp/search?hl=ja&num=10&q=' + word)
	# print(target_url)

	html_doc = requests.get(target_url).text
	soup = BeautifulSoup(html_doc, 'html.parser')

	columns = ["タイトル", "URL"]
	df = pd.DataFrame(columns=columns)

	page_tags = soup.select("div.kCrYT > a") #googleのアップデートにより、要修正

	for tag in page_tags:
		get_list = tag.find_all("div")
		title = get_list[0].string
		page_url = get_list[1].string
		se = pd.Series([title, page_url], columns)
		df = df.append(se, columns)
		try:
			df.to_csv('/Users/ユーザー名/Desktop/result_csv/{}.csv'.format(word))
		except Exception:
			os.system('cd ~/Desktop ;mkdir result_csv')
			df.to_csv('/Users/fumito.i/Desktop/result_csv/{}.csv'.format(word))
	print("「{}」の検索結果を、csv形式で保存しました".format(word))

try:
	n = int(input("何KW分実行しますか？ : "))
except Exception :
	print("数字のみで入力してください！")
	n = int(input("何KW分実行しますか？ : "))
request = str(n) + "個の検索KWごとに、スペース区切りで入力してください（例：KWが3個の場合「東京観光　大阪食べ物　新宿ディナー」） : "
kw_list = (input(request).split())

for kw in kw_list:
	get_google_result(kw)
