# # lottery_app.py

# import time
# import re
# from flask import Flask, render_template
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import WebDriverException, TimeoutException

# # 調整 Flask 實例：將 template_folder 設置為 '.' (當前目錄)
# app = Flask(__name__, template_folder='.')

# # 抓取彩票網站資料的核心函數
# def get_website_content_for_test():
#     """
#     使用 Selenium 抓取網站內容。
#     **注意：此處暫時使用 Google 台灣作為測試目標，以驗證環境是否正常。**
#     **當環境驗證通過後，請將 url 替換回台灣彩券網站。**
#     """
    
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox") 
#     chrome_options.add_argument("--disable-dev-shm-usage") 
#     chrome_options.add_argument("--disable-gpu") 
#     chrome_options.add_argument("--window-size=1920,1080")

#     driver = None
#     try:

#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=chrome_options)
        

#         driver.set_page_load_timeout(15)

#         url = 'https://www.taiwanlottery.com/' 
        
#         print(f"嘗試連線到測試網站: {url}")
#         driver.get(url)

#         time.sleep(3) 

       
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
        
#         page_title = soup.title.text if soup.title else "N/A"
      
#         results = {
#             'draw_period': "測試期數: 99999999",
#             'draw_date': "測試日期: 2025/12/03",
#             'main_numbers': ["T1", "E2", "S3", "T4", "E5", "R6"],
#             'second_area': page_title 
#         }

#         return results, None

#     except TimeoutException:
#         error_message = "連線超時錯誤: 嘗試載入頁面超過 15 秒。"
#         print(f"--- 錯誤詳細信息 ---:\n{error_message} (Selenium Timeout)")

#         return None, error_message
#     except WebDriverException as e:
#         error_message = f"WebDriver 錯誤: {e.msg.splitlines()[0]}"
#         print(f"--- 錯誤詳細信息 ---:\n{e.msg}")

#         return None, error_message
#     except Exception as e:
#         error_message = f"發生未知錯誤: {type(e).__name__} - {e}"
#         print(f"--- 錯誤詳細信息 ---:\n{error_message}")
     
#         return None, error_message
#     finally:
#         if driver:
#             driver.quit()

# @app.route('/')
# def index():
  
#     lottery_data, error = get_website_content_for_test()
    
 
#     return render_template('lottery.html', data=lottery_data, error=error)

# if __name__ == '__main__':
#     print("--- 應用程序啟動中 ---")
#     app.run(host='127.0.0.1', port=5000, debug=True)