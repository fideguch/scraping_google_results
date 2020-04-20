#google colaboratoryでの実行を想定
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from google.colab import files
from time import sleep

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
	file_name = (word + '.csv')
	df.to_csv(file_name , encoding = 'utf-8-sig')
	files.download(file_name)
	print("「{}」の検索結果を、csv形式で保存しました".format(word))
	sleep(5)

try:
	n = int(input("何KW分実行しますか？ : "))
except Exception :
	print("数字のみで入力してください！")
	n = int(input("何KW分実行しますか？ : "))
request = str(n) + "個の検索KWごとに、スペース区切りで入力してください \n（例：KWが3個の場合「東京観光　大阪食べ物　新宿ディナー」） : "
kw_list = (input(request).split())

for kw in kw_list:
	get_google_result(kw)
