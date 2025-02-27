#!/usr/bin/env python3

import notionlib

API_TOKEN = "ntn_3232...87O"
DB_ID = "26c3...1bb1"

notion = notionlib.Notion(API_TOKEN)


# READ A DATABASE

notion_pages_list = notion.query_a_database(notion_db_id=DB_ID)
print(notion_pages_list)


# CREATE A PAGE IN A DATABASE

properties_dict = {
    "Parc": {
        "type": "rich_text",
        "value": "parc_test"
    },
    "Bâtiment": {
        "type": "title",
        "value": "bat_test"
    },
    "date déploiement": {
        "type": "rich_text",
        "value": "date_test"
    },
    "Déploiement": {
        "type": "status",
        "value": "déployé"
    },
    "Tag": {
        "type": "multi_select",
        "value": ["Eng. Perf.", "surchauffe"]
    },
    "Commentaire": {
        "type": "rich_text",
        "value": "comment_test"
    },
    "nb Zones pilotées": {
        "type": "number",
        "value": 1
    }
}

resp = notion.create_a_page(notion_db_id=DB_ID, properties=properties_dict)

print(resp)
page_id = resp['id']

print(f"New page ID: {page_id}")


# UPDATE A PAGE IN A DATABASE

resp = notion.update_a_page(notion_page_id=page_id, properties=properties_dict)
