import re
import pdfplumber
import os

from Bill import Bill

class PDFBill(Bill):

    rowDic = [
        {'key':'money','index':7,'pattern':r'[0-9]+.[0-9]+'}
        ]

    def __init__(self,path):
        self.pdf = pdfplumber.open(path)
        context = ''
        for page in self.pdf.pages:
            context += page.extract_text()
        super().__init__(context)
        self.data['sourcePath'] = path
        basename = os.path.basename(path)
        self.data['fileName'] = basename
        self.data['ext'] = os.path.splitext(basename)[-1]

    def __del__(self):
        self.pdf.close()

    def matchs(self):
        return [r'申请日期:(?P<applyDate>[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})', 
                r'开票日期:(?P<applyDate>[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日)',
                r'合计.*（小写）(?P<money>[0-9]+.[0-9]+)',
                r'行程起止日期:(?P<orderDate>[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})'
                ]
    
    def isDiDiTravel(self):
        return self.context.find('DIDI TRAVEL')>=0
    
    def isInvoice(self):
        return self.context.find('电子普通发票')>=0
    
    def isDiDiInvoice(self):
        return self.isInvoice() and self.context.find('滴滴出行科技有限公司')>=0

    def extract(self):
        super().extract()
        if self.isDiDiTravel():
            self.data['fileName'] = '滴滴出行行程报销单'
            page = self.pdf.pages[0]
            table = page.extract_tables()[1]
            dataRow = table[1]
            for i in self.rowDic:
                if i['pattern']:
                    m = re.search(i['pattern'],dataRow[i['index']])
                    if m:
                        self.data[i['key']] = m.group(0)
                else:
                    self.data[i['key']] = dataRow[i['index']]
        if self.isInvoice():
            self.data['fileName'] = '电子发票'
        if self.isDiDiInvoice():
            self.data['fileName'] = '滴滴'+self.data['fileName']
