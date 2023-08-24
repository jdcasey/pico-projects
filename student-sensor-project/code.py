"""
Write a series of temperature measurements to a CSV file, including the seconds offset.
"""
import time
import board
import digitalio
import microcontroller

DATA_FILE = "/data.csv"
MEASURE_SECONDS = 10
MEASURE_DELAY = 0.1
SETTLE_DELAY_SECONDS = 2

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

start = time.time()

try:
    # Let the system settle so on-board measurements will be more accurate
    time.sleep(SETTLE_DELAY_SECONDS)

    # overwrite the data file and set the CSV header in the process
    # The 'w' here means "write", meaning write a whole new file (opposed to appending)
    with open(DATA_FILE, "w") as datalog:
        datalog.write("SECONDS,TEMP (C)\n")
        datalog.flush()

    # Take the measurements, which won't take long...so we don't need to worry about providing
    # read access while this is happening
    # The 'a' here means "append" to the existing file. It will start the file if it doesn't exist.
    with open(DATA_FILE, "a") as datalog:
        for _i in range(int(MEASURE_SECONDS / MEASURE_DELAY)):
            temp = microcontroller.cpu.temperature
            elapsed = time.time() - start

            line = '{0},{1:.1f}\n'.format(
                elapsed,
                temp
            )
            datalog.write(line)
            datalog.flush()

        # print("Write: ", line)
        time.sleep(MEASURE_DELAY)

    # When readings are done, turn on the LED and just park the program so nothing restarts
    while True:
        led.value = True

# Setup some basic blink codes in case something is wrong.
except OSError as e:  # Typically when the filesystem isn't writeable...
    delay = 0.5  # ...blink the LED every half second.
    if e.args[0] == 28:  # If the filesystem is full...
        delay = 0.25  # ...blink the LED faster!
    while True:
        led.value = not led.value
        time.sleep(delay)
