import sys
import io
import json

import log21
import simplenote

import OneNoteManager
import Models




def contains_title_and_content(content):

    text = "\n\n"

    amount = content.count(text)

    if amount < 0:
        return False


    return True

def delete_note(cred, note):
    sn = simplenote.Simplenote(cred.username, cred.password)

    print("Hehe!!")
    return

    sn.delete_note(note.note_id)


def get_simplenote_list(cred):
    sn = simplenote.Simplenote(cred.username, cred.password)

    elements = sn.get_note_list()

    notes = []

    for e in elements:

        in_valid = lambda obj : obj == 0

        if in_valid(e):
            continue

        for i in e:
            # In Simplenote, notes with no content the 'content' would be the title
            content = ""
            title = i['content']
            id = i['key']

            if contains_title_and_content(title):
                # Parse the title from the content
                #
                # The title and content are delimited by '\n\n'
                split = title.split("\n\n")

                title = split[0]

                split.remove(split[0])
                content = "\n\n".join(split)

            note = Models.SimpleNote(title, content)
            note.note_id = id
            notes.append(note)

    return notes

def iterate_simplenotes(notes):
    for note in notes:
        print("Title: %s" % (note.title))

        if note.content == "":
            print("Content: None")
        else:
            print("Content: %s" % (note.content))

def is_valid_notebook(onenote_notebooks, chosen_notebook):
    res = False

    notes = onenote_notebooks

    for value in notes["value"]:
        display_name = value["displayName"]

        if display_name == chosen_notebook:
            res = True
            break

    return res

def retrieve_notebook(onenote_notebooks, chosen_notebook):
    notes = onenote_notebooks

    for value in notes["value"]:
        display_name = value["displayName"]

        if display_name == chosen_notebook:
            return value

    return str()

def is_valid_section(onenote_sections, chosen_section):
    res = False

    sections = onenote_sections

    for value in sections["value"]:
        display_name = value["displayName"]

        if display_name == chosen_section:
            res = True
            break

    return res

def retrieve_section(onenote_sections, chosen_section):
    sections = onenote_sections

    for value in sections["value"]:
        display_name = value["displayName"]

        if display_name == chosen_section:
            return value

    return str()

def is_valid_note(onenote_notes, onenote_section):
    res = False

    notes = onenote_notes

    for value in notes["value"]:
        display_name = value["parentSection"]["displayName"]

        print("Section: %s" % (display_name))

        if display_name == onenote_section["displayName"]:
            res = True
            break


    return res


def export_to_onenote(simplenotes, onenote_mgr, chosen_notebook=None, chosen_section=None):
    onenote_notebooks = onenote_mgr.get_notebooks()

    if not is_valid_notebook(onenote_notebooks, chosen_notebook):
        print("Notebook not found for '%s'" % (chosen_notebook))
        return

    onenote_notebook = retrieve_notebook(onenote_notebooks, chosen_notebook)

    if onenote_notebook == "":
        print("No notebooks found")
        return

    onenote_sections = onenote_mgr.get_sections()

    if not is_valid_section(onenote_sections, chosen_section):
        print("Section not found for '%s'" % (chosen_section))
        return

    onenote_section = retrieve_section(onenote_sections, chosen_section)
    url="https://graph.microsoft.com/v1.0/me/onenote/sections/" + onenote_section["id"] + "/pages"
    onenote_notes = onenote_mgr.get_notes(url)

    count = 0

    for note in onenote_notes["value"]:
        count += 1

    if not is_valid_note(onenote_notes, onenote_section):
        print("Note not foudn for '%s'" % (chosen_section))
        return

    for note in simplenotes:
        simplenote_id = note.note_id


def main():

    if len(sys.argv) < 3:
        print("Provide arguments\n")
        print("main.py 'username' 'password'")

        sys.exit(-1)

    logger.info("simplenote_export running")

    cred = Models.SimplenoteCredentials(sys.argv[1], sys.argv[2])

    print("Username: %s" % (cred.username))

    print("Hello")

    notes = get_simplenote_list(cred)

    """
    What's left?
    1. Implement function to retrieve notes from OneNote
    2. Implement function to add note to OneNote
    3. Implement function to see if note exists in OneNote (Optional)
      - If this isn't feasible or will require more effort than expected, just retrieve notes from 
      OneNote after adding a note to get the updated notes

    Will need to add a note to a specific notebook and int a specific notebook
    1. [X] Get list of notebooks
    2. [X] Use the display name to find the desired notebook
    3. [X] If it isn't found, terminate the program. If found, parse out the display name and id of the notebook
    4. [X] Get a list of sections
    5. [X] Check to see if a section exists where the parent notebook is the one you selected. Terminate if not
    6. [X] Get OneNote Notes (By section id and check to see if there is a @data.nextLink)
    7. [X] Check to see if the notes are part of the section
    8. [X] Get a list of OneNote notes that's part of the section
    9. Iterate through Simplenote notes
    10. Check to see if a OneNote note exists that comes from the selected notebook and section. Terminate if not
    11. Check to see if the iterated Simplenote note exists in OneNote with the matched criteria. Terminate if so
    12. Create page in OneNote using the iterated Simplenote note
    13. Retrieve the OneNote pages again
    14. Check to see if the page has been created
    15. Delete the Simplenote note
    """

    onenote_mgr = OneNoteManager.OneNoteManager()
    
    dev = 1

    token = Models.ResponseToken()

    if dev == 0:
        print("Enter token: ")
        token_input = input()
        token.access_token = token_input
    elif dev == 1:
        fi = io.open("token.txt")
        token.access_token = fi.read()
    else:
        token = onenote_mgr.fetch_token()

    onenote_mgr.load_token(token)

    export_to_onenote(notes, onenote_mgr, chosen_notebook="Simplenote", chosen_section="From Simplenote")
    

    # iterate_simplenotes(notes)


logger = log21.get_logger('My Logger', level_names={21: 'SpecialInfo', log21.WARNING: ' ! ', log21.ERROR: '!!!'})
logger.log(21, 'Here', '%s', 'GO!', args=('we',))

if __name__ == "__main__":
    main()