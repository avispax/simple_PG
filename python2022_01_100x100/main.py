import os
import json


def generate_json():

    APDU_NAME = '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345'

    list = []
    for i in range(100):

        aid = format(i, 'x').rjust(32, 'A')

        d2list = []
        for j in range(100):
            d2 = {'apduId': aid,
                  'apduName': APDU_NAME,
                  'apduCommand': format(j, 'x').rjust(506, 'B')}
            d2list.append(d2)

        d1 = {'select': {'aid': aid, 'p2': '00'},
              'securityLevel': '33',
              'apduCommandList': d2list
              }
        list.append(d1)

    return list


def main():

    d = {'header': {'requestId': 'RSV123456S123456789012ABCDEF1234',
                    'operationType': '00000001',
                    'operationId': 'OSV123456S123456789012ABCDEF1234'
                    },
         'payload': {'serviceId': 'SV9STZ01',
                     'spAppId': 'DATZ1Z01',
                     'seManagementId': '1',
                     'seId': 'A00143',
                     'spAppleId': 'SATZ1Z01',
                     'needMoreProcess': False,
                     'previousProcessId': 'null',
                     'apduCommandInfoList': generate_json()
                     }
         }

    with open('./myJson.json', 'w') as f:
        json.dump(d, f)


if __name__ == '__main__':

    print('★Start - PG')

    # カレントディレクトリをこのファイルが存在するところに
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('- カレントディレクトリ : ' + os.getcwd())

    main()

    print('★End - PG')


# 以下、自分用メモ
