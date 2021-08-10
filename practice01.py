from flask import Flask
from flask_mail import Mail, Message

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
	return "success"

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 3000)
