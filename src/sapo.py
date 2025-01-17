from seleniumbase import SB
import csv
import os

def scrape():
	item_list = []

	with SB(uc=True, incognito=True, ad_block=True) as sb:
		url = "https://casa.sapo.pt/alugar-apartamentos/mais-baratos/porto/?lp=600"

		sb.activate_cdp_mode(url)
		items = sb.cdp.select_all(".property-info-content")
		for item in items:
			price = item.query_selector(".property-price-value")
			ptype = item.query_selector(".property-type")
			address = item.query_selector(".property-location")
			info = item.query_selector(".property-info")
			if price and ptype and address and info:
				price = price.text.strip()
				location = ptype.text.strip() + ", " + address.text.strip()
				link = info.get_attribute("href")
				if link:
					link = link
					temp = [price, location, link]
					item_list.append(temp)

	if not os.path.isdir("csv"):
		os.mkdir("csv")

	with open("csv/sapo.csv", "a") as file:
		for i in item_list:
			writer = csv.DictWriter(file, fieldnames=["price", "location", "link"])
			writer.writerow({"price": i[0], "location": i[1], "link": i[2]})
