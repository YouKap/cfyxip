from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        # 1. 增加浏览器伪装 (User-Agent)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("正在打开页面...")
            # 2. 关键改动：将 wait_until 从 networkidle 改为 domcontentloaded
            # 同时将超时手动延长到 60 秒，给网络波动留出余地
            page.goto("https://vps789.com/cfip/?remarks=domain", 
                      wait_until="domcontentloaded", 
                      timeout=60000)
            
            # 3. 精准等待：只要表格行出现就代表数据出来了
            print("等待表格数据渲染...")
            page.wait_for_selector(".el-table__row", timeout=20000)
            
            # 额外给 2 秒让 Vue/ElementPlus 把数据填进去
            time.sleep(2)

            # 提取数据 (保持原样)
            rows = page.query_selector_all(".el-table__row")
            domain_list = [row.query_selector("td").inner_text().strip() for row in rows if row.query_selector("td")]
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "domains.txt")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(domain_list))
            
            print(f"提取完成！抓取到 {len(domain_list)} 个域名，已保存。")
        except Exception as e:
            print(f"❌ 抓取过程中发生错误: {e}")
            raise e # 必须抛出异常，否则 GitHub Action 会认为任务成功
        finally:
            browser.close()

if __name__ == "__main__":
    run()