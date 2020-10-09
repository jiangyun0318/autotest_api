# coding=utf-8
from deepdiff import DeepDiff
from jsonpath_rw import parse
import json
from Util.codition_data import get_depend_data
from Common.get_sql import mysql


# 校验json格式
def handle_result_json(dict1, dict2):

    if isinstance(dict1, dict) and isinstance(dict2, dict):
        cmp_dict = DeepDiff(dict1, dict2, ignore_order=True).to_dict()
        if cmp_dict.get("dictionary_item_added"):
            return False
        else:
            return True
    return False


# 校验json部分字段
def handle_result_json_section(res_data, res_key):

    key = res_key.split('==')[0]

    if not isinstance(res_data, dict):
        res_data = json.loads(res_data)
    json_exe = parse(key)
    madle = json_exe.find(res_data)

    res = [math.value for math in madle][0]
    json_s = res_key.split('==')[1]

    return res, json_s

    # if str(res) == (res_key.split('==')[1]):
    #     return True
    # else:
    #     return False


# 校验sql预期值
def handle_result_sql(res_data, res_key):

    sql_data = ''
    depend = res_key.split('==')[0]
    depend_data = get_depend_data(res_data, depend)
    sql = res_key.split('==')[1]

    result = mysql.getOne(sql)

    for res in result:
        sql_data = result[res]

    return depend_data, sql_data


if __name__ == "__main__":
    dict2 = {
                "code": 0,
                "msg": "请求成功",
                "data": {
                    "userId": 216,
                    "userName": "江云",
                    "password": "",
                    "userType": "general",
                    "companyId": 238,
                    "mobile": "+86 15618779297",
                    "token": "f37bb18b-6ca1-4cbe-89f0-e6aa1531325d",
                    "clientType": "WEB",
                    "updated": "false"
                },
                "timestamp": 1585727018400
            }
    key = '"userName": "江云"'
    print(handle_result_json_section(dict2, 'data.userName==江云'))

    # dict1={"code":0,"msg":"请求成功","data":{"pageNum":1,"pageSize":10,"size":1,"startRow":1,"endRow":1,"total":23,"pages":1,"list":[{"page":'',"pageSize":'',"propertyId":11429,"propertyName":"金砖大厦东方汇经中心","countryId":1,"provinceId":310000,"cityId":310100,"countyId":310107,"provinceName":"上海","cityName":"上海市","countyName":"普陀区","address":"中山北路1958号","propertyAddress":"上海上海市普陀区中山北路1958号","propertyLat":31.2558670000,"propertyLon":121.4391040000,"subwayLat":31.2528250000,"subwayLon":121.4368640000,"nearestDistance":"690","nearestDistanceDesc":'',"totalArea":47000.00,"developer":"华源集团","averagePrice":4.00,"contactName":'',"businessContact":'',"propertyCompany":"联源物业","broadBand":"177,178,180,253,179,254","propertyCosts":25.00,"propertyCostsUnit":1,"groundParkingFee":'',"undergroundParkingFee":'',"groundParkingSpaceNum":20,"undergroundParkingSpaceNum":50,"parkingSpaceTotal":70,"parkingFreeRelated":'',"propertyPics":"[{\"url\":\"https://image.maxoffice.com/grasper/20200213/1581583989383ac013c4b824943278e63848e2b89043a.png\",\"id\":372,\"label\":\"实景图\"},{\"url\":\"https://image.maxoffice.com/grasper/20200213/1581583994836ff1a9811611b461481f03ab6971411d3.png\",\"id\":372,\"label\":\"实景图\"},{\"url\":\"https://image.maxoffice.com/grasper/20200225/1582617665833cb32f76cda89477bbc51484f23c25889.png\",\"id\":372,\"label\":\"实景图\"}]","famousCompany":'',"propertyIntroduction":'',"propertyLabel":'',"vrProperty":'',"vrUrl":'',"reviewStatus":0,"createdId":110,"createdDate":"2019-12-05 10:10:26","updatedId":138,"updatedDate":"2020-02-25 16:01:28","enabled":1,"deleted":0,"businessDistrictName":"中山北路","buildingArr":"11429_华源世界广场","buildingCount":1,"subwayArr":'',"businessDistrictArr":"2282","majorUserArr":"68,254","createdName":"Tina Xu","updatedName":"孙志杰","propertyCostUnitStr":"元/㎡/月","reviewStatusStr":"未提交审核","subwayStationList":'',"buildingList":[{"buildingName":"华源世界广场","buildingId":11429}],"broadBandStr":'',"fullPropertyCosts":'',"fullGroundParkingFee":'',"fullUndergroundParkingFee":'',"businessDistrictList":[{"businessId":2282,"businessName":"中山北路"}],"majorUsers":"龚国超，弥宪才","vrPropertyStr":'',"propertyLabelList":'',"propertyLabelStr":'',"safePage":1,"safePageSize":10}],"prePage":0,"nextPage":0,"isFirstPage":1,"isLastPage":1,"hasPreviousPage":0,"hasNextPage":0,"navigatePages":8,"navigatepageNums":[1],"navigateFirstPage":1,"navigateLastPage":1,"firstPage":1,"lastPage":1},"timestamp":1591864230077}
    #
    # print(handle_result_sql(dict1,'data.total==select count(*) from ob_property_info where deleted=0'))
