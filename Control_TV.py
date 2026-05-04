import os                           # For clear screen / create folder
import time                         # For delay
import click                        # For user input keys
import msvcrt                       # For Aging and flush()
import serial.tools.list_ports      # For serial communication
import threading                    # For serial_mode()
import sys                          # To exit the script in the middle of the program
import glob                         # To list out all .txt file in a folder
import subprocess                   # For uutx.exe 

# Global flags
serial_running = True
ui_flag = 0
ComPort = ''
project = 55
uirt_connection = False
uirt_usage = False

### DEFINES ###
keydown = 20
keyup = 19
keyleft = 21
keyright = 22
keyhome = 3
keyreturn = 4
keycenter = 23
key_enter = 66
key_del = 67
keyvolumemute = 164
keyvolumeup = 24
keyvolumedown = 25
keyhelp = 259
keypower = 177
key_media_stop = 86
keyinput = 178

class remote:
    power = '0000 0067 0000 000D 0060 0019 0030 0019 0018 0019 0030 0019 0018 0019 0030 0019 0018 0018 0018 0018 0031 0019 0018 0019 0018 0019 0018 0019 0018 040D'
    up = '0000 0067 0000 000D 0060 0019 0018 0019 0018 0019 0030 0019 0018 0019 0030 0019 0030 0019 0031 0019 0030 0019 0018 0019 0018 0019 0018 0019 0018 03F5'
    down = '0000 0064 0000 000D 0064 0018 0032 0018 0019 0018 0032 0019 0019 0018 0032 0018 0032 0019 0032 0019 0032 0018 0019 0018 0019 0018 0019 0019 0019 0423'
    left = '0000 0064 0000 000D 0063 001A 0019 0018 0019 0018 0032 0019 0019 0019 0031 0019 0032 0018 0019 0019 0032 0018 0019 0018 0019 0019 0019 001A 0019 0459'
    right = '0000 0064 0000 000D 0063 0019 0032 0019 0032 0018 0019 0018 0019 0019 0032 0018 0031 0019 0019 0019 0031 0019 0019 0019 0019 0019 0019 0019 0019 043E'
    center = '0000 0063 0000 000D 0064 0018 0032 0019 0019 0018 0032 0018 0019 0018 0019 0019 0031 0019 0032 0019 0032 0019 0019 0018 0019 0018 0019 0019 0019 0441'
    home = '0000 0063 0000 000D 0064 0019 0018 0019 0019 0019 0019 0019 0019 0018 0019 0019 0031 0019 0032 0019 0032 0019 0019 0019 0019 0019 0019 0018 0019 0475'
    youtube = '0000 0069 0000 0010 005F 0018 0030 0018 0030 0018 0030 0018 0018 0018 0018 0018 0018 0018 0030 0018 0018 0018 0018 0018 0030 0018 0018 0018 0018 0018 0018 0018 0030 0018 0030 0326'
    netflix = '0000 0064 0000 0010 0064 0019 0019 0018 0019 0018 0032 0018 0032 0019 0031 0018 0032 0019 0032 0019 0019 0019 0031 0018 0019 0019 0031 0019 0032 0018 0019 0018 0019 0018 0019 0364'
    option = '0000 0067 0000 0010 0060 0019 0030 0019 0030 0019 0018 0019 0030 0019 0018 0019 0018 0019 0030 0019 0018 0019 0018 0019 0030 0019 0018 0019 0018 0019 0018 0019 0030 0019 0030 0331'
    input = '0000 0064 0000 000D 0064 0019 0032 0019 0019 0019 0031 0018 0019 0019 0019 0018 0032 0019 0019 0018 0032 0019 0019 0019 0019 0019 0019 0019 0019 0457'
    back = '0000 0064 0000 0010 0064 0018 0032 0019 0031 0019 0019 0018 0019 0018 0019 0019 0032 0019 0019 0019 0032 0019 0031 0019 0032 0018 0019 0019 0031 0019 0019 0019 0019 0018 0032 0362'
    mute = '0000 0067 0000 000D 0060 0019 0018 0019 0018 0019 0030 0019 0018 0019 0030 0019 0018 0019 0018 0019 0030 0019 0018 0019 0018 0019 0018 0019 0018 0423'
    volume_up = '0000 0067 0000 000D 0060 0019 0018 0019 0030 0019 0018 0019 0018 0019 0030 0019 0018 0019 0018 0019 0030 0019 0018 0019 0018 0019 0018 0019 0018 0425'
    volume_down = '0000 0067 0000 000D 0060 0018 0030 0018 0030 0018 0018 0019 0018 0018 0030 0019 0018 0019 0018 0019 0030 0019 0018 0018 0018 0018 0018 0019 0018 0408'
    volume_mute = '0000 0067 0000 000D 0060 0019 0018 0019 0018 0019 0030 0019 0018 0019 0030 0019 0018 0019 0018 0019 0030 0019 0018 0019 0018 0019 0018 0019 0018 0423'
    red = '0000 0064 0000 0010 0064 0018 0032 0019 0019 0018 0031 0018 0019 0018 0019 0019 0032 0019 0019 0018 0031 0018 0032 0019 0032 0018 0019 0018 0032 0019 0019 0018 0019 0018 0032 0362'

user_input_list = ['\xe0P' , 'S', '\xe0H', 'W', '\xe0K', 'A', '\xe0M', 'D', 'H', '\x1b', 'B', '\r', 'E', '\t', 'I', 'M', ',', '.']
key_output_list = [keydown, keydown, keyup, keyup, keyleft, keyleft, keyright, keyright, keyhome, keyreturn, keyreturn, keycenter, keycenter, keyinput, keyinput, keyvolumemute, keyvolumeup, keyvolumedown]
uirt_output_list = [remote.down, remote.down, remote.up, remote.up, remote.left, remote.left, remote.right, remote.right, remote.home, remote.back, remote.back, remote.center, remote.center, remote.input, remote.input, remote.volume_mute, remote.volume_up, remote.volume_down]

"""
List index goes as follows:
0. Generic TV
1. Bluefin
2. Chutoro
3. Vulcan
4. Amaebi

None/Blank is used if the command does not exists or if it is for Generic TV

"""
project_name = ['Generic', 'Bluefin', 'Chutoro', 'Vulcan', 'Amaebi']
picture_setting = ['',
                   'am start -a android.intent.action.MAIN -n com.android.tv.settings/com.mediatek.tv.settings.picture.SonyPictureActivity',
                   'am start com.android.tv.settings/com.mediatek.tv.settings.picture.SonyPictureActivity',
                   'am start -a android.intent.action.MAIN -n com.realtek.advancesetting/.activity.MainActivity --es show_panel "show_picture_adjustment_item"',
                   'am start com.sony.dtv.configsettings/.PictureSettingActivity']
sound_setting = ['',
                 'am start com.android.tv.settings/com.mediatek.tv.settings.sound.SonySoundActivity',
                 'am start com.android.tv.settings/com.mediatek.tv.settings.sound.SonySoundActivity',
                 None,
                 None]
metadata_command = [None,
                    'echo meta getmeta > sys/devices/platform/mtk-tvpqu/mtk_dbg/dump_mtk_cus_info',
                    'echo meta getmeta > sys/devices/platform/mtk-tvpqu/mtk_dbg/dump_mtk_cus_info_lite',
                    None,
                    None]
sonypq_data_command = [None,
                       'echo ver > /sys/devices/platform/mtk-tvpqu/mtk_dbg/dump_mtk_cus_info',
                       'cat /sys/class/remoteproc/remoteproc1/device/dump/log | grep sopq',
                       None,
                       None]
service_menu_command = [None,
                        'am start com.sony.dtv.sonyservicemode/com.sony.dtv.servicemode.activity.MainActivity',
                        'am start com.sony.dtv.sonyservicemode/com.sony.dtv.servicemode.activity.MainActivity',
                        'am start com.realtek.servicemenu/.MainActivity',
                        'am start com.sony.dtv.sonyservicemode/com.sony.dtv.servicemode.activity.MainActivity']

DEFAULT_TIME_DELAY = 0.15
DEFAULT_TIME_DELAY_KEYBOARD = 0.05
DEFAULT_TIME_PER_COMMAND = 0.08

### Essential Functions ###

def clear_screen():
    os.system('cls')

def send_remote_command(ir_code, longpress = False):
    if longpress:
        cmd = f'uutx.exe -r30 -d1 "{ir_code}"'
    else:
        cmd = f'uutx.exe -r1 -d1 -s0 "{ir_code}"'
    subprocess.run(cmd)

def check_usbuirt_connection():
    cmd = f'uutx.exe -r1 -d1 "{remote.red}"'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

    # Prevent message from displaying
    # You can log or handle the error instead
    if result.returncode == 0:
        return True
    else:
        return False

def send_command(my_com = ""):
    while True:
        try:
            ser.reset_input_buffer()
            my_com = my_com + "\n"
            my_com = str.encode(my_com)
            ser.write(my_com)
            break
        except:
            print("Something went wrong, please reconnect COM Port")
            connect_com_port()
            reset_ui()
            return
        
def list_com_ports():
    ports = serial.tools.list_ports.comports()
    result = []
    
    for port in ports:
        try:
            # Try to open the port to check if it's available
            with serial.Serial(port.device) as ser:
                result.append(f"{port.device}")
        except (OSError, serial.SerialException):
            # If the port is in use, catch the error and mark it
            result.append(f"{port.device} (In use)")
    
    return result

def navigate_func(com):
    new_com = "input keyevent " + str(com)
    send_command(new_com)

def pause():
    enter = input("\n\n***********PRESS ENTER TO CONTINUE***********")

def press_any_key():
    print("\n\n***********PRESS ANY KEY TO CONTINUE***********")
    flush_input()
    getLetter = click.getchar()

def read_serial(print_status = True, timeout = 1):
    start_time = time.time()
    serial_list = []
    global serial_running

    while True:
        try:
            if ser.in_waiting:

                data = ser.readline().strip()  # Read and remove trailing newlines
                value = str(data, 'utf-8', errors='replace')  # Replace undecodable characters

                if print_status == True:
                    print(f"{value}")

                serial_list.append(value)
                start_time = time.time()  # Reset timer since data was received

            elif serial_running == False:
                serial_running = True       # Resets
                break

            elif time.time() - start_time > timeout and timeout != 0:  # Check if 5 seconds have passed
                break

        except Exception as e:
            print(f"Error: {e}")
            break
    
    return serial_list

def find_serial(keyword):
    logresult = read_serial(print_status = False)
    if keyword in logresult:
        return True
    else:
        return False

def reset_ui_normal():
    clear_screen()
    print(project_name[project] + " TV\n")
    print("Navigate TV can use Arrow Keys or WASD\n")
    print("E = Enter                                                                 1 = To Enable advance settings")
    print("B = Back                                                                  9 = To End Process")
    print("H = Home")
    print("I = Switch Input")
    print("P = To Open picture settings")
    print("U = To Open sound settings")
    print("O = To Open smart UI settings")
    print("\nT = To Enter Keyboard mode\n")
    print("L = To Longpress home")
    if uirt_connection: print("+ = To Turn On/Off TV")
    print("M = To Mute and Unmute TV")
    print(", = To Increase volume")
    print(". = To Decrease volume\n")
    print("Y = To open YouTube")
    print("N = To open Netflix\n")
    print("Current COM Port: " + ComPort)
    time.sleep(0.2)
    print("\nBegin: ",end="")

def reset_ui_advance():
    clear_screen()
    print(project_name[project] + " TV\n")
    print(r"1 = To Get PQ Metadata                                                    \ = To go back to simple controls")
    print("2 = To Get SonyPQ library and data version")
    print("3 = To Enter Service Menu")
    print("4 = To Input Custom Keyevent")
    print("5 = To Reboot TV")
    print("6 = To Enter Serial mode")
    print("7 = To Disconnect/Change COM Port")
    print("8 = To Enter Automation mode")
    print("9 = To End Process")
    print("0 = To Check current version of script")
    if uirt_connection: print("~ = To switch USB UIRT/Serial Control")
    print("- = To Perform TV control from script(.txt file)\n")
    print("C = To Clear screen\n")
    print("Current COM Port: " + ComPort)
    time.sleep(0.2)
    print("\nBegin: ",end="")

def print_out_keyevents():
    print("\nBelow is the listed keyevents that is often used:")

    keys = {
        "keydown": 20,
        "keyup": 19,
        "keyleft": 21,
        "keyright": 22,
        "keyhome": 3,
        "keyreturn": 4,
        "keyenter": 23,
        "keyvolumemute": 164,
        "keyvolumeup": 24,
        "keyvolumedown": 25,
        "keyhelp": 259,
        "keypower": 177,
        "key_media_stop": 86,
        "key_pause_play": 85,
        "key_tv": 170,
        "key_notification": 83,
        "key_input": 178,
        "keychannelup": 166,
        "keychanneldown": 167,
    }

    for name, code in keys.items():
        print(f"{name} = {code}")

    print("\nOther keyevents can be accessed here: \nhttps://gist.github.com/arjunv/2bbcca9a1a1c127749f8dcb6d36fb0bc")


def reset_ui():
    if ui_flag == 0:
        reset_ui_normal()
    else:
        reset_ui_advance()

def flush_input():
    while msvcrt.kbhit():
        msvcrt.getch()  # discard the buffered key

def get_user_input(capital = True):
    flush_input()
    getLetter = click.getchar()
    getLetter = str(getLetter)
    length_str = len(getLetter)
    if length_str > 1:
        string = getLetter
    elif capital:
        string = getLetter.capitalize()
    else:
        string = getLetter

    return string

def create_folder(folder_name, print_status = False):
    try:
        os.mkdir(folder_name)
        if print_status:
            print(f"Directory '{folder_name}' created successfully.")
    except FileExistsError:
        if print_status:
            print(f"Directory '{folder_name}' already exists.")
    except PermissionError:
        if print_status:
            print(f"Permission denied: Unable to create '{folder_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_comport():
    timeout = 3
    attempt = 0
    ser.reset_input_buffer()

    while True and attempt < timeout:

        ser.write(b'\n')
        ser.write(b'\x03\n')
        ser.write(('\n').encode())

        if ser.in_waiting:
            data = ser.read(ser.in_waiting).decode(errors='ignore')

            if "console" in data:
                return True
            
        time.sleep(2)
        attempt += 1

    return False

def connect_com_port():

    global project

    while True:

        print("\nHere are the available COM Ports:")
        com_ports = list_com_ports()

        # Print each port
        for port in com_ports:
            print(port)

        global ComPort

        newComport = input("\nPlease Enter the com port of your jig or Enter 1000 to end process. Make sure Tera Term is disconnected first (ex: COM15): COM")

        if newComport.isdigit() and int(newComport) > 100:
            print("\n\nProcess ended")
            press_any_key()
            clear_screen()
            sys.exit()

        ComPort = f'COM{newComport}'

        try:
            global ser
            ser = serial.Serial(ComPort, 115200, timeout=0.1)

            result = check_comport()
            if result == True:
                break
            else:
                choice = input("\nConsole not able to be found, want to continue (y/n)?: ")
                if choice == 'y':
                    project = 0
                    break
                ser.close()
                clear_screen()

        except:
            clear_screen()
            print("COM port not recognized or is in use. Re-enter or disconnect")

    check_project()

### Put Extra Functions below here ###

def check_project(): # To check which TV it is currently connected
    global project

    send_command("getprop | grep fingerprint")
    log = read_serial(print_status = False)

    for item in log:
        if "BF1" in item: # Bluefin
            project = 1
            break
        elif "CT1" in item: # Chutoro
            project = 2
            break
        elif "VU" in item: # Vulcan
            project = 3
            break
        elif "AE" in item: # Amaebi
            project = 4
            break
        else:
            project = 0

def check_userdebug_pkg():
    send_command("getprop ro.build.type")
    result = find_serial("userdebug")
    return result

def get_metadata():

    if metadata_command[project] is None:
        print("Not available for {} TV".format(project_name[project]))
        return

    if check_userdebug_pkg():
        send_command("su")
        send_command(metadata_command[project])
        print("\nPQ Metadata")
        read_serial()

    else:
        print("Command not available due to user PKG")
        pause()
        reset_ui()

def get_PQLIB():

    if sonypq_data_command[project] is None:
        print("Not available for {} TV".format(project_name[project]))
        return
    
    if check_userdebug_pkg():
        send_command("su")
        send_command(sonypq_data_command[project])
        print("\nPQ Lib")
        read_serial()

    else:
        print("Command not available due to user PKG")
        pause()
        reset_ui()

def open_service_menu():
    if service_menu_command[project] is None:
        print("Not available for {} TV".format(project_name[project]))
        return
    
    navigate_func(keyhelp)
    time.sleep(5)
    send_command(service_menu_command[project])

def reboot_tv():
    send_command("reboot")
    print("\nReboot in progress...\n")
    read_serial(timeout = 15)
    print("")
    print("TV REBOOTED")
    print("")
    time.sleep(5)

def get_user_inputs_aging():

    enflag = 0
    key = 'a' # dummy key
    mylist = []
    permitted_keys = ['W', 'A', 'S', 'D', 'H', 'B', 'E', 'L', '[', ']', 'I', 'P', 'O', 'F', 'U', 'G', ',', '.', 'M', '\xe0P', '\xe0H', '\xe0K', '\xe0M']
    startTime = time.time()

    while key != 'N':
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            enflag = 1
            if inp == b'\xe0' or inp == b'\x00':  # Check for prefix bytes
                key = inp + msvcrt.getch()  # Read the second part of the key
                key = key.decode(errors="ignore")
                key = '\xe0' + key

            else:
                key = str(inp)[2:3]
                key = key.capitalize()

            if key in permitted_keys:
                mylist.append(key)
                switch_case(key, get_string = False)

            startTime = time.time()

        elif time.time() - startTime > 0.5 and enflag == 1:
            mylist.append('F')
            startTime = time.time()

    return mylist

def from_list_to_control_tv(mylist):

    length = len(mylist)
    force_delay = ['E', 'B']
    comment_flag = 0

    for j in range(length):

        if mylist[j] == '【':
            comment_flag = 1
        elif  mylist[j] == '】':
            comment_flag = 0

        if comment_flag == 0:
            if mylist[j] == 'F':
                time.sleep(0.5)
            elif mylist[j] == 'G':
                time.sleep(10)
            else:
                if mylist[j] in force_delay:
                    time.sleep(0.5)
                switch_case(mylist[j], get_string = False)
                if mylist[j] in force_delay:
                    time.sleep(0.5)

def save_user_control_to_file(mylist):
    filename = input("\nPlease enter text filename: ")
    if '.txt' not in filename:
        filename = filename + '.txt'

    create_folder("scripts")

    file_path = os.path.join("scripts", filename)
    
    f = open(file_path, "w")

    for i in (mylist):
        f.write(i)

    f.close
    print("\nFile created at:", os.path.abspath(file_path))
    #print('\nText file: "{}" has been created'.format(filename))

def aging():

    reset_ui_normal() # To show keys for user
    print('Start your aging now, follow the UI menu above to move the TV accordingly. \n\nPress "F" to add 0.5 Second delay, Press "G" to add 10 Second delay, Press "N" when finish')
    
    mylist = get_user_inputs_aging()

    choice = input("\nDo you wish to continue with aging loop ? (Y/N): ")

    if choice.capitalize() == "Y":

        loop = input('\nInput the number of loops: ')
        loop = int(loop)
        print()

        for i in range(loop):
            print("Current loop is " + str(i+1) + " out of " + str(loop))
            from_list_to_control_tv(mylist)

    choice = input("\nDo you wish to save the key movements in a text file ? (Y/N): ")

    if choice.capitalize() == "Y":
        save_user_control_to_file(mylist)


def custom_keyevent():
    print_out_keyevents()
    print("\n\nInput your custom keyevent:\n")
    choice = input("Longpress ? (y/n): ")

    if choice.lower() == 'y':
        new_key = input("\ninput keyevent ")
        new_com = "input keyevent --longpress " + str(new_key)
        send_command(new_com)
    
    elif choice.lower() == 'n':
        new_key = input("\ninput keyevent ")

        try:
            new_repetition = int(input("repetition: "))
            new_delay = float(input("delay: "))

            for i in range(new_repetition):
                navigate_func(new_key)
                time.sleep(new_delay)

            if new_delay == 0:
                time.sleep(DEFAULT_TIME_PER_COMMAND * new_repetition)
                time.sleep(2)
        
        except:
            print("\nInvalid input for repetition or delay")
    
    else:
        print("\nInvalid input")

    press_any_key()
    reset_ui()

def keyboard():

    clear_screen()
    print("Press tab key to end keyboard mode")

    keyboard_layout = """
            ~` 1 2 3 4 5 6 7 8 9 0 - = backspace
            tab  Q W E R T Y U I O P [ ] \\
            caps  A S D F G H J K L ; ' enter
            shift  Z X C V B N M , . / shift
            ctrl fn alt  space  alt ctrl < ^ >
    """

    print("\n\n\n")
    print(keyboard_layout)
    print("\n\n\n")

    print("\nBegin: ",end="")
    
    other_keys = ['`', '\\', '"']
    while True:
        string = get_user_input(capital = False)
        if string == '\r':
            navigate_func(key_enter)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)
        elif string == '\b':
            navigate_func(key_del)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)
        elif string == '\xe0P': 
            navigate_func(keydown)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)
        elif string == '\xe0H':
            navigate_func(keyup)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)
        elif string == '\xe0K':
            navigate_func(keyleft)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)
        elif string == '\xe0M':
            navigate_func(keyright)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)
        elif string in other_keys:
            new_text = ("'" + string + "'")
            new_com = "input text " + new_text
            send_command(new_com)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)
        elif string == '\x1b':
            navigate_func(keyreturn)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)
        elif string == '\t':
            break
        else:
            new_text = ('"' + string + '"')
            new_com = "input text " + new_text
            send_command(new_com)
            time.sleep(DEFAULT_TIME_DELAY_KEYBOARD)

def write_to_serial():
    global serial_running
    exit_string = "Goodbye"

    while serial_running:
        msg = input()

        if msg == "0":
            ser.write(b'\x03')  # Send Ctrl+C to stop logcat

        elif msg.casefold() == exit_string.casefold():
            serial_running = False
            sys.exit()

        else:
            ser.write((msg + '\n').encode())

def serial_mode():
    global serial_running
    serial_running = True
    clear_screen()
    print('Input "Goodbye" to return back to main control function')
    print('If want to use "dmesg" and "logcat" or any command that requires "Ctrl + C" to exit, enter 0 to stop\n')

    ser.reset_input_buffer()

    # Start threads
    read_thread = threading.Thread(target=read_serial, args=(True, 0), daemon=True)
    write_thread = threading.Thread(target=write_to_serial, daemon=True)

    read_thread.start()
    write_thread.start()

    # Keep main thread alive
    read_thread.join()
    write_thread.join()

def disconnect_com_port_mode():
    ser.close()
    clear_screen()
    print("To reconnect serial port, press Y, \nTo change COM Port, press U, \n\nOtherwise press 9 to end program:",end="")
    while True:
        string = get_user_input()
        if string == 'Y':           # Reconnect
            try:
                ser.open()
                ser.write(b'\x03\n')
                check_project()
                reset_ui_advance()
                break
            except:                 # if something went wrong
                print("\n\nSomething went wrong, please reconnect COM Port")
                connect_com_port()
                reset_ui_advance()
                break
        elif string == 'U':         # Change com port
            ser.close()
            connect_com_port()
            reset_ui_advance()
            break
        elif string == '9':
            return '9'
    
    return '7'

def read_from_file_to_tv():
    create_folder("scripts")

    path_name = os.getcwd() + "\\scripts\\"

    print("\n\nPlease deposit .txt file here: " + path_name)

    ############# List out all scripts available in the file #############
    txt_files = glob.glob(path_name + "*.txt")

    if len(txt_files) != 0:
        print("\nList of available scripts:")
        for i in range(0, len(txt_files)):
            print(str(i+1) + ". " + txt_files[i].split(path_name)[1])

    ######################################################################
    
    filename = input("\nEnter filename to open: ")
    filename = os.getcwd() + "\\scripts\\" + filename

    if '.txt' not in filename:
        filename = filename + '.txt'

    try:
        with open(filename, "r", encoding="utf-8") as f:
            mylist = [line.strip() for line in f.readlines()]

    except:
        print("\nError: {} does not exist".format(filename.split(path_name)[1]))
        return

    f.close()

    new_string = ''.join(mylist)
    new_list = list(new_string)

    loop = input('\nEnter the number of loops: ')
    print('\nKey movements will begin\n')

    for i in range (int(loop)):
        print("Current loop is " + str(i+1) + " out of " + str(loop))
        from_list_to_control_tv(new_list)

    print('\nComplete')

### Below Function is the Main Function ###

def switch_case(string = '234', get_string = True):

    global ui_flag
    global uirt_connection
    global uirt_usage

    if get_string:
        string = get_user_input()

    if string in user_input_list: # General remote movements i.e. up, down, left, right, centre
        if uirt_usage:
            index = user_input_list.index(string)
            send_remote_command(uirt_output_list[index])
        else:
            index = user_input_list.index(string)
            navigate_func(key_output_list[index])
            time.sleep(DEFAULT_TIME_DELAY)
    
    elif string == '\b': # Delete key (Usually used in keyboard mode)
        navigate_func(key_del)
        time.sleep(DEFAULT_TIME_DELAY)

    elif string == 'L': # Menu button
        if uirt_usage:
            send_remote_command(remote.home, longpress = True)
        else:
            navigate_func('--longpress 3')
        time.sleep(DEFAULT_TIME_DELAY)

    elif string == '[':
        if uirt_usage:
            send_remote_command(remote.left, longpress = True)
        else:
            navigate_func('--longpress 21')
        time.sleep(1)

    elif string == ']':
        if uirt_usage:
            send_remote_command(remote.right, longpress = True)
        else:
            navigate_func('--longpress 22')
        time.sleep(1)

    elif string == 'P': # Picture settings UI
        send_command(picture_setting[project])
        time.sleep(DEFAULT_TIME_DELAY)
    
    elif string == 'U': # Audio settings UI
        if sound_setting[project] is not None:
            send_command(sound_setting[project])
            time.sleep(DEFAULT_TIME_DELAY)

    elif string == 'O': # Option
        if uirt_usage:
            send_remote_command(remote.option)
            time.sleep(DEFAULT_TIME_DELAY)
        else:
            send_command("am start com.sony.dtv.smartui/.settings.SmartSettingsActivity")
            time.sleep(DEFAULT_TIME_DELAY)

    elif string == '+': # IR Power
        if uirt_connection:
            send_remote_command(remote.power)
            time.sleep(DEFAULT_TIME_DELAY)

    elif string == 'Y': # YouTube
        """if check_userdebug_pkg():
            link = input("\n\nYouTube Link (Leave blank if you just want to open YouTube): ")
            send_command("su")
            send_command("am start -a android.intent.action.MAIN -n com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.MainActivity {}".format(link))
            pause()
            reset_ui()
        else:"""
        send_command("am start com.google.android.youtube.tv")

    elif string == 'N': # Netflix
        send_command("am start com.netflix.ninja/.MainActivity")

    elif string == '1': # Enable additional UI / Get PQ Metadata
        if ui_flag == 0:
            reset_ui_advance()
            ui_flag = 1
        else:
            get_metadata()
            time.sleep(DEFAULT_TIME_DELAY)

    elif string == '2': # Get PQ lib data
        if ui_flag == 1:
            get_PQLIB()
            time.sleep(DEFAULT_TIME_DELAY)

    elif string == '3': # Service Menu
        if ui_flag == 1:
            open_service_menu()
            time.sleep(DEFAULT_TIME_DELAY)

    elif string == '4': # Custom Keyevent
        if ui_flag == 1:
            reset_ui_advance()
            custom_keyevent()

    elif string == '5': # Reboot TV
        if ui_flag == 1:
            reboot_tv()
            pause()
            reset_ui_advance()

    elif string == '6': # Serial mode
        if ui_flag == 1:
            serial_mode()
            reset_ui_advance()

    elif string == '7': # Disconnect COM Port
        if ui_flag == 1:
            string = disconnect_com_port_mode()

    elif string == '8': # Aging mode
        if ui_flag == 1:
            aging()
            pause()
            reset_ui_advance()

    elif string == '0': # Check script version
        if ui_flag == 1:
            print(f"Script Version is: {os.path.basename(__file__)}")
            press_any_key()
            reset_ui_advance()

    elif string == '~': # Switch remote and serial control
        if ui_flag == 1:
            if uirt_connection:
                uirt_usage = not uirt_usage

                if uirt_usage:
                    print("Switched to USB UIRT control")
                else:
                    print("Switched to serial control")
    
    elif string == '-': # Read from text file and control the tv using the data read
        if ui_flag == 1:
            read_from_file_to_tv()
            pause()
            reset_ui_advance()

    elif string == 'C': # Clears UI
        reset_ui()

    elif string == '\\': # Reset UI back to normal
        if ui_flag == 1:
            reset_ui_normal()
            ui_flag = 0

    elif string == 'T': # Keyboard Mode
        keyboard()
        reset_ui()

    if get_string is True:
        return string
    
def main():

    ### Main Code Begins Here ###

    global ComPort
    global ser
    global uirt_connection
    global uirt_usage

    string = '123'

    clear_screen()
    print("Control TV")

    connect_com_port()
    uirt_connection = check_usbuirt_connection()

    if uirt_connection:
        uirt_choice = input("\nWould you like to use USB UIRT for control (y/n)?: ")

        if uirt_choice.capitalize() == 'Y':
            uirt_usage = True
        else:
            uirt_usage = False

        pause()

    reset_ui_normal()

    while string != '9':
        string = switch_case()

    print("\n\nProcess ended")
    press_any_key()
    clear_screen()

if __name__ == "__main__":
    main()