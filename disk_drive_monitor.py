import os
import requests
from bs4 import BeautifulSoup
import openpyxl
import json

# from slugify import slugify

urls_list = [
    'http://172.168.1.202:61220/',
    # 'http://192.168.10.119:61220/',
]

file_name = os.path.normpath('C:/logs/hdd_state.json')
logs_path = os.path.normpath('C:/logs')
lsi_log = 'megasas.log'
mega_cli = os.path.normpath('C:/scripts/MegaCLI/MegaCli') + ' -AdpBbuCmd -a0 > null'

hdd_state = []


#     {
#         'server_name': '',
#         'bbu_state': '',
#         'disk_drive': [
#             {
#                 'drive_id': '',
#                 'wlc': '',
#                 'realloc': ''
#             }
#
#         ]
#     }
# ]


def get_hdd_state(url):
    item = {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    item['server_name'] = soup.body.div.div.div.contents[4].contents[1].contents[3].text.strip()
    item['bbu_state'] = ''
    item['disk_drive'] = []

    if 'LENOVOX3550M5' in item['server_name']:
        os.chdir(logs_path)
        command = 'del ' + os.path.join(logs_path, lsi_log)
        os.system(command)
        command = mega_cli
        os.system(command)
        with open(os.path.join(logs_path, lsi_log), 'r') as f:
            for ff in f.readlines():
                if 'Battery State' in ff:
                    item['bbu_state'] = ff[15:].strip()
                    break

        for item2 in soup.findAll('a'):
            disk_drive = {}
            try:
                if 'drive' in item2['name']:
                    realloc, wlc = '100', '100'
                    drive_id = item2.findNext().div.table.contents[5].contents[3].text.strip()
                    drive_attrs = item2.findNext().div.contents[23].table.findAll('tr', 'rg')
                    for drive_attr in drive_attrs:
                        if 'Reallocated Sectors Count' in drive_attr.contents[2]:
                            realloc = int(drive_attr.contents[4].text.strip())
                            continue
                        if 'Wear Leveling Count' in drive_attr.contents[2]:
                            wlc = int(drive_attr.contents[4].text.strip())
                            continue
                    disk_drive['drive_id'] = drive_id
                    disk_drive['wlc'] = wlc
                    disk_drive['realloc'] = realloc
                    item['disk_drive'].append(disk_drive)
            except KeyError:
                continue
        hdd_state.append(item)

    # if 'R710' in item['server_name']:
    #     for item2 in soup.findAll('td'):
    #         if 'Hard Disk Serial Number' in item2.text:
    #             disk_drive = {}
    #             drive_id = item2.parent.contents[3].text.strip()
    #             if drive_id == '?':
    #                 continue
    #             print(drive_id)
    #             for drive_attrs in item2.parent.parent.parent.findAll('h3'):
    #                 if drive_attrs.text == 'S.M.A.R.T.':
    #                     drive_attrs = drive_attrs.nextSibling
    #                     drive_attrs = drive_attrs.findAll('td')
    #                     for _ in drive_attrs:
    #                         if 'Write errors corrected without substantial delay' in _:
    #                             print(_)
    #                     # print(drive_attrs)
    #
    #             # drive_attrs = item2.findNext().div.contents[23].table.findAll('tr', 'rg')
    #
    #             #     for drive_attr in drive_attrs:
    #             #         if 'Reallocated Sectors Count' in drive_attr.contents[2]:
    #             #             realloc = drive_attr.contents[4].text.strip()
    #             #             continue
    #             #         if 'Wear Leveling Count' in drive_attr.contents[2]:
    #             #             wlc = drive_attr.contents[4].text.strip()
    #             #             continue
    #             #     disk_drive['drive_id'] = drive_id
    #             #     disk_drive['wlc'] = wlc
    #             #     disk_drive['realloc'] = realloc
    #             #     item['disk_drive'].append(disk_drive)
    #             # except KeyError:
    #             #     continue
    #             # hdd_state.append(item)


def main():
    for item in urls_list:
        get_hdd_state(item)
    with open(file_name, 'w') as fp:
        json.dump(hdd_state, fp, indent=2)
    print(json.dumps(hdd_state, indent=2))


if __name__ == '__main__':
    main()
