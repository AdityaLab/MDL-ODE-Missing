import csv

if __name__ == '__main__':
    with open ('Covid19CasesWH.csv','w') as CSVFileW:
        SolutionFile = csv.writer(CSVFileW)
        with open ('data.csv','r') as CSVFileR:
            DataFile = csv.reader(CSVFileR)
            Sentence = next(DataFile)  
            SolutionFile.writerow(['OnsetDate','CaseNum','CaseSum','UncaseNum','UncaseSum'])
            casesyesterday = 0
            for Sentence in DataFile:
                X,date,county,state,fips,cases,deaths = Sentence
                CaseNum = int(cases)-int(casesyesterday)
                CaseSum = int(cases)
                casesyesterday = cases
                UncaseNum = 4 * CaseNum
                UncaseSum = 4 * CaseSum
                SolutionFile.writerow([date,str(CaseNum),str(CaseSum),str(UncaseNum),str(UncaseSum)])
