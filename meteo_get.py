import serial
import mysql.connector as mysql
import configparser

import lib.post_meteo as post_meteo
meteo=post_meteo.Meteo(interval_min=3)
wind=post_meteo.Wind(interval_min=3)

ser = serial.Serial('COM8', 9600, timeout=None)

config = configparser.ConfigParser()
config.read("settings.ini")

def Read_COM():
    data: bytes = ser.readline()
    arr = str(data).split(',')

    if "WS1AVG" in str(data):

        cursor = db.cursor()
        query = "INSERT INTO meteo_dump_wind (`WS1AVG`, `WD1AVG`, `WS1MIN2`, `WS1AVG2`, `WS1MAX2`, `WD1MIN2`, `WD1AVG2`, `WD1MAX2`, `WS1MIN10`, `WS1AVG10`, `WS1MAX10`, `WD1MIN10`, `WD1AVG10`, `WD1MAX10`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = [arr[1][:-1][max(arr[1].find('=')+1, 0):], \
                  arr[2][:-1][max(arr[2].find('=')+1, 0):], \
                  arr[3][:-1][max(arr[3].find('=')+1, 0):], \
                  arr[4][:-1][max(arr[4].find('=')+1, 0):], \
                  arr[5][:-1][max(arr[5].find('=')+1, 0):], \
                  arr[6][:-1][max(arr[6].find('=')+1, 0):], \
                  arr[7][:-1][max(arr[7].find('=')+1, 0):], \
                  arr[8][:-1][max(arr[8].find('=')+1, 0):], \
                  arr[9][:-1][max(arr[9].find('=')+1, 0):], \
                  arr[10][:-1][max(arr[10].find('=')+1, 0):], \
                  arr[11][:-1][max(arr[11].find('=')+1, 0):], \
                  arr[12][:-1][max(arr[12].find('=')+1, 0):], \
                  arr[13][:-1][max(arr[13].find('=')+1, 0):], \
                  arr[14][:-1][max(arr[14].find('=')+1, 0):]]
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        wind.send(values)
        
        print("WS1AVG = скорость ветра (м/с)  за 3 сек = " + arr[1][:max(arr[1].find('C'), 0)][max(arr[1].find('=')+1, 0):] + "   " + arr[1])
        print("WD1AVG = направление ветра (град) за 3 сек = " + arr[2][:max(arr[2].find('C'), 0)][max(arr[2].find('=')+1, 0):] + "   " + arr[2])
        print("WS1MIN2 = скорость ветра (м/с) минимальное значение за 2 минуты = " +  arr[3][:max(arr[3].find('C'), 0)][max(arr[3].find('=')+1, 0):] + "   " + arr[3])
        print("WS1AVG2 = скорость ветра (м/с) среднее значение за 2 минуты = " +  arr[4][:max(arr[4].find('C'), 0)][max(arr[4].find('=')+1, 0):] + "   " + arr[4])
        print("WS1MAX2 = скорость ветра (м/с) максимальное значение за 2 минуты = " +  arr[5][:max(arr[5].find('C'), 0)][max(arr[5].find('=')+1, 0):] + "   " + arr[5])
        print("WD1MIN2 = направление ветра (град) минимальное значение за 2 минуты = " +  arr[6][:max(arr[6].find('C'), 0)][max(arr[6].find('=')+1, 0):] + "   " + arr[6])
        print("WD1AVG2 = направление ветра (град) среднее значение за 2 минуты = " +  arr[7][:max(arr[7].find('C'), 0)][max(arr[7].find('=')+1, 0):] + "   " + arr[7])
        print("WD1MAX2 = направление ветра (град) максимальное значение за 2 минуты = " +  arr[8][:max(arr[8].find('C'), 0)][max(arr[8].find('=')+1, 0):] + "   " + arr[8])
        print("WS1MIN10 = скорость ветра (м/с) минимальное значение за 10 минут = " +  arr[9][:max(arr[9].find('C'), 0)][max(arr[9].find('=')+1, 0):] + "   " + arr[9])
        print("WS1AVG10 = скорость ветра (м/с) среднее значение за 10 минут = " +  arr[10][:max(arr[10].find('C'), 0)][max(arr[10].find('=')+1, 0):] + "   " + arr[10])
        print("WS1MAX10 = скорость ветра (м/с) максимальное значение за 2 минуты = " +  arr[11][:max(arr[11].find('C'), 0)][max(arr[11].find('=')+1, 0):] + "   " + arr[11])
        print("WD1MIN10 = направление ветра (град) минимальное значение за 10 минут = " +  arr[12][:max(arr[12].find('C'), 0)][max(arr[12].find('=')+1, 0):] + "   " + arr[12])
        print("WD1AVG10 = направление ветра (град) среднее значение за 10 минут = " +  arr[13][:max(arr[13].find('C'), 0)][max(arr[13].find('=')+1, 0):] + "   " + arr[13])
        print("WD1MAX10 = направление ветра (град) максимальное значение за 10 минут = " +  arr[14][:max(arr[14].find('C'), 0)][max(arr[14].find('=')+1, 0):] + "   " + arr[14])
        print("ST = статус логгера = " +  arr[15][:max(arr[15].find('C'), 0)][max(arr[15].find('=')+1, 0):] + "   " + arr[15])

    if "TA=" in str(data):

        cursor = db.cursor()
        query = "INSERT INTO meteo_dump_solar_temp_press (`TA`, `DP`, `WC`, `RH`, `PA`, `PR`, `PR1H`, `PR24h`, `SR_1M`, `SR_1D`, `SR_45_1M`, `SR_45_1D`, `SD_1H`, `SD_1D`, `SD_45_1H`, `SD_45_1D`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = [arr[1][:-1][max(arr[1].find('=') + 1, 0):], \
                  arr[2][:-1][max(arr[2].find('=') + 1, 0):], \
                  arr[3][:-1][max(arr[3].find('=') + 1, 0):], \
                  arr[4][:-1][max(arr[4].find('=') + 1, 0):], \
                  arr[5][:-1][max(arr[5].find('=') + 1, 0):], \
                  arr[6][:-1][max(arr[6].find('=') + 1, 0):], \
                  arr[7][:-1][max(arr[7].find('=') + 1, 0):], \
                  arr[8][:-1][max(arr[8].find('=') + 1, 0):], \
                  arr[9][:-1][max(arr[9].find('=') + 1, 0):], \
                  arr[10][:-1][max(arr[10].find('=') + 1, 0):], \
                  arr[11][:-1][max(arr[11].find('=') + 1, 0):], \
                  arr[12][:-1][max(arr[12].find('=') + 1, 0):], \
                  arr[13][:-1][max(arr[13].find('=') + 1, 0):], \
                  arr[14][:-1][max(arr[14].find('=') + 1, 0):], \
                  arr[15][:-1][max(arr[15].find('=') + 1, 0):], \
                  arr[16][:-1][max(arr[16].find('=') + 1, 0):]]
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        
        meteo.send(values)
        
        print("TA = среднее значение температуры за 1 минуту  ( °C ) = " + arr[1][:max(arr[1].find('C'), 0)][max(arr[1].find('=')+1, 0):] + "   " + arr[1])
        print("DP = точка росы  ( °C ) = " + arr[2][:max(arr[2].find('C'), 0)][max(arr[2].find('=')+1, 0):] + "   " + arr[2])
        print("WC = охлаждение ветром ( °C ) = " + arr[3][:-1][max(arr[3].find('=')+1, 0):] + "   " + arr[3])
        print("RH = относительная влажность (%) = " +  arr[4][:max(arr[4].find('C'), 0)][max(arr[4].find('=')+1, 0):] + "   " + arr[4])
        print("PA = атмосферное давление  (mm Hg) = " +  arr[5][:max(arr[5].find('C'), 0)][max(arr[5].find('=')+1, 0):] + "   " + arr[5])
        print("PR = Количество жидких осадков мгновенное значение (мм) = " +  arr[6][:max(arr[6].find('C'), 0)][max(arr[6].find('=')+1, 0):] + "   " + arr[6])
        print("PR1H = Количество жидких осадков сумма за 1 час (мм) = " +  arr[7][:max(arr[7].find('C'), 0)][max(arr[7].find('=')+1, 0):] + "   " + arr[7])
        print("PR24h = Количество жидких осадков сумма за сутки (мм) = " +  arr[8][:max(arr[8].find('C'), 0)][max(arr[8].find('=')+1, 0):] + "   " + arr[8])
        print("SR_1M = Данные от CMP6 установленного параллельно относительно поверхности земли (Вт/м²) среднее значение за 1 минуту = " +  arr[9][:max(arr[9].find('C'), 0)][max(arr[9].find('=')+1, 0):] + "   " + arr[9])
        print("SR_1D = Данные от CMP6 установленного параллельно относительно поверхности земли (Вт/м²) среднее значение за 24 часа = " +  arr[10][:max(arr[10].find('C'), 0)][max(arr[10].find('=')+1, 0):] + "   " + arr[10])
        print("SR_45_1M = Данные от CMP6 установленного 45 градусов относительно поверхности земли (Вт/м²) среднее значение за 1 минуту = " +  arr[11][:max(arr[11].find('C'), 0)][max(arr[11].find('=')+1, 0):] + "   " + arr[11])
        print("SR_45_1D = Данные от CMP6 установленного 45 градусов относительно поверхности земли (Вт/м²) среднее значение за 24 часа = " +  arr[12][:max(arr[12].find('C'), 0)][max(arr[12].find('=')+1, 0):] + "   " + arr[12])
        print("SD_1H = Данные от CMP6 установленного 45 градусов относительно поверхности земли (Вт/м²) суммарное значение за 1 час = " +  arr[13][:max(arr[13].find('C'), 0)][max(arr[13].find('=')+1, 0):] + "   " + arr[13])
        print("SD_1D = Данные от CMP6 установленного 45 градусов относительно поверхности земли (Вт/м²) суммарное значение за 24 часа = " +  arr[14][:max(arr[14].find('C'), 0)][max(arr[14].find('=')+1, 0):] + "   " + arr[14])
        print("SD_45_1H = Данные от CMP6 установленного 45 градусов относительно поверхности земли (Вт/м²) суммарное значение за 1 час = " +  arr[15][:max(arr[15].find('C'), 0)][max(arr[15].find('=')+1, 0):] + "   " + arr[15])
        print("SD_45_1D = Данные от CMP6 установленного 45 градусов относительно поверхности земли (Вт/м²) суммарное значение за 24 часа = " +  arr[16][:max(arr[16].find('C'), 0)][max(arr[16].find('=')+1, 0):] + "   " + arr[16])
        print("V = рабочее напряжение = " +  arr[17][:max(arr[17].find('C'), 0)][max(arr[17].find('=')+1, 0):] + "   " + arr[17])

while True:
    try:
        #cursor = db.cursor()
        Read_COM()
    except mysql.connection.errors.IntegrityError:
        pass
    except:
        try:
            config.read("settings.ini")
            db = mysql.connect(
                host=config["Meteo"]["host"],
                port=config["Meteo"]["port"],
                user=config["Meteo"]["user"],
                passwd=config["Meteo"]["passwd"],
                database=config["Meteo"]["database"]
            )
            cursor = db.cursor()
        except:
            pass

