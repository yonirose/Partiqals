# -*- coding: utf-8 -*-
from pymongo import MongoClient
import gridfs

client = MongoClient()
db = client.partiqals
partdb = db.part
distdb = db.dist
manufacdb = db.manufac
pdfdb = gridfs.GridFS(client.datasheet_pdf)
invendb = db.inventory
cursordb = db.cursor
