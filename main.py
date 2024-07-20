from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()

path = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
co.set_browser_path(path)
co.use_system_user_path()
print(co.user_data_path)

page = ChromiumPage(addr_or_opts=co)

url = 'https://www.baidu.com/'
page.get(url)

