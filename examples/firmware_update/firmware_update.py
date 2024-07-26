from max_ble_hci import BleHci

PORT = "/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DT03O6J1-if00-port0"

def main(): 
    conn = BleHci(PORT)


    # make sure you have to erase the flash memory before you flash to it
    '''
    start_address: the start address of flash memory you want to erase. 
        ex: address 0x10004000



        len: length of memory you want to erase. 
        ex: size 0x38000 
    '''
    conn.erase_memory("0x10040000", "0x38000")

    conn.update_firmware("helloW.bin")

    #reset the device to reload the uploaded firmware
    try:
        conn.reset_device()
    except:
        pass

    
if __name__ == "__main__":
    main()

