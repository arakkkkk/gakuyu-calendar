import glob
from datetime import datetime

def getJsonByDirectory(path) -> dict:
    files = glob.glob(path+"/*")
    res_json = {}
    for file in files:
        f = open(file)
        file_content = f.read()
        f.close()
    
        equip_category = file.split("/")[-1].split(".")[0]
        equipments = [ row.split(",") for row in file_content.split("\n") if len(row) > 0]
        res_json[equip_category] = equipments

    return res_json

def request2datetime(datetime_json):
    date = datetime_json["date"]
    time = datetime_json["time"]
    res_datetime = datetime(
            int(date.split("-")[0]),
            int(date.split("-")[1]),
            int(date.split("-")[2]),
            int(time.split(":")[0]),
            int(time.split(":")[1])
            )
    return res_datetime

