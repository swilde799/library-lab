import os
import hashlib
from gridfs import GridFSBucket
from db_config import DBConfig

db = DBConfig.get_db()
fs = GridFSBucket(db, bucket_name="fs")

def upload_file(file_path, filename=None):
    if not filename: filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        fs.upload_from_stream(filename, f)
    DBConfig.log_action("insert", "fs.files", filename)

def list_files():
    return list(db.fs.files.find({}, {"filename": 1, "length": 1, "uploadDate": 1}))
