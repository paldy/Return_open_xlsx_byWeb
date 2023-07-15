from typing import List
from typing_extensions import Annotated
from fastapi import FastAPI, Form, UploadFile, Request, HTTPException, File
from starlette.responses import FileResponse 
from pydantic import EmailStr
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os


app = FastAPI(title="password of xlsx file")

HOW_FAT_THE_FILE_IS = 1000000  # max_size of the file
FILES_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

ACCOUNT_SID = 'AC1ac06bxxxxxxxxe0ebaf39019a19a349'
AUTH_TOKEN = '59f74f70xxxxxxxxxxxxxxx9ffb06'

# from and to - phone numbers:
FROM = '+1415xxxxx86'
TO = '+37xxxxxxxxx'



def safe_file(files: list, email: str):
    try:
        os.mkdir(email)
    except FileExistsError:
        pass
    for f in files:
        with open(f"{email}/{f.filename}", "wb") as fb:
            fb.write(f.file.read())


def send_wamessage(email: str):
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            from_=f'whatsapp:{FROM}',
            body=f'You have got a new task to crack xlsx file from {email}',
            to=f'whatsapp:{TO}'
            )
        print(f'message.error_code: {message.error_code}')
        print(f'message.status:     {message.status}')
        print(f'message.price:      {message.price}')
        print()
    except TwilioRestException as e:
        print('Catch error here', e)  


@app.post("/uploadfiles/")
async def create_upload_files(
        request: Request, 
        files: Annotated[List[UploadFile], File(description="Multiple files as UploadFile")], 
        email: EmailStr = Form(...)
        ):

    headers_size = request.headers["content-length"]
    if len(files)>0 and (int(headers_size)/len(files) > HOW_FAT_THE_FILE_IS):
        raise HTTPException(400, detail="Too big files")

    for f in files:
        if f.content_type != FILES_CONTENT_TYPE:
            raise HTTPException(400, detail="Invalid document type")

    safe_file(files, email)
    send_wamessage(email)

    return "File(s) is uploaded successfully"


@app.get("/")
async def main():
    return FileResponse('index.html')
