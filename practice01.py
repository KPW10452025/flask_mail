from flask import Flask
from flask_mail import Mail, Message
from threading import Thread

import os

from dotenv import load_dotenv # 利用 dotenv 載入環境變數
load_dotenv() # dotenv 基本語法 # take environment variables from .env

app = Flask(__name__) # 必須寫在 app.config 前面

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
# app.config["MAIL_SERVER"] = 默認為'localhost'
# 郵件服務器的名稱/IP地址
# gmail 為 'smtp.gmail.com'
# hotmail 為 'smtp.live.com'

app.config["MAIL_PORT"] = 465
# app.config["MAIL_PORT"] = 默認為25
# 所用服務器的端口號，通常為 25 或是 465
# gamil 為 465

app.config["MAIL_USE_TLS"] = False
# 默認為 False
# 啟用/禁用傳輸安全層加密

app.config["MAIL_USE_SSL"] = True
# app.config["MAIL_USE_SSL"] = 默認為 False
# 啟用/禁用安全套接字層加密 

# app.config["MAIL_DEBUG"] = 默認為 app.debug
# 調試支持，默認是Flask應用程序的調試狀態
# 如果在檔案其他位置有以下編碼，就無須設置此 config

# app.debug = True

# app.config['DEBUG'] = True

# if __name__ == '__main__':
# 	app.run(debug = True)

# if __name__ == "__main__":
#     app.debug = True
#     app.run()

app.config["MAIL_USERNAME"] = os.environ.get("GMAIL_USERNAME")
# app.config["MAIL_USERNAME"] = 默認為 None
# 發件人的用戶名 
# 如果有設置環境變數則可以使用 os.environ.get('MAIL_USERNAME') 取得

app.config["MAIL_PASSWORD"] = os.environ.get("GMAIL_PASSWORD")
# app.config["MAIL_PASSWORD"] = 默認為 None
# 發件人的密碼 
# 如果有設置環境變數則可以使用 os.environ.get('MAIL_PASSWORD') 取得

app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("GMAIL_USERNAME")
# 默認為 None
# 設置默認發件人 

app.config["MAIL_MAX_EMAILS"] = None
# 默認為 None
# 設置要發送的最大郵件 

app.config["MAIL_SUPPRESS_SEND"] = False
# 默認為 False
# 默認為 app.testing
# app.config["TESTING"]
# 設置 True 的時候可以限制發送郵件
# 在開發測試的時候，實作 send() 時就不會真的發送郵件

app.config["MAIL_ASCII_ATTACHMENTS"] = False
# 默認為 False
# 如果設置為true，則將附加的文件名轉換為ASCII
# 現今常用的編碼為 unicode
# ascii 只有英文，而且字數少，除非伺服器限定使用 ascii，不然都默認 False

# 以此方式，所有的郵件設置會一次性渲染
mail = Mail(app) # 必須寫在 app.config 後面

# 如果你有不同專案要走不同郵件設置的話，用此方式較佳
# 如果你使用工廠模式的話，也會以此方式來做初始化
# mail = Mail()
# mail.init_app(app)

# 寄一封信給一個人
@app.route("/send")
def send():
	# msg = Message("Hello", sender="from@example.com", recipients=["to@example.com"])
	# 第一個參數 "Hello" 是郵件的標題
	# 第二個參數 sender 是寄件人
	# 因為已經在 config 設定 app.config["MAIL_DEFAULT_SENDER"]
	# 所以在這裡可以不用再次設定 sender
	# 第三個參數 recipients 是收件人
	# 測試用 email 可以搜尋 temporary email
	msg = Message("Hello", recipients=["tujiqabe.ogopenoq@vintomaper.com"])
	# 使用 msg.body 用來設定內容
	# 亦可以使用 msg.html 來設定內容
	# 但要注意的是，如果使用 msg.html 會蓋掉 msg.body 導致 msg.body 的內容不會顯示
	msg.body = "This is from msg.body"
	msg.html = "<b>This is from msg.html</b>"
	mail.send(msg)
	return "/send success"

# 寄一封信給一堆人
# 運用 with 開啟一個 connection 專門用來不斷寄信
# 此方法的特點為，這個 connection 寄件次數會受到 app.config["MAIL_MAX_EMAILS"] 所限制
# 當 app.config["MAIL_MAX_EMAILS"] = 10 時，無論 users(或者各種字典、資料庫等)有多少筆資料，結果只會寄送10次
@app.route("/bulk")
def bulk():
	# 這裡的 users 是一個字典，也可以是連接的資料庫等
	users = [{"name" : "Tom", "email" : "tujiqabe.ogopenoq@vintomaper.com"},
	         {"name" : "Dan", "email" : "tujiqabe2.ogopenoq@vintomaper.com"},
	         {"name" : "Ken", "email" : "tujiqabe3.ogopenoq@vintomaper.com"},
	         {"name" : "Sue", "email" : "tujiqabe4.ogopenoq@vintomaper.com"}]
	with mail.connect() as conn:
		for user in users:
			msg = Message("Bulk!", recipients=[user["email"]])
			msg.body = "This is sent by app.route('/bulk'), and is written by msg.body."
			conn.send(msg)
	return "/bulk success"

# 如果今天我要寄給很多人，但又不想被 MAIL_MAX_EMAILS 限制時
# 可以用以下方法實現
# 把 recipients=[user["email"]] 改成 recipients=[user.email]
# 但是這個說明力並無法運作，因為 user.email 是連接資料庫的語法，這個文檔並沒有設計資料庫
@app.route("/bulk_2")
def bulk_2():
	users = [{"name" : "Tom", "email" : "tujiqabe.ogopenoq@vintomaper.com"}]
	with mail.connect() as conn:
		for user in users:
			msg = Message("Bulk_2", recipients=[user.email])
			msg.body = "This is sent by app.route('/bulk_2'), and is written by msg.body."
			conn.send(msg)
	return "/bulk_2 success"

# 如何寄送一個夾帶郵件的信 How to add attachments to the message
# 我在專案檔案夾中新增一個名為 MHrise0001.jpeg 的圖片
@app.route("/attachment")
def attachment():
	# temporary email 郵件無法收取 attachment，這裡我使用自己的信箱
	# 此信箱已被隱藏在環境變數，所以需要 os.environ.get() 調用
	msg = Message("Attachment", recipients=[os.environ.get("TEST_MAIL")])
	msg.html = "<b>This is sent by app.route('/attachment'), and is written by msg.html.</b>"
	# open_resource 是 flask 用來 open resources 的語法
	with app.open_resource("MHrise0001.jpeg") as pics:
		msg.attach("MHrise0001.jpeg", "image/jpeg", pics.read())
	mail.send(msg)
	return "/attachment success"

# 非同步寄送郵件
# 使用非同步的主因在於不希望使用者在按下發送信件按鈕之後需要浪費時間等待寄送信件的程序
# 這個等待時間會造成使用者體驗不佳，而且使用者也不需要浪費時間等待
# 因此利用多執行緒將使用者點擊按鈕之後的信件派送程序切割

@app.route("/Use_Thread")
def Use_Thread():
	msg = Message('Use_Thread', recipients=[os.environ.get("TEST_MAIL")])
	msg.html = "<b>This is sent by app.route('/Use_Thread'), and is written by msg.html.</b>"
	Thread(target=send_async_email, args=[app, msg]).start()
	return "/Use_Thread success"

# 使用多線程 target=要接續的目標函式 args=要傳送過去的參數
# 因為 args=[app, msg] 有兩個參數 所以人方函式的參數也必須放入 app, msg
# 必需讓程序是在相同的 Context 內，因此必需利用 app.app_context 來確保線程

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 3000)

# 補充：如何查詢 Gmail 的外寄郵件(SMTP)伺服器的 config
# 開啟 Gmail 的 "設定"
# 點選 "轉寄和 POP/IMAP"
# 找到下方 "IMAP 存取" 並點選 "瞭解詳情"
# 這時候會來到新頁面，尋找 "外寄郵件 (SMTP) 伺服器"
# 會看到以下資料
# smtp.gmail.com
# 需要安全資料傳輸層 (SSL)：是
# 需要傳輸層安全性 (TLS)：是 (如果可用)
# 需要驗證：是
# 安全資料傳輸層 (SSL) 通訊埠：465
# 傳輸層安全性 (TLS)/STARTTLS 通訊埠：587
