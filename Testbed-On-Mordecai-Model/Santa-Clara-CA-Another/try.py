import numpy as np

if __name__ == '__main__':
    ReportedSum = []
    with open('us-counties-source.txt','r') as DataFile:
        Sentence = DataFile.readline()
        for counter in range(61):
            Sentence = DataFile.readline()
            if not Sentence:
                print ("Error!")
            Sentence = Sentence.split(',')
            ReportedSum.append(int(Sentence[5]))

    Reported = [0]*61
    Reported[0] = ReportedSum[0]
    for counter in range(1,61):
        Reported[counter] = ReportedSum[counter] - ReportedSum[counter-1]
        Reported = np.array(Reported)

    D = Reported / 0.1

    SumD = [0]*61
    SumD[0] = D[0]
    for counter in range(1,61):
        SumD[counter] = SumD[counter-1] + D[counter]

    with open('us-counties.txt','w') as WriteFile:
        with open('us-counties-source.txt','r') as ReadFile:
            Sentence = ReadFile.readline()
            Sentence = Sentence[0:len(Sentence)-1] + ',uncases\n'
            WriteFile.write(Sentence)
            for counter in range(61):
                Sentence = ReadFile.readline()
                if not Sentence:
                    print ("Error!")
                Sentence = Sentence[0:len(Sentence)-1] + ',' + str(int(SumD[counter]-ReportedSum[counter])) + '\n'
                WriteFile.write(Sentence)
