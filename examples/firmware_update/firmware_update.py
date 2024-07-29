from max_ble_hci import BleHci

PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O6J1-if00-port0"

def main(): 
    conn = BleHci(PORT)


    # make sure you have to erase the flash memory before you flash to it
    conn.erase_memory("10:04:00:00", "03:80:00")

    conn.firmware_update("hello_world.bin")

    #reset the device to reload the uploaded firmware
    try:
        conn.reset_device()
    except:
        pass

    
if __name__ == "__main__":
    main()

