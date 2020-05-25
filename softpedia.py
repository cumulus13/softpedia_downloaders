#!c:/SDK/Anaconda2/python.exe
from __future__ import print_function
import os, sys
import requests
from bs4 import BeautifulSoup as bs
from pydebugger.debug import debug
from make_colors import make_colors
import re
import ast
from idm import IDMan
from pywget import wget
import traceback
import argparse
import textwrap
import cmdw
try:
	import tkimage
except:
	from . import tkimage
if sys.version_info.major == 3:
	raw_input = input
	import urllib.parse as urllib
else:
	import urllib
import inspect
import msvcrt as getch
from multiprocessing import Process


class softpedia_error(Exception):
	pass
	
class softpedia(object):
	def __init__(self):
		super(softpedia, self)
		self.all_page_data = []
		self.first_screenshot_view = False
		self.has_get_screenshot = False
		
	def pause(self, page=''):
		lineno = str(inspect.stack()[1][2])		
		if page:
			page = make_colors("[" + str(page) + "]", "lw", "bl")
		else:
			page = make_colors("[" + str(lineno) + "]", "lw", "bl")
		note = make_colors("Enter to Continue . ", "lw", "lr") + "[" + page + "] " + make_colors("x|q = exit|quit", "lw", "lr")
		print(note)
		q = getch.getch()
		if q == 'x' or q == 'q':
			sys.exit(make_colors("EXIT !", 'lw','lr'))
	
	def download(self, url, download_path=os.getcwd(), confirm=False, use_wget=False):
		if use_wget:
			wget.download(url, download_path)
		else:
			try:
				idm = IDMan()
				idm.download(url, download_path, confirm=confirm)
			except:
				traceback.format_exc()
				wget.download(url, download_path)
				
	def get_download_link(self, url, download_path=os.getcwd(), confirm=False, show_download_link=False):
		a = requests.get(url)
		b = bs(a.content, 'lxml')
		
		download_link_0 = b.find('a', {'itemprop':'downloadUrl'}).get('onclick')
		debug(download_link_0 = download_link_0, debug=False)
		data = re.findall("popup6_open\({(.*?),tsf", download_link_0)
		debug(data=data,debug=False)
		if data:
			data = "{"+ data[0] + "}"
			data = ast.literal_eval(data)
		debug(data=data,debug=False)
		
		if data:
			url1 = "https://www.softpedia.com/_xaja/dlinfo.php"
			a1 = requests.post(url1, data=data)
			b1 = bs(a1.content, 'lxml')
			dllinkbox2 = b1.find_all('div', {'class':'dllinkbox2'})
			debug(dllinkbox2=dllinkbox2, debug=False)
			
			if dllinkbox2:
				download_link_print = ""
				if len(dllinkbox2) > 1:
					n = 1
					for i in dllinkbox2:
						number = str(n)
						if len(str(n)) == 1:
							number = "0" + str(n)
						if show_download_link:
							download_link_print = "[" + make_colors(self._download(i, download_path, confirm, False), 'lightred', 'lightyellow') + "]"
						print(make_colors(number + ".", 'lightyellow') + " " + make_colors(i.find('a').get('title'), 'lightwhite', 'lightblue') + " " + download_link_print)
						n += 1
					q = raw_input(make_colors("Select number to download:", 'black', 'lightgreen') + " ")
					if q and str(q).strip().isdigit() and not int(str(q).strip()) > len(dllinkbox2):
						if show_download_link:
							print(make_colors("Start download", "lightcyan") + ": " + make_colors(download_link_print, "lightwhite", "lightmagenta"))
						self._download(i, download_path, confirm)
				else:
					if show_download_link:
						download_link_print = "[" + make_colors(self._download(dllinkbox2[0], download_path, confirm, False), 'lightred', 'lightyellow') + "]"
						print(make_colors("Start download", "lightcyan") + ": " + make_colors(download_link_print, "lightwhite", "lightmagenta"))
					self._download(dllinkbox2[0], download_path, confirm)
				
		else:
			print(make_colors("NO DATA !", "lightwhite", "lightred"))
			
	def _download(self, dllinkbox2, download_path=os.getcwd(), confirm=False, download_it=True):
		link = dllinkbox2.find('a').get('href')
		a2 = requests.get(link)
		b2 = bs(a2.content, 'lxml')
		download_link = b2.find('div', {'id':'manstart'}).find('a').get('href')
		debug(download_link = download_link, debug=False)
		if download_link:
			if download_it:
				self.download(download_link, download_path, confirm)
			return download_link
		else:
			print(make_colors("NO Download Link Found !", "lightwhite", "lightred"))
		return False
		
	def get_homepage(self, url, bs_object=None, show = False):
		if not bs_object:
			a = requests.get(url)
			bs_object = bs(a.content, 'lxml')
			b = bs_object
		else:
			b = bs_object
		dt_upcase = b.find('dt', {'class':'upcase hp'})
		debug(dt_upcase=dt_upcase)
		if dt_upcase:
			homepage = dt_upcase.find('a').get('data-href')
			if show:
				print(make_colors("HomePage", 'lightwhite', 'lightblue') + ": " + make_colors(homepage, "lightred", 'lightyellow'))
			return homepage
		else:
			publisher = b.find('dd', {'itemprop': 'publisher'})
			if not publisher:
				debug(url = url)
				self.pause()
				print(make_colors("No Homepage !", "lightwhite", "lightred"))
			else:
				publisher_link = publisher.find('a')
				if publisher_link:
					homepage = publisher_link.get('href')
					if show:
						print(make_colors("HomePage", 'lightwhite', 'lightblue') + ": " + make_colors(homepage, "lightred", 'lightyellow'))
					return homepage
				else:
					debug(url = url)
					debug(publisher_link = publisher_link)
					self.pause()
					print(make_colors("No Homepage Link !", "lightwhite", "lightred"))
		return False
			
	def get_title(self, url, bs_object=None):
		if not bs_object:
			a = requests.get(url)
			bs_object = bs(a.content, 'lxml')
			b = bs_object
		else:
			b = bs_object
		container_48 = b.find('div', {'class':'pagetop grid_48 pagetop2 srcnobg pagetopbrd'}).find('h1')
		debug(container_48 = container_48)
		title = container_48.find('a').get('title')
		debug(title=title)
		name = container_48.find('a').find('span').text
		debug(name=name)
		return title, name
		
				
	
	def del_evenReadonly(self, action, name, exc):
		import stat
		os.chmod(name, stat.S_IWRITE)
		os.remove(name)
		
	def get_screenshot(self, url, bs_object=None, show=False, confirm=False):
		if not bs_object:
			a = requests.get(url)
			bs_object = bs(a.content, 'lxml')
		b = bs_object
		
		images = []
		scrslide_posrel = b.find('div', {'class':'scrslide posrel'})
		debug(scrslide_posrel = scrslide_posrel)
		if not scrslide_posrel:
			#self.pause()
			print(make_colors("No Screenshot !", "lightwhite", "lightred"))
			return images
		slide = scrslide_posrel.find('div', {'class':'slide'})
		
		all_image_a = slide.find_all('a')
		for i in all_image_a:
			images.append(i.get('href'))
		debug(show=show)
		if show:
			images_downloaded = []
			title, name = self.get_title(url, bs_object=b)
			if not os.path.isdir(os.path.join(os.path.dirname(__file__), "temp")):
				os.makedirs(os.path.join(os.path.dirname(__file__), "temp"))
			else:
				#os.removedirs("temp")
				#os.unlink("temp")
				debug(first_screenshot_view = self.first_screenshot_view)
				if not self.first_screenshot_view:
					import shutil
					shutil.rmtree("temp", onerror = self.del_evenReadonly)
					os.makedirs(os.path.join(os.path.dirname(__file__), "temp"))
			for i in images:
				if not self.first_screenshot_view:
					self.download(i, os.path.join(os.path.dirname(__file__), "temp"), confirm, True)
				if os.path.isfile(os.path.join(os.path.dirname(__file__), "temp", os.path.basename(i))):
					images_downloaded.append(os.path.join(os.path.dirname(__file__), "temp", os.path.basename(i)))
			debug(images_downloaded=images_downloaded)
			if len(images_downloaded) > 2:
				#tkimage.showImage(title, images_downloaded[0], images_downloaded[1], images_downloaded[1:])
				#tkimage.main("temp")
				tx = Process(target=tkimage.main, args=("temp", ))
				tx.start()
				self.first_screenshot_view = True
			return images_downloaded
		return images
	
	def search(self, query, download_path=os.getcwd(), confirm=False, show_download_link=False, n=1):
		data = {}
		url = "https://www.softpedia.com/dyn-search.php?search_term=" + str(query)
		a = requests.get(url)
		b = bs(a.content, 'lxml')
		container_48 = b.find_all('div', {'class':'container_48'})
		debug(container_48 = container_48[2])
		page_head = container_48[2].find('div', {'class':'pagetop grid_48'}).find('h1')
		if page_head:
			page_head = page_head.text
			print(make_colors(str(page_head).upper(), 'b', 'lg'))
		debug(page_head = page_head)
		warning = container_48[2].find('h2', {'class':'grid_48 mgbot_30 fsz32 nosel srctitle col-red-l'})
		if warning:
			warning = warning.text
			debug(warning = warning)
			return warning, False, False
		
		#self.pause()
		all_div = container_48[2].find_all('div', {'class': re.compile('grid_48 dlcls dlcls')})
		debug(all_div = all_div)
		if not all_div:
			self.pause()
		for i in all_div:
			info_fr = i.find('div', {'class':'info fr'}).find_all('li')
			#debug(info_fr = info_fr)
			downloaded = ""
			size = ""
			if info_fr and len(info_fr) == 2:
				downloaded = re.split(" downloads| download", info_fr[0].text)[0]
				debug(downloaded = downloaded)
				size = info_fr[1].text
				debug(size=size)
			
			title_a = i.find('h4', {'class':'ln'}).find('a')
			link = title_a.get('href')
			title = title_a.get('title')
			debug(link = link)
			debug(title = title)
			description = i.find('p', {'class':'ln'}).text
			debug(description= description)
			
			div_ln = i.find('div', {'class':'ln'})
			upload = ""
			rating = ""
			support = ""
			upload = div_ln.find('div', {'class':'ts'})
			if upload:
				upload = upload.text
			rating = div_ln.find('div', {'class':'rating'})
			if rating:
				rating = rating.get('title')
			support = div_ln.find('div', {'class':'os'})
			if support:
				support = support.text
			
			data.update({
				n: {'title':title,
					'description': description,
					'size':size,
					'downloaded':downloaded,
					'upload':upload,
					'rating':rating,
					'support':support,
					'link':link,
				}})
			n+=1
			
			debug(upload = upload)
			debug(rating=rating)
			debug(support=support)
			if os.getenv('debug'):
				print("-"*100)
		
		debug(data=data)
		nums_page, page = self.pagination(url, b)
		return data, nums_page, page
		
	def _get(self, url, bs_object=None, get_screenshot=False):
		if get_screenshot:
			self.has_get_screenshot = True
		if not bs_object:
			a = requests.get(url)
			bs_object = bs(a.content, 'lxml')
			b = bs_object
		else:
			b = bs_object
			
		screenshot = []
		homepage = self.get_homepage(url, bs_object)
		title = self.get_title(url, bs_object) # title, name
		if get_screenshot:
			screenshot = self.get_screenshot(url, bs_object, show = True)
		license = self.get_license(url, bs_object)
		description = self.get_description(url, bs_object) # head, main_description, origin
		
		return license, description, homepage, title, screenshot
	
	def _get_index(self, check, all_page_data):
		index_0 = None
		index_1 = None
		if self.all_page_data:
			for i in all_page_data:
				index_0 = i.index(check)
				index_1 = all_page_data.index(i)
				if index_0:
					break
			if index_0:
				return index_1
			else:
				raise softpedia_error(make_colors("No Index for data check !", 'lightwhite', 'lightred', ['blink']))
		else:
			raise softpedia_error(make_colors("No data all_page_data !", 'lightwhite', 'lightred', ['blink']))
		
	def wrap_description(self, description):
		_prefix = len('Short Description') + 2
		if cmdw.getWidth() < 112:
			width = cmdw.getWidth() - (_prefix + 2)
		else:
			width = int((cmdw.getWidth() / 2) - (_prefix + 2))
		prefix = " " * _prefix
		wrapped = textwrap.wrap(description, width = width)
		#debug(wrapped = wrapped)
		if len(wrapped) > 1:
			first_line = wrapped[0]
			print(make_colors(first_line, 'lightblue'))
			for i in wrapped[1:]:
				print(prefix + make_colors(i, 'lightcyan'))
		else:
			return make_colors(description, 'lightgreen')

	def _print_description_wrap(self, description = None, number = None):
		if number and isinstance(number, int):
			if self.all_page_data:
				license, description, homepage, title, screenshot = self.all_page_data[number]
				print(make_colors(title[1], 'lightwhite', 'magenta'))
				print(make_colors("Short Description :", "lightwhite", "blue") + self.wrap_description(description[0]))
				sys.stdout.write(make_colors("Long Description  :", "lightwhite", "green"))
				self.wrap_description(description[1])
				
		else:
			if isinstance(description, tuple):
				if self.all_page_data:
					index = self._get_index(description, self.all_page_data)
					if index:
						license, description, homepage, title, screenshot = self.all_page_data[index]
						print(make_colors(title[1], 'lightwhite', 'magenta'))
						print(make_colors("Short Description :", "lightwhite", "blue") + self.wrap_description(description[0]))
						sys.stdout.write(make_colors("Long Description  :", "lightwhite", "green"))
						self.wrap_description(description[1])
					else:
						raise softpedia_error(make_colors("No Index Found !", 'lightwhite', 'lightred', ['blink']))
				else:
					print(make_colors("Short Description :", "lightwhite", "blue") + self.wrap_description(description[0]))
					sys.stdout.write(make_colors("Long Description  :", "lightwhite", "green"))
					self.wrap_description(description[1])
			else:
				raise softpedia_error(make_colors("Invalid data tupple of description !", 'lightwhite', 'lightred', ['blink']))
			
	def _print_center(self, strings, foreground, background = None):
		width = cmdw.getWidth()
		if len(strings) < width:
			_width = (width - len(strings)) / 2
			print((" " *(_width - 2)) + make_colors(strings, foreground, background))
		else:
			print(make_colors(strings, foreground, background))
			
	def _print_description(self, description = None, number = None, url = None):
		if url:
			license, description, homepage, title, screenshot = self._get(url)
			self._print_center(title[1], 'lightwhite', 'magenta')
			self._print_center(description[0], "lightwhite", "blue")
			self._print_center(description[2][0].strip(), "lightcyan")
			print(make_colors("\n".join(description[2][1:]), "lightcyan"))
			
		elif number and isinstance(int(str(number).strip()), int):
			if self.all_page_data:
				license, description, homepage, title, screenshot = self.all_page_data[number]
				self._print_center(title[1], 'lightwhite', 'magenta')
				self._print_center(description[0], "lightwhite", "blue")
				self._print_center(description[2][0].strip(), "lightcyan")
				print(make_colors("\n".join(description[2][1:]), "lightcyan"))
	
		else:
			if isinstance(description, tuple):
				if self.all_page_data:
					index = self._get_index(description, self.all_page_data)
					if index:
						license, description, homepage, title, screenshot = self.all_page_data[index]
						self._print_center(title[1], 'lightwhite', 'magenta')
						self._print_center(description[0], "lightwhite", "blue")
						self._print_center(description[2][0].strip(), "lightcyan")
						print(make_colors("\n".join(description[2][1:]), "lightcyan"))
					else:
						raise softpedia_error(make_colors("No Index Found !", 'lightwhite', 'lightred', ['blink']))
				else:
					self._print_center(description[0], "lightwhite", "blue")
					self._print_center(description[2][0].strip(), "lightcyan")
					print(make_colors("\n".join(description[2][1:]), "lightcyan"))
			else:
				raise softpedia_error(make_colors("Invalid data tupple of description !", 'lightwhite', 'lightred', ['blink']))		
		
	def get_license(self, url, bs_object=None):
		if not bs_object:
			a = requests.get(url)
			bs_object = bs(a.content, 'lxml')
			b = bs_object
		else:
			b = bs_object
		
		license = b.find('div', {'class':'grid_37 prefix_1 fr'}).find('span', {'class':re.compile('bold upcase license ')})
		if license:
			license = license.find('span', {'class':re.compile('col-')}).text.strip()
			return license
		else:
			debug(license = b.find('div', {'class':'grid_37 prefix_1 fr'}))
		return " "
		
	def pagination(self, url, bs_object=None):
		if not bs_object:
			a = requests.get(url)
			bs_object = bs(a.content, 'lxml')
			b = bs_object
		else:
			b = bs_object
		
		div_fr_ta_right = b.find('div', {'class':'fr ta_right'})
		debug(div_fr_ta_rightv = div_fr_ta_right)
		if div_fr_ta_right:
			nums_page = None
			nums_page = div_fr_ta_right.find('a', {'title':'Navigate to last page'})
			debug(nums_page = nums_page)
			#self.pause()
			if nums_page:
				nums_page = nums_page.text
			debug(nums_page = nums_page)
			all_a = div_fr_ta_right.find_all('a')
			pages = {}
			for i in all_a:
				try:
					pages.update({int(i.text): i.get('href')})
				except:
					pages.update({i.text: i.get('href')})
			debug(pages = pages)
		
			return nums_page, pages
		return False, False
		
	def print_nav(self, error=None):
		note1 = make_colors("Select Number", 'lightwhite', 'lightblue') + " [" + make_colors("[n]d = download n", 'lightgreen') + ", " + make_colors("[n]i = get info n", "lightmagenta") + ", " + make_colors("[n]s = Show Screenshot", "lightyellow") + ", " + make_colors("[n]p = Go to page n", 'lightcyan') + ", " +  make_colors("e[x]it|[q]uit = exit|quit", 'lightred') + ", " + make_colors("download_path=[dir], set download path", 'lightblue') + ", " + make_colors("[n = Number selected] default select number is get info n", 'lightwhite', 'lightblue') + ": "
		if error:
			if error == 0 or error == "0":
				print(make_colors("No Download Found !", "lightwhite", "lightred", ['blink']))
				return False, make_colors("No Download Found !", "lightwhite", "lightred", ['blink'])
			elif error == 1 or error == '1':
				print(make_colors("No DATA Found !", "lightwhite", "lightred", ['blink']))
				return False, make_colors("No DATA Found !", "lightwhite", "lightred", ['blink'])
		q = raw_input(note1)
		return True, q
		
	def get_description(self, url, bs_object=None):
		if not bs_object:
			a = requests.get(url)
			bs_object = bs(a.content, 'lxml')
			b = bs_object
		else:
			b = bs_object
		
		edreview = b.find('div', {'id':'edreview'})
		head = edreview.find('h2').find('strong', {'class':'fl'}).text
		debug(head=head)
		mgbot_10 = edreview.find_all('p', {'class':'mgbot_10'})
		description_pre = []
		description = []
		for i in mgbot_10:
			description_pre.append(urllib.unquote(i.text))
		
		for i in description_pre:
			description.append(i.encode('utf-8'))
		long_desc = "\n".join(description)
		debug(long_desc=long_desc)
		
		return urllib.unquote(head), long_desc, description
		
	def navigator(self, search_query=None, download_path=os.getcwd(), confirm=False, show_download_link=False, use_wget=False, show_license=False, data_search=None, nums_page=None, page=None):
		license, description, homepage, title, screenshot = '', '', '', '', ''
		if not search_query:
			search_query = raw_input("What Search for:", "lightwhite", "lightblue")
		#if not data_search and not page:
		if search_query and not data_search:
			data_search, nums_page, page = self.search(search_query, download_path, confirm, show_download_link)
			debug(data_search = data_search)
			if isinstance(data_search, str) or isinstance(data_search, unicode):
				print(make_colors(data_search, 'lw','lr', ['blink']))
				sys.exit()
		else:
			debug(data_search = data_search)
			if isinstance(data_search, str) or isinstance(data_search, unicode):
				print(make_colors(data_search, 'lw','lr', ['blink']))
				sys.exit()
			if show_license:
				self.all_page_data = []
			for i in data_search:
				license = ""
				if show_license:
					license, description, homepage, title, screenshot = self._get(data_search.get(i).get('link'))
					self.all_page_data.append([license, description, homepage, title, screenshot])
					#license = self.get_license(data_search.get(i).get('link'))
					license = "[" + make_colors(license, "lightred", "lightwhite") + "]"
				number = str(i)
				if len(number) == 1:
					number = "0" + number
				print(make_colors(number, 'lightyellow') + ". " + make_colors(data_search.get(i).get('title'), 'lightwhite', 'blue') + " [" + make_colors(data_search.get(i).get('size'), 'lightwhite', 'lightmagenta') + " | " + make_colors(data_search.get(i).get('downloaded'), 'black', 'lightgreen') + "]" + license)
			if nums_page:
				print(make_colors("Numbers Of Page:", 'lightwhite', 'magenta') + " " + make_colors(str(nums_page), 'lightred', 'lightwhite'))
			check_error, q = self.print_nav()
			if q and str(q).isdigit() and int(q) <= len(list(data_search.keys())):
				#self.pause()
				description = ''
				if not self.all_page_data:
					url = data_search.get(int(str(q).strip())).get('link')
					license, description, homepage, title, screenshot = self._get(url)
				if not self.has_get_screenshot and not screenshot:
					screenshot = self.get_screenshot(url, show = True)
				print("\n")
				print(make_colors("NAME", 'lightcyan') + (12 - 4) * ' ' + ":" + make_colors(title[0], 'lightwhite', 'blue'))
				print(make_colors("LICENSE", 'lightred') + (12 - 7) * ' ' + ":" + make_colors(license, 'lightwhite', 'red'))
				print(make_colors("HOMEPAGE", 'lightgreen') + (12 - 8) * ' ' + ":" + make_colors(homepage, 'black', 'lightgreen'))
				print("\n")
				if self.all_page_data:
					self._print_description(description, (int(str(q).strip()) - 1))
				else:
					self._print_description(description)
				
				qd = raw_input(make_colors("Download it [y/n/enter]:", 'lw', 'b'))
				if qd and qd.strip() == 'y':
					self.get_download_link(url, download_path, confirm, show_download_link)
				
			elif str(q).strip()[-1] == 's':
				if len(str(q).strip()) > 1:
					number_selected = str(q).strip()[:-1]
				else:
					number_selected = raw_input(make_colors("Select number of screenshot to show: ", 'lightwhite', 'lightred'))
					
				if number_selected and str(number_selected).isdigit() and int(number_selected) <= len(list(data_search.keys())):
					if not self.all_page_data:
						url = data_search.get(int(str(number_selected).strip())).get('link')
						license, description, homepage, title, screenshot = self._get(url)
					else:
						license, description, homepage, title, screenshot = self.all_page_data[int(number_selected)-1]
					
					tx = Process(target=tkimage.main, args=("temp", ))
					tx.start()
					self.first_screenshot_view = True
					#tkimage.main("temp")
				else:
					print(make_colors("Invalid Number selected !", 'lw', 'lr', ['blinks']))
					
			elif str(q).strip()[-1] == 'd':
				if len(str(q).strip()) > 1:
					number_selected = str(q).strip()[:-1]
				else:
					number_selected = raw_input(make_colors("Select number to download: ", 'lightwhite', 'lightred'))
				
				if number_selected and str(number_selected).isdigit() and int(number_selected) <= len(list(data_search.keys())):
					url = data_search.get(int(str(number_selected).strip())).get('link')
					self.get_download_link(url, download_path, confirm, show_download_link)
				else:
					print(make_colors("Invalid Number selected !", 'lw', 'lr', ['blinks']))
					
			elif str(q).strip() == 'x' or str(q).strip() == 'q':
				sys.exit()
				
		return self.navigator(search_query, download_path, confirm, show_download_link, use_wget, data_search = data_search, nums_page = nums_page, page = page)
		
	def usage(self):
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('-q', '--search', action = 'store', help = 'Search for')
		parser.add_argument('-l', '--link', action='store', help='Softpedia Link, example: "https://www.softpedia.com/get/Network-Tools/Network-Information/Squid-Efficiency-Analyzer.shtml"')
		parser.add_argument('-p', '--download-path', action='store', help='Download Path Save to', default=os.getcwd())
		parser.add_argument('-c', '--confirm', action='store', help='Confirm Download before')
		parser.add_argument('-S', '--show-download-link', action='store_true', help='Show Download link')
		parser.add_argument('-license', '--show-license', action='store_true', help='Show license')
		parser.add_argument('-H', '--homepage', action='store_true', help='Get HomePage Developer/Official Site')
		parser.add_argument('-s', '--screenshot', action='store_true', help='Show Screenshor')
		parser.add_argument('-w', '--wget', action = 'store_true', help = 'Force use wget for any download')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			if args.homepage:
				self.get_homepage(args.link, show = True)
			elif args.screenshot:
				self.get_screenshot(args.link, show=True, confirm=args.confirm)
			
			else:
				#self.get_download_link(args.LINK, args.download_path, args.confirm,
				#args.show_download_link)
				if args.search:
					self.navigator(args.search, args.download_path, args.confirm, args.show_download_link, args.wget, args.show_license)

if __name__ == '__main__':	
	c = softpedia()
	c.usage()
	#c.navigator("firewall")
	#c.navigator("squid")
	#description = c.get_description("https://www.softpedia.com/get/Network-Tools/Network-Information/Squid-Efficiency-Analyzer.shtml")
	#c._print_description(description)
	#c.get_description('https://www.softpedia.com/get/Network-Tools/Network-Information/Squid-Efficiency-Analyzer.shtml')

