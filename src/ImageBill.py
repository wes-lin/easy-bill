
import os
from Bill import Bill

class ImageBill(Bill):

    def __init__(self,path,context):
        super().__init__(context)
        self.data['sourcePath'] = path
        basename = os.path.basename(path)
        self.data['fileName'] = basename
        self.data['ext'] = os.path.splitext(basename)[-1]