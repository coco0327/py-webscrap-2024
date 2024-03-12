import csv


class CSVWriter:
    def __init__(self, filename):
        # CSV 파일 작성 객체 초기화
        fieldnames = ["Title", "Company", "Location", "Reward", "URL"]
        self.filename = f"{filename} jobs.csv"
        self.fieldnames = fieldnames
        
    def write_file(self, data):
        # 데이터를 CSV 파일로 작성
        with open(self.filename, 'w', newline='\n') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for job in data:
                writer.writerow(job)