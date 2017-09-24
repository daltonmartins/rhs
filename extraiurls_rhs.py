
# coding: utf-8

# In[55]:


from bs4 import BeautifulSoup
import pymysql
import csv

#conexão com o banco de dados
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='rhs')

cur = conn.cursor()

# consulta ao banco de dados
# coleta os textos da tabela field_data_body
# coleta os metadados do texto da tabela node
cur.execute("SELECT f.body_value,f.entity_id,n.uid,u.name,from_unixtime(n.created) FROM field_data_body f INNER JOIN node n ON f.entity_id=n.nid JOIN users u ON n.uid=u.uid WHERE f.bundle='blog'")


#laço para busca dos links da rede
listaParaGerarCsv = []
for row in cur:
    soup = BeautifulSoup(row[0],'html.parser')
    
    for a in soup.find_all('a', href=True):
        listaInterna = []
        listaInterna.append(a['href'])
        listaInterna.append(row[1])
        listaInterna.append(row[2])
        listaInterna.append(row[3])
        listaInterna.append(row[4])
        listaParaGerarCsv.append(listaInterna)

        
#fecha conexão com banco de dados    
cur.close()
conn.close()
  
    
with open('listagem_links_rhs.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"',quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Link', 'No', 'NID','Usuario','Timestamp'])
    for linha in listaParaGerarCsv:
        spamwriter.writerow(linha)          

print ('Arquivo gerado no diretorio: ')


# In[25]:


import pymysql

