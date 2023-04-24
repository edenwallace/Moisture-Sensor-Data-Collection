AIRVALUE = 519 # Value sensor outputs while in open air
WATERVALUE = 215 # Value sensor outputs while fully submerged in water

if __name__ == '__main__':
    # Arduino plugged into the usb port above the flash drive is /dev/ttyUSB0
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    conn = mariadb.connect(
        user="eden",
        password="waterbottlebattery",
        host="107.175.8.57",
        port=3306,
        database="plant_moisture")
    cur = conn.cursor()

    while True:
        # Collect data from serial
        ser.reset_input_buffer()
        absoluteMoisture = ser.readline().decode('utf-8').rstrip()

        # Ignore line if empty, else convert to int
        if (absoluteMoisture == ''): continue
        else: absoluteMoisture = int(absoluteMoisture)
        # Formula for moisture percentage. Format: 0.0 to 100.0
        moisturePercent = (100 * (1 - ((absoluteMoisture - WATERVALUE) / (AIRVALUE - WATERVALUE))))

        # Math to get value as 1-100% if number is between AIRVALUE and WATERVALUE
        if (absoluteMoisture <= WATERVALUE):
            print('100%')
            moisturePercent = 100.0
        elif (absoluteMoisture >= AIRVALUE):
            print('0%')
            moisturePercent = 0.0
        else:
            print("%.2f%%" % moisturePercent)

        # script runs every 4 hours and sends to db
        time.sleep(14400)
        try:
            cur.execute("INSERT INTO moisture (absolute_moisture, percentage) VALUES (?,?)", (absoluteMoisture,int(moisturePercent)))
            conn.commit()
            print (f"Last Inserted ID: {cur.lastrowid}")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)