# Definizione di una classe di eccezione personalizzata per gestire errori specifici
class ExamException(Exception):
    pass

# Definizione della classe che rappresenta un file CSV contenente una serie temporale
class CSVTimeSeriesFile:
    
    # Metodo costruttore
    def __init__(self, name):
        
        if not isinstance(name, str):
            raise ExamException(
                'Invalid type for name, only string supported. Got "{}"'.format(
                    type(name)
                )
            )
        # Assegna il nome del file all'attributo dell'istanza
        self.name = name

    # Metodo per ottenere i dati dal file CSV
    def get_data(self):
        output = []

        try:
            with open(self.name, "r") as my_file:
                for index, line in enumerate(my_file):
                    
                    line = line.strip()
                    if line == "" or line.startswith("#"):
                        continue

                    elements = line.split(",")

                    if elements[0] != "epoch" and elements[1] != "temperature":
                        try:
                            # Converte il primo elemento in intero (epoch) e il secondo in float (temperatura)
                            epoch = int(elements[0])  # casting ad int
                            temp = float(elements[1])
                        except ValueError:
                            continue  # Ignora la riga se ci sono errori nel cast
                        except IndexError:
                            continue  # Ignora la riga se non ci sono abbastanza elementi

                        # Controllo se l'epoch è in ordine crescente e non duplicato
                        if len(output) > 0 and epoch <= output[-1][0]:
                            raise ExamException(
                                "Gli epoch non sono in ordine o ci sono duplicati"
                            )
                        
                        output.append([epoch, temp])

        except FileNotFoundError:
            # Gestisce il caso in cui il file non esiste
            raise ExamException(
                f'Errore nella lettura del file: "{self.name}" non trovato'
            )

        except Exception as e:
            raise ExamException(f"Errore nella lettura del file: {str(e)}")

        # Controlla se il file è vuoto
        if len(output) == 0:
            raise ExamException("File vuoto")

        # Restituisce i dati raccolti
        return output

# Funzione per calcolare la massima differenza giornaliera di temperatura
def compute_daily_max_difference(time_series):

    # Controlla se time_series è una lista
    if not isinstance(time_series, list):
        raise ExamException("Time_series ha valore non valido, supporta solo valore di tipo lista")


    # Controlla se ogni elemento in time_series è una lista
    for item in time_series:
        if not isinstance(item, list):
            raise ExamException("Tipo non valido per l elemento in time_series, supporta solo lista di liste")

    # Inizializza una lista vuota per memorizzare le misurazioni giornaliere
    daily_measurements = []
    # Inizializza una lista vuota per memorizzare le differenze massime giornaliere
    output = []
    # Inizializza una variabile per tracciare il giorno corrente
    current_day = None

    # Itera sui dati della serie temporale
    for i in range(len(time_series)):
        epoch, temp = time_series[i]
        day = epoch - (epoch % 86400)

        if current_day is None:
            current_day = day

        if day == current_day:
            daily_measurements.append(temp)

        else:
            # Se è iniziato un nuovo giorno, calcola la differenza massima per il giorno precedente
            if daily_measurements:
                if len(daily_measurements) > 1:
                    daily_max_diff = max(daily_measurements) - min(daily_measurements)
                else:
                    daily_max_diff = None
                output.append(daily_max_diff)
                # Reimposta le misurazioni giornaliere con la temperatura corrente
                daily_measurements = [temp]
            # Aggiorna current_day al nuovo giorno
            current_day = day

    # Calcola la differenza massima per l'ultimo giorno
    if daily_measurements:
        if len(daily_measurements) > 1:
            daily_max_diff = max(daily_measurements) - min(daily_measurements)
        else:
            daily_max_diff = None
        output.append(daily_max_diff)

    # Restituisce le differenze massime giornaliere
    return output

# Istanzia un oggetto della classe CSVTimeSeriesFile con il nome del file "data.csv"
time_series = CSVTimeSeriesFile(name="data.csv")
# Ottiene i dati dal file
data = time_series.get_data()
# Calcola le differenze massime giornaliere di temperatura
daily_max_differences = compute_daily_max_difference(data)
print(daily_max_differences)