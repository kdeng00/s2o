import json
import sys
import time

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

    # print("Hehe!!")
    # return

    res = sn.delete_note(note.note_id)
    print("Deleted '%s' from Simplenote" % note.title)


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
                split = title.split("\r\n")

                title = split[0]

                split.remove(split[0])

                if len(split) == 1:
                    content = split[0]
                elif len(split) == 2:
                    content = split[1]


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

    for value in notes['value']:
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

def note_exists_in_onenote(note, onenote_notes):
    for o_note in onenote_notes['value']:
        if note.title == o_note['title']:
            return True
    
    return False

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

    config = onenote_mgr.config

    onenote_section = retrieve_section(onenote_sections, chosen_section)
    url = f"{config.base_url}me/onenote/sections/" + onenote_section["id"] + "/pages"
    onenote_notes = onenote_mgr.get_notes(url)

    count = 0

    for note in onenote_notes["value"]:
        count += 1

    if not is_valid_note(onenote_notes, onenote_section):
        print("Note not foudn for '%s'" % (chosen_section))
        return

    interval = config.interval
    limit = config.limit
    total_notes_added = 0
    bundle_notes_added = 0

    for note in simplenotes:
        if note_exists_in_onenote(note, onenote_notes):
            continue

        json_data = onenote_mgr.add_note(note, onenote_section)

        if json_data != None or "error" not in json_data:
            cred = Models.SimplenoteCredentials(username=None, password=None)
            sn = onenote_mgr.config.vendors['simplenote']

            cred.username = sn['username']
            cred.password = sn['password']
            delete_note(cred, note)
        
            if bundle_notes_added == limit:
                if interval > 300:
                    time.sleep(300)
                else:
                    time.sleep(interval)

                config = load_config()
                onenote_mgr.config = config
                onenote_notes = onenote_mgr.get_notes(url)

                bundle_notes_added = 0
            else:
                bundle_notes_added += 1

            total_notes_added += 1
    
    if total_notes_added > 0:
        print("Deleted %d notes" % (total_notes_added))




def load_config():
    filepath = sys.argv[1]

    json_data = json.load(open(filepath))
    dump = json.dumps(json_data)

    loaded = json.loads(dump)
    config = Models.Config(**loaded)

    return config


def main():

    if len(sys.argv) != 2:
        print("Provide argument")
        print("Main.py \"config.json\"")

        sys.exit(-1)


    print("s20")

    config = load_config()

    if config.vendors == None or config.vendors['onenote'] == None:
        print("No vendor or onenote section")
        sys.exit(-1)
    
    o_note = config.vendors['onenote']

    if o_note['target_notebook'] == None or o_note['target_section'] == None:
        print("Notebook or section is empty")
        sys.exit(-1)

    cred_ob = config.vendors['simplenote']
    cred = Models.SimplenoteCredentials(cred_ob['username'], cred_ob['password'])
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
    9. [X] Iterate through Simplenote notes
    10. [X] Check to see if a OneNote note exists that comes from the selected notebook and section. Terminate if not
    11. [X] Create page in OneNote using the iterated Simplenote note
    12. [X] Retrieve the OneNote pages again
    13. [X] Check to see if the page has been created
    14. [X] Delete the Simplenote note
    """

    config.token_init()

    onenote_mgr = OneNoteManager.OneNoteManager(config=config)

    chosen_notebook = config.vendors['onenote']['target_notebook']
    chosen_section = config.vendors['onenote']['target_section']
    export_to_onenote(notes, onenote_mgr, chosen_notebook=chosen_notebook, chosen_section=chosen_section)
    

# logger = log21.get_logger('My Logger', level_names={21: 'SpecialInfo', log21.WARNING: ' ! ', log21.ERROR: '!!!'})
# logger.log(21, 'Here', '%s', 'GO!', args=('we',))

if __name__ == "__main__":
    main()