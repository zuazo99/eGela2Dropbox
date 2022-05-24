import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper


server_addr = "localhost"
server_port = 8090
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _app_key = 'os5tgok1ed5bss7'
    _app_secret = '6z806rfr9k4nl10'
    _access_token = ""
    _path = "/"
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # sartu kodea hemen
        # 8090.portuan entzuten dagoen zerbitzaria sortu
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # nabigatzailetik 302 eskaera jaso
        client_connection, client_address = server_socket.accept()
        eskaera = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print(eskaera)

        # eskaeraren "auth_code" bilatu
        lehenengo_lerroa = eskaera.decode("utf8").split('\n')[0]
        aux_auth_code = lehenengo_lerroa.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print("\tauth_code: " + auth_code)

        # erabiltzaileari erantzun bat bueltatu
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response.encode(encoding="utf8"))
        client_connection.close()
        server_socket.close()

        return auth_code

    def do_oauth(self):
        # sartu kodea hemen
        auth_uri = "https://www.dropbox.com/oauth2/authorize"
        datos = {'client_id': self._app_key,
                 'response_type': "code",
                 'redirect_uri': redirect_uri}

        datos_encoded = urllib.parse.urlencode(datos)
        webbrowser.open_new(auth_uri + "?" + datos_encoded)

        print("# Step 4: Handle the OAuth 2.0 server response")
        auth_code = self.local_server()
        # auth_code = raw_input('Enter code')
        print("# Step 5: Exchange authorization code for refresh and access tokens")
        token_uri = "https://api.dropboxapi.com/oauth2/token"
        datos = {'code': auth_code,
                 'grant_type': 'authorization_code',
                 'client_id': self._app_key,
                 'client_secret': self._app_secret,
                 'redirect_uri': redirect_uri}
        respuesta = requests.post(token_uri, data=datos, allow_redirects=False)
        status = respuesta.status_code
        print("\tStatus: " + str(status))

        contenido = respuesta.text
        print("\tCotenido:")
        print(contenido)
        contenido_json = json.loads(contenido)
        access_token = contenido_json['access_token']
        print("\taccess_token: " + access_token)

        self._access_token = access_token
        self._root.destroy()

    def list_folder(self, msg_listbox, cursor="", edukia_json_entries=[]):
        """ Zerrendatzen du karpeta baten edukia"""
        print("/list_folder")
        if self._path == "/":
            self._path = ""

        if not cursor:
            print("/list_folder")
            uri = 'https://api.dropboxapi.com/2/files/list_folder'
            datuak = {'path': self._path,
                      'recursive': False,
                      "include_mounted_folders": True,
                      "include_non_downloadable_files": True
                      }
            # sartu kodea hemen
            datuak_json = json.dumps(datuak)

        else:
            print("/list_folder/continue")
            uri = 'https://api.dropboxapi.com/2/files/list_folder/continue'
            datuak = {'cursor': cursor}
            # sartu kodea hemen
            datuak_json = json.dumps(datuak)

        # Call Dropbox API
        # sartu kodea hemen
        goiburuak = {'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}

        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tContenido: ")
        print(edukia)
        edukia_json = json.loads(edukia)
        edukia_json_entries = edukia_json['entries']
        if edukia_json['has_more']:
            # sartu kodea hemen
            self.list_folder(msg_listbox, edukia_json['cursor'], edukia_json_entries)
        else:
            # sartu kodea hemen
            self._files = helper.update_listbox2(msg_listbox, self._path, edukia_json_entries)

    def transfer_file(self, file_path, file_data):
        print("/upload " + file_path)
        # sartu kodea hemen
        # https://www.dropbox.com/developers/documentation/http/documentation#files-upload
        uri = "https://content.dropboxapi.com/2/files/upload"
        dropbox_api_arg = {'path': file_path,
                           'mode': 'add',
                           'autorename': True,
                           'mute': False,
                           'strict_conflict': False}
        dropbox_api_arg_json = json.dumps(dropbox_api_arg)
        goiburuak = {'Host': 'content.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/octet-stream',
                     'Dropbox-API-Arg': dropbox_api_arg_json}
        erantzuna = requests.post(uri, headers=goiburuak, data=file_data, allow_redirects=False)
        status = erantzuna.status_code
        deskribapena = erantzuna.reason
        print('Status: ' + str(status) + 'Deskribapena: ' + str(deskribapena))

    def delete_file(self, file_path):
        """ Fitxategi bat ezabatzen du """
        print("/delete_file " + file_path)
        # sartu kodea hemen
        uri = 'https://api.dropboxapi.com/2/files/delete_v2'

        datuak = {'path': file_path}
        datuak_json = json.dumps(datuak)

        goiburuak = {'Host': 'api.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_json, allow_redirects=False)
        status = erantzuna.status_code
        print('Status: ' + str(status))

    def create_folder(self, path):
        """ Fitxategi bat sortu egiten du"""
        print("/create_folder " + path)
        #https://www.dropbox.com/developers/documentation/http/documentation#files-create_folder
        # sartu kodea hemen

        uri = 'https://api.dropboxapi.com/2/files/create_folder_v2'
        datuak = {'path': path,
                  'autorename': False}
        datuak_json = json.dumps(datuak)
        goiburuak = {'Host': 'api.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_json, allow_redirects=False)
        status = erantzuna.status_code
        print('Status: ' + str(status))

    def download_zip(self, file_path):
        """ Downloads zip of the current folder. NOT SUPPORTED FOR ROOT FOLDER."""
        url = 'https://content.dropboxapi.com/2/files/download_zip'
        d = {"path": file_path}

        headers = {'Authorization': 'Bearer ' +
                                    self._access_token, 'Dropbox-API-Arg': json.dumps(d)}

        post_ = requests.post(url, headers=headers, allow_redirects=False)

        fName = str(file_path).split("/")[len(str(file_path).split("/")) - 1]
        print(file_path)
        print(fName)
        with open(fName + ".zip", 'wb') as fd:
            fd.write(post_.content)

