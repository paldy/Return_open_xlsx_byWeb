import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        "upload_app:app",
        # host='0.0.0.0',
        host='gogo199.online',
        port=6712,
        reload=True
    )

