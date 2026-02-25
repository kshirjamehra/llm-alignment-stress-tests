import markdown
import os

def convert_md_to_html(md_path, html_path):
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    html = markdown.markdown(text, extensions=['tables'])
    
    # Add simple CSS
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; color: #333; }}
table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background-color: #f2f2f2; }}
h1, h2, h3 {{ color: #2c3e50; }}
code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
blockquote {{ border-left: 5px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px; color: #555; background-color: #f9f9f9; }}
</style>
</head>
<body>
{html}
</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Converted {md_path} to {html_path}")

if __name__ == "__main__":
    report_md = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports', 'final_report.md')
    report_html = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports', 'final_report.html')
    convert_md_to_html(report_md, report_html)
