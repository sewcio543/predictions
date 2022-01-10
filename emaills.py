import smtplib

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("sewcio543@gmail.com", "sewcio543Sewerinio")
server.sendmail("sewcio543@gmail.com", "wojtek.sewern@gmail.com","HEllo")
server.quit()
print("Successfully sent email")

