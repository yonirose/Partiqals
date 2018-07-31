# -*- coding: utf-8 -*-
from pymongo import MongoClient
import gridfs

client = MongoClient()
db = client.partipedia
partdb = db.part
distdb = db.dist
manufacdb = db.manufac
metadb = db.meta
pdfdb = gridfs.GridFS(client.datasheet_pdf)
invendb = db.inventory
cursordb = db.cursor