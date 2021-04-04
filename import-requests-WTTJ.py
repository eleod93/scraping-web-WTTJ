from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import sqlite3


def createTable(c):
  c.execute('''CREATE TABLE jobs
             (id INTEGER PRIMARY KEY,
             poste text,
             entreprise text,
             contrat text,
             date_debut text,
             salaire text,
             ville text,
             etude text,
             secteur text,
             annee text,
             collaborateur text,
             age_moyen text,
             post_link text,
             linkedin_entreprise text)''')

def insertJob(c, identifiant, poste, entreprise, contrat, date_debut, salaire, ville, etude, secteur, annee, collaborateur, age_moyen, post_link, linkedin_entreprise):
  c.execute('''INSERT INTO jobs(id, poste, entreprise, contrat, date_debut, salaire, ville, etude, secteur, annee, collaborateur, age_moyen, post_link, linkedin_entreprise)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (identifiant, poste, entreprise, contrat, date_debut, salaire, ville, etude, secteur, annee, collaborateur, age_moyen, post_link, linkedin_entreprise))

def createLinkedinExcel():
    with open('linkedin_data.csv', 'w') as my_file:
        my_file.write("Linkedin_URL")

def insertLinkedindata(data):
    with open('linkedin_data.csv') as file:
        output = file.read()
    memory = output
    with open('linkedin_data.csv', 'w') as my_File:
        my_File.write(memory + "\n" + str(data[3]))

def getHTML(self):
  # Récupérer le HTML d'un url
  html = requests.get(self).text
  soup = BeautifulSoup(html, 'lxml')
  return soup

def getJobInfos(url):
  job_summary = getHTML(url).find('ul',{'data-testid':'job-summary-job-metas'})
  data = []
  # Récupérer le type de contrat du poste
  if job_summary.find('i',{'name':'contract'}) is None:
    contract = ''
  else :
    contract = job_summary.find('i',{'name':'contract'}).parent.next_sibling.get_text()

  # Récupérer la date de début du poste
  if job_summary.find('i',{'name':'clock'})is None:
    clock = ''
  else:
    clock = job_summary.find('i',{'name':'clock'}).parent.next_sibling.find('time')['datetime']

  # Récupérer le salaire du poste
  if job_summary.find('i',{'name':'salary'}) is None :
    salary =''
  else:
    salary = job_summary.find('i',{'name':'salary'}).parent.next_sibling.get_text()

  # Récupérer la localisation du poste
  if job_summary.find('i',{'name':'location'}) is None :
    location = ''
  else:
    location = job_summary.find('i',{'name':'location'}).next_element.get_text()

  # Récupérer le niveau d'étude requis du poste
  if job_summary.find('i',{'name':'education_level'}) is None :
    education_level =''
  else:
    education_level = job_summary.find('i',{'name':'education_level'}).next_element.get_text()

  data.extend([contract,clock,salary,location,education_level])
  return data

def getEntrepriseInfo(url):
  data = []
  page_entreprise = getHTML(url)
  infos = page_entreprise.find_all('span',{'class':'sc-1n18lhk-3 bWFoBD'})
  annee = infos[0].get_text()
  collaborateur = infos[1].get_text()
  age_moyen = infos[2].get_text()

  if page_entreprise.find('i',{'name':'linkedin'},title=True) is None:
    linkedin_entreprise = ''
  else:
    linkedin_entreprise= page_entreprise.find('i',{'name':'linkedin'},title=True).parent['href']

  data.extend([annee, collaborateur, age_moyen, linkedin_entreprise])
  return data


def brownse_and_scrape_jobs(i, url):
  print("Now Scraping")
  soup = BeautifulSoup(url, 'lxml')
  jobs = soup.find_all('div', {'class':'sc-7dlxn3-5 djGVHr'})
  for job in jobs:
    # Récuperer le poste et l'entreprise
    poste = job.find('h3', {'class':'sc-1kkiv1h-9 sc-7dlxn3-4 ivyJep iXGQr'}).get_text()
    entreprise = job.find('h4', {'class':'sc-1kkiv1h-10 dzYJcI'}).find('span',{'ais-Highlight sc-1s0dgt4-13 guUpAr'}).get_text().capitalize()

    # Récupérer des infos sur le poste
    poste_link = 'https://www.welcometothejungle.com' + job.find('a', href=True)['href']
    secteur = getHTML(poste_link).find('div',{'class':'sc-17gqtt5-0 gtomeq'}).find('span',{'class':'sc-1qc42fc-2 bzLbYV'}).get_text()

    # Récupérer le linkedin de l'entreprise
    wttj_page_entreprise = 'https://www.welcometothejungle.com' + getHTML(poste_link).find('a', {'class':'sc-17gqtt5-1 gUEgnZ'})['href']
    # print(getEntrepriseInfo(wttj_page_entreprise))

    insertLinkedindata(getEntrepriseInfo(wttj_page_entreprise))
    insertJob(c, i, poste, entreprise, getJobInfos(poste_link)[0], getJobInfos(poste_link)[1], getJobInfos(poste_link)[2], getJobInfos(poste_link)[3], getJobInfos(poste_link)[4], secteur,getEntrepriseInfo(wttj_page_entreprise)[0], getEntrepriseInfo(wttj_page_entreprise)[1], getEntrepriseInfo(wttj_page_entreprise)[2], poste_link, wttj_page_entreprise)
    i = i+1



int = 1
i = 1

# url = 'https://www.welcometothejungle.com/fr/companies/aos'
# tests = getHTML(url).find_all('span',{'class':'sc-1n18lhk-3 bWFoBD'})
# annee = tests[0].get_text()
# collaborateur = tests[1].get_text()
# age_moyen = tests[2].get_text()


# print(annee, collaborateur, age_moyen)


driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver')
quote_page = 'https://www.welcometothejungle.com/fr/jobs?page='

# Créer un SQL et un fichier excel
conn = sqlite3.connect('example_WTTJ.db')
c = conn.cursor()
createTable(c)
createLinkedinExcel()

# Ouvrir WTTJ et Scraper toutes les pages du site
while int < 2:
  page = quote_page + str(int) + '&aroundQuery=&refinementList%5Borganization.size.fr%5D=&refinementList%5Bprofession_name.fr.Business%5D%5B%5D=Business%20Development'
  driver.get(page)
  driver.implicitly_wait(100) # seconds
  brownse_and_scrape_jobs(i, driver.page_source)
  print('La page ' + str(int) + ' a été scrappé')
  int = int + 1

# print(data)
driver.quit()
conn.commit()
conn.close()

print('La base SQL a été mise à jour')

