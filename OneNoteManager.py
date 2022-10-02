import json
import os
import subprocess
import webbrowser

import ast
import msal
import requests

import Models

class OneNoteManager(object):

    def __init__(self, token=None, config=None):
        self.token = token
        self.config = config

        if self.config != None:
            self.initialize_onenote(self.config)

    def initialize_onenote(self, config):
        self.__APP_ID = config.app_id
        self.__SECRET = config.secret
        self.__SCOPES = config.scopes
        self.__AUTHORITY_URL = config.authority_url
        self.__base_url = config.base_url
        self.__token = Models.ResponseToken(access_token=config.token)

    
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
    def add_note(self, note, onenote_section):
        section_id = onenote_section['id']

        url = f"https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages"

        data = self.note_to_data(note)
        headers = self.__auth_header()
        headers['Content-type'] = "application/xhtml+xml"
        req = requests.post(url, data=data, headers=headers)
        content = req.content
        j_obj = content.decode("utf8")

        json_data = json.dumps(j_obj)

        if "error" not in json_data:
            print("Added note '%s' to OneNote" % note.title)

        return json_data
    
    # Returns string representation of the note used for creating pages
    def note_to_data(self, note):
        title_str = note.title
        content_str = note.content

        data =""

        if content_str == "":
            data = f"<!DOCTYPE html><html><head><title>{title_str}</title></head> <body></body></html>"
        else:
            data = f"<!DOCTYPE html><html><head><title>{title_str}</title></head> <body>{content_str}</body></html>"

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

        if os.name == "nt":
            useless_cat_call = subprocess.run(["clip.exe"], stdout=subprocess.PIPE, text=True, input=user_code)
        elif os.name == "posix":
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


    __APP_ID = "Enter app id"
    __SECRET = "Enter secret"
    __SCOPES = []

    __AUTHORITY_URL = "https://login.microsoftonline.com/consumers/"
    __base_url = "https://graph.microsoft.com/v1.0/"
    __endpoint = __base_url + "me"
    __token = Models.ResponseToken()
