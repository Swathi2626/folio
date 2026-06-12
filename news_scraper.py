import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText


SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")



def scrape_hacker_news():
    news_list = []
    try:
        response = requests.get("https://news.ycombinator.com/", timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("span", class_="titleline")[:3] 
        for item in links:
            a_tag = item.find("a")
            news_list.append({"source": "Hacker News", "title": a_tag.text, "link": a_tag["href"]})
    except Exception as e:
        print(f"Error scraping Hacker News: {e}")
    return news_list

def scrape_bbc_news():
    news_list = []
    try:
        response = requests.get("https://www.bbc.com/news/technology", timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        headings = soup.find_all("h2")[:3]
        for item in headings:
            title = item.text.strip()
            parent_a = item.find_parent("a")
            if parent_a and parent_a['href'].startswith('/'):
                link = f"https://www.bbc.com{parent_a['href']}"
            elif parent_a:
                link = parent_a['href']
            else:
                link = "https://www.bbc.com/news/technology"
            news_list.append({"source": "BBC News", "title": title, "link": link})
    except Exception as e:
        print(f"Error scraping BBC News: {e}")
    return news_list

def scrape_the_verge():
    news_list = []
    try:
       
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get("https://www.theverge.com/", headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        links = soup.find_all("a", href=True)
        
        count = 0
        for item in links:
            href = item["href"]
            title = item.text.strip()
            
            if len(title) > 25 and ("-20" in href or "/202" in href):
               
                link = f"https://www.theverge.com{href}" if href.startswith('/') else href
               
                if not any(news['title'] == title for news in news_list):
                    news_list.append({
                        "source": "The Verge",
                        "title": title,
                        "link": link
                    })
                    count += 1
            
        
            if count == 3:
                break
                
    except Exception as e:
        print(f"Error scraping The Verge: {e}")
    return news_list


def build_html_template(all_news):
    """Takes the list of articles and formats them into an HTML layout."""
    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f6f7;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
            <h2 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 0;">📰 Morning Headline Digest</h2>
            <p style="font-size: 14px; color: #7f8c8d;">Your automated script successfully compiled today's top stories:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <thead>
                    <tr style="background-color: #34495e; color: #ffffff; text-align: left;">
                        <th style="padding: 10px; font-size: 14px; width: 30%;">Source</th>
                        <th style="padding: 10px; font-size: 14px; width: 70%;">Headline</th>
                    </tr>
                </thead>
                <tbody>
    """
    for item in all_news:
        html_content += f"""
                    <tr style="border-bottom: 1px solid #e0e0e0;">
                        <td style="padding: 12px; font-weight: bold; color: #2980b9; font-size: 13px;">{item['source']}</td>
                        <td style="padding: 12px; font-size: 14px;">
                            <a href="{item['link']}" style="color: #333333; text-decoration: none; font-weight: 500;" target="_blank">{item['title']}</a>
                        </td>
                    </tr>
        """
    html_content += """
                </tbody>
            </table>
            <hr style="border: 0; border-top: 1px solid #eeeeee; margin-top: 20px;">
            <p style="font-size: 11px; color: #bdc3c7; text-align: center; margin-bottom: 0;">Generated automatically by Pulse Automation System</p>
        </div>
    </body>
    </html>
    """
    return html_content


def send_email(html_body):
    """Logs into Gmail's secure server and sends the HTML content."""
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = '🗞️ Your Custom Morning News Briefing'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        print("Connecting to secure Gmail SMTP server...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ Email dispatched perfectly! Check your inbox.")
    except Exception as e:
        print(f"❌ Failed to dispatch email. Error details: {e}")

if __name__ == "__main__":
    print("🚀 Gathering updates across news websites...")
    
    master_news_list = []
    master_news_list.extend(scrape_hacker_news())
    master_news_list.extend(scrape_bbc_news())
    master_news_list.extend(scrape_the_verge())
    
    print(f"📊 Collected a total of {len(master_news_list)} headlines.")
    
    final_html_output = build_html_template(master_news_list)
    
    send_email(final_html_output)