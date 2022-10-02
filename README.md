# s2o

s2o is a software utility tool to export notes from Simplenote to OneNote. This software exports notes from Simplenote and creates notes in a specific notebook and section. Once the note has been created, the note is deleted from Simplenote.


## Configuration

```JSON
{
    "token": "some_token",
    "secret": "some secret",
    "app_id": "sdf348thg348fh3f",
    "mode": "token",
    "scopes": ["Create", "Read"],
    "authority_url": "https://some-link.com",
    "base_url": "https://some-other-link.com",
    "limit": 100,
    "interval": 300,
    "vendors": {
        "simplenote": {
            "username": "me",
            "password": "who",
            "source_notebook": "",
            "source_section": ""
        },
        "onenote": {
            "username": "",
            "password": "",
            "target_notebook": "New notebook",
            "target_section": "New Section"
        }
    }
}
```

* `token` - Access token used for making OneNote requests. This token will be used if the `mode` is token
* `secret` - The secret phrase when creating the App from Microsoft dev platform
* `app_id` - The application ID when creating the App from Microsoft dev platform
* `mode` - Mode that determines how a token will be retrieved. Supported modes are *token input* and *token*. *token input* will require you to provide the token via the shell. *token* will use the value specified in the `token` field
* `scopes` - Requested scope actions
* `authority_url` - URL for authorization
* `base_url` - Base URL for Microsoft Graph API
* `limit` - The limit in which notes can be exported before sleeping. This is used to prevent too many requests in a short period of time which results in a denial of service
* `interval` - Time in seconds to sleep after a certain amount of notes have been exported. The amount is specified by the `limit` field
* `vendors` - Suported vendors
    * `simplenote:username` - Username of the Simplenote account
    * `simplenote:password` - Password of the Simplenote account
    * `simplenote:source_notebook` - Not used
    * `simplenote:source_section` - Not used
    * `onenote:username` - Not used
    * `onenote:password` - Not used
    * `onenote:target_notebook` - Target notebook to save notes from Simplenote
    * `onenote:target_section` -- Target section to save notes from Simplenote


## Usages

```BASH
python main.py [path to config.json]
```