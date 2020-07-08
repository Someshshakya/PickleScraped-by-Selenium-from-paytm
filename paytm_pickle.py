from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
import time,os,json


##In this file we will scrap the data from the Paytm website and
# then we create an Html file where we will write the all the scraped data..

def details():
	if os.path.exists("pickle_final.json"):
		# print("data from the json file")
		with open("pickle_final.json","r") as file_open:
			file_read = file_open.read()
			store = json.loads(file_read)
			file_open.close()
			return store
	else:
		# print("data from the web")
		chrome_path = "/home/somesh/Desktop/chrome/chromedriver"
		driver = webdriver.Chrome(chrome_path)
		url = "https://paytmmall.com/shop/search?from=recentSearch&userQuery=pickle"
		driver.get(url)
		res = driver.execute_script('return document.documentElement.outerHTML')

		# html = driver.page_source
		soup = BeautifulSoup(res,"html.parser")
		# print(soup)

		final_list = []
		detail_dict = {"Rs.":"","Image":"","Brand Name":"","discount":""}
		main_div = soup.find_all(class_="_1fje")
		for i in main_div:
			each_div = i.find_all(class_="_2i1r")
			for each in each_div:

				#  This will scrap discount of each product
				allSpan = each.find("div",class_="_2bo3")
				spann = allSpan.find_all("span")
				if len(spann)>1:
					dis = each.find("span",class_="c-ax").text
					detail_dict["discount"]=dis[1:].strip()
				else:
					detail_dict["discount"]="0%"

				# This will scrap the url of the image
				image = each.find("img")["src"]
				detail_dict["Image"]=image

				# This will scrap the name of the brand
				quatity = each.find("div",class_="_2PhD")
				name = (quatity.text).split()
				name_of=""
				for pic in name:
					if pic in "Pickle":
						name_of+="Pickle"
						break
					name_of += pic+" "
				detail_dict["Brand Name"]=name_of.strip()

				# This will scrap the price of each product
				rs = each.find("div",class_="_1kMS").text
				detail_dict["Rs."]=rs+" -/"

				
				final_list.append(detail_dict)
				# print(detail_dict)
				detail_dict = {"Rs.":"","Image":"","Brand Name":"","discount":""}

				with open("pickle_final.json","w+") as file_open:
					dum = json.dumps(final_list) 
					file_open.write(dum)
					file_open.close()

		return final_list			
		# After scraping this will close the current tab
		driver.close()
		

# pprint(details())
# def s():
# 	with open("pickle2.json","r") as file_open:
# 		file_read = file_open.read()
# 		store = json.loads(file_read)
# 		file_open.close()
# 		return store

data = details()
# data = s()
def putting():
	with open("pickle1.html","w+") as file_open:
		file_open.write("<html>\n<head>\n<title>Pickle Entry</title>\n</head>\n<body>")
		file_open.write("<table border=1>")
		file_open.write("<tr>\n<td>S.No.</td>\n<td>Picture</td>\n<td>Name</td>\n<td>Price</td>\n<td>Discount</td>\n</tr>\n")
		c=1
		for pickle in data:
			print(pickle)
			name2 = pickle["Brand Name"]
			image2 = pickle["Image"]
			rs2 = pickle["Rs."]
			dicount2 = pickle["discount"]
			a = ' style="width:80px;height:100px"'
			file_open.write("<tr>")
			file_open.write("<td>"+str(c)+"."+"</td>"+"<td>"+'<img src="'+image2+'"'+a+'>'+"<td>"+name2+"</td>"+"</td>"+"<td>"+"Rs."+rs2+"</td>"+"<td>"+dicount2+"</td>")
			file_open.write("/<tr>")
			c+=1
		file_open.write("</table>\n</body>\n</html>")

pprint(putting())

# a = "somesh" +'"'
# print(a)