import threading
import time

def walk_dog(first):
    time.sleep(5)
    print(f"Walking with {first} is done ...")

def take_out_trash():
    time.sleep(3)
    print("Taking out the trash...")

def get_mail():
    time.sleep(1)
    print("Getting the mail...")

chore1 = threading.Thread(target=walk_dog, args=("Bd",))
chore2 = threading.Thread(target=take_out_trash)
chore3 = threading.Thread(target=get_mail)
chore1.start()
chore2.start()
chore3.start()

chore1.join()
chore2.join()
chore3.join()

print("All chores are done!")

#end = time.time() + 8
#while time.time() < end:
   #print("Waiting for chores to finish...")
    #time.sleep(1)