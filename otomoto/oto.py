from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, JavascriptException


def list_destails(index):
	list_parameter = browser.find_elements_by_xpath('//ul[1]/li[contains(@class,"offer-params__item")]')
	bike_type, bike_brand, bike_model, bike_production_date, bike_size, bike_power, bike_counter = (None,)*7

	for element in list_parameter:
		elementText = element.find_element_by_class_name('offer-params__label').text

		if elementText == code_model:
			bike_model = element.find_element_by_class_name('offer-params__link').text
		elif elementText == code_brand:
			bike_brand = element.find_element_by_class_name('offer-params__link').text
			if bike_brand.strip() == 'Romet':
				print("%d to Romet, next..." % index)
				return
		elif elementText == code_type:
			bike_type = element.find_element_by_class_name('offer-params__link').text
		elif elementText == code_production_date:
			bike_production_date = element.find_element_by_class_name('offer-params__value').text
		elif code_size == elementText:
			bike_size = element.find_element_by_class_name('offer-params__value').text
		elif code_power == elementText:
			bike_power = element.find_element_by_class_name('offer-params__value').text
		elif code_counter == elementText:
			bike_counter = element.find_element_by_class_name('offer-params__value').text
		elif code_engine_type == elementText:
			bike_engine_type = element.find_element_by_class_name('offer-params__value').text

			if bike_engine_type.strip() == 'Elektryczny':
				print("%d to Elektryk, next..." % index)
				return




	if bike_size != None:
		bike_size = bike_size.split(' ')[0]

	if bike_size == None or int(bike_size) > 240 and int(bike_size) < 400:
		str_oferta = 'Oferta %d: %s' % (index, link)
		str_details = '\n Marka: %s\n Model: %s\n Typ: %s\n Rok: %s\n Poj: %s\n Moc: %s\n Przebieg: %s\n ' % (bike_brand, bike_model, bike_type, bike_production_date, bike_size, bike_power, bike_counter)

		print(str_oferta)
		print(str_details)
	
		with open('moto.txt', 'a+') as file:
			file.write(str_oferta)
			file.write(str_details)

		file.close()
	else:
		return


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9014")
#Change chrome driver path accordingly
chrome_driver = "C:/Users/aro/Documents/chromedriver/chromedriver.exe"
browser = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)


# stringi:
code_brand = 'Marka pojazdu'
code_model = 'Model pojazdu'
code_production_date = 'Rok produkcji'
code_counter = 'Przebieg'
code_size = 'Pojemność skokowa'
code_power = 'Moc'
code_engine_type = 'Typ Silnika'
code_type = 'Typ'


URL = 'https://www.otomoto.pl/osobowe/od-2006/opoczno/?search%5Bfilter_float_price%3Ato%5D=12000&search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search%5Bfilter_enum_country_origin%5D%5B0%5D=pl&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=85&search%5Bcountry%5D='
URL_PAGE = 'https://www.otomoto.pl/motocykle-i-quady/od-2010/?search%5Bfilter_float_price%3Ato%5D=13000&search%5Border%5D=created_at%3Adesc&search%5Bcountry%5D=&page={}'

for i in range(20,30):
	browser.get(URL_PAGE.format(i))

	elems = browser.find_elements_by_xpath("//div/h2/a[contains(@class, 'offer-title__link')]")
	links = [link.get_attribute("href") for link in elems]

	print('Going thru page: %d...' % i)

	for index, link in enumerate(links):
		browser.get(link)
		print('%d. %s' % (index, link))
		list_destails(index)



























'''
with open('auta.txt', 'a+') as file:

	for link in links:
		print(('post: ' + link))
		browser.get(link)

		brand = browser.find_element_by_xpath('//ul[1]/li[3]/div/a').text
		carType = browser.find_element_by_xpath('//ul[1]/li[4]/div/a').text
		# version = browser.find_element_by_xpath('//ul[1]/li[5]/div/a').text
		# production = browser.find_element_by_xpath('//ul[1]/li[6]/div').text
		# distance = browser.find_element_by_xpath('//ul[1]/li[7]/div').text
		# engine = browser.find_element_by_xpath('//ul[1]/li[8]/div').text
		# fuel = browser.find_element_by_xpath('//ul[1]/li[9]/div/a').text
		# hp = browser.find_element_by_xpath('//ul[1]/li[10]/div').text

		str1 = (brand + " " + carType ) #+ " " + version + " " + production)
		# str2 = (distance + " " + engine + " " + fuel + " " + hp)
		postText = browser.find_element_by_xpath('//div[contains(@class,"offer-description__description")]').text

		print(str1)
		# print(str2)
		print(postText)

		file.write((link + '\n'))
		file.write((str1 + '\n'))
		# file.write((str2 + '\n'))
		file.write((postText + '\n'))
		file.write('\n')

	file.close()



brand = browser.find_element_by_xpath('//ul[1]/li[3]/div/a').text
model = browser.find_element_by_xpath('//ul[1]/li[4]/div/a').text
# version = browser.find_element_by_xpath('//ul[1]/li[5]/div/a').text
# production = browser.find_element_by_xpath('//ul[1]/li[6]/div').text
# distance = browser.find_element_by_xpath('//ul[1]/li[7]/div').text
# engine = browser.find_element_by_xpath('//ul[1]/li[8]/div').text
# fuel = browser.find_element_by_xpath('//ul[1]/li[9]/div/a').text
# hp = browser.find_element_by_xpath('//ul[1]/li[10]/div').text

str1 = (brand + " " + model ) #+ " " + version + " " + production)
# str2 = (distance + " " + engine + " " + fuel + " " + hp)
postText = browser.find_element_by_xpath('//div[contains(@class,"offer-description__description")]').text

print(str1, end ='\n')
# print(str2)
# print(postText)
'''



# elementText = lista[3].find_element_by_class_name('offer-params__label').text

# print(elementText)