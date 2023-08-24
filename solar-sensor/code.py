# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Data logging example for Pico. Logs the temperature to a file on the Pico.
"""
import time
import board
import digitalio
import microcontroller

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

start = time.time()


def format_ts(ts):
    return '{0}/{1:02d}/{2:02d}T{3:02d}:{4:02d}:{5:02d}'.format(
        ts[0],
        ts[1],
        ts[2],
        ts[3],
        ts[4],
        ts[5],
    )


def run():
    try:
        with open("/data.log", "a") as datalog:
            start_ts = time.localtime(start)
            datalog.write('START: {0}\n'.format(
                format_ts(start_ts)
            ))
            datalog.flush()

        while True:
            temp = microcontroller.cpu.temperature
            elapsed = time.time() - start

            with open("/data.log", "a") as datalog:
                datalog.write('{0},{1},{2:.1f}\n'.format(
                    format_ts(time.localtime(time.time())),
                    elapsed,
                    temp
                ))
                datalog.flush()

            print("Write: ", temp)
            for _i in range(4):
                led.value = not led.value
                time.sleep(1)
                led.value = not led.value
                time.sleep(1)
            time.sleep(58)

    except OSError as e:  # Typically when the filesystem isn't writeable...
        delay = 0.5  # ...blink the LED every half second.
        if e.args[0] == 28:  # If the filesystem is full...
            delay = 0.25  # ...blink the LED faster!
        while True:
            led.value = not led.value
            time.sleep(delay)


run()
