from json import dumps as stringify
from requests import get, post, Response

def put_blob(filename, file_bytes) -> dict:


    try:
        response: Response = post(
            "https://tempfile.org/api/upload/local",
            files={"files": (filename, file_bytes)},
            data={"expiryHours": "1"}
        )

        if not response.ok:
            raise Exception(f"HTTP {response.status}: {response.statusText}")

        result: dict = response.json()

        if not result.get("success", False):
            raise Exception("No success!")
        
        return result
    except Exception as error:
        print('Upload failed:', error.message)
    
    return {"success": False}

def get_blob(url) -> dict:
    response: Response = get(url)
    if not response.ok:
        print("Response not OK")
        return {"success": False}
    body: dict = response.json()
    if not body.get("success", False):
        print("No success!")
        return {"success": False}
    return body

def get_bytes(body: dict):
    if not body.get("success", False):
        raise Exception("Get bytes fail")
    response = get(f"https://tempfile.org{body["file"]["downloadUrl"]}")
    if not response.ok:
        raise Exception("Get bytes fail, response not ok")
    return response.content