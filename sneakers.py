import requests
import random
import time

#add your own discord webhook link
def send_embed_with_info(product_description):
	webhook_link = "url"
	embed = {
		"url":"https:"+product_description['meta_data']["canonical"],
		"author":{
			"name":"Nigger sneakers"
		},
		"title": f"{product_description['name']}[{product_description['id']}]",
		"description": product_description['product_description']['subtitle']+f"\nPrice: {product_description['pricing_information']['currentPrice']}€",
		"image":{
			"url":product_description['product_description']['description_assets']['image_url']
		}
	}
	reponse = requests.post(webhook_link,json={
		"embeds":[embed]
	})
def generate_search_url(offset=0,search_keyword="all"):
	search_keyword.replace(" ","%20")
	url = f"https://www.adidas.fr/api/plp/content-engine/search?query={search_keyword}&start={offset}"
	return url
def get_all_searched_for_items(keyword="all"):
	print(f"Started search on adidas.fr with keyword: [{keyword}]...")
	s = requests.session()
	s.headers.update( {'User-Agent': 'Mozilla/5.0'} )
	url = generate_search_url(search_keyword=keyword)
	response = s.get(url)
	response = response.json()
	number_of_elements = response["raw"]["itemList"]["count"]
	number_of_elements_in_page = response["raw"]["itemList"]["viewSize"]
	desired_products_ids = []
	for i in range(0,number_of_elements,number_of_elements_in_page):
		completion_percentage = (i*10)/number_of_elements
		progress = "["+int(completion_percentage)*"="+(10-int(completion_percentage))*" "+"]"
		print(f"Search_progress {round(completion_percentage*10,3)}/100: "+progress+"...",end="\r")
		#time.sleep(random.randint(100,4000)/1000)
		this_url = generate_search_url(offset=i,search_keyword=keyword)
		response = s.get(this_url)
		response = response.json()
		for u in range(len(response["raw"]["itemList"]["items"])):
			desired_products_ids.append(response["raw"]["itemList"]["items"][u]["productId"])
	print( f"Search_progress 100.00/100: [" + 10*"=" + "]...", end="\n" )
	print(f"Completed search for {keyword}!")
	s.close()
	return desired_products_ids
def get_all_infos(id):
	s = requests.session()
	header1 = {'User-Agent': 'Mozilla/5.0'}
	s.headers.update(header1)
	response = s.get(f"https://www.adidas.fr/api/products/{id}")
	product_info = response.json()
	try:
		print("Product id:",product_info["id"])
		print("Product name:",product_info["name"])
		print(product_info["pricing_information"]["currentPrice"],"€")
	except:
		print(product_info)
	s.close()
	return product_info


ids = get_all_searched_for_items(keyword="sneakers")
for id in ids:
	product_info = get_all_infos(id)
	try:
		send_embed_with_info(product_info)
	except:
		pass
	print("="*50)
	time.sleep(random.randint(10,1000)/1000)
