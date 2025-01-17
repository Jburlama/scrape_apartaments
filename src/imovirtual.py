from seleniumbase import SB
import csv
import os

def scrape():
	item_list = []

	with SB(uc=True, incognito=True, ad_block=True) as sb:
		url = "https://www.imovirtual.com/pt/resultados/arrendar/apartamento/porto/porto?by=PRICE&direction=ASC&viewType=listing"
		sb.activate_cdp_mode(url)
		items = sb.cdp.select_all(".css-13gthep")
		for item in items:
			price = item.query_selector(".css-2bt9f1")
			short_desc = item.query_selector(".css-u3orbr")
			location = item.query_selector(".css-42r2ms")
			link = item.query_selector(".css-16vl3c1")
			if price and short_desc and location and link:
				link = "https://www.imovirtual.com" + link.get_attribute("href")
				price = price.text.strip()
				short_desc = short_desc.text.strip()
				location = location.text.strip()

				temp_list = [price, location, short_desc, link]
				item_list.append(temp_list)

	if not os.path.isdir("csv"):
		os.mkdir("csv")

	with open("csv/imovirtual.csv", "a") as file:
		for i in item_list:
			writer = csv.DictWriter(file, fieldnames=["price", "location", "short_desc", "link"])
			writer.writerow({
							"price": i[0],
							"location": i[1],
							"short_desc": i[2],
							"link": i[3]})
