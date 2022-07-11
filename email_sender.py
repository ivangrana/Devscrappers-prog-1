import smtplib,getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
mail_content = str('oioi')
#Senha e email do remetente
remetente = 'devscrappers@outlook.com'
senha = getpass.getpass("Insira a senha ->")
destinatario = 'ivan.grana@icen.ufpa.br'
#MIME
message = MIMEMultipart()
message['From'] = remetente
message['To'] = destinatario
message['Subject'] = 'links raspados'   #Assunto do email

#corpo e anexos
message.attach(MIMEText(mail_content, 'plain'))
#Criação da sessão SMTP
s = smtplib.SMTP('smtp.office365.com', 587) #porta 587 do gmail
s.starttls() #TLS
s.login(remetente, senha) #fazendo o login...
text = message.as_string()
s.sendmail(remetente, destinatario, text)
s.quit()
print('Email enviado')
