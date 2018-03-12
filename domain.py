#!/usr/bin/python
import random
import requests
import sys,getopt
import re

global filter_ips,filter_ports,cookie,filter_urls

requests.packages.urllib3.disable_warnings()

# The filter for has been scaned ip
filter_ips = []

# The filter for has been scaned url
filter_urls = []

def requests_headers():
	'''
	Random UA  for every requests && Use cookie to scan
	'''
	user_agent = ['Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0',
	'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre',
	'Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60','Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)',
	'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
	'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5']
	UA = random.choice(user_agent)
	headers = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': 'http://www.cnnetarmy.com',
	'User-Agent':UA,'Upgrade-Insecure-Requests':'1','Connection':'keep-alive','Cache-Control':'max-age=0',
	'Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8'}
	return headers

def requests_proxies():
	'''
	Proxies for every requests
	'''
	proxies = {
	'http':'',#127.0.0.1:1080 shadowsocks
	'https':''#127.0.0.1:8080 BurpSuite
	}
	return proxies


def baidu_site(key_domain):
	'''
	Get baidu site:target.com result
	'''
	headers = requests_headers()
	proxies = requests_proxies()
	baidu_domains,check = [],[]
	baidu_url = 'https://www.baidu.com/s?ie=UTF-8&wd=site:{}'.format(key_domain)
	try:
		r = requests.get(url=baidu_url,headers=headers,timeout=10,proxies=proxies,verify=False).text
		if 'class=\"nors\"' not in r:# Check first
			for page in range(0,100):# max page_number
				pn = page * 10
				newurl = 'https://www.baidu.com/s?ie=UTF-8&wd=site:{}&pn={}&oq=site:{}'.format(key_domain,pn,key_domain)
				keys = requests.get(url=newurl,headers=headers,proxies=proxies,timeout=10,verify=False).text
				flags = re.findall(r'style=\"text-decoration:none;\">(.*?)%s.*?<\/a><div class=\"c-tools\"'%key_domain,keys)
				check_flag = re.findall(r'class="(.*?)"',keys)
				for flag in flags:
					domain_handle = flag.replace('https://','').replace('http://','')
					# xxooxxoo.xoxo.com ignore "..."
					if domain_handle not in check and domain_handle != '':
						check.append(domain_handle)
						domain_flag = domain_handle + key_domain
						print ('[+] Get baidu site:domain > ' + domain_flag)
						baidu_domains.append(domain_flag)
						if len(check_flag) < 2:
							return baidu_domains
		else:
			print ('[!] baidu site:domain no result')
			return baidu_domains
	except Exception as e:
		print (e)
		pass
	return baidu_domains

def print_usage():
	usage='python domain.py -H site\n'+'Example:python domain.py -H baidu.com'
	print(usage)

	
baidu_site('baidu.com')


if __name__ == '__main__':
	opts,args = getopt.getopt(sys.argv[1:],"hH:",["help","host="])
	for op,value in opts:
		if op in ('-h','help'):
			print_usage()
		elif op in ('-H','-host'):
			value.replace('http://','.')
			value.replace('https://','.')
			try:
				if len(value.split('.'))==3:
					tmp=value.split('.')
					dom=[]
					dom.append(tmp[1])
					dom.append(tmp[2])
					domain=dom.join('.')
					print ('Domain: '+str(domain))
					print (baidu_site(domain))
				elif len(value.split('.'))==2:
					print ('Domain: '+value)
					print (baidu_site(str(value)))
				else:
					print ("Wrong usage")
			except Exception as e:
				print (e)
		else:
			print_usage()
