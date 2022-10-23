def open_json(fileName):
    import json
    if fileName != '':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName, mode = 'r', encoding = "utf-8") as file:
                data = json.loads(file.read())
                file.close()
                return data

def write_json(fileName, enter):
    import json
    if fileName != '':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName, mode = 'w', encoding = "utf-8") as file:
                json.dump(enter, file)
                file.close()

def print_time(enter):
    import time
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] {enter}')