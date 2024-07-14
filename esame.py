class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        if not isinstance(name, str):
            raise ExamException(
                'Invalid type for name, only string supported. Got "{}"'.format(
                    type(name)
                )
            )
        self.name = name

    def get_data(self):
        output = []

        try:
            with open(self.name, "r") as my_file:
                for index, line in enumerate(my_file):
                    line = line.strip()

                    # Ignora righe vuote o commentate
                    if line == "" or line.startswith("#"):
                        continue

                    elements = line.split(",")

                    # Ignora righe con meno di due elementi
                    if len(elements) < 2:
                        continue

                    if elements[0] != "epoch":
                        try:
                            epoch = int(float(elements[0]))  # casting ad int
                            temp = float(elements[1])
                        except ValueError:
                            continue  # Ignora la riga se ci sono errori nel cast
                        except IndexError:
                            continue  # Ignora la riga se non ci sono abbastanza elementi

                        # Controllo se l'epoch è in ordine e non duplicato
                        if len(output) > 0 and epoch <= output[-1][0]:
                            raise ExamException(
                                "Gli epoch non sono in ordine o ci sono duplicati"
                            )

                        output.append([epoch, temp])

        except FileNotFoundError:
            raise ExamException(
                f'Errore nella lettura del file: "{self.name}" non trovato'
            )

        except Exception as e:
            raise ExamException(f"Errore nella lettura del file: {str(e)}")

        if len(output) == 0:
            raise ExamException("File vuoto")

        return output


def compute_daily_max_difference(time_series):
    daily_measurements = []
    output = []
    current_day = None

    for i in range(len(time_series)):
        epoch, temp = time_series[i]
        day = epoch - (epoch % 86400)

        if current_day is None:
            current_day = day

        if day == current_day:
            daily_measurements.append(temp)
        else:
            if daily_measurements:
                if len(daily_measurements) > 1:
                    daily_max_diff = max(daily_measurements) - min(daily_measurements)
                else:
                    daily_max_diff = None
                output.append(daily_max_diff)
                daily_measurements = [temp]
            current_day = day

    

    return output

time_series = CSVTimeSeriesFile(name="data.csv")
data = time_series.get_data()
daily_max_differences = compute_daily_max_difference(data)
print(daily_max_differences)