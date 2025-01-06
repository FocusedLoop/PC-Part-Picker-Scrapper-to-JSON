import json, re

buildFile = r"C:\Users\joshu\OneDrive\Desktop\temp_python_workspace\bot\scrappedFiles\pc_build_parts.json"
partMapFile = r""

with open(buildFile, "r") as file:
    json_data = json.load(file)

# price = json_data[0]["Part List"]["Parts"][5]["Price"]
# part = json_data[0]["Part List"]["Parts"][5]["Name"]
# print(part, price)

# x = re.findall(r"\bRX 580", part)
# print(x)

def find_null(json):
    missingPrices = []
    jsonLength = json[-1]["Build"] + 1
    for i in range(jsonLength):
        listLength = len(json_data[i]["Part List"]["Parts"])
        for j in range(listLength):
            part = json_data[i]["Part List"]["Parts"][j]["Name"]
            price = json_data[i]["Part List"]["Parts"][j]["Price"]
            if price == None:
                missingPrices.append(part)
    return missingPrices


print(find_null(json_data))
print(len(find_null(json_data)))