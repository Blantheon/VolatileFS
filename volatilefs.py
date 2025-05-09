import apsw
import os
from typing import Iterable
from io import BytesIO
#from hexdump import hexdump

def set_environnement():
    if os.path.isfile('db'):
        os.remove('db')
    c = apsw.Connection('db')
    c.execute('CREATE TABLE empty( age INT PRIMARY KEY NOT NULL);')
    c.execute('DROP TABLE empty')
    del c


def human_readable_size(size_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {units[i]}"


class VolatileFS(apsw.VFS):
    def __init__(self, db_bytes, vfsname='volatilefs', basevfs=''):
        self.vfs_name = vfsname
        self.base_vfs = basevfs
        self.db: bytes = BytesIO(db_bytes)
        super().__init__(self.vfs_name, self.base_vfs)
    
    def xOpen(self, name: str, flags: Iterable[int]):
        self.file = VolatileFSFile(self.db, self.base_vfs, name, flags)
        return self.file
        

class VolatileFSFile(apsw.VFSFile):
    def __init__(self, db, inheritfromvfsname, filename, flags):
        self.buffer = db
        super().__init__(inheritfromvfsname, filename, flags)
    
    def xClose(self):
        super().xClose()

    def xRead(self, amount: int, offset: int):
        self.buffer.seek(offset)
        data = self.buffer.read(amount)
        if len(data) < amount:
            data += b'\x00' * (amount - len(data))
        return data
        #return super().xRead(amount, offset)

    def xWrite(self, data: bytes, offset: int):
        if len(self.buffer.getvalue()) < offset + len(data):
            size = offset + len(data) - len(self.buffer.getvalue())
            self.buffer.seek(0, 2)
            self.buffer.write(b'\x00' * size)
        self.buffer.seek(offset)
        self.buffer.write(data)
        
    def xTruncate(self, size: int):
        current = self.buffer.getvalue()
        self.buffer = current[:size]

    def xFileSize(self) -> int:
        return len(self.buffer.getvalue())




set_environnement()

with open('db', 'rb') as f:
    bytes = f.read()

vfs = VolatileFS(bytes)
con = apsw.Connection('db', vfs=vfs.vfs_name)

with open('buffer1', 'wb') as f:
    f.write(vfs.file.buffer.getvalue())

con.execute('''CREATE TABLE password(\
                        name TEXT PRIMARY KEY NOT NULL,\
                        user TEXT,\
                        password TEXT NOT NULL,\
                        url TEXT,\
                        description TEXT);''')

with open('buffer2', 'wb') as f:
    f.write(vfs.file.buffer.getvalue())

con.execute('INSERT INTO password VALUES ("google","Myman", "A Good Pass", "https://google.com", "A Big Description")')

with open('buffer3', 'wb') as f:
    f.write(vfs.file.buffer.getvalue())

s = len(vfs.file.buffer.getvalue())
print(f'The bytesIO has a size of: {human_readable_size(s)}')

for i in con.execute('SELECT * FROM password'):
    print(i)

