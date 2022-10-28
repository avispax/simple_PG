import plyvel

# db = plyvel.DB(r'C:\\Users\\aviee\\AppData\\Roaming\\Vampire_Survivors\\Local Storage\\leveldb')
db = plyvel.DB(r'C:\Users\aviee\AppData\Roaming\Vampire_Survivors\Local Storage\leveldb', create_if_missing=False)

for key, value in db:
    print('"{0}"\t"{1}"'.format(key, value))

db.put(b'_file://\x00\x01CapacitorStorage.Coins', b'\x0199999')
