from seleniumbase import SB
import csv
import os

def scrape():
	item_list = []
	
	with SB(uc=True, incognito=True, ad_block=True) as sb:
		url = "https://www.idealista.pt/arrendar-casas/porto/com-apartamentos,moradias,equipamento_mobilado,arrendamento-longa-duracao/?ordem=precos-asc"

		sb.activate_cdp_mode(url)
		items = sb.cdp.select_all(".item-info-container")
		for item in items:
			price = item.query_selector(".item-price")
			address = item.query_selector(".item-link ")
			if price and address:
				link = address.get_attribute("href")
				if link:
					price = price.text.strip()
					address = address.text.strip()
					link = "https://www.idealista.pt" + link
					temp = [price, address, link]
					item_list.append(temp)

	if not os.path.isdir("csv"):
		os.mkdir("csv")
	
	with open("csv/idealista.csv", "a") as file:
		for i in item_list:
			writer = csv.DictWriter(file, fieldnames=["price", "address", "link"])
			writer.writerow({"price": i[0], "address": i[1], "link": i[2]})
