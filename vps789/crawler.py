from playwright.sync_api import sync_playwright
import time
import os  # 新增

def run():
    with sync_playwright() as p:
        # 启动浏览器 (无头模式)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 访问页面
        print("正在打开页面...")
        page.goto("https://vps789.com/cfip/?remarks=domain", wait_until="networkidle")
        
        # 等待表格渲染
        page.wait_for_selector(".el-table__row", timeout=15000)
        
        # 模拟真实等待
        time.sleep(2)

        # 提取数据
        rows = page.query_selector_all(".el-table__row")
        domain_list = []
        
        for row in rows:
            first_col = row.query_selector("td") 
            if first_col:
                domain = first_col.inner_text().strip()
                if domain:
                    domain_list.append(domain)
        
        # --- 路径修正逻辑开始 ---
        # 获取当前脚本所在文件夹 (即 vps789 目录)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接出完整保存路径
        file_path = os.path.join(current_dir, "domains.txt")
        
        # 保存到指定文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(domain_list))
        # --- 路径修正逻辑结束 ---
        
        print(f"清理完成！提取到 {len(domain_list)} 个域名。")
        print(f"文件已保存至: {file_path}")
        
        browser.close()

if __name__ == "__main__":
    run()