from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

class Playwright:
    def __init__(self, keyword):
        self.results = []  # 검색 결과 저장 리스트 초기화
        self.browser = None
        self.keyword = keyword
        self.url = "https://www.wanted.co.kr/jobsfeed"
    
    def initialize_browser(self):
        # Playwright 초기화 및 브라우저 실행
        p = sync_playwright().start()
        self.browser = p.chromium.launch(headless=False)
            
    def create_page(self):
        # 새로운 페이지 생성
        self.page = self.browser.new_page()
        
    def goto_url(self):
        # 지정한 URL로 이동
        self.page.goto(self.url)
        
    def access_to_data_page(self):
        # 검색어 입력 및 데이터 페이지에 접근
        self.page.click("button.Aside_searchButton__Xhqq3")
        self.page.get_by_placeholder("검색어를 입력해 주세요.").fill(self.keyword)
        self.page.keyboard.down("Enter")

        time.sleep(5)

        self.page.click("a#search_tab_position")

        for x in range(5):
            time.sleep(2)
            self.page.keyboard.down("End")

        self.content = self.page.content()
        
    def scrap_data(self):
        # 웹 페이지에서 데이터 스크랩
        soup = BeautifulSoup(self.content, "html.parser")

        jobs = soup.find_all("div", class_="JobCard_container__FqChn")

        for job in jobs:
            link = f"https://www.wanted.co.kr{job.find('a')['href']}"
            title = job.find("strong", class_="JobCard_title__ddkwM").text
            company = job.find("span", class_="JobCard_companyName__vZMqJ").text
            location = job.find("span", class_="JobCard_location__2EOr5").text
            reward = job.find("span", class_="JobCard_reward__sdyHn").text
            job_data = DataAppend(title, company, location, reward, link)
            job_data.add_to_results(self.results)
            
    def exit_browser(self):
        self.browser.close()
            
            
class DataAppend:
    def __init__(self, title, company, location, reward, url):
        # 데이터 객체 초기화
        self.title = title
        self.company = company
        self.location = location
        self.reward = reward
        self.url = url
        self.job_data = {
            'Title': self.title,
            'Company': self.company,
            'Location': self.location,
            'Reward': self.reward,
            'URL': self.url,
        }
        
    def add_to_results(self, results):
        # 결과 리스트에 데이터 추가
        results.append(self.job_data)


        