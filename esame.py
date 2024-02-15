
class ExamException(Exception):
    pass
def media_lista(lista):
    n = len(lista)
    somma=0
    for element in lista:
        somma = somma + element[1]
    return somma/n

class CSVTimeSeriesFile():

    def __init__(self, name):
        self.name = name

    def get_data(self):

        flag = 0    #uso una flag per far proseguire il programma

        try:     #controllo che il file esista
            my_file = open(self.name, 'r')
        except: 
            raise ExamException('Il nome del file non è valido')

        

        self.dati = []
        precedente = []
        test = []
        for line in my_file:   #itero su ogni riga del file

            flag = 0
            riga = []
            riga = line.split(',')


            if riga[0] != "date":    #ignoro la prima riga di testo

                try:#controllo che il numero dei passeggeri sia valido
                    riga[1] = int(riga[1])
                    if riga[1]<=0:
                        flag=1
                except:
                    flag=1

                  #controllo che la data sia valida
                try:
                    test = riga[0].split('-')
                    if len(test) != 2:
                        flag=1
                    test[0]= int(test[0])
                    test[1]= int(test[1])
                    if test[1]>12 or test[1]<0:
                        flag=1



                except:
                    flag=1


                riga=riga[0:2]
                if flag==0:#controllo l'ordine
                    if precedente != []:
                        if test[0]<precedente[0] or (test[1]<=precedente[1] and test[0]==precedente[0]):
                            raise ExamException('La lista non è ordinata')
                    self.dati.append(riga)
                    precedente = test
        if self.dati == []:
            raise ExamException('La lista non ha alcun valore valido')
        my_file.close()
        return self.dati

def compute_increments(time_series, first_year, last_year):    
    
    if not isinstance(time_series,list):#controlli sulla lista
        raise ExamException("L'input non è una lista")
    if len(time_series)==0:
        raise ExamException("La lista è vuota")

    try:#uso questo blocco try per verificare che la lista in input sia corretta sfruttando le operazioni stesse, devo solo aggiungere qualche controllo (ved. variabile prova)
        flag1=0    #controllo gli input degli anni
        flag2=0
        if not isinstance(first_year,str) or not isinstance(last_year,str):
            raise ExamException('Estremi non validi')
        try:
            first_year = int(first_year)
            last_year = int(last_year)
        except:
            raise ExamException('Estremi non validi')
        if not last_year>0 or not first_year>0:
            raise ExamException('Estremi non validi')
        precedente = []
        for item in time_series:
           
                
            
            
            prova=item[0].split('-')#controllo aggiuntivo sui mesi
            prova[1]=int(prova[1])
            if not len(prova)==2:
                raise Exception('')#eccezioni vuote che mi danno l'exception giusta dopo il try
            if not 0<prova[1]<=12:
                raise Exception('')
            
            
            item[0]=item[0].split('-')[0:1]#tiro fuori l'anno in numero intero
            item[0][0]=int(item[0][0])
            if item[0][0] == first_year:#controllo che gli estremio siano nel file con un sistema di flag
                flag1=1
            if item[0][0]== last_year:
                flag2=1
    
        if flag1==0 or flag2==0:
            raise ExamException('Estremi non validi')
        anno = first_year
    
        diz = {}
        while anno<last_year: #uso le list comprehension per creare una sottolista per ogni anno
            sub1 = [item for item in time_series if item[0][0] == anno]#metto due volte [0] perchè item[0] è una lista di un unico elemento
            sub2 = [item for item in time_series if item[0][0] == anno+1]
            anno1 = anno
            while len(sub2) == 0: #trovo la sottolista successiva non vuota più vicina
                anno = anno+1
                sub2 = [item for item in time_series if item[0][0] == anno+1]
            

            diz[str(anno1)+'-'+str(anno+1)]= media_lista(sub2)-media_lista(sub1) #calcolo dell'incremento

            anno=anno+1 
    except ExamException:
        raise ExamException('Estremi non validi')
    except:
        raise ExamException('La lista in input non è corretta o nella forma giusta')
    
    
    return(diz)


