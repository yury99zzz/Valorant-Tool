import os
import subprocess
import requests
import customtkinter
import json
import threading
import difflib
import sys
import time
import base64
import pyperclip
import webbrowser
import copy
from random import choice
from valclient.client import Client
from PIL import Image, ImageDraw
from io import BytesIO


# auto generate config files
# If removed WILL BREAK!!!
defaultConfig = {
    "agents": {
            "None": "00000",
            "Jett": "add6443a-41bd-e414-f6ad-e58d267f4e95",
            "Reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
            "Raze": "f94c3b30-42be-e959-889c-5aa313dba261",
            "Yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
            "Phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69",
            "Neon": "bb2a4828-46eb-8cd1-e765-15848195d751",
            "Breach": "5f8d3a7f-467b-97f3-062c-13acf203c006",
            "Skye": "6f2a04ca-43e0-be17-7f36-b3908627744d",
            "Sova": "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
            "Killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746",
            "Cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
            "Sage": "569fdd95-4d10-43ab-ca70-79becc718b46",
            "Chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
            "Omen": "8e253930-4c05-31dd-1b6c-968525494517",
            "Brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
            "Astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
            "Viper": "707eab51-4836-f488-046a-cda6bf494859",
            "Fade": "dade69B4-4f5a-8528-247b-219e5a1facd6",
            "Gekko": "E370FA57-4757-3604-3648-499E1F642D3F",
            "Deadlock": "CC8B64C8-4B25-4FF9-6E7F-37B4DA43D235",
            "Iso": "0E38B510-41A8-5780-5E8F-568B2A4F2D6C",
            "Clove": "1DBF2EDD-4729-0984-3115-DAA5EED44993",
            "Harbor": "95B78ED7-4637-86D9-7E41-71BA8C293152",
            "KAY/O": "601dbbe7-43ce-be57-2a40-4abd24953621",
            "Vyse": "efba5359-4016-a1e5-7626-b1ae76895940",
            "Tejo": "B444168C-4E35-8076-DB47-EF9BF368F384",
            "Waylay": "DF1CB487-4902-002E-5C17-D28E83E78588"
        },
    "regions": {
        "Europe": "eu",
        "North America": "na",
        "Asia Pacific": "ap",
        "Latin America": "latam",
        "Brazil": "br",
        "Korea": "kr"
    },
    "region": "eu",
    "agent": "None",
    "instalockMode": "Lock",
    "ran": False,
    "mapMode": "Normal",
    "mapAgentSelect": {
        "Ascent": "None",
        "Split": "None",
        "Fracture": "None",
        "Bind": "None",
        "Breeze": "None",
        "Abyss": "None",
        "Lotus": "None",
        "Sunset": "None",
        "Pearl": "None",
        "Icebox": "None",
        "Haven": "None"
    },
    "delay": 4.0,
    "skinsOrder": [
        "Vandal",
        "Phantom",
        "Operator",
        "Sheriff",
        "Melee",
        "Classic",
        "Ghost",
        "Odin",
        "Ares",
        "Guardian",
        "Bulldog",
        "Outlaw",
        "Marshal",
        "Spectre",
        "Judge",
        "Bucky",
        "Stinger",
        "Frenzy",
        "Shorty"
    ],
    "CheckForUpdates": True,
    "Scaling": 100,
    "Theme": "System"
}
defaultSkins= {
    "9c82e19d-4575-0200-1a81-3eacf00cf872": {
        "name": "Default Vandal",
        "defaultChroma": "19629ae1-4996-ae98-7742-24a240d41f99",
        "size": [
            275,
            75
        ],
        "link": "https://media.valorant-api.com/weapons/9c82e19d-4575-0200-1a81-3eacf00cf872/displayicon.png"
    },
    "ee8e8d15-496b-07ac-e5f6-8fae5d4c7b1a": {
        "name": "Default Phantom",
        "size": [
            275,
            65
        ],
        "link": "https://media.valorant-api.com/weapons/ee8e8d15-496b-07ac-e5f6-8fae5d4c7b1a/displayicon.png",
        "defaultChroma": "52221ba2-4e4c-ec76-8c81-3483506d5242"
    },
    "a03b24d3-4319-996d-0f8c-94bbfba1dfc7": {
        "name": "Default Operator",
        "size": [
            300,
            60
        ],
        "link": "https://media.valorant-api.com/weapons/a03b24d3-4319-996d-0f8c-94bbfba1dfc7/displayicon.png",
        "defaultChroma": "4914f50d-49f9-6424-ca80-9486c45a138d"
    },
    "e336c6b8-418d-9340-d77f-7a9e4cfe0702": {
        "name": "Default Sheriff",
        "size": [
            170,
            75
        ],
        "link": "https://media.valorant-api.com/weapons/e336c6b8-418d-9340-d77f-7a9e4cfe0702/displayicon.png",
        "defaultChroma": "5a59bd61-48a9-af61-c00f-4aa21deca9a8"
    },
    "2f59173c-4bed-b6c3-2191-dea9b58be9c7": {
        "name": "Default Melee",
        "size": [
            200,
            75
        ],
        "link": "https://media.valorant-api.com/weapons/2f59173c-4bed-b6c3-2191-dea9b58be9c7/displayicon.png",
        "defaultChroma": "cac83e5c-47a1-3519-5420-1db1fdbc4892"
    },
    "29a0cfab-485b-f5d5-779a-b59f85e204a8": {
        "name": "Default Classic",
        "size": [
            120,
            75
        ],
        "link": "https://media.valorant-api.com/weapons/29a0cfab-485b-f5d5-779a-b59f85e204a8/displayicon.png",
        "defaultChroma": "4b2d5b4f-4955-4208-286c-abadec250cdd"
    },
    "1baa85b4-4c70-1284-64bb-6481dfc3bb4e": {
        "name": "Default Ghost",
        "size": [
            200,
            65
        ],
        "link": "https://media.valorant-api.com/weapons/1baa85b4-4c70-1284-64bb-6481dfc3bb4e/displayicon.png",
        "defaultChroma": "947a28b6-4e0f-61fb-e795-bc9a5e7b7129"
    },
    "63e6c2b6-4a8e-869c-3d4c-e38355226584": {
        "name": "Default Odin",
        "size": [
            310,
            75
        ],
        "link": "https://media.valorant-api.com/weapons/63e6c2b6-4a8e-869c-3d4c-e38355226584/displayicon.png",
        "defaultChroma": "2f93861d-4b2f-2175-af0c-3ba0c736e257"
    },
    "55d8a0f4-4274-ca67-fe2c-06ab45efdf58": {
        "name": "Default Ares",
        "size": [
            280,
            60
        ],
        "link": "https://media.valorant-api.com/weapons/55d8a0f4-4274-ca67-fe2c-06ab45efdf58/displayicon.png",
        "defaultChroma": "b33de820-4061-8b85-31ce-808f1a2c58f5"
    },
    "4ade7faa-4cf1-8376-95ef-39884480959b": {
        "name": "Default Guardian",
        "size": [
            280,
            60
        ],
        "link": "https://media.valorant-api.com/weapons/4ade7faa-4cf1-8376-95ef-39884480959b/displayicon.png",
        "defaultChroma": "0f934388-418a-a9e7-42a7-21b27402e46c"
    },
    "ae3de142-4d85-2547-dd26-4e90bed35cf7": {
        "name": "Default Bulldog",
        "size": [
            265,
            65
        ],
        "link": "https://media.valorant-api.com/weapons/ae3de142-4d85-2547-dd26-4e90bed35cf7/displayicon.png",
        "defaultChroma": "bf35f404-4a14-6953-ced2-5bafd21639a0"
    },
    "5f0aaf7a-4289-3998-d5ff-eb9a5cf7ef5c": {
        "name": "Default Outlaw",
        "size": [
            300,
            60
        ],
        "link": "https://media.valorant-api.com/weapons/5f0aaf7a-4289-3998-d5ff-eb9a5cf7ef5c/displayicon.png",
        "defaultChroma": "66c8d241-4f7c-6652-3aaa-51bafffbd493"
    },
    "c4883e50-4494-202c-3ec3-6b8a9284f00b": {
        "name": "Default Marshal",
        "size": [
            300,
            60
        ],
        "link": "https://media.valorant-api.com/weapons/c4883e50-4494-202c-3ec3-6b8a9284f00b/displayicon.png",
        "defaultChroma": "1afec971-4170-f29b-1c94-07a0eff270ab"
    },
    "462080d1-4035-2937-7c09-27aa2a5c27a7": {
        "name": "Default Spectre",
        "size": [
            205,
            70
        ],
        "link": "https://media.valorant-api.com/weapons/462080d1-4035-2937-7c09-27aa2a5c27a7/displayicon.png",
        "defaultChroma": "a9aaccca-4cdc-02ea-1d7e-89bbacecc0e2"
    },
    "ec845bf4-4f79-ddda-a3da-0db3774b2794": {
        "name": "Default Judge",
        "size": [
            270,
            70
        ],
        "link": "https://media.valorant-api.com/weapons/ec845bf4-4f79-ddda-a3da-0db3774b2794/displayicon.png",
        "defaultChroma": "b71ae8d6-44bb-aa4c-0d2a-dc9ed9e66410"
    },
    "910be174-449b-c412-ab22-d0873436b21b": {
        "name": "Default Bucky",
        "size": [
            290,
            50
        ],
        "link": "https://media.valorant-api.com/weapons/910be174-449b-c412-ab22-d0873436b21b/displayicon.png",
        "defaultChroma": "3d8ffcfe-4786-0180-42d7-e1be18dd1cab"
    },
    "f7e1b454-4ad4-1063-ec0a-159e56b58941": {
        "name": "Default Stinger",
        "size": [
            200,
            65
        ],
        "link": "https://media.valorant-api.com/weapons/f7e1b454-4ad4-1063-ec0a-159e56b58941/displayicon.png",
        "defaultChroma": "31bb2115-4c62-d37c-43c4-11b8fee7f212"
    },
    "44d4e95c-4157-0037-81b2-17841bf2e8e3": {
        "name": "Default Frenzy",
        "size": [
            120,
            70
        ],
        "link": "https://media.valorant-api.com/weapons/44d4e95c-4157-0037-81b2-17841bf2e8e3/displayicon.png",
        "defaultChroma": "dc99ed5a-4d75-87a0-c921-75963ea3c1e1"
    },
    "42da8ccc-40d5-affc-beec-15aa47b42eda": {
        "name": "Default Shorty",
        "size": [
            190,
            60
        ],
        "link": "https://media.valorant-api.com/weapons/42da8ccc-40d5-affc-beec-15aa47b42eda/displayicon.png",
        "defaultChroma": "95608504-4c8b-1408-1612-0f8200421c49"
    }
}
# get paths
appDataFolderName = 'Valorant-Tool'
appDataPath = os.path.join(os.getenv('APPDATA'), appDataFolderName)
os.makedirs(appDataPath, exist_ok=True)
configPath = os.path.join(appDataPath, 'config.json')
themePath = os.path.join(appDataPath, 'colorTheme.json')
iconPath = os.path.join(appDataPath, 'FastPick.ico')
# Check file existance and missing agents and maps and update them
if not os.path.exists(configPath):
    with open(configPath, 'w') as file:
        json.dump(defaultConfig, file, indent=4)

defaultTheme = {
    "CTk": {
        "fg_color": ["gray92", "gray14"]
    },
    "CTkToplevel": {
        "fg_color": ["gray92", "gray14"]
    },
    "CTkFrame": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["gray86", "gray17"],
        "top_fg_color": ["gray81", "gray20"],
        "border_color": ["gray65", "gray28"]
    },
    "CTkButton": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["#D03434", "#A11D1D"],
        "hover_color": ["#B22E2E", "#791414"],
        "border_color": ["#3E454A", "#949A9F"],
        "text_color": ["#DCE4EE", "#DCE4EE"],
        "text_color_disabled": ["gray74", "gray60"]
    },
    "CTkLabel": {
        "corner_radius": 0,
        "fg_color": "transparent",
        "text_color": ["gray10", "#DCE4EE"]
    },
    "CTkEntry": {
        "corner_radius": 6,
        "border_width": 2,
        "fg_color": ["#F9F9FA", "#343638"],
        "border_color": ["#979DA2", "#565B5E"],
        "text_color": ["gray10", "#DCE4EE"],
        "placeholder_text_color": ["gray52", "gray62"]
    },
    "CTkCheckBox": {
        "corner_radius": 6,
        "border_width": 3,
        "fg_color": ["#D03434", "#A11D1D"],
        "border_color": ["#3E454A", "#949A9F"],
        "hover_color": ["#D03434", "#A11D1D"],
        "checkmark_color": ["#DCE4EE", "gray90"],
        "text_color": ["gray10", "#DCE4EE"],
        "text_color_disabled": ["gray60", "gray45"]
    },
    "CTkSwitch": {
        "corner_radius": 1000,
        "border_width": 3,
        "button_length": 0,
        "fg_color": ["#939BA2", "#4A4D50"],
        "progress_color": ["#D03434", "#A11D1D"],
        "button_color": ["gray36", "#D5D9DE"],
        "button_hover_color": ["gray20", "gray100"],
        "text_color": ["gray10", "#DCE4EE"],
        "text_color_disabled": ["gray60", "gray45"]
    },
    "CTkRadioButton": {
        "corner_radius": 1000,
        "border_width_checked": 6,
        "border_width_unchecked": 3,
        "fg_color": ["#D03434", "#A11D1D"],
        "border_color": ["#3E454A", "#949A9F"],
        "hover_color": ["#B22E2E", "#791414"],
        "text_color": ["gray10", "#DCE4EE"],
        "text_color_disabled": ["gray60", "gray45"]
    },
    "CTkProgressBar": {
        "corner_radius": 1000,
        "border_width": 0,
        "fg_color": ["#939BA2", "#4A4D50"],
        "progress_color": ["#D03434", "#A11D1D"],
        "border_color": ["gray", "gray"]
    },
    "CTkSlider": {
        "corner_radius": 1000,
        "button_corner_radius": 1000,
        "border_width": 6,
        "button_length": 0,
        "fg_color": ["#939BA2", "#4A4D50"],
        "progress_color": ["gray40", "#AAB0B5"],
        "button_color": ["#D03434", "#A11D1D"],
        "button_hover_color": ["#B22E2E", "#791414"]
    },
    "CTkOptionMenu": {
        "corner_radius": 6,
        "fg_color": ["#D03434", "#A11D1D"],
        "button_color": ["#B22E2E", "#791414"],
        "button_hover_color": ["#942525", "#661818"],
        "text_color": ["#DCE4EE", "#DCE4EE"],
        "text_color_disabled": ["gray74", "gray60"]
    },
    "CTkComboBox": {
        "corner_radius": 6,
        "border_width": 2,
        "fg_color": ["#F9F9FA", "#343638"],
        "border_color": ["#979DA2", "#565B5E"],
        "button_color": ["#979DA2", "#565B5E"],
        "button_hover_color": ["#6E7174", "#7A848D"],
        "text_color": ["gray10", "#DCE4EE"],
        "text_color_disabled": ["gray50", "gray45"]
    },
    "CTkScrollbar": {
        "corner_radius": 1000,
        "border_spacing": 4,
        "fg_color": "transparent",
        "button_color": ["gray55", "gray41"],
        "button_hover_color": ["gray40", "gray53"]
    },
    "CTkSegmentedButton": {
        "corner_radius": 6,
        "border_width": 2,
        "fg_color": ["#979DA2", "gray29"],
        "selected_color": ["#D03434", "#A11D1D"],
        "selected_hover_color": ["#B22E2E", "#791414"],
        "unselected_color": ["#979DA2", "gray29"],
        "unselected_hover_color": ["gray70", "gray41"],
        "text_color": ["#DCE4EE", "#DCE4EE"],
        "text_color_disabled": ["gray74", "gray60"]
    },
    "CTkTextbox": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["#F9F9FA", "#1D1E1E"],
        "border_color": ["#979DA2", "#565B5E"],
        "text_color": ["gray10", "#DCE4EE"],
        "scrollbar_button_color": ["gray55", "gray41"],
        "scrollbar_button_hover_color": ["gray40", "gray53"]
    },
    "CTkScrollableFrame": {
        "label_fg_color": ["gray78", "gray23"]
    },
    "DropdownMenu": {
        "fg_color": ["gray90", "gray20"],
        "hover_color": ["gray75", "gray28"],
        "text_color": ["gray10", "gray90"]
    },
    "CTkFont": {
        "macOS": {
        "family": "SF Display",
        "size": 13,
        "weight": "normal"
        },
        "Windows": {
        "family": "Roboto",
        "size": 13,
        "weight": "normal"
        },
        "Linux": {
        "family": "Roboto",
        "size": 13,
        "weight": "normal"
        }
    }
}


if not os.path.exists(themePath):
    with open(themePath, 'w') as tf:
        json.dump(defaultTheme, tf, indent=4)


def updateAgents():
    try:
        with open(configPath, 'r') as file:
            currentConfig = json.load(file)
        apiAgentsData = requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true")
        apiAgentsData = apiAgentsData.json()
        apiAgents = apiAgentsData['data']
        for agent in apiAgents:
            if agent['displayName'] not in currentConfig['agents'].keys():
                currentConfig['agents'][agent['displayName']] = agent['uuid']
                print(f"Added {agent['displayName']}")
        with open(configPath, 'w') as file:
            json.dump(currentConfig, file, indent=4)
        print("Finished Updating Agents")
    except Exception as e:
        print(e)
def updateMaps():
    try:
        with open(configPath, 'r') as file:
            currentConfig = json.load(file)
        apiMapsData = requests.get("https://valorant-api.com/v1/maps")
        apiMapsData = apiMapsData.json()
        apiMaps = apiMapsData['data']
        for map in apiMaps:
            if map['tacticalDescription'] == None:
                continue
            if map['displayName'] not in currentConfig['mapAgentSelect'].keys():
                currentConfig['mapAgentSelect'][map['displayName']] = "None"
                print(f"Added {map['displayName']}")
        if 'mapMode' not in currentConfig:
            currentConfig['mapMode'] = "Normal"
        if 'Scaling' not in currentConfig:
            currentConfig['Scaling'] = defaultConfig['Scaling']
        with open(configPath, 'w') as file:
            json.dump(currentConfig, file, indent=4)
        print("Finished Updating Maps")
    except Exception as e:
        print(e)
def AddedValues():
    try:
        with open(configPath, 'r') as file:
            currentConfig = json.load(file)
        if 'delay' not in currentConfig:
            currentConfig['delay'] = 4.0
        if 'skinsOrder' not in currentConfig:
            currentConfig['skinsOrder'] = defaultConfig['skinsOrder']
        if 'CheckForUpdates' not in currentConfig:
            currentConfig['CheckForUpdates'] = defaultConfig['CheckForUpdates']
        if 'Theme' not in currentConfig:
            currentConfig['Theme'] = "System"
        if 'instalockMode' not in currentConfig:
            currentConfig['instalockMode'] = "Lock"
        with open(configPath, 'w') as file:
            json.dump(currentConfig, file, indent=4)
        print("Finished Updating Values")
    except Exception as e:
        print(e)
# the img in base64 
def reIm():
    logo_in_base64 = """iVBORw0KGgoAAAANSUhEUgAAAYAAAAIACAYAAACLn7v6AAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAAGYktHRAD/AP8A/6C9p5MAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAHdElNRQfpCgEJEBRQWmKNAABQRUlEQVR42u3deZRlV30f+u9v73Onmqt6bg09aEQSYpIYBDhg49jGdmRD4gc48fOMV5Ll+DmOk6ws+wkbD/Ej8YCHDLz4ZeGE8GyeY8CYyRCMBRJmkDBonrrVUs9dc93p7P17f5x7q6tbLfXet/vUPXXu9wPV3aq6p868f3vvs/fvAERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERES0KWTYG0A0DLfevwyowCQpxHgABqqa/VABhYFJPbTqkDqHaifF6ngD0FlYB3RqHUwun0S1A7TqCXTDnWSdwvjsd3kjcFayvxODMWOArsClgtQKKtagIoBLgdQ5OFsBpIskSeFTAwAwEIgRqDMQOHgxEFEYeCgAlWzbq4mDiMGXrt827MNLW0Qy7A0gGobOv//nMLuvQusP/i2aSysQABUAJrGwB64F6g3oxDiM1CBG0LIWVgQKhxSAVcGKsfACmNRBoAAkCwQ26VWtBFAPOAfxCnEeC+oBn0LgYLyi5T2cWBjjYZyDpB2IVNBc7QLagtgKNO3Ct9aAlXm4xVUIgLT3hd52VwDYN/8A0sNPDPvQ0hbCFgCNpFv+058CxoyhXnur1BsHoNqF9124tKXNtTO6srSo7VYbaZpqt52im3pNOw7d1IlX1cQaqSRWTGKQ2Kyqvh4GoFCf/UsAhQhERKw1Yq2BGFERgbVWbGJEjFFjDEQMxAiMGBhjISIQY8QYC2sTJJWaJMkYjK3BmiogFgJARdFpndITxz7g2835B37+JwHhrU0XxxYAjST38P2Q3Ve+ovuR//HvtNvZAUChqvDewaUp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"""   
    return logo_in_base64
def settingsLogo():
    image = """iVBORw0KGgoAAAANSUhEUgAAALwAAAC3CAYAAACojjRoAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAACRNSURBVHhe7Z1bbBzXmee/c6sLq5tNik2TJh2KsiLKFLTLhPRi7CgrWDOAAxtQxkEGSAIIixjwPOQheTSSB2MM5CGCH2cCGIMloN1FgORhMHFGOyHieVAigONgYMmhR1BbnFXc5ogSGRXJbnYX63Ju+yCW3GpTZpPsbvalfgABquuQYp/691ff+c7lj7TWkLB/Vmdn3/AXF6f4ysqYCgJHhqFV3eYgENMMsGV5bHh4KXPu3Dv9L730s+o2CbWDEsHvnzsXL77t37w5w113RAaBrYUwkZQYGMNKCFLdfjcwpVJx/um/AZQmRCFKQ5JOF3pOnvwgEf3BSAS/T+5cvPj25nvvvagKhaxGyFSeZ1a3qSfItj2aShV6Tp/+fSL6/YOrX0jYndXZ2Te869fPqkIhC0rZjRY7AID2fUeUy31hPj8ZLS8f83O5meo2CbuTCH6PbMzNXShdv/5C5LrDknNLBgGrbtMoEEKMF4tZf3FxqvpaQm0kgt8Dfi434y0snIny+ZMQhjZwblS3aSQ8iqjyfYevrIwF+fxk9fWE3UkEvweCfH7Sv3lzRnleWgvRtMgeQ4TACGPKXXfEW1g4k6Q1eycRfI3E0Z0XiwNSCFMrRavbNAPueUx5Xtq/eXMmifJ7JxF8jQT5/GSwtDShgiCFlDq0fiMAWCNkJlF+fxzajWsn/FxuJlpePqbL5bTyfecw0plKkii/fxLB1wh33RHuuiNaykNJZSpJovz+SQRfI8HS0oTyvDTRes8zqI2AhyFTnpf2rl8/m0T52kkEXwOb8/MvS9cd1kKwSOuW6DMiBNYAliyXM8UrV15JonxttMTNa2U25uYu+IuLU7JcziitCRGiZfqMRxFVnpfmKytjm/PzL1dfT/gsLXPzWpF4sMpXVsaU56WbPdG0G0QILIUwebE4wF13ZGNu7kJ1m4RHSQS/C/FgVQrR8PUy+yKKTFkq9QVLSxOw/SGtbpLwKYngdyFYWpqQQWC3ymC1GgmgIAxt6brD0fLyMXty8lp1m2bh53IzlV/V11uBllse/LiOOowbuTo7+8bm1avn/Xz+lPB9m7RogMA9PRGyrELfuXP/OPCXfznbzL6K71ewvYqTu+4IAADLZu8ao6Mft9oy5pYS/Mbc3IXKTouJO88aH89Bk8S/MTd3wVtYOLP53nsvctcdhShqzZQGACSlyjCMsnn06K3sd77zt40WWbXI/cXFKVEu9+tyOa2CwAEAiHdp2RMTC0Ovvfbj6t9xWLSM4B+3VS7e4oZSqRJNpTbsiYmFWPyNEr6fy80E+fzk2uXLr/offfQlVSodqW7TamDHCUkms9z7/PPvNirKx/1SKXLpusOyXM7IILBRxaScJkQQy/JZNnvXPnXq2lM//OH3Hv1th0NLCL56qxwmxORBYAAAMMuKdBTJuANJKlUk2eyKNTa26ExNzVdGfT+Xm6nXjV6dnX1j7fLl70rXfZJHkdmq6UyMpFQx2y7Yzzzzh4Hz5y/VM8rHQvcWFs4ES0sTscgfrhqllPAoop8p2RpGSCgNcV+f23Py5Afjb731V49cPwQOXfD511//h61bt76sCoWsFMJ8XOogKVXMMAQIIcE0fZJOF1gmsxY/NgEAjNHRjwEADnqz/VxuZvXSpR+VFxb+O2xt9Tdzk8dBwIbhG6OjH/e9+OIves+c+fVBPvyVaYu3sHDGv3lzhheLA7JU6oMwtIFSwre26G6BAFHKgbGI9vevtoLoD1XwsdjFxsYQcG7UuihLUqqYaXKtlMC27WHLKrNMZg2lUiVrbGyRZbN3D3LDV2dn3yi8++63+erqU1EUpT4TuVqUePBqHT9+Y/T73399P++/Om3hKytj3HVHlOelNUImD0O21/5oJdEfmuD3K/ZKJIACSmEn8cfHWuw119+Ym7uwdvnyq8Ht26dlqdTXapNNn4ekVDGMQ5LN3ut9/vl395I375S28GIxq3zfQRjT/Qi9klYR/aEIvh5ir0ZSqogQ+GHe6DglkkoVnenpq9W5fvXPxrn/xtzcheKVK69s3bjxnCwWj6gosqvbtjrEsjhg7LOhoTvO9PTVeABbPb6pLP/ulLZghGzueYaSEu2WttRKK4i+6YJvhNirifN9BBBgxymxbPZunOtXV3ji6fj4Eb5148ZzolzugzA0hVK4Xje7WUhKFUFIEMaCeLAYv2/YHt9Uln/F+vpgPdKWWjls0TdV8PFZLo0UeyUSQDHHeZjusEzGrazwxDc9WFqaiJaXx2Wp1KeFMCEMD20LX72IhRUf4mSMjuatsbFFsb4+CADAV1bG4miuhTDrkbbUymGKvmmCv3Px4tve9etn+erqUyqK7EaLvRIJoDAhmjlOpLT2STpdgO0avwxDK648IIxpJERLrYg8CJJSZVAqtVICTNNHjAkAAM05RVJSKYRJMMZREJBmP8kOS/RNEXyl2CXn1mEOBGMRSCk/feOcGxJANfumN4v4vSGEZPyaboG1QYch+oYLvpXEXklc4emUaF4rDwf3LQKxLK4QaproGyr4SrFrAKuWiYqE7qOZkb5hgq+cQdUAltraaonIntCaNCvSNyTaPlJ6VMpOxJ6wGzIIGNbaEBsbQ1u3bn35zsWLb1e3qQd1F/ydixffDvP5SbGxMYS1NtplHUrC4ROLXhUKWf/mzZnV2dk3qtsclLoKfnV29o1gaWmCF4tZhBBLxJ6wV2QQsPjMHX9xcare+3TrJviNubkL3HVHpOsOQxAkOXvCvlGeZ8ogsPnKyli9z8Kvi+DjP0isrw/KMLTk1lZvdZuEhL2ACTFVEDjVu98OSl0E/8iCLM5NASAeaZCQsA/qbRAH9RI8AEC8GhEAAAGgR68mJOwNGYZATDOofv2g1E3wAAD0yJH7D76hjSnuJ3QNGCGJLctj2ezd6msHoa6CBwAgqVTR7On51HsxIWGPSEqVJkSgVKpkjI5+vNMehv1SV8GzbPYutixPC5EIPmHfMMMQxLJ8mkptVKbK9aBugrcnJ68Zo6Mfo1SqpAkREkBVt0lIqAkhJEmlivHm/HpSN8HD9sCVplIbxLJ81tOTVGoS9oykVIFp+iSbXal3OgP1FjwAgD0xsUBSqSII8XDtdUJCrTDT5CSdLlhjY4v1Tmeg3oKP0xqSza6AafqS0iStSagZCaC0UoJlMmvO1NR8vaM71FvwsJ3WWGNjiySdLjDTTAavCTWDCdHYtj02PLzUiOgOjRC8PTl5zZmammeZzBrSOkyifEKtMMeJWCbjNmKwGlN3wcN2lLdPnbqGHaeURPmEWpCUKqV1wwarMQ0R/MMon83eRVqHSYkyYTcaPViNaYjgoTrKO04S5RMeSzMGqzENE3xllNdKJRNRCY+F9fQ8OCirgYPVmIYJHrajPBseXkKUhoZlJXX5hJ0RQjZ6sBrTUMHD9gpKkk4XpFJJhE/4DI2eWa2m4YJn2exdlsmsEUrD6msJCc0arMY0VPDxzCsbHl7CjlMCxqLqNgndi6RUIa3DZgxWYxoqeNg+njleX4Mo5clEVEIMM02OHadknzp1rRnRHZoheACA3jNnfm2Oj+ewbXvMMJJVlAmfliKz2bvNiu7QLMHbk5PXMufOvcMyGRcBBEmUT2hmKbKSpggetkuUzvT01WS5QQJAc0uRlTRN8JUTUcC56oaJKAmgJKVqe4+m1IwJMM1HvjRjQhMi43Zd0S/bT/hmlSIraZrgYTvKo1SqBAAAtK0dZXYkFjh2nBDZtsfS6YLR2+ta/f33jKGhT4zBwSU2MPDIlzE4uGQMDX1i9fffM3p7XZZOF5Bte9hxwk7/AOhyOd3MdAYaeVz2TmzMzV1wf/7zHwS3b5/mSpmtdDD/QZDbJmpaax57KsW+sTSV2nh4fMkuiPX1QVEu9+tyOf2I/xJCbEen6zZFUqoIxtwaHb3d9+KLvxh67bUfV7dpFE0TvJ/Lzaz96levbb733ouyWBxVnrej43a7ER/mH5ummePjOXrkyH2Wzd6NHQOrf+bziE2BY4e9MJ+fjP1Sm2EE1zQYi1hf3/2e06d/nzl37p2DuqfXStMEHxv++h999CXu+33tHq0QxgJRysE0fZJOF3pOnvwgNkKO2+w3N632UC1eufLK1q1bX47N17QQrN1dBgEASE/Ppnn06K3es2cvH8Q5fS80RfB+LjezOT//8trly9+VrvtkOxr+xmBCpMJYEsYC7DglY3z8Vnp6+reNvGFx/5WuX38hyudPKs9LS84trBRRUh66Odm+MYyQZTJu79mzl2MD5eom9Ya8+eab1a/VDT+Xm2GDg/fK77//Fxv//M//g7vuCNLa1kK05U2KozpOpzfZwMBK+rnn/iVz9uw/Zb/1rZ+ywcF71e3rBRscvJeanr6KMFbYsnxZKvVrrTEIQUFrBFq35dOSYAxaSqw5N4wvfOGPIARrZD9CIyN8pcN16fr1F4Lbt0/Lcjkjo4i1pbEZY1FlVB84f/6SVeHo3Sz8XG4myOcn1y5ffrUy2reKO+JekACKGAYnqVTRHBr6pPfs2cuV455G9G3dBR8/fqsdriEMbZDSaLdHMCZEKkIENk3PyGZXnOnpq816/H4ecRHAu379bOS6wyoMHSwlbef+jR3DaSq1YU9MLMTitycnr/m53Ew9+rwugo8HWfEAq9LWvJ0drjEhEgiJUCpViiNQM0totbA6O/vG5tWr58PV1aO6XE63Y1CRAMqwLKmVepAyOk6JpFJFks2uWGNji3HFC7YXI1b//F7Yl+DjT1v8eI2Wl4/5i4tTYT4/KcvljPK8tBTChCgyYxfo6t/R6lSK3Tp+/MbA+fOXDtrZjSKugAW3b59uV9HHxHMaIIQE0/SJZfnV4u89c+bXsM+UZ8+Cr8zN47RFuu5wXCvumEkSwwhJKlVsdbHHVIpelssZiKK2n+f4jPgrJvTS09O/rUx5qn/2cdQs+OrcXLrusCyXMzIIbAhDGyglHeO0vS12c2jok+x3vvO3rS72mHgmO1xdPdopood4cAuAwTBCRIjAtu1hyyobo6N5a2xs0Zmamq9V+LsKPk5bdsrNgVLSEdF8GwmgKKUS2XbJeuqp2+0k9piHyzfu3DmufT8thCAdEYS2qcz3K6O+ferUtVqEv6PgKweh3sLCGe/69bOdkpt/HpX25wPnz/+vVhug1srq7Owba5cvf1dsbAxhIUzJedvPyu6EpFQx0+RI6xA7Tolls3crhQ875PmfEXycuviLi1N8ZWWMu+6I8ry0BrA6KZrvBLJtj/b3r/acPPnB0Kuv/qS6s9oFP5ebWb106UdbN248J4vFI+08s10LOwmfDQ8vxaXNyqf0IzOtD2u777//gn/79n/lrjuqhUjxKLJRGFKsVEe680kAhQ0jYr296z2nTr3fzmKH7ZlZLYQR/elPX5Ce16eFYKBUW1ZtagErhTTnVHDOEEIW39gY4GtrT/Ll5adFoZDVQhj2iRMfQqXg46hQ/sMfvipWV8e0lI6IIhOFIetUocdQQhQwFpkjI388cv78/04///xvqtu0G/aJEx/ye/eO8uXlp+XWVhprTXSbLkGoFQyANOdUCkExQoYol9OyUMiqra1ULHry5ptvPvIIFJubWeX7ac15x0b0ajSlgjhOyf7iF/+979y5XzZ6PUezILbtBfn8M3xt7UnFudnJUb6SbeETEMLQWhPpeWn1YG+BgQEANufnXw7z+UnNeZ/w/Y7O93aCMBYcxv7KRmNXbJ4njHXl5nnt+44slfr4yspYtLx8DG/MzV3wFxenZLmcCQsFq9MqL7vCWIQdp2SOj+eavb+yGSSb5wEwIaYKAoe77giOlpeP8ZWVMWDMJgBd8ciLkQAKI/TQIrHdau61YCenOAMPAkOGoQUAgLnrjqggcMJCIVXdsNMxLOvBlHU2uxKvz+hErIpTnDtx8/yuSPlwLIoBAGQYWqhLBqiVaKUESacL6enp31Zf6zTiU5y7Na2J+TRfr/gUdAMSQCFKuTE6mu/E3L2a+BRnrVRXH3XYXQPUSigFsKyAplIbez1ZoN2wt09xRqlUCVHa1c6K3Sv4B6N3XuuZMe2ONT6eo6nUBmIsifDdCNZaA2NdZdJAjxy5jwlJcvhuBFH62WWi3QBjIUGoO997Nwu+q8E4EXxC94Ap7VpHxUTwXYji3ZvGJ4LvQjDrjPNYa6Zik1Mi+C5EtelRh/sGfTqn2rWC193sk9yFy0hiulbwXXvTOTel1t353rtZ8AohBJx3xLkttSLW1weVlF2WwCc5/EOUlEysrw9Wv96JBPn8pCiX+3WHHtnxuSQ5PAAIARAEliiX+4N8frL6cifh53Iz0fLyMV0up7UQHeOttR+69o0TAIwoZdJ1h6Pl5WPx4VOdCnfdEV4sDiCMuy/CE/Iwp+lawQMAcM8zeLGY9RcXp6qvdRpifX1Qlkp9PAy7LoeXAJqYZgCPCL7iU9AtKCmR8n2Hr6yMdXJaE+Tzk2E+P6mFMEF03+pgs7c3wJblsWz2LgYAIKYZMMuKqht2OgQAI4wpd90Rb2HhTCemNX4uN1O8cuUVXixmEULtaTd0AASAAiEClEqVjNHRjzHLZu9iy/KUlF21NjyGhyFTnpf2rl8/24lRfnN+/uWtW7e+rHzf4VHUdfm71dsbYssqW2Nji9b4eA4bo6Mfs+HhJZJOF7Bh+NU/0OkQIbDk3OLFYrZ45cornRTlN+bmLpSuX39Blkp9wLnRddUZwwg1pSVjdDTvTE3N25OT18jFn/3sQy2EEd27d0x6Xh+SEmPGoF2tJfcDRgi2bSAZMowwNT19tbpNu+HncjPF3/3ula2bN2d0qdSvu2iSDVHKMaURTqU2zaGhT7Lf/Obfx2cOkTfffBPsEyc+RBgrfv/+qJaSKiEwAgBkmlpwjjBAR09Fa60xbItehWEPwljFp822K+X33/+LzStXvsFdd0Rzbnf6uZKxPQ7COEKW5ZH+ftc8enSxUuxQeXpwLHrMGEeMcUypUFJiBIDwA+Hjjha+UgRJiXUQOGprK2U+9dTtdj1U1c/lZtZ++cu/DvP5Sel5fe3o4boXEKWcYMzBMDzS3+9aTz/9kXP69L9lzp79p+rT5B45H94+ceJDNjCwYgwN3WFPPLGMGQsxpZHmnGAAhBhDQmvUqacKY4yRFIJJz0sT2/baNbVZ/9WvXtv81399SWxuZolSTCvVUbm7BFAYAAFjETLNAKdSm6S3d916+umP+l544Z30s89e6X3uuXd3Ovb8Mw4gMd1oe5N4PLU2klJlULqjn2t6evq3tdhZPlbwlexkbKaCIKV830EYUx6GDISATunYxMWvdah08COUhmBZQezgR1OpDXrkyH1namq+1ntUk+BjYv+n2LpSl8vpR8TfKR6tkPi0HjaP82it9G6C7QOmPi+iV7MnwcdUmhMDAHSaCzdAezlx+7nczPLf/d1b7e7ELQEUJkQzx4mU1o914Y5d4Pci9Jh9CR62Ozn+j2E713+Y8rjuSGxYrLQmwLnRjuKvFL05NPRJ79mzl1vNyjKO7FE+f1IWi0faUexxNNdac2zbHstk3EqRx9G8HgFn34LficqUx795c0YFgcOLxSwEgSU5t5DWVLdZuoMJkYoQgU3TM7LZFWd6+upTP/zh96rbHQars7NvbF69ej5cXT2qy+U00pq1mydrZVBhmYxrjo/n4pQlTlf2G813oq6Cj4lTHm9h4QwAgHf9+tnIdYdVEKQk5+1pT89YRBgLcF+fe9g+rn5sLxr3axg67ZizSwBFDINXjpUeZyhcLx6pw9cL+8SJD0EINvCNb/xPWSr1syeeWOb37o1r3+8hALQt68JKEdAaqyiyZaGQ3VpcnEYYKxCCNWuCys/lZsrvv/8Xa7/85V+X//CHr8q1tWHQukcI0ZbWoowxiRkLzNHR2/GMKBscvNfI/myI4GHbHBdiv9DV1THAWEf37o2LMLRByrZ67D5EKUIQwioMTel5fUEuNyM2NwdkqdTfSOHHQi/+7nevFObmLgSffDIpS6V+pLWlfN9oR7HDA7tQTtPpQurZZ3/b+9xz7zaq/yppmOAfQQgm1taGxf37I6pU6mvnhUxaKSwQIlhrQ3leT3Tv3nj4xz+e4uvrT8bCF647Ilx3ZL830M/lZuLfEQt988qVb/i53LNyY2NQC5ESnJvQ5st9iWluGSMj+Z7JyWvm2Nh/7Le/9kJDcvid2Jibu1C8cuWVrRs3nuOFwmAnrO+QlCpmmhxpHWLHKbFs9i4bHl6iR47cj6sLe3UXCfL5yWh5+Rh33RGxvj4YV72U56U1QiYPQ9YR8xyMRayv737P6dO/z5w79049KjC10DTBw3ZVofDuu98O7tz5YtsOXncgFv72lHcYT5KgVKoUzwZW/8xOiPX1QVEu98cTevKBe7QZz2Z3hNC3+4tgzK3R0dt9L774i2aWepsqeD+Xm1n6m7/5P8Hy8nGpVMfcwBgJoIBSqBQ/YkxgQviubiOcm0pKpjmnlSLvqCUb28SC7zl+/MOnfvSj7zWqIrMTTe3Izfn5l7FledWvdwoEABMhsPI8U/u+w0ulvmhzMxtsbDwZra4eje7fH+Nra498Rffvj0Wrq0eDjY0no83NLC+V+rTvO8rzTCIE7jSxA2yfCbRNs7dVNq0zN+bmLsRno8D21rrqNp1G/AEgQmAkJUGcUwjDR74Q5xRJSeJ2HSnwKggAxozBYWyeb0rnPlx+sLQ0IUulvnacJEmoL4e1eb4pgrcnJ69Fy8vHpOsOQxjaEqCLz6pOgO0nvAZo+ub5pgjez+VmttOZLFDaMRsSEg4GjyKqfN8J8/nJzfn5l6uvN4KmCC/I5ye969fPQhBYfGurrSdLEuoHEQJrIZgslzP+4uJUvAarkTRc8P72yVeyXM5oACuJ7gmPwLmhPC/NV1bGmnGobcPFtzk//zJfWRlTnpfuxpOvEnZHCmHyYnGAu+5I9bV601DBV5YiZZefS57weAjGWJZKfc0wp2iYAJNSZEKtREFAtBBmM05xbpjgk1JkQq2QJp7i3DDBx6VIWS5nklJkwm5wz2PK89L+zZszjYzyDRNhkM9PBktLEzII7KQUmbAbBABrhMxGR/mGCN7fNtGSrjuMEbKT6J5QC/Fyg0ZG+YYJ0V9cnOLFYpZ7Xttv9EhoDkSIB1G+WBxoVJRviOCDfH6Sr6yMKd93lJRtud8y4XDgYchkqdQXLC1NNCLK113wfi434y0snIktEpN0JmEvECEwhKHdKDvRuovx4WC1Sy0SE+oApSReX1N96aDUVfCVg1UIQzuZWU3YD3xri8ogsBvhkl53QfqLi1Nx7b36WkJCLRAAjGyb6nI5Xe+0pq6CD/L5SVEu98sgsJOFYgkHIdzctFQQOPVeUFY3wcfpjC6X00jKzjgjPuHQ0EohGYZW9esHpa6i5K47ooLAQYaRpDMJBwJFUUPK2XUVPACADEMriqKkOpNwIBRCDTkwqe6CJ6YZGIbBq19PSNgLGmNNTDOofv2g1FXwLJu9iy3LU1J+/ilbCQm7kBoaKmPL8lg2e7f62kGom+Dtyclrxujox2x4eIlYlo8dJxF9wr7AjhMC5z4bHl4yRkc/rudRfHUTPGx78NgTEwssm72LtA6JZSWpTcKeIJbFkdYhy2bv2hMTC/U+VbiuggcAGHrttR/bp05dw319rkIoSkSfUCvEsrhCKMJ9fa596tS1Rpwq3LDTg/Ovv/4PW7dufVlsbAxhrQ0ZBEnlJuGxxGKn/f2rPSdPfjD+1lt/Vd2mHtQ9wseMv/XWX/WcPPkB7e9fTSJ9wueBKG2K2KGRgoc2EL2ktOs2lktKVSttqEeUcmCsKWKHRqY0lcTpjSoUshrAUltbh74LCiEk4++11qQdjZNr5eF7YyyKXyOEoEgIcphLQHBPT4QAHlqBNlrs0CzBAwDcuXjx7dhXFJRyRKlkYty8vpYAyrAsKZVShNJQEyIQYwIAQD84t91GGNPDFkE9kZQqg1KplRJgmj5JpwvENIN4jYoslfowQjb3PENJiZr1gVdKAU2nQ8C46WbPTRM8VDlHIyHSUaFgN1r0j/NfYsPDSwAA9MiR+8HS0kS0vDweeyoB54YWoq0H2QhjAaYZxu/ZGB3NV1q5ewsLZ4KlpQnpusO8WMwq33cQxpR7Hmuk8JVSYPT1+ZrSkjk09Env2bOXG1GNeRxNFTxsH7+3dvnyq8Ht26eREOlwc9NsRAdLShUzDIEAgsc57PW/9NLP4hNro+XlY/7i4lSceknOLal12636lACKYqzANEOaShV6Tp/+fWzlDttzJbC9ujV2DPQXF6ea4RaolALjyBEPMVYwxsdvDZw/f6nedfbdaLrgoUr0slzO1OsYvoe5qmGEhNIQO06JpFJFZ3r6qjM1NV9pIVk5e+fncjP25OQ1v8LSna+uPgVK2e1YTsWG4ZNMZr3SEjJ+j9VtHx6JmM9PegsLZ/ybN2diB8F6pnkSQJm9vSEyzfWe06d/P/Tqqz/Z6e9pNIcieNgWvfvzn/8guHPnuAqC1EF8W3fKVeO0JXPu3DvW+HhuL5175+LFtzffe+9F6bpP8ihqyBOoYTAWkXS6YB0/fmOvETSO+nG6E6d5EIa20poc5B6BYYQklSpax4/fGP3+91/fy/2oJ81x4t4B+8SJD8Xa2jC/d29c+34PaI1BqZrX0UsAhQEQGEbIGPPBtsukt3fdevrpj5zTp/+tZ3Ly2sDXv34p/fzzv9mrwzMbGFjZyuX+mygUshRjpoWo+e86TLbTuC02MLCS+epX/2/2W9/6aXWbz4MNDt6zT5z4kA0MrBhDQ3fMJ5/8RHFuYUoFwlgiANAIAWFMCwBUs+U9YxG2LM8aGfk4+81v/n36+ed/U92kWRya4AEAUtPTV4Pbt/9L5LpPqiiyEQDaTfSSUkUtixOEOOrpKdH+/vvG0NB/2l/84r/3fuUrv0k/++wVY3j4P7Pf+tZP9yr0GOG6I3xl5Sj/059GheelQcq22K7IDEOAbZd7nnnm2sDXv35pv+8/Fj6xba/3z/7sX5BhhIgQgSgVQIjQCCmitUIIKWSaWmj9ePEzFhHGAuOJJ+5m/vzP/3GvH8J6c6iCBwDo/epX/9n74IOz0vPSwLmhEYJqgcUiRw8mr8qkp6fIstkVY2zs/1VG876vfe0XIAQ7aAQRrjsi1taGxerqF1Sp1Kc5r8sYo5FIAIUx5qS3d733K1/5Td/XvvaL6jZ7hQ0O3mODg/dS09NXtRAGPXLkT2xg4E80k3FxX98GplQAgEQISSBE0Z4eKZVCgLFCSmHS07OJHafMBgZWnOnpqyM/+MHr1f9Hszm0HL6aOxcvvu3fvPngxOEgsFGF6DUhgliWT1KpIslmVyrLa1BReagnG3NzF4pXrryydePGc7xQGDxQ/tokcDq9bj/zzB8Gzp+/tNdxSy1Unh5QWeER5XK/LpfTvFgcgDg4MBYS0wzi+9WsOvtutIzgYbtOH5fIVBA4AADYsjyUSpVoKrURl9fim/m4ykO9WJ2dfaPw7rvfDldWjgrfb+1DYQ0jZNnscu/zz7/rTE3NNyIIVFNZ4YmWl49x1x2pdPGIS8DNrLPvRksJHrYja9x5sL2LKhY5VJUTG42fy82sXrr0o9L7759DnKdbtUQpKVWGYZTNo0dvNXsiJ6Y6+sffN+ODtxdaTvBQ1XnQZJFXszo7+8ba5cvfbeUSJe7piYjj3D/M+nY1jX767peWFHyrENel1y5fftX/6KMvqVLpSHWbw0YCKGrbvjk8/MkTr776k1aLqK1Gy0WrViKOUNbY2CJJpwtgGC23TxcTorFte+b4eK5yJjlhZxLB70L/Sy/9jGWzd1kms0YoDVttDT1znIhlMq49MbFQfS3hsySCr4HeM2d+zYaHl7DjlJhhiOrrh4WkVGkhOMlmV+q9u79TSQRfA/bk5LXMuXPvkFSqiACCVtkxZFAqwbICmkptJOlMbSSCrxFrfDznTE9fxY5TYo7TElsVpVIKW1aZHjlyv/paws4kgq8Re3LymjM1NR+fudMKUR4RIlgms1bv07k6mUTwe8AaH8/Zp05da4Uojyjl2LY9lEqVkvy9dhLB74FWivIaY4Utq2yNjS0m+XvtJILfI60Q5RHGglAaskxmzZmamk+ie+0kgt8jlVFeKyUOI8ojSjl2nJJ96tS1JLrvjUTw+8AaH8+x4eElbNse6+lpbl2esQhM0zfGx28l0X3vJILfJ/bExALLZFytddPSGmJZnDAWGNnsSnp6+rfJupm9kwh+H9jbZ+Gb4+M5mkoVkG171W3qDXacEDD2cV+f60xPXz2MJcCdQLJa8gA83BV169aX40OckJQYGMNqHxu/MaVS8U8fGBhAaUIUojQkluWzbPauferUtVbZPdSOJII/ILHo411a9bZaJKYZYMvy2PDwkj0xsZBE9oPx/wEaT3CwsILLMAAAAABJRU5ErkJggg=="""
    image_data = base64.b64decode(image)
    image = Image.open(BytesIO(image_data))
    return image
settingsImage = settingsLogo()
# call config files
updateAgents()
updateMaps()
AddedValues()
# convert from base64 to an ico file
def download_image(base64img):
    procc = base64.b64decode(base64img)
    image = Image.open(BytesIO(procc))
    iconPathExist = os.path.exists(iconPath)
    if not iconPathExist:
        image.save(iconPath)
        return iconPath
    else:
        return iconPath
image = download_image(reIm())

agents = {}
running = False
white_text = "#DCE4EE"
red_text = "#ff0f0f"
blue_text = "#00FFFF"
yellow_text = "#e8ec97"
defenderColor = (0, 255, 255, 1)
attackerColor = (255, 15, 15, 0)
startTheGame = "Start/Restart Valorant First!!!"
try:
    with open(configPath, 'r') as f:
        config = json.load(f)
        ranBefore = config['ran']
        agents = config['agents']
        region = config['region']
        regions = config['regions']
        selectedAgent = config['agent']
        currentMode = config['mapMode']
        existingMaps = config['mapAgentSelect']
        sliderValue = config['delay']
        allowedUpdates = config['CheckForUpdates']
        Scaling = config['Scaling']
        Theme = config['Theme']
        instalockMode = config['instalockMode']
except KeyError as e:
    print(e)
    with open(configPath, 'w') as file:
        json.dump(defaultConfig, file, indent=4)
    with open(configPath, 'r') as f:
        config = json.load(f)
        ranBefore = config['ran']
        agents = config['agents']
        region = config['region']
        regions = config['regions']
        selectedAgent = config['agent']
        currentMode = config['mapMode']
        existingMaps = config['mapAgentSelect']
        sliderValue = config['delay']
        allowedUpdates = config['CheckForUpdates']
        Scaling = config['Scaling']
        Theme = config['Theme']
        instalockMode['instalockMode']

# app colors
customtkinter.set_appearance_mode(Theme)
customtkinter.set_default_color_theme(themePath)
customtkinter.FontManager.default_font_family = "Helvetica"
customtkinter.FontManager.default_font_size = 12 
customtkinter.FontManager.default_font_weight = "bold"
customtkinter.set_window_scaling(Scaling / 100)
customtkinter.set_widget_scaling(Scaling / 100)

# app options
app = customtkinter.CTk()
app.title("Valorant Tool")
app.geometry("900x600")
app.resizable(False, False)
app.iconbitmap(image)

# Top image
img = customtkinter.CTkImage(light_image=Image.open(image), dark_image=Image.open(image), size=(170,170))
imgLabel = customtkinter.CTkLabel(app, text="", image=img)
imgLabel.place(relx= 0.42, rely= 0.09)
def findKeysByValue(ob, value):
    value_lower = value.lower()
    keys = [key for key, val in ob.items() if isinstance(val, str) and val.lower() == value_lower]
    return keys

# settings menu
def settingsMenu():
    with open(configPath, 'r') as file:
        config = json.load(file)
    settingsWindow = customtkinter.CTkToplevel(app)
    settingsWindow.title("Settings")
    settingsWindow.geometry("500x300")
    settingsWindow.resizable(0, 0)
    settingsWindow.after(250, lambda: settingsWindow.iconbitmap(image))
    settingsWindow.after(250, settingsWindow.focus_force)
    settFrame = customtkinter.CTkScrollableFrame(settingsWindow, height=245, width=480)
    settFrame.pack_propagate(True)
    settFrame.pack(padx=10, pady=8)
    settDoneButton = customtkinter.CTkButton(settingsWindow, text="Done", command=settingsWindow.destroy)
    settDoneButton.pack(padx=10, pady=3)
    themeButtonsText = customtkinter.CTkLabel(settFrame, text=f"Theme({config['Theme']}):")
    themeButtonsText.pack(pady=7)
    def changeThemeFunc(v):
        customtkinter.set_appearance_mode(v)
        config['Theme'] = v
        with open(configPath, 'w') as file:
            json.dump(config, file, indent=4)
    difThemeButton = customtkinter.CTkSegmentedButton(settFrame, command=changeThemeFunc, values=["System", "Light", "Dark"])
    difThemeButton.pack(pady=7)
    difThemeButton.set(config['Theme'])
            
    scaleButtonsText = customtkinter.CTkLabel(settFrame, text=f"Scale({config['Scaling']}):")
    scaleButtonsText.pack(pady=7)
    def changeScaleButton(v):
        v = int(v)
        scaleButtonsText.configure(text=f"Scale({v}):")
        if (config['Scaling'] == v): 
            return
        config['Scaling'] = v
        customtkinter.set_window_scaling(v / 100)
        customtkinter.set_widget_scaling(v / 100)
        with open(configPath, 'w') as file:
            json.dump(config, file, indent=4)
    scaleButton = customtkinter.CTkSegmentedButton(settFrame, width=30, height=20, values=["50", "75", "100", "125", "150"], command= changeScaleButton)
    scaleButton.pack(pady=7)
    scaleButton.set(str(config['Scaling']))
    
    regionSettChange = customtkinter.CTkLabel(settFrame, text="Region:")
    regionSettChange.pack(pady=7)
    def changeRegionSett(v):
        if (config['region'] == v): 
            return
        config['region'] = regions[v]
        comboboxRegion.set(v)
        print(f'Changed Region to {v}')
        with open(configPath, 'w') as file:
            json.dump(config, file, indent=4)
        showRegionSelect(relogin=True)
    regionSelectorSett = customtkinter.CTkSegmentedButton(settFrame, width=30, height=20, values=list(regions.keys()), command= changeRegionSett)
    regionSelectorSett.pack(pady=7)
    with open(configPath, 'r') as f:
        newR = json.load(f)
        region = newR['region']
    regionSelectorSett.set(str(findKeysByValue(regions, region)[0]))
    
    instalockSettLabel = customtkinter.CTkLabel(settFrame, text="Instalock Mode:")
    instalockSettLabel.pack(pady=7)
    def changeLockModeSett(v):
        if (config['instalockMode'] == v): 
            return
        config['instalockMode'] = v
        print(f'Changed Instalock Mode to {v}')
        with open(configPath, 'w') as file:
            json.dump(config, file, indent=4)
    lockSelectorSett = customtkinter.CTkSegmentedButton(settFrame, values=["Lock", "Hover"], command= changeLockModeSett)
    lockSelectorSett.pack(pady=7)
    with open(configPath, 'r') as f:
        newR = json.load(f)
        instalockMode = newR['instalockMode']
    lockSelectorSett.set(instalockMode)
      
settImg = customtkinter.CTkImage(light_image=settingsImage, dark_image=settingsImage, size=(20,20))
settingsButton = customtkinter.CTkButton(app, text="", image=settImg, width=22, fg_color="transparent", command=settingsMenu)
settingsButton.place(rely=0, relx=0.96)

    

def showSelected():
    util_frame.pack(padx=20, pady=20)
    util_frame.place(relx=0.015, rely =0.45)
    
    agent_frame.pack(padx=20, pady=20)
    agent_frame.place(relx=0.51, rely =0.42)
    
    start_frame.pack(padx=20, pady=20)
    start_frame.place(relx=0.08, rely =0.7)
    
    region_frame.pack_forget()
    region_frame.place_forget()    
def selectRegion():
    newRegion = str(comboboxRegion.get())
    newRegion = regions[newRegion]
    with open(configPath, 'w') as f:
        config['region'] = newRegion
        config['ran'] = True
        json.dump(config, f, indent=4)
    with open(configPath, 'r') as f:
        newR = json.load(f)
        region = newR['region']
    global client
    client = Client(region=newRegion)
    try:
        client.activate()
        print(f"logged in with region: {newRegion}")
    except Exception as e:
        labelRegionStats.configure(text=startTheGame, text_color=red_text)
        print(f'{e}')
        return
    showSelected()
def showRegionSelect(fail = False, relogin = False):
    print('Back to region select')
    util_frame.pack_forget()
    util_frame.place_forget()
    
    agent_frame.pack_forget()
    agent_frame.place_forget()
    
    start_frame.pack_forget()
    start_frame.place_forget()
    
    region_frame.pack(padx=20, pady=20)
    region_frame.place(relx=0.03, rely=0.5)
    if fail == True or relogin == True:
        buttonRegion.configure(region_frame, text="Retry", command=selectRegion)
        labelRegionStats.place(relx=0.507,rely=0.28)
        if relogin == True:
            buttonRegion.configure(region_frame, text="Relogin", command=selectRegion)
            labelRegionStats.configure(text="Please press Relogin to confirm the region", text_color=white_text)
            labelRegionStats.place(relx=0.507,rely=0.28)
        buttonRegion.place(relx=0.424,rely=0.38)
        comboboxRegion.pack_forget()
        comboboxRegion.place_forget()
        labelRegion.pack_forget()
        labelRegion.place_forget()
    else:
        comboboxRegion.place(relx=0.424,rely=0.359)
        comboboxRegion.set(value=findKeysByValue(regions, region)[0])
        buttonRegion.configure(region_frame, text="Select", command=selectRegion)
        buttonRegion.place(relx=0.424,rely=0.5)
region_frame = customtkinter.CTkFrame(app, 848, 280)
region_frame.pack_propagate(False)
comboboxRegion = customtkinter.CTkComboBox(region_frame, values=list(regions.keys()), state="readonly")
comboboxRegion.place(relx=0.424,rely=0.359)
comboboxRegion.set(value=findKeysByValue(regions, region)[0])
buttonRegion = customtkinter.CTkButton(region_frame, text="Select", command=selectRegion)
buttonRegion.place(relx=0.424,rely=0.5)
labelRegion = customtkinter.CTkLabel(region_frame, text="Please Select Your Region:")
labelRegion.place(relx=0.42,rely=0.2)
labelRegionStats = customtkinter.CTkLabel(region_frame, text="Make Sure That Valorant Is Running", text_color=white_text)
labelRegionStats.place(relx=0.507,rely=0.69, anchor= customtkinter.CENTER)
    
# region select frame and options

util_frame = customtkinter.CTkFrame(master=app,width=435 ,height=120, corner_radius=20)
buttonGetNames = customtkinter.CTkButton(master=util_frame, text="Get Hidden Names", state="disabled", width= 85)
buttonGetNames.place(relx=0.38, rely=0.69, anchor= customtkinter.CENTER)
boolVar = customtkinter.BooleanVar(value=False)
buttonGetNamesSwitch = customtkinter.CTkCheckBox(master=util_frame, text="Tracker Mode", state="normal", variable=boolVar, onvalue=True, offvalue=False)
buttonGetNamesSwitch.place(relx=0.68, rely=0.69, anchor= customtkinter.CENTER)
buttonGetNamesWithStats = customtkinter.CTkButton(master=util_frame, text="Get Stats With Names", state="disabled", width= 85)
buttonGetNamesWithStats.place(relx=0.38, rely=0.36, anchor= customtkinter.CENTER)
buttonGetLoadouts = customtkinter.CTkButton(master=util_frame, text="Get Loadouts", state="disabled", width= 85)
buttonGetLoadouts.place(relx=0.68, rely=0.36, anchor= customtkinter.CENTER)
'''
Advanced Scrollable Dropdown class for customtkinter widgets
Author: Akash Bora
'''
class CTkScrollableDropdown(customtkinter.CTkToplevel):
    
    def __init__(self, attach, x=None, y=None, button_color=None, height: int = 200, width: int = None,
                 fg_color=None, button_height: int = 20, justify="center", scrollbar_button_color=None,
                 scrollbar=True, scrollbar_button_hover_color=None, frame_border_width=2, values=[],
                 command=None, image_values=[], alpha: float = 0.97, frame_corner_radius=20, double_click=False,
                 resize=True, frame_border_color=None, text_color=None, autocomplete=False, 
                 hover_color=None, **button_kwargs):
        
        super().__init__(master=attach.winfo_toplevel(), takefocus=1)
        
        self.focus()
        self.lift()
        self.alpha = alpha
        self.attach = attach
        self.corner = frame_corner_radius
        self.padding = 0
        self.focus_something = False
        self.disable = True
        self.update()
        
        if sys.platform.startswith("win"):
            self.after(100, lambda: self.overrideredirect(True))
            self.transparent_color = self._apply_appearance_mode(self._fg_color)
            self.attributes("-transparentcolor", self.transparent_color)
        elif sys.platform.startswith("darwin"):
            self.overrideredirect(True)
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
            self.focus_something = True
        else:
            self.overrideredirect(True)
            self.transparent_color = '#000001'
            self.corner = 0
            self.padding = 18
            self.withdraw()

        self.hide = True
        self.attach.bind('<Configure>', lambda e: self._withdraw() if not self.disable else None, add="+")
        self.attach.winfo_toplevel().bind('<Configure>', lambda e: self._withdraw() if not self.disable else None, add="+")
        self.attach.winfo_toplevel().bind("<ButtonPress>", lambda e: self._withdraw() if not self.disable else None, add="+")        
        self.bind("<Escape>", lambda e: self._withdraw() if not self.disable else None, add="+")
        
        self.attributes('-alpha', 0)
        self.disable = False
        self.fg_color = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"] if fg_color is None else fg_color
        self.scroll_button_color = customtkinter.ThemeManager.theme["CTkScrollbar"]["button_color"] if scrollbar_button_color is None else scrollbar_button_color
        self.scroll_hover_color = customtkinter.ThemeManager.theme["CTkScrollbar"]["button_hover_color"] if scrollbar_button_hover_color is None else scrollbar_button_hover_color
        self.frame_border_color = customtkinter.ThemeManager.theme["CTkFrame"]["border_color"] if frame_border_color is None else frame_border_color
        self.button_color = customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"] if button_color is None else button_color
        self.text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else text_color
        self.hover_color = customtkinter.ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else hover_color
        
        
        if scrollbar is False:
            self.scroll_button_color = self.fg_color
            self.scroll_hover_color = self.fg_color
            
        self.frame = customtkinter.CTkScrollableFrame(self, bg_color=self.transparent_color, fg_color=self.fg_color,
                                        scrollbar_button_hover_color=self.scroll_hover_color,
                                        corner_radius=self.corner, border_width=frame_border_width,
                                        scrollbar_button_color=self.scroll_button_color,
                                        border_color=self.frame_border_color)
        self.frame._scrollbar.grid_configure(padx=3)
        self.frame.pack(expand=True, fill="both")
        self.dummy_entry = customtkinter.CTkEntry(self.frame, fg_color="transparent", border_width=0, height=1, width=1)
        self.no_match = customtkinter.CTkLabel(self.frame, text="No Match")
        self.height = height
        self.height_new = height
        self.width = width
        self.command = command
        self.fade = False
        self.resize = resize
        self.autocomplete = autocomplete
        self.var_update = customtkinter.StringVar()
        self.appear = False
        
        if justify.lower()=="left":
            self.justify = "w"
        elif justify.lower()=="right":
            self.justify = "e"
        else:
            self.justify = "c"
            
        self.button_height = button_height
        self.values = values
        self.button_num = len(self.values)
        self.image_values = None if len(image_values)!=len(self.values) else image_values
        
        self.resizable(width=False, height=False)
        self.transient(self.master)
        self._init_buttons(**button_kwargs)

        # Add binding for different ctk widgets
        if double_click or type(self.attach) is customtkinter.CTkEntry or type(self.attach) is customtkinter.CTkComboBox:
            self.attach.bind('<Double-Button-1>', lambda e: self._iconify(), add="+")
        else:
            self.attach.bind('<Button-1>', lambda e: self._iconify(), add="+")

        if type(self.attach) is customtkinter.CTkComboBox:
            self.attach._canvas.tag_bind("right_parts", "<Button-1>", lambda e: self._iconify())
            self.attach._canvas.tag_bind("dropdown_arrow", "<Button-1>", lambda e: self._iconify())
            if self.command is None:
                self.command = self.attach.set
              
        if type(self.attach) is customtkinter.CTkOptionMenu:
            self.attach._canvas.bind("<Button-1>", lambda e: self._iconify())
            self.attach._text_label.bind("<Button-1>", lambda e: self._iconify())
            if self.command is None:
                self.command = self.attach.set
                
        self.attach.bind("<Destroy>", lambda _: self._destroy(), add="+")
        
        self.update_idletasks()
        self.x = x
        self.y = y

        if self.autocomplete:
            self.bind_autocomplete()
            
        self.deiconify()
        self.withdraw()

        self.attributes("-alpha", self.alpha)

    def _destroy(self):
        self.after(500, self.destroy_popup)
        
    def _withdraw(self):
        if self.winfo_viewable() and self.hide:
            self.withdraw()
        
        self.event_generate("<<Closed>>")
        self.hide = True

    def _update(self, a, b, c):
        self.live_update(self.attach._entry.get())
        
    def bind_autocomplete(self, ):
        def appear(x):
            self.appear = True
            
        if type(self.attach) is customtkinter.CTkComboBox:
            self.attach._entry.configure(textvariable=self.var_update)
            self.attach._entry.bind("<Key>", appear)
            self.attach.set(self.values[0])
            self.var_update.trace_add('write', self._update)
            
        if type(self.attach) is customtkinter.CTkEntry:
            self.attach.configure(textvariable=self.var_update)
            self.attach.bind("<Key>", appear)
            self.var_update.trace_add('write', self._update)
        
    def fade_out(self):
        for i in range(100,0,-10):
            if not self.winfo_exists():
                break
            self.attributes("-alpha", i/100)
            self.update()
            time.sleep(1/100)
            
    def fade_in(self):
        for i in range(0,100,10):
            if not self.winfo_exists():
                break
            self.attributes("-alpha", i/100)
            self.update()
            time.sleep(1/100)
            
    def _init_buttons(self, **button_kwargs):
        self.i = 0
        self.widgets = {}
        for row in self.values:
            self.widgets[self.i] = customtkinter.CTkButton(self.frame,
                                                          text=row,
                                                          height=self.button_height,
                                                          fg_color=self.button_color,
                                                          text_color=self.text_color,
                                                          image=self.image_values[self.i] if self.image_values is not None else None,
                                                          anchor=self.justify,
                                                          hover_color=self.hover_color,
                                                          command=lambda k=row: self._attach_key_press(k), **button_kwargs)
            self.widgets[self.i].pack(fill="x", pady=2, padx=(self.padding, 0))
            self.i+=1
 
        self.hide = False
            
    def destroy_popup(self):
        self.destroy()
        self.disable = True

    def place_dropdown(self):
        self.x_pos = self.attach.winfo_rootx() if self.x is None else self.x + self.attach.winfo_rootx()
        self.y_pos = self.attach.winfo_rooty() + self.attach.winfo_reqheight() + 5 if self.y is None else self.y + self.attach.winfo_rooty()
        self.width_new = self.attach.winfo_width() if self.width is None else self.width
        
        if self.resize:
            if self.button_num<=5:      
                self.height_new = self.button_height * self.button_num + 55
            else:
                self.height_new = self.button_height * self.button_num + 35
            if self.height_new>self.height:
                self.height_new = self.height

        self.geometry('{}x{}+{}+{}'.format(self.width_new, self.height_new,
                                           self.x_pos, self.y_pos))
        self.fade_in()
        self.attributes('-alpha', self.alpha)
        self.attach.focus()

    def _iconify(self):
        if self.attach.cget("state")=="disabled": return
        if self.disable: return
        if self.winfo_ismapped():
            self.hide = False
        if self.hide:
            self.event_generate("<<Opened>>")      
            self.focus()
            self.hide = False
            self.place_dropdown()
            self._deiconify()  
            if self.focus_something:
                self.dummy_entry.pack()
                self.dummy_entry.focus_set()
                self.after(100, self.dummy_entry.pack_forget)
        else:
            self.withdraw()
            self.hide = True
            
    def _attach_key_press(self, k):
        self.event_generate("<<Selected>>")
        self.fade = True
        if self.command:
            self.command(k)
        self.fade = False
        self.fade_out()
        self.withdraw()
        self.hide = True
            
    def live_update(self, string=None):
        if not self.appear: return
        if self.disable: return
        if self.fade: return
        if string:
            string = string.lower()
            self._deiconify()
            i=1
            for key in self.widgets.keys():
                s = self.widgets[key].cget("text").lower()
                text_similarity = difflib.SequenceMatcher(None, s[0:len(string)], string).ratio()
                similar = s.startswith(string) or text_similarity > 0.75
                if not similar:
                    self.widgets[key].pack_forget()
                else:
                    self.widgets[key].pack(fill="x", pady=2, padx=(self.padding, 0))
                    i+=1
                    
            if i==1:
                self.no_match.pack(fill="x", pady=2, padx=(self.padding, 0))
            else:
                self.no_match.pack_forget()
            self.button_num = i
            self.place_dropdown()
            
        else:
            self.no_match.pack_forget()
            self.button_num = len(self.values)
            for key in self.widgets.keys():
                self.widgets[key].destroy()
            self._init_buttons()
            self.place_dropdown()
            
        self.frame._parent_canvas.yview_moveto(0.0)
        self.appear = False
        
    def insert(self, value, **kwargs):
        self.widgets[self.i] = customtkinter.CTkButton(self.frame,
                                                       text=value,
                                                       height=self.button_height,
                                                       fg_color=self.button_color,
                                                       text_color=self.text_color,
                                                       hover_color=self.hover_color,
                                                       anchor=self.justify,
                                                       command=lambda k=value: self._attach_key_press(k), **kwargs)
        self.widgets[self.i].pack(fill="x", pady=2, padx=(self.padding, 0))
        self.i+=1
        self.values.append(value)
        
    def _deiconify(self):
        if len(self.values)>0:
            self.deiconify()

    def popup(self, x=None, y=None):
        self.x = x
        self.y = y
        self.hide = True
        self._iconify()

    def hide(self):
        self._withdraw()
        
    def configure(self, **kwargs):
        if "height" in kwargs:
            self.height = kwargs.pop("height")
            self.height_new = self.height
            
        if "alpha" in kwargs:
            self.alpha = kwargs.pop("alpha")
            
        if "width" in kwargs:
            self.width = kwargs.pop("width")
            
        if "fg_color" in kwargs:
            self.frame.configure(fg_color=kwargs.pop("fg_color"))
            
        if "values" in kwargs:
            self.values = kwargs.pop("values")
            self.image_values = None
            self.button_num = len(self.values)
            for key in self.widgets.keys():
                self.widgets[key].destroy()
            self._init_buttons()
 
        if "image_values" in kwargs:
            self.image_values = kwargs.pop("image_values")
            self.image_values = None if len(self.image_values)!=len(self.values) else self.image_values
            if self.image_values is not None:
                i=0
                for key in self.widgets.keys():
                    self.widgets[key].configure(image=self.image_values[i])
                    i+=1
                    
        if "button_color" in kwargs:
            for key in self.widgets.keys():
                self.widgets[key].configure(fg_color=kwargs.pop("button_color"))
                
        if "font" in kwargs:
            for key in self.widgets.keys():
                self.widgets[key].configure(font=kwargs.pop("font"))
                
        if "hover_color" not in kwargs:
            kwargs["hover_color"] = self.hover_color
        
        for key in self.widgets.keys():
            self.widgets[key].configure(**kwargs)
# CTkTable Widget by Akascape
class CTkTable(customtkinter.CTkFrame):
    """ CTkTable Widget """
    
    def __init__(
        self,
        master: any,
        row: int = None,
        column: int = None,
        padx: int = 1, 
        pady: int = 0,
        width: int = 140,
        height: int = 28,
        values: list = None,
        colors: list = [None, None],
        orientation: str = "horizontal",
        color_phase: str = "horizontal",
        border_width: int = 0,
        text_color: str or tuple = None, # type: ignore
        border_color: str or tuple = None, # type: ignore
        font: tuple = None,
        header_color: str or tuple = None, # type: ignore
        corner_radius: int = 25,
        write: str = False,
        command = None,
        anchor: str = "c",
        hover_color: str or tuple = None, # type: ignore
        hover: bool = False,
        justify: str = "center",
        wraplength: int = 1000,
        **kwargs):
        
        super().__init__(master, fg_color="transparent")
        
        if values is None:
            values = [[None,None],[None,None]]
            
        self.master = master # parent widget
        self.rows = row if row else len(values) # number of default rows
        self.columns = column if column else len(values[0])# number of default columns
        self.width = width
        self.height = height
        self.padx = padx # internal padding between the rows/columns
        self.pady = pady
        self.command = command
        self.values = values # the default values of the table
        self.colors = colors # colors of the table if required
        self.header_color = header_color # specify the topmost row color
        self.phase = color_phase
        self.corner = corner_radius
        self.write = write
        self.justify = justify
        self.binded_objects = []
            
        if self.write:
            border_width = border_width=+1
            
        if hover_color is not None and hover is False:
            hover=True
            
        self.anchor = anchor
        self.wraplength = wraplength
        self.hover = hover 
        self.border_width = border_width
        self.hover_color = customtkinter.ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else hover_color
        self.orient = orientation
        self.border_color = customtkinter.ThemeManager.theme["CTkButton"]["border_color"] if border_color is None else border_color
        self.inside_frame = customtkinter.CTkFrame(self, border_width=0, fg_color="transparent")
        super().configure(border_color=self.border_color, border_width=self.border_width, corner_radius=self.corner)
        self.inside_frame.pack(expand=True, fill="both", padx=self.border_width, pady=self.border_width)

        self.text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else text_color
        self.font = font
        # if colors are None then use the default frame colors:
        self.data = {}
        self.fg_color = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"] if not self.colors[0] else self.colors[0]
        self.fg_color2 = customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"] if not self.colors[1] else self.colors[1]

        if self.colors[0] is None and self.colors[1] is None:
            if self.fg_color==self.master.cget("fg_color"):
                self.fg_color = customtkinter.ThemeManager.theme["CTk"]["fg_color"]
            if self.fg_color2==self.master.cget("fg_color"):
                self.fg_color2 = customtkinter.ThemeManager.theme["CTk"]["fg_color"]
            
        self.frame = {}
        self.corner_buttons = {}
        self.draw_table(**kwargs)
        
    def draw_table(self, **kwargs):

        """ draw the table """
        for i in range(self.rows):
            for j in range(self.columns):
                self.inside_frame.grid_rowconfigure(i, weight=1)
                self.inside_frame.grid_columnconfigure(j, weight=1)
                if self.phase=="horizontal":
                    if i%2==0:
                        fg = self.fg_color
                    else:
                        fg = self.fg_color2
                else:
                    if j%2==0:
                        fg = self.fg_color
                    else:
                        fg = self.fg_color2
                        
                if self.header_color:
                    if self.orient=="horizontal":
                        if i==0:
                            fg = self.header_color
                    else:
                        if j==0:
                            fg = self.header_color

                corner_radius = self.corner
                if (self.border_width>=5) and (self.corner>=5):
                    tr = self.border_color
                else:
                    tr = ""
                if i==0 and j==0:
                    corners = [tr, fg, fg, fg]
                    hover_modify = self.hover
        
                elif i==self.rows-1 and j==self.columns-1:
                    corners = [fg ,fg, tr, fg]
                    hover_modify = self.hover
        
                elif i==self.rows-1 and j==0:
                    corners = [fg ,fg, fg, tr]
                    hover_modify = self.hover
       
                elif i==0 and j==self.columns-1:
                    corners = [fg, tr, fg, fg]
                    hover_modify = self.hover
 
                else:
                    corners = [fg, fg, fg, fg]
                    corner_radius = 0
                    hover_modify = False
            
                if i==0:
                    pady = (0, self.pady)
                else:
                    pady = self.pady
                    
                if j==0:
                    padx = (0, self.padx)
                else:
                    padx = self.padx
                    
                if i==self.rows-1:
                    pady = (self.pady,0)
                
                if j==self.columns-1:
                    padx = (self.padx,0)

                if self.values:
                    try:
                        if self.orient=="horizontal":
                            value = self.values[i][j]
                        else:
                            value = self.values[j][i]
                    except IndexError: value = " "
                else:
                    value = " "
                    
                if value=="":
                    value = " "
                
                if (i,j) in self.data.keys():
                    if self.data[i,j]["args"]:
                        args = self.data[i,j]["args"]
                    else:
                        args = copy.deepcopy(kwargs)
                else:
                    args = copy.deepcopy(kwargs)
                
                
                self.data[i,j] = {"row": i, "column" : j, "value" : value, "args": args}
                
                args = self.data[i,j]["args"]
                
                if "text_color" not in args:
                    args["text_color"] = self.text_color
                if "height" not in args:
                    args["height"] = self.height
                if "width" not in args:
                    args["width"] = self.width
                if "fg_color" not in args:
                    args["fg_color"] = fg
                if args["fg_color"]!=fg:
                    args["fg_color"] = fg
                if "corner_radius" in args:
                    del args["corner_radius"]
                if "border_color" in args:
                    del args["border_color"]
                if "border_width" in args:
                    del args["border_width"]
                if "color_phase" in args:
                    del args["color_phase"]
                if "orientation" in args:
                    del args["orientation"]
                if "write" in args:
                    del args["write"]
       
                if self.write:
                    if "anchor" in args:
                        del args["anchor"] 
                    if "hover_color" in args:
                        del args["hover_color"] 
                    if "hover" in args:
                        del args["hover"]
                    if "justify" not in args:
                        args["justify"] = self.justify
                    
                    self.frame[i,j] = customtkinter.CTkEntry(self.inside_frame,
                                                             font=self.font,
                                                             corner_radius=0,
                                                             **args)
                    if value is None:
                        value = " "
                    self.frame[i,j].insert(0, str(value))
                    self.frame[i,j].bind("<Key>", lambda e, row=i, column=j, data=self.data: self.after(100, lambda: self.manipulate_data(row, column)))
                    self.frame[i,j].grid(column=j, row=i, padx=padx, pady=pady, sticky="nsew")
                    
                    if self.header_color:
                        if i==0:
                            self.frame[i,j].configure(state="readonly")
    
                else:
                    if "anchor" not in args:
                        args["anchor"] = self.anchor
                    if "hover_color" not in args:
                        args["hover_color"] = self.hover_color
                    if "hover" not in args:
                        args["hover"] = self.hover
                    if "justify" in args:
                        anchor =  args["justify"]
                        if anchor=="center":
                            anchor="c"
                        elif anchor=="left":
                            anchor="w"
                        elif anchor=="right":
                            anchor="e"
                        args.update({"anchor": anchor})
                        del args["justify"]
                    if value is None:
                        value = " "
                    self.frame[i,j] = customtkinter.CTkButton(self.inside_frame, background_corner_colors=corners,
                                                              font=self.font, 
                                                              corner_radius=corner_radius,
                                                              text=value,
                                                              border_width=0,
                                                              command=(lambda e=self.data[i,j]: self.command(e)) if self.command else None, **args)
                    self.frame[i,j].grid(column=j, row=i, padx=padx, pady=pady, sticky="nsew")
                    if self.frame[i,j]._text_label is not None:
                        self.frame[i,j]._text_label.config(wraplength=self.wraplength)
                    
                    if hover_modify:
                        self.dynamic_hover(self.frame[i,j], i, j)
                        
                self.rowconfigure(i, weight=1)
                self.columnconfigure(j, weight=1)
        for x in self.frame:
            for y in self.binded_objects:
                self.frame[x].bind(*y)
        
    def dynamic_hover(self, frame, i, j):
        """ internal function to change corner cell colors """
        self.corner_buttons[i,j] = frame
        fg = self.data[i,j]["args"]["fg_color"]
        hv = self.data[i,j]["args"]["hover_color"]
        if (self.border_width>=5) and (self.corner>=5):
            tr = self.border_color
        else:
            tr = ""
        if i==0 and j==0:
            corners = [tr, fg, fg, fg]
            hover_corners = [tr, hv, hv, hv]
        elif i==self.rows-1 and j==self.columns-1:
            corners = [fg ,fg, tr, fg]
            hover_corners = [hv, hv, tr, hv]
        elif i==self.rows-1 and j==0:
            corners = [fg ,fg, fg, tr]
            hover_corners = [hv, hv, hv, tr]
        elif i==0 and j==self.columns-1:
            corners = [fg, tr, fg, fg]
            hover_corners = [hv, tr, hv, hv]
        else:
            return
        
        frame.configure(background_corner_colors=corners, fg_color=fg)
        frame.bind("<Enter>", lambda e, x=i, y=j, color=hover_corners, fg=hv:
                             self.frame[x,y].configure(background_corner_colors=color, fg_color=fg))
        frame.bind("<Leave>", lambda e, x=i, y=j, color=corners, fg=fg:
                            self.frame[x,y].configure(background_corner_colors=color, fg_color=fg))
        
    def manipulate_data(self, row, column):
        """ entry callback """
        self.update_data()
        data = self.data[row,column]
        if self.command: self.command(data)
        
    def update_data(self):
        """ update the data when values are changes """
        for i in self.frame:
            if self.write:
                self.data[i]["value"]=self.frame[i].get()
            else:
                self.data[i]["value"]=self.frame[i].cget("text")

        self.values = []
        for i in range(self.rows):
            row_data = []
            for j in range(self.columns):
                row_data.append(self.data[i,j]["value"])
            self.values.append(row_data)
            
    def edit_row(self, row, value=None, **kwargs):
        """ edit all parameters of a single row """
        for i in range(self.columns):
            self.frame[row, i].configure(require_redraw=True, **kwargs)
            self.data[row, i]["args"].update(kwargs)
            if value is not None:
                self.insert(row, i, value)
            if (row,i) in self.corner_buttons.keys():
                self.dynamic_hover(self.corner_buttons[row,i],row,i)
        self.update_data()
       
    def edit_column(self, column, value=None, **kwargs):
        """ edit all parameters of a single column """
        for i in range(self.rows):
            self.frame[i, column].configure(require_redraw=True, **kwargs)
            self.data[i, column]["args"].update(kwargs)
            if value is not None:
                self.insert(i, column, value)
            if (i, column) in self.corner_buttons.keys():
                self.dynamic_hover(self.corner_buttons[i, column], i, column)
        self.update_data()
        
    def update_values(self, values, **kwargs):
        """ update all values at once """
        for i in self.frame.values():
            i.destroy()
        self.frame = {}
        self.values = values
        self.draw_table(**kwargs)
        self.update_data()
        
    def add_row(self, values, index=None, **kwargs):
        """ add a new row """
        for i in self.frame.values():
            i.destroy()
        self.frame = {}
        if index is None:
            index = len(self.values)      
        try:
            self.values.insert(index, values)
            self.rows+=1
        except IndexError: pass
 
        self.draw_table(**kwargs)
        self.update_data()
        
    def add_column(self, values, index=None, **kwargs):
        """ add a new column """
        for i in self.frame.values():
            i.destroy()
        self.frame = {}
        if index is None:
            index = len(self.values[0])
        x = 0
        for i in self.values:
            try:
                i.insert(index, values[x])
                x+=1
            except IndexError: pass
        self.columns+=1
        self.draw_table(**kwargs)
        self.update_data()
        
    def delete_row(self, index=None):
        """ delete a particular row """
        if len(self.values)==1:
            return
        if index is None or index>=len(self.values):
            index = len(self.values)-1
        self.values.pop(index)
        for i in self.frame.values():
            i.destroy()
        self.rows-=1
        self.frame = {}
        self.draw_table()
        self.update_data()

        
    def delete_column(self, index=None):
        """ delete a particular column """
        if len(self.values[0])==1:
            return
        if index is None or index>=len(self.values[0]):
            try:
                index = len(self.values)-1
            except IndexError:
                return
        for i in self.values:
            i.pop(index)
        for i in self.frame.values():
            i.destroy()
        self.columns-=1
        self.frame = {}
        self.draw_table()
        self.update_data()

        
    def delete_rows(self, indices=[]):
        """ delete a particular row """
        if len(indices)==0:
            return
        self.values = [v for i, v in enumerate(self.values) if i not in indices]
        for i in indices:
            for j in range(self.columns):
                self.data[i, j]["args"] = ""
        for i in self.frame.values():
            i.destroy()
        self.rows -= len(set(indices))
        self.frame = {}
        self.draw_table()
        self.update_data()
        
    def delete_columns(self, indices=[]):
        """ delete a particular column """
        if len(indices)==0:
            return
        x = 0
        
        for k in self.values:
            self.values[x] = [v for i, v in enumerate(k) if i not in indices]
            x+=1
        for i in indices:
            for j in range(self.rows):
                self.data[j, i]["args"] = ""
                
        for i in self.frame.values():
            i.destroy()
        self.columns -= len(set(indices))
        self.frame = {}
        self.draw_table()
        self.update_data()
        
    def get_row(self, row):
        """ get values of one row """
        return self.values[row]
    
    def get_column(self, column):
        """ get values of one column """
        column_list = []
        for i in self.values:
            column_list.append(i[column])
        return column_list

    def select_row(self, row):
        """ select an entire row """
        self.edit_row(row, fg_color=self.hover_color)
        if self.orient!="horizontal":
            if self.header_color:
                self.edit_column(0, fg_color=self.header_color)
        else:
            if self.header_color:
                self.edit_row(0, fg_color=self.header_color)
        return self.get_row(row)
    
    def select_column(self, column):
        """ select an entire column """
        self.edit_column(column, fg_color=self.hover_color)
        if self.orient!="horizontal":
            if self.header_color:
                self.edit_column(0, fg_color=self.header_color)
        else:
            if self.header_color:
                self.edit_row(0, fg_color=self.header_color)
        return self.get_column(column)
    
    def deselect_row(self, row):
        """ deselect an entire row """
        self.edit_row(row, fg_color=self.fg_color if row%2==0 else self.fg_color2)
        if self.orient!="horizontal":
            if self.header_color:
                self.edit_column(0, fg_color=self.header_color)
        else:
            if self.header_color:
                self.edit_row(0, fg_color=self.header_color)
                
    def deselect_column(self, column):
        """ deselect an entire column """
        for i in range(self.rows):
            self.frame[i,column].configure(fg_color=self.fg_color if i%2==0 else self.fg_color2)
        if self.orient!="horizontal":
            if self.header_color:
                self.edit_column(0, fg_color=self.header_color)
        else:
            if self.header_color:
                self.edit_row(0, fg_color=self.header_color)

    def select(self, row, column):
        """ select any cell """
        if row == 0 and column == 0:
            hover_corners = ["", self.hover_color, self.hover_color, self.hover_color]
        elif row == self.rows - 1 and column == self.columns - 1:
            hover_corners = [self.hover_color, self.hover_color, "", self.hover_color]
        elif row == self.rows - 1 and column == 0:
            hover_corners=[self.hover_color, self.hover_color, self.hover_color, ""]
        elif row == 0 and column == self.columns - 1:
            hover_corners = [self.hover_color, "", self.hover_color, self.hover_color]
        else:
            hover_corners = [self.hover_color, self.hover_color, self.hover_color, self.hover_color]
        self.frame[row, column].configure(background_corner_colors=hover_corners, fg_color=self.hover_color)

    def deselect(self, row, column):
        """ deselect any cell """
        self.frame[row,column].configure(fg_color=self.fg_color if row%2==0 else self.fg_color2)
        
    def insert(self, row, column, value, **kwargs):
        """ insert value in a specific block [row, column] """
        if kwargs: self.data[row,column]["args"].update(kwargs)
        if self.write:
            self.frame[row,column].delete(0, customtkinter.END)
            self.frame[row,column].insert(0, value)
            self.frame[row,column].configure(**kwargs)
        else:        
            self.frame[row,column].configure(require_redraw=True, text=value, **kwargs)
            if (row, column) in self.corner_buttons.keys():
                self.dynamic_hover(self.corner_buttons[row, column], row, column)
        
        self.update_data()
        
    def edit(self, row, column, **kwargs):
        """ change parameters of a cell without changing value """
        if kwargs: self.data[row,column]["args"].update(kwargs)
        if self.write:
            self.frame[row,column].configure(**kwargs)
        else:        
            self.frame[row,column].configure(require_redraw=True, **kwargs)
            if (row, column) in self.corner_buttons.keys():
                self.dynamic_hover(self.corner_buttons[row, column], row, column)
        
        self.update_data()
        
    def delete(self, row, column, **kwargs):
        """ delete a value from a specific block [row, column] """
        if self.write:
            self.frame[row,column].delete(0, customtkinter.END)
            self.frame[row,column].configure(**kwargs)
        else:     
            self.frame[row,column].configure(require_redraw=True, text="", **kwargs)
        if kwargs: self.data[row,column]["args"].update(kwargs)
        self.update_data()
        
    def get(self, row=None, column=None):
        """ get the required cell """
        if row is not None and column is not None:
            return self.data[row,column]["value"]
        else:
            return self.values
        
    def get_selected_row(self):
        """ Return the index and data of the selected row """
        selected_row_index = None
        for i in range(self.rows):
            if self.frame[i, 0].cget("fg_color") == self.hover_color:
                selected_row_index = i
                break
        selected_row_data = self.get_row(selected_row_index) if selected_row_index is not None else None
        return {"row_index": selected_row_index, "values": selected_row_data}
    
    def get_selected_column(self):
        """ Return the index and data of the selected row """
        selected_column_index = None
        for i in range(self.columns):
            if self.frame[0, i].cget("fg_color") == self.hover_color:
                selected_column_index = i
                break
        selected_column_data = self.get_column(selected_column_index) if selected_column_index is not None else None
        return {"column_index": selected_column_index, "values": selected_column_data}
    
    def configure(self, **kwargs):
        """ configure table widget attributes"""
        
        if "colors" in kwargs:
            self.colors = kwargs.pop("colors")
            self.fg_color = self.colors[0]
            self.fg_color2 = self.colors[1]
        if "fg_color" in kwargs:
            self.colors = (kwargs["fg_color"], kwargs.pop("fg_color"))
            self.fg_color = self.colors[0]
            self.fg_color2 = self.colors[1]
        if "bg_color" in kwargs:
            super().configure(bg_color=kwargs["bg_color"])
            self.inside_frame.configure(fg_color=kwargs["bg_color"])
        if "header_color" in kwargs:
            self.header_color = kwargs.pop("header_color")
        if "rows" in kwargs:
            self.rows = kwargs.pop("rows")
        if "columns" in kwargs:
            self.columns = kwargs.pop("columns")
        if "values" in kwargs:
            self.values = kwargs.pop("values")
        if "padx" in kwargs:
            self.padx = kwargs.pop("padx")
        if "pady" in kwargs:
            self.pady = kwargs.pop("pady")
        if "wraplength" in kwargs:
            self.wraplength = kwargs.pop("wraplength")

        for i in range(self.rows):
            for j in range(self.columns):
                self.data[i,j]["args"].update(kwargs)
                
        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
        if "border_width" in kwargs:
            self.border_width = kwargs.pop("border_width")
            super().configure(border_width=self.border_width)
            self.inside_frame.pack(expand=True, fill="both", padx=self.border_width, pady=self.border_width)
        if "border_color" in kwargs:
            self.border_color = kwargs.pop("border_color")
            super().configure(border_color=self.border_color)
        if "hover" in kwargs:
            self.hover = kwargs.pop("hover")
        if "anchor" in kwargs:
            self.anchor = kwargs.pop("anchor")
        if "corner_radius" in kwargs:
            self.corner = kwargs.pop("corner_radius")
            super().configure(corner_radius=self.corner)
        if "color_phase" in kwargs:
            self.phase = kwargs.pop("color_phase")
        if "justify" in kwargs:
            self.justify = kwargs.pop("justify")
        if "orientation" in kwargs:
            self.orient = kwargs.pop("orientation")
        if "write" in kwargs:
            self.write = kwargs.pop("write")
        if "width" in kwargs:
            self.width = kwargs.pop("width")
        if "height" in kwargs:
            self.height = kwargs.pop("height")
            
        self.update_values(self.values, **kwargs)

    def cget(self, param):
        if param=="width":
            return self.frame[0,0].winfo_reqwidth()
        if param=="height":
            return self.frame[0,0].winfo_reqheight()
        if param=="colors":
            return (self.fg_color, self.fg_color2)
        if param=="hover_color":
            return self.hover_color
        if param=="text_color":
            return self.text_color
        if param=="border_width":
            return self.border_width
        if param=="border_color":
            return self.border_color
        if param=="hover":
            return self.hover
        if param=="anchor":
            return self.anchor
        if param=="wraplength":
            return self.wraplength
        if param=="padx":
            return self.padx
        if param=="pady":
            return self.pady
        if param=="header_color":
            return self.header_color
        if param=="row":
            return self.rows
        if param=="column":
            return self.columns
        if param=="values":
            return self.values
        if param=="color_phase":
            return self.phase
        if param=="justify":
            return self.justify
        if param=="orientation":
            return self.orient
        if param=="write":
            return self.write
        
        return super().cget(param)
    
    def bind(self, sequence: str = None, command = None, add = True):
        """ bind all cells """
        self.binded_objects.append([sequence, command, add])
        
        super().bind(sequence, command, add)
        for i in self.frame:
            self.frame[i].bind(sequence, command, add)
        self.inside_frame.bind(sequence, command, add)
        
    def unbind(self, sequence: str = None, funcid: str = None):
        for i in self.binded_objects:
            if sequence in i:
                self.binded_objects.remove(i)
                
        super().unbind(sequence, funcid)
        for i in self.frame:
            self.frame[i].unbind(sequence, funcid)
        self.inside_frame.unbind(sequence, funcid)

# agent select frame and options
def switchSelectingMode():
    newMode = agent_frame.get()
    if newMode == "Delay":
        return
    config['mapMode'] = newMode
    with open(configPath, 'w') as file:
        json.dump(config, file, indent=4)
agent_frame = customtkinter.CTkTabview(master=app, width=435 ,height=140, corner_radius=20, command=switchSelectingMode)
normal = agent_frame.add("Normal")
Map = agent_frame.add("Map")
Random = agent_frame.add("Random")
DelayO = agent_frame.add("Delay")
def decValueDanger(v):
    if v >= 4:
        return { "text": f"{v}s Locks After agent select screen (SAFE)", "color": white_text }
    else:
        return { "text": f"{v}s Locks before agent select screen (DANGEROUS)", "color": red_text }
def sliderCommand(v):
    newTextSlider = decValueDanger(v)
    buttonStartSliderText.configure(text=newTextSlider['text'], text_color=newTextSlider['color'])
    config['delay'] = v
    with open(configPath, 'w') as file:
        json.dump(config, file, indent=4)
buttonStartDelay = customtkinter.CTkSlider(master=DelayO, from_=0, to=8, number_of_steps=16, command=sliderCommand)
buttonStartDelay.set(sliderValue)
buttonStartDelay.pack(pady=5, anchor="n")
newTextSlider = decValueDanger(sliderValue)
buttonStartSliderText = customtkinter.CTkLabel(master=DelayO, text=newTextSlider['text'], text_color=newTextSlider['color'])
buttonStartSliderText.place(relx=0.5, rely=0.7, anchor= customtkinter.CENTER)
agent_frame.set(currentMode)
def selectAgent(a):
    comboboxAgents.set(a)
    config['agent'] = str(a)
    with open(configPath, 'w') as f:
        json.dump(config, f, indent=4)
comboboxAgents = customtkinter.CTkComboBox(master=normal, values=list(agents.keys()), state="readonly", command=selectAgent)
comboboxAgents.set(value=selectedAgent)
comboboxAgents.place(relx=0.5, rely=0.56, anchor= customtkinter.CENTER)
buttonAgentsMap = customtkinter.CTkButton(master=Map, text="Select Agent For Each Map")
buttonAgentsMap.place(relx=0.5, rely=0.4, anchor= customtkinter.CENTER)
buttonAgentRandom = customtkinter.CTkLabel(master=Random, text="Press Start To Start Locking A Random Agent")
buttonAgentRandom.place(relx=0.5, rely=0.45, anchor= customtkinter.CENTER)
sct = CTkScrollableDropdown(comboboxAgents, values=list(agents.keys()), autocomplete= False, command=selectAgent)
buttonAgentText = customtkinter.CTkLabel(master=normal, text="Select Your Agent To Start Locking in First:")
buttonAgentText.place(relx=0.5, rely=0.1, anchor= customtkinter.CENTER)

#start frame and options

start_frame = customtkinter.CTkFrame(master=app,width=777 ,height=120, corner_radius=20)
buttonStart = customtkinter.CTkButton(master=start_frame, text="Start", state="disabled")
buttonStart.place(relx=0.5, rely=0.4, anchor= customtkinter.CENTER)
buttonStartDodge = customtkinter.CTkButton(master=start_frame, text="Dodge", state="disabled", width= 85)
buttonStartDodge.place(relx=0.35, rely=0.4, anchor= customtkinter.CENTER)
buttonStartCheck = customtkinter.CTkButton(master=start_frame, text="Check Side", state="disabled", width= 85)
buttonStartCheck.place(relx=0.65, rely=0.4, anchor= customtkinter.CENTER)
buttonStartText = customtkinter.CTkLabel(master=start_frame, text="Pick your Agent or Action and Start :)", text_color=white_text)
buttonStartText.place(relx=0.5, rely=0.7, anchor= customtkinter.CENTER)

def capitalize_first_letter(string: str) -> str:
    lowercased_string = string.lower()
    capitalized_string = lowercased_string.capitalize()
    return capitalized_string

def RankToTier(Rank: int) -> str:
    ranksReq = requests.get("https://valorant-api.com/v1/competitivetiers")
    Ep5SeasinID = "03621f52-342b-cf4e-4f86-9350a49c6d04"
    ranks = {}
    rank = "Unrated"
    if ranksReq.status_code == 404:
        return "Unknown"
    for t in ranksReq.json()['data']:
        if t["uuid"] == Ep5SeasinID:
            ranks = t['tiers']
    for r in ranks:
        if r["tier"] == Rank:
            rank = r ["tierName"]
    return rank

def MapIdToMapName(MapId: str) -> str:
    mapReq = requests.get("https://valorant-api.com/v1/maps")
    if (MapId == "Unknown"):
        return "Unknown"
    mapName = "Unknown"
    if ((mapReq.status_code == 404) or (mapReq.json()['status'] == 404)):
        return map
    maps = mapReq.json()['data']
    if not maps:
        return mapName
    for map in maps:
        if map['mapUrl'].lower() == MapId.lower():
            mapName = map['displayName']
    return mapName

def create_circle_image_with_background(image, new_size, color):
    image = image.resize(new_size, Image.LANCZOS)
    image = image.convert("RGBA")
    size = min(new_size)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    circular_image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circular_image.paste(image, (0, 0), mask)
    blue_background = Image.new("RGBA", (size, size), color)
    blue_background.putalpha(mask)
    final_image = Image.alpha_composite(blue_background, circular_image)

    return final_image

def download_image(url):
    response = requests.get(url)
    image_data = response.content
    return Image.open(BytesIO(image_data))

def inGamePlayerObj(player):
    with open(configPath, 'r') as f:
        config = json.load(f)
        agents = config['agents']
        skinsOrder = config['skinsOrder']
    deWeapons = defaultSkins
    agentID = player['CharacterID']
    agent = findKeysByValue(agents, agentID)[0]
    playerSide = player['TeamID']
    allyRC = defenderColor
    allyR = "Defender"
    if (playerSide == 'Red'):
        allyRC = attackerColor
        allyR = "Attacker"

    skinsInOrder = {}

    for name in skinsOrder:
        for key, value in deWeapons.items():
            if value["name"].replace("Default ", "") == name:
                skinsInOrder[key] = value
                break
    IPO = {
        "ID": player['Subject'] ,
        "agentSide": f"{allyR} {agent}",
        "icon": f"https://media.valorant-api.com/agents/{agentID}/displayicon.png",
        "color": allyRC,
        "skins": copy.deepcopy(skinsInOrder),
    }
    return IPO
        
def skinToChroma(ID):
    reqS = requests.get(f"https://valorant-api.com/v1/weapons/skinchromas/{ID}")
    jsonS = reqS.json()
    jsonData = jsonS['data']
    return { "name": jsonData["displayName"], "link": jsonData['fullRender'] }
        
    
def mapMenu():
    newWindow = customtkinter.CTkToplevel(app)
    newWindow.withdraw()
    newWindow.geometry("900x300")
    newWindow.title("Fast Pick Agent Select")
    newWindow.resizable(0, 0)
    newWindow.after(250, lambda: newWindow.iconbitmap(image))
    newWindow.grab_set()
    tabView = customtkinter.CTkTabview(newWindow, width=870, height=200)
    tabView.pack(expand= False, pady=20)
    cbs = {}
    def ph(newA):
        selectedMap = tabView.get()
        comboboxMap = cbs[selectedMap]
        comboboxMap.set(newA)
        existingMaps[selectedMap] = newA
        with open(configPath, 'w') as file:
            json.dump(config, file, indent=4)
    for map in existingMaps.keys():
        tV = tabView.add(map)
        comboboxAgentsMap = customtkinter.CTkComboBox(master=tV, values=list(agents.keys()), state="readonly")
        comboboxAgentsMap.set(value=existingMaps[map])
        comboboxAgentsMap.pack(pady=30, anchor= customtkinter.S)
        sxt = CTkScrollableDropdown(comboboxAgentsMap, values=list(agents.keys()), command=ph, autocomplete=False)
        cbs[map] = comboboxAgentsMap
    def Save():
        newWindow.destroy()
        newWindow.update()
    doneButton = customtkinter.CTkButton(newWindow, text="Done", command=Save)
    doneButton.pack(pady=20)
    newWindow.deiconify()
    

def getPlayerStats(player, side, fillerName):
    playerID = player['Subject']
    playerSide = side
    ally_result = "Attacker"
    if (playerSide == 'Blue'):
        ally_result = 'Defender'
    playerNameData = client.put(
        endpoint="/name-service/v2/players", 
        endpoint_type="pd", 
        json_data=[playerID]
    )[0]
    agent_keys = findKeysByValue(agents, player['CharacterID'])
    agent = agent_keys[0] if agent_keys else "Undefined"
    if agent == "Undefined":
        agent = fillerName
    seasonID = None
    seasonContent = client.fetch_content()
    for seasons in seasonContent['Seasons']:
        if (seasons["Type"] == "act") and (seasons["IsActive"] == True):
            seasonID = seasons["ID"]
    if not seasons:
        return seasonID
    gameName = playerNameData['GameName']
    tagLine = playerNameData['TagLine']
    data = {
        "fullPlayerName": f'{gameName}#{tagLine}',
        "side": ally_result,
        "agent": agent,
        "rank": "N/a",
        "rr": 0,
        "peakrank": "N/a",
        "wr": "N/a",
        "kd": "N/a",
        "hs": "N/a",
        "totalGames": "N/a"
    }
    try:
        playerMMR = client.fetch_mmr(playerID)
        seasonal_info = playerMMR["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"]
        peakRank = 0
        currentRank = 0
        if not seasonal_info:
            raise Exception("")
        for season_id, season_data in seasonal_info.items():
            wins_by_tier = season_data["WinsByTier"]
            if wins_by_tier:
                max_tier = max(int(tier) for tier in wins_by_tier.keys())
                if max_tier > peakRank:
                    peakRank = max_tier
        data["peakrank"] = capitalize_first_letter(RankToTier(peakRank))
        data["rank"] = capitalize_first_letter(RankToTier(currentRank))
        currentRank = playerMMR["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["CompetitiveTier"]
        currentRR = playerMMR["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["RankedRating"]
        wins = playerMMR["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["NumberOfWinsWithPlacements"]
        total_games = playerMMR["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"][seasonID]["NumberOfGames"]
        wr = 0
        try:
            wr = int(wins / total_games * 100)
        except ZeroDivisionError:
            wr = 100
        data["totalGames"] = total_games
        data["wr"] = wr
        data["rank"] = capitalize_first_letter(RankToTier(currentRank))
        data["rr"] = currentRR
        
    except Exception as e:
        print(f"MMR Error: {e} With Player: {gameName}")
    try:
        lastComp = client.fetch(endpoint= f"/mmr/v1/players/{playerID}/competitiveupdates?startIndex=0&endIndex=1&queue=competitive", endpoint_type="pd")
        lastCompData = client.fetch_match_details(lastComp['Matches'][0]['MatchID'])
        total_hits = 0
        total_headshots = 0
        for Round in lastCompData["roundResults"]:
            for currentPlayer in Round["playerStats"]:
                if currentPlayer["subject"] == playerID:
                    for hits in currentPlayer["damage"]:
                        total_hits += hits["legshots"]
                        total_hits += hits["bodyshots"]
                        total_hits += hits["headshots"]
                        total_headshots += hits["headshots"]
        data['hs'] = round((total_headshots/total_hits)*100, 1)
        for targetPlayer in lastCompData["players"]:
            if targetPlayer["subject"] == playerID:
                kills = targetPlayer["stats"]["kills"]
                deaths = targetPlayer["stats"]["deaths"]

        if deaths == 0:
            data['kd'] = kills
        elif kills == 0:
            data['kd'] = 0
        else:
            data['kd'] = round(kills/deaths, 2)
        return data
    except Exception as e:
        print(f"last Comp Error: {e} With Player: {gameName}")
    return data
    
    

def stop():
    global running
    running = False
    buttonStart.configure(text="Start", command=startButton)
    buttonStartText.configure(text="Pick your Agent or Action and Start :)", text_color=white_text)

def checkSides():
    sessionState = client.fetch_presence(client.puuid)
    if not sessionState:
        showRegionSelect(True)
        labelRegionStats.configure(text=startTheGame, text_color=red_text)
        return
    else:
        sessionState = (sessionState.get('sessionLoopState') if isinstance(sessionState, dict) else None)
        if sessionState is None:
            try:
                client.pregame_fetch_match()
                sessionState = "PREGAME"
            except Exception:
                try:
                    client.coregame_fetch_match()
                    sessionState = "INGAME"
                except Exception:
                    sessionState = "MENUS"
    if sessionState == "PREGAME":
        buttonStartText.configure(text='Agent Select Screen Found', text_color=white_text)
        ally = client.pregame_fetch_match()['AllyTeam']
        ally_team = ally['TeamID']
        ally_result = "Null"
        side_color = "#DCE4EE"
        if (ally_team == 'Red'):
            ally_result = 'Attacker'
            side_color = red_text
        elif (ally_team == 'Blue'):
            ally_result = 'Defender'
            side_color = blue_text
        buttonStartText.configure(text=f'You\'re: {ally_result}', text_color=side_color)
        return
    else:
        buttonStartText.configure(text='You Must Be In Agent Select First', text_color=red_text)
def dodgeMatch():
    sessionState = client.fetch_presence(client.puuid)
    if not sessionState:
        showRegionSelect(True)
        labelRegionStats.configure(text=startTheGame, text_color=red_text)
        return
    else:
        sessionState = (sessionState.get('sessionLoopState') if isinstance(sessionState, dict) else None)
        if sessionState is None:
            try:
                client.pregame_fetch_match()
                sessionState = "PREGAME"
            except Exception:
                try:
                    client.coregame_fetch_match()
                    sessionState = "INGAME"
                except Exception:
                    sessionState = "MENUS"
    if sessionState == "PREGAME":
        buttonStartText.configure(text='Agent Select Screen Found', text_color=white_text)
        client.pregame_quit_match()
        buttonStartText.configure(text='Successfully dodged the Match', text_color=white_text)
        return
    else:
        buttonStartText.configure(text='You Must Be In Agent Select First', text_color=red_text)
def disProButtons():
    buttonGetLoadouts.configure(state="disabled", width=80)
    buttonGetNames.configure(state="disabled", width=100)
    buttonGetNamesWithStats.configure(state="disabled", width=120)
def enProButtons():
    buttonGetLoadouts.configure(state="normal", width=80)
    buttonGetNames.configure(state="normal", width=100)
    buttonGetNamesWithStats.configure(state="normal", width=120) 

def getLoadoutsPro():
    try:
        presence = client.fetch_presence(client.puuid)
        if not presence:
            showRegionSelect(True)
            labelRegionStats.configure(text=startTheGame, text_color=red_text)
            return
        else:
            sessionState = (presence.get('sessionLoopState') if isinstance(presence, dict) else None)
            if sessionState is None:
                try:
                    client.pregame_fetch_match()
                    sessionState = "PREGAME"
                except Exception:
                    try:
                        client.coregame_fetch_match()
                        sessionState = "INGAME"
                    except Exception:
                        sessionState = "MENUS"
        if sessionState == "INGAME":
            disProButtons()
            buttonStartText.configure(text='Getting Loadouts(May Take A While)...', text_color=white_text)
            currentMatch = client.coregame_fetch_match()
            players = currentMatch['Players']
            infoPlayers = {}
            for player in players:
                if(player['Subject'] == client.puuid):
                    continue
                PO = inGamePlayerObj(player)
                infoPlayers[player['Subject']] = PO
            
            if not infoPlayers:
                buttonStartText.configure(text='No Players Found!!', text_color=red_text)
                enProButtons()
            loadouts = client.coregame_fetch_match_loadouts()
            loadouts = loadouts['Loadouts']
            for loadout in loadouts:
                loadoutOfPlayer = loadout['Loadout']
                if loadoutOfPlayer['Subject'] == client.puuid:
                    continue
                loadedPlayer = infoPlayers[loadoutOfPlayer['Subject']]['skins']
                for gunId, gun in loadedPlayer.items():
                    gunChromaId = loadoutOfPlayer['Items'][gunId]['Sockets']["3ad1b2b2-acdb-4524-852f-954a76ddae0a"]['Item']['ID']
                    if gunChromaId == gun['defaultChroma']:
                        continue
                    updatedLoadout = skinToChroma(gunChromaId)
                    gun['name'] = updatedLoadout['name']
                    gun['link'] = updatedLoadout['link']
            loadoutWindow = customtkinter.CTkToplevel(app)
            loadoutWindow.withdraw()
            loadoutWindow.geometry("900x500")
            loadoutWindow.title("Fast Pick Loadouts Tab")
            loadoutWindow.resizable(0, 0)
            loadoutWindow.after(250, lambda: loadoutWindow.iconbitmap(image))
            loadoutWindow.grab_set()
            def doneButtonFun():
                loadoutWindow.destroy()
            listFrame = customtkinter.CTkScrollableFrame(loadoutWindow, orientation="horizontal")
            listFrame.pack(fill="both", padx=18, pady=12, expand=True)
            doneButton = customtkinter.CTkButton(loadoutWindow, text="Done", height=23, command=doneButtonFun)
            doneButton.pack(padx=20, pady=8)
            for key, value in infoPlayers.items():
                agentImg = download_image(value["icon"])
                cir_img = create_circle_image_with_background(agentImg, (80, 80), value["color"])

                ogimg = customtkinter.CTkImage(
                    dark_image=cir_img, light_image=cir_img, size=(60, 60)
                )
                playerFrame = customtkinter.CTkScrollableFrame(
                    listFrame, width=330, height=380, fg_color="gray12"
                )
                playerFrame.pack(side="left", padx=10, pady=10)
                imgLabel = customtkinter.CTkLabel(playerFrame, text="", image=ogimg)
                imgLabel.pack(fill="both", expand=True)

                textLabel = customtkinter.CTkLabel(playerFrame, text=value['agentSide'])
                textLabel.pack(fill="both")

                for gunIdS, gunS in value["skins"].items():
                    gunFrame = customtkinter.CTkFrame(playerFrame, height=100)
                    gunFrame.pack_propagate(False)
                    gunFrame.pack(fill="x", pady=5)
                    vandalSkin = download_image(
                        gunS["link"]
                    )
                    gunimg = customtkinter.CTkImage(
                        light_image=vandalSkin,
                        dark_image=vandalSkin,
                        size=(gunS["size"][0], gunS["size"][1]),
                    )
                    gunlabel = customtkinter.CTkLabel(gunFrame, image=gunimg, text="")
                    gunlabel.pack(expand=True)
                    skinName = gunS['name'].replace("\n", " ")
                    textLabel = customtkinter.CTkLabel(gunFrame, text=skinName)
                    textLabel.pack(fill="x")
            loadoutWindow.deiconify()
            enProButtons()
            buttonStartText.configure(text='Got all Players loadouts!!', text_color=white_text)
        else:
            buttonStartText.configure(text='You Must Pass Agent Select To Use This!!', text_color=red_text)
            return
    except Exception as e:
        print(e)
        enProButtons()
        buttonStartText.configure(text='An Error Occurred While Getting loadouts', text_color=red_text)
    

def getHiddenNames():
    sessionState = client.fetch_presence(client.puuid)
    players = []
    if not sessionState:
        showRegionSelect(True)
        labelRegionStats.configure(text=startTheGame, text_color=red_text)
        return
    else:
        sessionState = (sessionState.get('sessionLoopState') if isinstance(sessionState, dict) else None)
        if sessionState is None:
            try:
                client.pregame_fetch_match()
                sessionState = "PREGAME"
            except Exception:
                try:
                    client.coregame_fetch_match()
                    sessionState = "INGAME"
                except Exception:
                    sessionState = "MENUS"
        trackerMode = buttonGetNamesSwitch.get()
    if sessionState == "INGAME":
        buttonStartText.configure(text='Getting Hidden Names', text_color=white_text)
        currentMatch = client.coregame_fetch_match()
        for player in currentMatch['Players']:
            if trackerMode == False:
                if(player['Subject'] == client.puuid) or (player['PlayerIdentity']['Incognito'] == False):
                    continue
            players.append(player)
        if not players:
            buttonStartText.configure(text='No Hidden Names Found', text_color=red_text)
            return
    elif sessionState == "PREGAME":
        buttonStartText.configure(text='Getting Hidden Names', text_color=white_text)
        currentMatch = client.pregame_fetch_match()
        for index, player in enumerate(currentMatch['AllyTeam']['Players'], start=1):
            player['fillerName'] = f"Player{index}"
            if trackerMode == False:
                if(player['Subject'] == client.puuid) or (player['PlayerIdentity']['Incognito'] == False):
                    continue
            player['TeamID'] = currentMatch["AllyTeam"]["TeamID"]
            players.append(player)
        if not players:
            buttonStartText.configure(text='No Hidden Names Found', text_color=red_text)
            return
    else:
        buttonStartText.configure(text='Start A Game First !!', text_color=red_text)
        return
    buttonStartText.configure(text='Found Hidden Names !!', text_color=white_text)
    newWindow = customtkinter.CTkToplevel(app)
    newWindow.geometry("400x390")
    newWindow.title("Fast Pick Agent Names")
    newWindow.resizable(0, 0)
    newWindow.after(250, lambda: newWindow.iconbitmap(image))
    newWindow.grab_set()
    mainFrame = customtkinter.CTkScrollableFrame(newWindow, 300, 300, 20)
    button = customtkinter.CTkLabel(mainFrame, text="Hidden Names Click To Copy:")
    button.pack(pady=5, anchor="nw")
    if trackerMode == True:
        button.configure(text="Click To Open Tracker Page:")
    mainFrame.pack(padx= 20, pady= 10)
    def kill():
        newWindow.destroy()
        newWindow.update()
    doneButton = customtkinter.CTkButton(newWindow, text="Done", command=kill)
    doneButton.pack(padx=20,pady=5)
    for hiddenPlayer in players:
        ally_team = hiddenPlayer['TeamID']
        ally_result = "Null"
        if (ally_team == 'Red'):
            ally_result = 'Attacker'
        elif (ally_team == 'Blue'):
            ally_result = 'Defender'
        agent_keys = findKeysByValue(agents, hiddenPlayer['CharacterID'])
        agent = agent_keys[0] if agent_keys else "Undefined"
        if (agent == "Undefined") and sessionState == "PREGAME":
            agent = hiddenPlayer['fillerName']
        playerId = hiddenPlayer['Subject']
        playerNameData = client.put(
            endpoint="/name-service/v2/players", 
            endpoint_type="pd", 
            json_data=[playerId]
        )[0]
        playerName = playerNameData['GameName']
        playerTag = f"#{playerNameData['TagLine']}"
        fullName = f"{playerName}{playerTag}"
        def decideCopy(fullName: str):
            if trackerMode == True:
                fullName = fullName.replace("#", "%23")
                webbrowser.open(f"https://tracker.gg/valorant/profile/riot/{fullName}/overview")
            else:
                pyperclip.copy(f"{fullName}")
        button = customtkinter.CTkButton(mainFrame, text=f"{ally_result} {agent}: {playerName}{playerTag}", corner_radius=30, command=lambda fullName=fullName: decideCopy(fullName))
        button.pack(pady=5, anchor="nw")
    return
def getHiddenNamesWithStatsPro():
    sessionState = client.fetch_presence(client.puuid)
    if not sessionState:
        showRegionSelect(True)
        labelRegionStats.configure(text=startTheGame, text_color=red_text)
        return
    else:
        sessionState = (sessionState.get('sessionLoopState') if isinstance(sessionState, dict) else None)
        if sessionState is None:
            try:
                client.pregame_fetch_match()
                sessionState = "PREGAME"
            except Exception:
                try:
                    client.coregame_fetch_match()
                    sessionState = "INGAME"
                except Exception:
                    sessionState = "MENUS"
        defplayers = []
        atkplayers = []
    if sessionState == "INGAME":
        disProButtons()
        buttonStartText.configure(text='Getting Hidden Names and Stats...', text_color=white_text)
        currentMatch = client.coregame_fetch_match()
        for index, player in enumerate(currentMatch['Players'], start=1):
            playerStats = getPlayerStats(player, player['TeamID'], f"Player{index}")
            if(playerStats["side"] == "Defender"):
                defplayers.append(playerStats)
            if(playerStats["side"] == "Attacker"):
                atkplayers.append(playerStats)
        if (not defplayers) and (not atkplayers):
            enProButtons()
            buttonStartText.configure(text='No Players Found', text_color=red_text)
            return
    elif sessionState == "PREGAME":
        disProButtons()
        buttonStartText.configure(text='Getting Hidden Names and Stats...', text_color=white_text)
        currentMatch = client.pregame_fetch_match()
        for index, player in enumerate(currentMatch['AllyTeam']['Players'], start=1):
            playerStats = getPlayerStats(player, currentMatch['AllyTeam']['TeamID'], f"Player{index}")
            if(playerStats["side"] == "Defender"):
                defplayers.append(playerStats)
            if(playerStats["side"] == "Attacker"):
                atkplayers.append(playerStats)
        if (not defplayers) and (not atkplayers):
            enProButtons()
            buttonStartText.configure(text='No Players Found', text_color=red_text)
            return
    else:
        buttonStartText.configure(text='Start A Game First !!', text_color=red_text)
        return
    enProButtons()
    buttonStartText.configure(text='Found Hidden Names and Stats !!', text_color=white_text)
    valueOfPlayers = [["Side Agent:", "Name:", "Rank(RR):", "Peak Rank", "WinRate%(TG)", "KD%", "HeadShot%"]]
    if defplayers:
        for defplayer in defplayers:
            fullName = defplayer["fullPlayerName"]
            agent= defplayer["agent"]
            side = defplayer["side"]
            rank = defplayer["rank"]
            rr = defplayer["rr"]
            peakRank = defplayer["peakrank"]
            wr = defplayer["wr"]
            totalGames = defplayer["totalGames"]
            kd = defplayer["kd"]
            hs = defplayer["hs"]
            defPlayer = [ f"{side} {agent}", f"{fullName}", f"{rank}({rr})", f"{peakRank}", f"{wr}({totalGames})", f"{kd}", f"{hs}"]
            valueOfPlayers.append(defPlayer)
    if atkplayers:
        for atkplayer in atkplayers:
            fullName = atkplayer["fullPlayerName"]
            agent= atkplayer["agent"]
            side = atkplayer["side"]
            rank = atkplayer["rank"]
            rr = atkplayer["rr"]
            peakRank = atkplayer["peakrank"]
            wr = atkplayer["wr"]
            totalGames = atkplayer["totalGames"]
            kd = atkplayer["kd"]
            hs = atkplayer["hs"]
            atkPlayer = [ f"{side} {agent}", f"{fullName}", f"{rank}({rr})", f"{peakRank}", f"{wr}({totalGames})", f"{kd}", f"{hs}"]
            valueOfPlayers.append(atkPlayer)
    newWindow = customtkinter.CTkToplevel(app)
    newWindow.geometry("1050x415")
    newWindow.title("Fast Pick Stats Tab")
    newWindow.resizable(0, 0)
    newWindow.after(250, lambda: newWindow.iconbitmap(image))
    newWindow.grab_set()
    tree = CTkTable(newWindow, 11, 7, values=valueOfPlayers)
    tree.pack(expand= False, pady=20)
    for i in range(1, 11):
        rowS = tree.get_row(i)
        if str(rowS[1]) == f"{client.player_name}#{client.player_tag}":
            tree.edit_row(i, text_color=yellow_text)
            continue
        if "Defender" in str(rowS[0]):
            tree.edit_row(i, text_color=blue_text)
        else:
            tree.edit_row(i, text_color=red_text)
    def kill():
        newWindow.destroy()
        newWindow.update()
    doneButton = customtkinter.CTkButton(newWindow, text="Done", command=kill)
    doneButton.pack(pady=20)
    playerAgentList = tree.get_column(0)
    if 'Side Agent:' in playerAgentList:
        playerAgentList.remove('Side Agent:')
    
    scrollUsers = customtkinter.CTkComboBox(newWindow, values=playerAgentList, state="readonly", width=180)
    scrollUsers.set(playerAgentList[0])
    scrollUsers.place(relx=0.1, rely=0.884)
    CTkScrollableDropdown(scrollUsers, values=playerAgentList)
    def CopyName():
        treeData = tree.get()
        for si in treeData:
            selectedUser = str(scrollUsers.get())
            if(selectedUser == si[0]):
                pyperclip.copy(si[1])
    buttonCopyUserName = customtkinter.CTkButton(newWindow, text="Copy Name", width=85, command=CopyName)
    buttonCopyUserName.place(relx=0.277, rely=0.884)
    return
def start():
    print("Starting...")
    global running
    running = True
    preferredAgent = str(comboboxAgents.get())
    
    with open(configPath, 'r') as f:
        config = json.load(f)
        agents = config['agents']
        currentMode = config['mapMode']
        existingMaps = config['mapAgentSelect']
        currentDelay = config['delay']
        instalockMode = config['instalockMode']
    
    buttonStart.configure(text="Stop", command=stop)
    buttonStartText.configure(text="Waiting For a Match to Begin...", text_color=white_text)
    timesLooped = 0
    playedMatches = []
    while running:
        try:
            if timesLooped > 0:
                time.sleep(currentDelay)
                
            if not running:
                print("broke the loop")
                break  
            timesLooped += 1
            print("looping")
            sessionState = client.fetch_presence(client.puuid)
            if not sessionState:
                showRegionSelect(True)
                labelRegionStats.configure(text=startTheGame, text_color=red_text)
                return
            else:
                sessionState = (sessionState.get('sessionLoopState') if isinstance(sessionState, dict) else None)
                if sessionState is None:
                    try:
                        client.pregame_fetch_match()
                        sessionState = "PREGAME"
                    except Exception:
                        try:
                            client.coregame_fetch_match()
                            sessionState = "INGAME"
                        except Exception:
                            sessionState = "MENUS"
            print(sessionState)
            if sessionState == "PREGAME":
                match = client.pregame_fetch_match()
                if (match['ID'] not in playedMatches):
                    mapId = match['MapID']
                    if not match['MapID']:
                        mapId = "Unknown"
                    mapName = MapIdToMapName(mapId)
                    if currentMode == "Map":
                        preferredAgent = existingMaps[mapName]
                    if currentMode == "Random":
                        preferredAgent = str(choice(list(agents.keys() - agents['None'])))
                    if preferredAgent == "None":
                        print(f"None IS Selected For This Map")
                        continue
                    buttonStartText.configure(text='Agent Select Screen Found', text_color= white_text)
                    client.pregame_select_character(agents[preferredAgent])
                    if instalockMode == "Lock":
                        client.pregame_lock_character(agents[preferredAgent])
                    playedMatches.append(client.pregame_fetch_match()['ID'])
                    ally = client.pregame_fetch_match()['AllyTeam']
                    ally_team = ally['TeamID']
                    ally_result = "Null"
                    side_color = "#DCE4EE"
                    if (ally_team == 'Red'):
                        ally_result = 'Attacker'
                        side_color = red_text
                    elif (ally_team == 'Blue'):
                        ally_result = 'Defender'
                        side_color = blue_text
                    buttonStartText.configure(text=f'you are: {ally_result}\nLocked {preferredAgent}', text_color=side_color) 
        except Exception as e:
            if "You are not in a pre-game" in str(e):
                print("YOU ARE NOT IN PREGAME")
                continue
            running = False
            showRegionSelect(True)
            labelRegionStats.configure(text=startTheGame, text_color=red_text)
            print(f"Error in Start: {e}")
            

def startButton():
    print("targeting Thread function start")
    selThread = threading.Thread(target=start, daemon=True)
    print("Starting thread process for select")
    selThread.start()
def getHiddenNamesWithStats():
    print("targeting Thread function names")
    selThread = threading.Thread(target=getHiddenNamesWithStatsPro, daemon=True)
    print("Starting thread process for getting hidden names")
    selThread.start()
def getLoadouts():
    print("targeting Thread function names")
    selThread = threading.Thread(target=getLoadoutsPro, daemon=True)
    print("Starting thread process for getting Loadouts")
    selThread.start()

debug = False
class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.insert(customtkinter.END, string)
        self.widget.see(customtkinter.END)

    def flush(self):
        pass
if '--debug' in sys.argv or '-d' in sys.argv:
    debug = True
    debugWindow = customtkinter.CTkToplevel(app)
    debugWindow.title("Fast Pick Debug Window")
    debugWindow.geometry("700x380")
    debugWindow.resizable(0, 0)
    debugWindow.after(250, lambda: debugWindow.iconbitmap(image))
    debugWindow.after(250, debugWindow.focus_force)

    outputPrint = customtkinter.CTkTextbox(debugWindow, wrap=customtkinter.WORD)
    outputPrint.pack(fill="both", expand=True, padx=10, pady=10)

    sys.stdout = TextRedirector(outputPrint, "stdout")
    sys.stderr = TextRedirector(outputPrint, "stderr")

if ranBefore != True:
    showRegionSelect()
elif ranBefore == True:
    client = Client(region=region)
    try:
        client.activate()
        showSelected()
    except Exception as e:
        if debug == True :
            showSelected()
        else:
            showRegionSelect(True)
            labelRegionStats.configure(text=startTheGame, text_color=red_text)
            print(f'{e}')

# Check For Updates logic

# version deta
current_ver = "1.0"
versionLabel = customtkinter.CTkLabel(app, text=f"Version {current_ver}", anchor="w", fg_color="transparent")
versionLabel.place(rely=0.956, relx=0.008)

#github (deleted)

#Discord = yury_zzzzz

# botton setting
buttonStart.configure(state="normal", command=startButton)
buttonStartDodge.configure(state="normal", command=dodgeMatch)
buttonStartCheck.configure(state="normal", command=checkSides)
buttonGetNames.configure(state="normal", command=getHiddenNames)
buttonGetNamesWithStats.configure(state="normal", command=getHiddenNamesWithStats)
buttonAgentsMap.configure(command=mapMenu)
buttonGetLoadouts.configure(state="normal", command=getLoadouts)

app.mainloop()


