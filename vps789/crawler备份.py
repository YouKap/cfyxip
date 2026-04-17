from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("正在打开页面...")
        # 加上 remarks=domain 参数直接锁定域名列表
        page.goto("https://vps789.com/cfip/?remarks=domain", wait_until="networkidle")
        
        full_domain_list = [] 
        page_num = 1

        while True:
            print(f"正在读取第 {page_num} 页数据...")
            
            # 等待表格渲染
            try:
                page.wait_for_selector(".el-table__row", timeout=15000)
            except:
                print("未发现表格行，抓取结束。")
                break

            # 关键：稍微等待，确保 Vue 渲染完成
            time.sleep(2) 

            # 提取当前页所有域名
            rows = page.query_selector_all(".el-table__row")
            for row in rows:
                first_col = row.query_selector("td") 
                if first_col:
                    domain = first_col.inner_text().strip()
                    if domain:
                        full_domain_list.append(domain)
            
            # 分页逻辑：寻找“下一页”按钮
            next_btn = page.query_selector("button.btn-next")
            
            # 如果找不到按钮或按钮被禁用(disabled)，则停止
            if not next_btn or next_btn.is_disabled():
                print("已经到达最后一页。")
                break
            
            # 点击下一页
            next_btn.click()
            page_num += 1
            # 翻页后必须多等一会，防止 DOM 还没刷新就抓到了上一页的旧数据
            time.sleep(3) 

        # --- 精准保存路径 ---
        # 获取 crawler.py 所在的文件夹路径 (即 vps789 目录)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "domains.txt")
        
        # 写入文件：不做去重，不做排序，完全按照网页展示顺序
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(full_domain_list))
        
        print(f"\n[任务成功] 总计抓取条数: {len(full_domain_list)}")
        print(f"[文件位置] {file_path}")
        
        browser.close()

if __name__ == "__main__":
    run()