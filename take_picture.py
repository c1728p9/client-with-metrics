import socket
import argparse
import threading
import Queue
import Tkinter
from PIL import Image, ImageTk  
from StringIO import StringIO

from functools import partial


DEFAULT_PORT = 1234
#https://docs.python.org/2/howto/sockets.html

parser = argparse.ArgumentParser(description='Camera tool')
parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                    help="Port to send to")
parser.add_argument('--addr', type=str, default="192.168.1.69",
                    help="Addr to send to E.X. "
                    "'fd00:ff1:ce0b:a5e0:fec2:3d00:4:ea8c'")
args = parser.parse_args()

addr = args.addr
port = args.port

def main():
    global root
    global canvas
    root = Tkinter.Tk()
    #root.geometry("800x800")

    global queue
    queue = Queue.Queue()
    def periodicCall():
        while queue.qsize():
            msg = queue.get(0)
            try:
                msg()
            except:
                pass
        root.after(200, periodicCall)
    root.after(100, periodicCall)

    thread = threading.Thread(target=socket_thread)
    thread.start()

    root.mainloop()

canvas = None
def draw_image(data):
    global canvas
    print("Data size: %s" % len(data))
    if canvas is not None:
        canvas.pack_forget()
    image = Image.open(StringIO(data))  
    photo = ImageTk.PhotoImage(image) 
    print("Width, height %s, %s" % (photo.width(), photo.height()))
    canvas = Tkinter.Canvas(root, width=photo.width(), height=photo.height())
    canvas.grid(row = 0, column = 0)
#     with open("pic02.jpg", "rb") as file_handle:
#         data = file_handle.read();  
    canvas.create_image(0,0, image=photo, anchor=Tkinter.NW)
    canvas.image = photo
    canvas.pack()


# class GuiPart:
#     def _ _init_ _(self, master, queue, endCommand):
#         self.queue = queue
#         # Set up the GUI
#         console = Tkinter.Button(master, text='Done', command=endCommand)
#         console.pack(  )
#         # Add more GUI stuff here depending on your specific needs
# 
#     def processIncoming(self):
#         """Handle all messages currently in the queue, if any."""
#         while self.queue.qsize(  ):
#             try:
#                 msg = self.queue.get(0)
#                 # Check contents of message and do whatever is needed. As a
#                 # simple test, print it (in real life, you would
#                 # suitably update the GUI's display in a richer fashion).
#                 print msg
#             except Queue.Empty:
#                 # just on general principles, although we don't
#                 # expect this branch to be taken in this case
#                 pass


def socket_thread():
    # Create server socket
    sock_listen = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_STREAM)
    sock_listen.bind(('', port))
    sock_listen.listen(5)
    while True:
        
        # Send connect message
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("camera", (addr, port))
        print("Message sent")
        
        # Accept connection and read picture
        read_sock, read_addr = sock_listen.accept()
        print("Accepted connection")
        with open("picture.jpg", "wb") as f:
            try:
                picture_data = ""
                while (True):
                    data = read_sock.recv(1024)
                    if len(data) == 0:
                        break
                    print("Size: %s" % len(data))
                    f.write(data)
                    picture_data += data
                    print("Got data")
            finally:
                read_sock.shutdown(socket.SHUT_RDWR)
                read_sock.close()
                print("Thread data length: %s" % len(picture_data))
                queue.put(partial(draw_image, picture_data))

if __name__ == "__main__":
    main()
# def read_socket(socket):
#     while (True):
#         data = socket.recv(4096)
#         if len(data) > 0:
#             print("Data recieved: %s" % data)
#         if done:
#             print("Read thread exiting")
#             break



# print 'tcp %s:%d connect' % (addr[0], addr[1])
# 
# read_thread = threading.Thread(target=read_socket, args=(read_sock,))
# read_thread.daemon = True
# read_thread.start()
# try:
#     while (True):
#         data = raw_input("Enter command:")
#         read_sock.send(data)
#         print("Message sent: %s" % data)
# finally:
#     read_sock.shutdown(socket.SHUT_RDWR)
#     read_sock.close()
