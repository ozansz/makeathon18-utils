import machine
import ssd1306
spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)
oled = ssd1306.SSD1306_SPI(128, 32, spi, machine.Pin(16), machine.Pin(5), machine.Pin(4))
