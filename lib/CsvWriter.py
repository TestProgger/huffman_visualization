import csv
from .Code import Code
class CsvWriter:
    def __init__(self , filename : str):
        self.filename = filename
        self.prepared_dict = []

    def prepare_data(self , haffman_col : list[Code], code_comb : list[str] , Ne : list[str] , pNe : list[float] ):
        for ind in range(0 , len(haffman_col)):
            self.prepared_dict.append(
                {
                    'Xi' : haffman_col[ind].code,
                    'p(Xi)' : haffman_col[ind].probability,
                    'Кодовая комбинация' : code_comb[ind] ,
                    'Nэi' : Ne[ind],
                    'p(xi)*Nэi' : pNe[ind]
                }
            )

    def write(self):
        headers = [ 'Xi' , 'p(Xi)' , 'Кодовая комбинация' , 'Nэi' , 'p(xi)*Nэi' ]
        print(self.prepared_dict)
        with open("./out/" + self.filename + ".csv" , "w" , encoding='utf-8') as csvW:
            csv_writer = csv.DictWriter(csvW  , lineterminator="\r", fieldnames=headers)
            csv_writer.writeheader()
            for row in self.prepared_dict:
                csv_writer.writerow(row)