import json
import webbrowser
import subprocess

import ast
import msal
import requests

import Models

"""
APP_ID = "3079e919-8f04-41b7-8b97-5694679bd4f3"
SECRET = "23379d03-b2a5-4dd2-a4d0-233b3b40588f"
SECRET = "v-Z8Q~iy~vA77IarV5izSqG0e3uX-qBtItFHudd2"
# "Notes.Create", "Notes.Read", "Notes.Read.All", "Notes.ReadWrite", "Notes.ReadWrite.All", "Notes.ReadWrite.CreatedByApp"
# SCOPES = ['']
SCOPES = ["Notes.Create", "Notes.Read", "Notes.Read.All", "Notes.ReadWrite", "Notes.ReadWrite.All", "Notes.ReadWrite.CreatedByApp"]

AUTHORITY_URL = "https://login.microsoftonline.com/consumers/"
base_url = "https://graph.microsoft.com/v1.0/"
endpoint = base_url + "me"
"""


class OneNoteManager(object):

    def __init__(self, token=None):
        self.token = token

    
    def __auth_header(self):
        headers = {"Authorization": f"Bearer {self.__token.access_token}"}

        return headers

    # retrieving OneNote notebooks
    def get_notebooks(self):
        url = "https://graph.microsoft.com/v1.0/me/onenote/notebooks"

        headers = self.__auth_header()
        req = requests.get(url, headers=headers)
        content = req.content
        j_obj = content.decode("utf8")


        note_d = dict()
        note_d = json.loads(j_obj)

        return note_d


        return json_data

    # retrieving OneNote sections
    def get_sections(self):
        url = "https://graph.microsoft.com/v1.0/me/onenote/sections"

        headers = self.__auth_header()
        req = requests.get(url, headers=headers)
        content = req.content
        j_obj = content.decode("utf8")

        sect_d = dict()
        sect_d = json.loads(j_obj)

        return sect_d

    # retrieving OneNote notes given a url
    def get_notes(self, url):
        notes = dict()

        headers = self.__auth_header()
        req = requests.get(url, headers=headers)
        content = req.content
        j_obj = content.decode("utf8")

        notes = json.loads(j_obj)

        if "@odata.nextLink" in notes:
            nextLink = notes["@odata.nextLink"] 
            notes_s = self.get_notes(nextLink)

            for note in notes_s["value"]:
                notes["value"].append(note)

        return notes

    # Implement this function
    def add_note(self, note):

        url = "https://graph.microsoft.com/v1.0/me/onenote/sections/{section-id}/pages"

        data = {"dsfsdf", "sdfsdf"}
        headers = self.__auth_header()
        req = requests.post(url, data=data, headers=headers)
        content = req.content
        j_obj = content.decode("utf8").replace("'", '"')

        json_data = json.dumps(j_obj)

        print("Add")

        return json_data
    
    # Returns string representation of the note used for creating pages
    def note_to_data(self, note):
        title_str = note.title
        content_str = note.content

        data =""

        if content_str == "":
            data = f"<!DOCTYPE html><html><head><title>title_str</title></head> <body></body></html>"
        else:
            data = f"<!DOCTYPE html><html><head><title>title_str</title></head> <body>content_str</body></html>"

        return data


    def fetch_token(self):
        app = msal.PublicClientApplication(self.__APP_ID,
            authority=self.__AUTHORITY_URL
        )

        accounts = app.get_accounts()

        if accounts:
            app.acquire_token_silent(scopes=self.__SCOPES, account=accounts[0])

        flow = app.initiate_device_flow(scopes=self.__SCOPES)
        user_code = flow['user_code']
        print('User code: %s' % (user_code))
        print("Enter code in browser to continue (Has been entered into clipboard)\n")


        useless_cat_call = subprocess.run(["clip.exe"], stdout=subprocess.PIPE, text=True, input=user_code)

        app_code = flow['message']

        webbrowser.open(flow['verification_uri'])

        token_response = app.acquire_token_by_device_flow(flow)

        json_data = json.dumps(token_response)
        self.__token = Models.ResponseToken(**json.loads((json_data)))

        print("Access token: %s" % (self.__token.access_token))

        return self.__token

    def load_token(self, token):
        self.__token = token


    __APP_ID = "3079e919-8f04-41b7-8b97-5694679bd4f3"
    __SECRET = "v-Z8Q~iy~vA77IarV5izSqG0e3uX-qBtItFHudd2"
    __SCOPES = ["Notes.Create", "Notes.Read", "Notes.Read.All", "Notes.ReadWrite", "Notes.ReadWrite.All", "Notes.ReadWrite.CreatedByApp"]

    __AUTHORITY_URL = "https://login.microsoftonline.com/consumers/"
    __base_url = "https://graph.microsoft.com/v1.0/"
    __endpoint = __base_url + "me"
    __token = Models.ResponseToken()