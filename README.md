# VolatileFS

VolatileFS is a custom Virtual File System (VFS) for APSW (Another Python SQLite Wrapper). 
This personal project is designed to load an SQLite database from disk into RAM and perform all subsequent operations entirely in memory.

By working exclusively in RAM, VolatileFS allows applications to handle decrypted or sensitive data without ever writing it back to persistent storage. 
This approach is particularly useful for scenarios where data confidentiality is critical, such as when working with encrypted databases that must be decrypted at runtime.

### Key Features

    Loads a database file into memory at startup.

    All read/write operations occur in RAM only.

    Avoids writing sensitive or decrypted data back to disk.

    Built for experimentation and secure, temporary data handling.
