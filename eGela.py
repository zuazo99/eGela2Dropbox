from tkinter import messagebox as tkMessageBox
import requests
import urllib
from bs4 import BeautifulSoup
import time
import helper
import os
import sys

class eGela:
    _login = 0
    _cookie = ""
    _ikasgaia = ""
    _loginToken = ''
    _uriEskaera = ''
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. ESKAERA (Login inprimakia lortu 'logintoken' ateratzeko #####")
        # GET /login/index.php HTTP / 1.1
        # Host: egela.ehu.eus
        metodoa = 'GET'
        uria = "https://egela.ehu.eus/login/index.php"
        goiburuak = {'Host': 'egela.ehu.eus'}

        erantzuna = requests.get(uria, headers=goiburuak, allow_redirects=False)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("1.Eskaeraren metodoa eta URIa :", metodoa, uria)
        print("1.Eskaera: " + str(kodea) + " " + deskribapena)
        # Cookia lortu
        self._cookie = erantzuna.headers['Set-Cookie'].split(';')[0]
        print("1.Eskaeraren Cookia: ", self._cookie)

        # Location URL-a dagoen begiratu

        if ('Location' in erantzuna.headers) is False:
            self._uriEskaera = uria

        print("URI ESKAERA ", self._uriEskaera)
        print("##### HTML-aren azterketa... #####")
        # LoginToken lortu nahi
        html = erantzuna.content

        # HTML parseatuko dugu

        soup = BeautifulSoup(html, 'html.parser')
        token = soup.find('input', {'name': 'logintoken'})

        if token.has_attr('value'):
            self._loginToken = token['value']
            print("Login Token: ", self._loginToken)

        progress = 25
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 2. ESKAERA (Kautotzea -datu bidalketa-) #####")
        print(self._uriEskaera)
        metodoa = "POST"
        # POST / login / index.php
        # HTTP / 1.1
        # Host: egela.ehu.eus
        # Cookie: MoodleSessionegela = 8lbkbfufvtbr9agthn02peal4hn2dnd0
        # Content - Type: application / x - www - form - urlencoded
        # Content - Length: 78
        #
        # logintoken = QCcDskOLf5BMyHTPpb1vuatiUvy21xMF & username = 909854 & password = Euiti2020

        goiburuak = {'Host': 'egela.ehu.eus',
                     'Cookie': self._cookie,
                     'Content-Type': 'application/x-www-form-urlencoded'}
        edukia = {'logintoken': self._loginToken,
                  'username': username.get(),
                  'password': password.get()}
        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))
        erantzuna = requests.post(self._uriEskaera, headers=goiburuak, data=edukia, allow_redirects=False)

        print("2.Eskaeraren metodoa eta URIa :", metodoa, self._uriEskaera)
        print("2.Eskaeraren edukia", edukia)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("2.Eskaera: " + str(kodea) + " " + deskribapena)

        print("\n##### LOGIN EGIAZTAPENA #####")
        if ('Set-Cookie' in erantzuna.headers) is True:
            # sartu kodea hemen
            self._login = 1
            print("KAUTOTU ONDO!!!!!!")
            # KLASEAREN ATRIBUTUAK EGUNERATU

            # sartu kodea hemen

        else:
            self._root.destroy()
            tkMessageBox.showinfo("Alert Message", "Login incorrect!")
            sys.exit(1)
        # Cookia berria lortu
        self._cookie = erantzuna.headers['Set-Cookie'].split(';')[0]
        print("2.Eskaeran Cookie: ", self._cookie)
        if ('Location' in erantzuna.headers) is True:
            self._uriEskaera = erantzuna.headers['Location']

        print("2.Eskaeran LOCATION: ", self._uriEskaera)

        progress = 50
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA (berbidalketa) #####")
        # sartu kodea hemen

        print(self._uriEskaera)
        metodoa = "GET"
        # GET / login / index.php?testsession = 55890
        # HTTP / 1.1
        # Host: egela.ehu.eus
        # Cookie: MoodleSessionegela = 0mflt9n2juknpcrkrd977tut1l8k41ct
        goiburuak = {'Host': self._uriEskaera.split('/')[2],
                     'Cookie': self._cookie}
        erantzuna = requests.get(self._uriEskaera, headers=goiburuak, allow_redirects=False)
        print("3.Eskaeraren metodoa eta URIa :", metodoa, self._uriEskaera)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("3.Eskaera: " + str(kodea) + " " + deskribapena)
        if ('Location' in erantzuna.headers) is True:
            self._uriEskaera = erantzuna.headers['Location']
        print("3.Eskaeran Cookia: ", self._cookie)
        print("3.Eskaeran LOCATION: ", self._uriEskaera)

        progress = 75
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 4. ESKAERA (eGelako orrialde nagusia) #####")

        print(self._uriEskaera)
        metodoa = "GET"
        # GET / HTTP / 1.1
        # Host: egela.ehu.eus
        # Cookie: MoodleSessionegela = a8bleg0kbfrve2qbottur5fvvblbtdat
        goiburuak = {'Host': self._uriEskaera.split('/')[2],
                     'Cookie': self._cookie}

        erantzuna = requests.get(self._uriEskaera, headers=goiburuak, allow_redirects=False)
        print("4.Eskaeraren metodoa eta URIa :", metodoa, self._uriEskaera)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("4.Eskaera " + str(kodea) + " " + deskribapena)
        print("4.Eskaeran Cookia: ", self._cookie)
        html = erantzuna.content

        htmlString = str(html)
        soup = BeautifulSoup(html, 'html.parser')
        izena = soup.find('span', {'class': 'usertext mr-1'})
        print("Nire Izena: ", izena.text)
        errenkadak = soup.find_all('div', {'class': 'info'})
        for idx, errenkada in enumerate(errenkadak):
            irakasgaiak = errenkada.h3.a.text
            if (irakasgaiak == 'Web Sistemak'):
                self._ikasgaia = errenkada.a['href']
                print("Irakasgaia: ", irakasgaiak)
                print("Eskaera: ", self._ikasgaia)

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()

        print("\n##### LOGIN EGIAZTAPENA #####")
        if erantzuna.status_code == 200 and izena != -1:
            # sartu kodea hemen
            self._login = 1
            print("KAUTOTU ONDO!!!!!!")
            # KLASEAREN ATRIBUTUAK EGUNERATU
            self._root.destroy()
            # sartu kodea hemen

        else:
            tkMessageBox.showinfo("Alert Message", "Login incorrect!")

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 5. ESKAERA (Ikasgairen eGelako orrialdea) #####")
        # sartu kodea hemen
        # Web Sistema ikasgaiko eskaera egindo da metodo honetan.
        # GET / course / view.php?id = 57996
        # HTTP / 1.1
        # Host: egela.ehu.eus
        # Cookie: MoodleSessionegela = u47586166f8ag046jf14eau8vbhjr1a2

        metodoa = 'GET'
        goiburuak = {'Host': self._ikasgaia.split('/')[2],
                     'Cookie': self._cookie}

        erantzuna = requests.get(self._ikasgaia, headers=goiburuak, allow_redirects=False)
        print("5.Eskaeraren metodoa eta URIa :", metodoa, self._ikasgaia)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("5.Eskaera " + str(kodea) + " " + deskribapena)
        print("5.Eskaeran Cookia: ", self._cookie)

        progress_step = float(100.0 / 12)  #len(self._refs)

        print("\n##### HTML-aren azterketa... #####")
        # sartu kodea hemen

        html = erantzuna.content
        soup = BeautifulSoup(html, 'html.parser')
        estekak = soup.find_all('img', {'class': 'iconlarge activityicon'})
        # estekaPDP = estekak['src']
        # print(estekak)
        # print(estekaPDP)
        for errenkada in estekak:
            progress += progress_step
            progress_var.set(progress)
            if (errenkada['src'].find("/pdf") != -1):  # Ez badu aurkitzen -1 itzultzen du.
                print("\n##### PDF-a bat aurkitu da! #####")
                pdf_link = errenkada['src']
                self._uriEskaera = errenkada.parent['href']  # https://api.jquery.com/parent/
                print(pdf_link)
                print(self._uriEskaera)

                metodoa = 'GET'
                goiburuak = {'Host': self._uriEskaera.split('/')[2],
                             'Cookie': self._cookie}

                erantzuna = requests.get(self._uriEskaera, headers=goiburuak, allow_redirects=False)
                print("pdfEskaera --> Eskaeraren metodoa eta URIa :", metodoa, self._uriEskaera)
                kodea = erantzuna.status_code
                deskribapena = erantzuna.reason
                print("pdfEskaera --> " + str(kodea) + " " + deskribapena)
                print("pdfEskaera --> Cookia: ", self._cookie)
                html = erantzuna.content
                soup = BeautifulSoup(html, 'html.parser')
                pdf = soup.find('div', {'class': 'resourceworkaround'})
                print(pdf)
                pdf_Uri = pdf.a['href']
                pdf_Izena = pdf_Uri.split('/')[-1]
                print("PDF_URI: ", pdf_Uri)
                print()
                print("PDF_IZENA: ", pdf_Izena)

                self._refs.append({'pdf_name': pdf_Izena, 'pdf_link': pdf_Uri})
            # print(html)



        progress_bar.update()
        time.sleep(0.1)

        print(self._refs)
        popup.destroy()

        return self._refs


    def get_pdf(self, selection):
        self.pdfKarpetaSortu()
        print("##### PDF-a deskargatzen... #####")
        # sartu kodea hemen
        pdfUri = self._refs[selection]['pdf_link']
        print(pdfUri)
        metodoa = 'GET'
        goiburuak = {'Host': pdfUri.split('/')[2],
                     'Cookie': self._cookie}

        erantzuna = requests.get(pdfUri, headers=goiburuak, allow_redirects=False)
        print("pdfDeskarga --> Eskaeraren metodoa eta URIa :", metodoa, pdfUri)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("pdfDeskarga --> " + str(kodea) + " " + deskribapena)
        print("pdfDeskarga --> Cookia: ", self._cookie)

        # pdf-aren edukia fitxategi batean gordetzen
        pdf_file = erantzuna.content
        pdf_name = self._refs[selection]['pdf_name']
        file = open("./pdf/" + pdf_name, "wb")
        file.write(pdf_file)
        file.close()

        return pdf_name, pdf_file

    def pdfKarpetaSortu(self):
        if not os.path.exists("pdf"):
            os.mkdir("pdf")

