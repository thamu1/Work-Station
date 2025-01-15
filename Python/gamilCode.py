import smtplib

server=smtplib.SMTP_SSL('smtp.gmail.com',smtplib.SMTP_SSL_PORT)
server.ehlo()
server.login("taahirimraan8601@gmail.com","*************") # vptcjlkehrqssyik  # nnqilrmberidzbqa

sender = "taahirimraan8601@gmail.com"
receiver = input("enter your Mail id : ")


subject = f"Your account was hacked"

body = f"Hello,\n\n{subject}."
msg = f"From: {sender}\nTo: {receiver}\nSubject: {subject}\n\n{body}"

server.sendmail(sender,receiver,msg)

print("mail sent")
server.quit()

# =================================  OUTLOOk ======================================================

# import smtplib

# server=smtplib.SMTP_SSL('smtp.office365.com',smtplib.SMTP_SSL_PORT)
# server.ehlo()
# # msg=f"{subject}\n\n YOU HAVE SUCCESSFULLY BOOKED... "

# server.login("thamotharan.c@softcrylic.co.in","zcrylgdjyckfkfsz")

# # sender = "thamotharan.c@softcrylic.co.in"
# sender = "thamotharan.c@softcrylic.co.in"
# receiver = input("enter your Mail id : ")


# subject = f"Your account was hacked"

# body = f"Hello,\n\n{subject}."
# msg = f"From: {sender}\nTo: {receiver}\nSubject: {subject}\n\n{body}"

# server.sendmail(sender,receiver,msg)

# print("mail sent")
# server.quit()
