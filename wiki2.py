import webbrowser
import csv
import requests

def wiki(word1, word2='', word3='', word4='', lastname=''):
	if word2 <> '' and word3 <> '' and word4 <> '':
		addr = 'https://en.wikipedia.org/w/index.php?title=Special:Search&search=%s+%s+%s+%s' % (word1, word2, word3, word4)
	elif word2<> '' and word3 <> '':
		addr = 'https://en.wikipedia.org/w/index.php?title=Special:Search&search=%s+%s+%s' % (word1, word2, word3)	
	elif word2 <> '':
		addr = 'https://en.wikipedia.org/w/index.php?title=Special:Search&search=%s+%s' % (word1, word2)
	else:
		addr = 'https://en.wikipedia.org/w/index.php?title=Special:Search&search=%s' % (word1)
	print(addr)
	search = requests.get(addr)
	url = search.url
	if lastname.lower() in search.text.lower() and lastname.lower() <> word1.lower() and lastname.lower() <> word2.lower() and lastname.lower() <> word3.lower() and lastname.lower() <> word4.lower():
		return url
	else:
		print 'No Match for %s' % (word1 + ' ' + word2 + ' ' + word3 + ' ' + word4)

def wordsplit(names):

	names = names.lower()
	names = names.replace(' & ', ' and ')

	if ' ' in names:
		space1 = names.find(' ')
		first = names[0:space1]
		names = names[space1+1:]
		if ' ' in names:
			space2 = names.find(' ')
			second = names[0:space2]
			names = names[space2+1:]
			if ' ' in names:
				space3 = names.find(' ')
				third = names[0:space3]
				fourth = names[space3+1:]
			else:
				third = names
				fourth = ''
		else:
			second = names
			third = ''
			fourth = ''
	else:
		first = names
		second = ''
		third = ''
		fourth = ''

	print first		
	print second
	print third
	print fourth
	
	return first, second, third, fourth
	
crpdict = {
	' Assoc':' Associates',
	' Corp':' Corporation',
	' Assn':' Association',
	' Inc':' ',
	' Corp':' '
	}

file = open('lastnames.csv', 'rU')
readfile = csv.reader(file)
data = list(readfile)

item = 0

while item < len(data) and int(data[item][2]) > 19999:
	
	place = item
	
	if len(data[item][1]) < 6:
		item = item + 1
	elif int(data[item][2]) > 36999:
		item = item + 1	
	else:
		names = data[item][1]
		first, second, third, fourth = wordsplit(names)
		
		lastname = data[item][0]
		url = wiki(first, second, third, fourth, lastname)
		try:
			if 'index' not in url and 'disambiguation' not in url:
				webbrowser.open(url)
				item = place + 1
		except:
			print ''
		while item == place:
			for i in crpdict.keys():	
				if i in names and len(names.replace(i, crpdict[i])) > 5:
					names2 = names.replace(i, crpdict[i])
					first, second, third, fourth = wordsplit(names2)
					url2 = wiki(first, second, third, fourth, lastname)
					try:
						if 'index' not in url2 and 'disambiguation' not in url2:
							webbrowser.open(url2)
							item = place + 1
					except:
						print ''
			item = place + 1