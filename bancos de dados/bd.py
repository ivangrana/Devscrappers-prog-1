import sqlite3
con = sqlite3.connect('contas.db')
cur = con.cursor()

# cur.execute('''CREATE TABLE stocks
#                (Email text, Senha text)''')

def cadastro():
    email = input("inserir email:")
    senha = input("inserir senha:")
    cur.execute("INSERT INTO stocks VALUES (?,?)",(email,senha))
    con.commit()


print(cur.execute('SELECT * FROM stocks ORDER BY Email').fetchall())
con.close()