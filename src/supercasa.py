from seleniumbase import SB
import csv
import os

def scrape():
	item_list = []

	with SB(uc=True, incognito=True, ad_block=True) as sb:
		url = "https://supercasa.pt/arrendar-casas/porto?ordem=preco-asc"

		sb.activate_cdp_mode(url)
		items = sb.cdp.select_all(".property-info")
		for item in items:
			price = item.query_selector(".property-price")
			title = item.query_selector(".property-list-title")
			description = item.query_selector(".property-description-text")
			if price and title and description:
				price = price.text.split(" ")
				price = price[0] + price[1]
				price = price.strip()
				link = title.get_attribute("href")
				link = "https://supercasa.pt" + link
				title = title.text.strip()
				description = description.text.strip()
				
				temp = [price, title, description, link]
				item_list.append(temp)

	if not os.path.isdir("csv"):
		os.mkdir("csv")

	with open("csv/supersaca.csv", "a") as file:
		for i in item_list:
			writer = csv.DictWriter(file, fieldnames=["price", "title", "description", "link"])
			writer.writerow({
								"price": i[0],
								"title": i[1],
								"description": i[2],
								"link": i[3]})
