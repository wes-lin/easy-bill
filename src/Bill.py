import re
import arrow

class Bill:
    
    def __init__(self , context):
        self.context = re.sub(r"^\s+|￥|\n|\r","",context)
        self.data = {}

    def matchs(self):
        return [r'下单时间(?P<orderDate>[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})',
                r'总计(?P<money>[0-9]+.[0-9]+)',
                r'合计(?P<money>[0-9]+.[0-9]+)']

    def extract(self):
        for match in self.matchs():
            objMatch = re.search(match,self.context)
            if(objMatch):
                for key in objMatch.groupdict().keys():
                    val = ''
                    #时间转成统一格式 YYYY-MM-DD
                    if key.find('Date')>=0:
                        val = arrow.get(re.sub('[\u4e00-\u9fa5]','',objMatch.group(key))).format('YYYY-MM-DD')
                    else:
                        val = objMatch.group(key)
                    self.data[key] = val

    def getData(self):
        return self.data

# t = Bill('adad下单时间2021-11-0317:48总优惠￥19总计￥39.1adadad')
# t.extract()
# print(t.data)