import csv
import os

class Report():
    def __init__(self):
        self.field_names = ['Tamanho do plano', 'Agente', 'recompensa', 'distancia percorrida', 'Alcançou', 'Média recompensa']
                
        if os.path.exists('report2.csv'):
            with open('report2.csv', 'r') as csvfile:
                sniffer = csv.Sniffer()
                self.has_header = sniffer.has_header(csvfile.read(2048))
                csvfile.seek(0)
                
            if (not self.has_header):
                with open('report2.csv', 'w', newline='') as csvfile:
                    fieldnames = ['Tamanho do plano', 'Agente', 'recompensa', 'distancia percorrida', 'Alcançou', 'Média recompensa']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
        else: 
            with open('report2.csv', 'w', newline='') as csvfile:
                fieldnames = ['Tamanho do plano', 'Agente', 'recompensa', 'distancia percorrida', 'Alcançou', 'Média recompensa']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
    
    def add_row(self, n, agt, recompensa, dist, alcancou):
            with open('report2.csv', 'a', newline='') as csvfile:
                self.file = csvfile
                self.writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
                
                if (alcancou and dist > 0):
                   media_recompensa = str(recompensa/dist).replace('.', ',')
                else:
                    media_recompensa = 0
                
                self.writer.writerow({'Tamanho do plano': f'{n*n}', 'Agente': f'{agt}','recompensa': f'{recompensa}', 'distancia percorrida': f'{dist}', 'Alcançou': f'{alcancou}', 'Média recompensa': f'{media_recompensa}'})
        