from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Victor's MP3 Player")
root.iconbitmap('C:/Users/vkvan/Downloads/gui/mp3.ico')
root.geometry("860x620")

# initialize pygame mixer
pygame.mixer.init()


# grab song length info
def play_time():
    # check to see if song is stopped to prevent diff instances of play_time running
    if stopped:
        return

    # get the current time
    current_time = pygame.mixer.music.get_pos() / 1000

    # current float into GMT time
    conv_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # get currently playing song
    current_song = playlist.curselection()
    # grab the song title from the playlist
    song = playlist.get(current_song)
    # format the song title and play it
    song = f'C:/Users/vkvan/Downloads/gui/{song}.mp3'

    # use mutagen to get song length and convert to time format
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    conv_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    current_time += 1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {conv_song_length} of {conv_song_length}')

    elif paused:
        pass

    elif int(my_slider.get()) == int(current_time):
        # slider has not been moved
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:
        # slider has been moved
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        # current float into GMT time
        conv_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        # output to status bar
        status_bar.config(text=f'Time Elapsed: {conv_current_time} of {conv_song_length}')
        # move thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    # update time bar
    status_bar.after(1000, play_time)


# add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='C:/Users/vkvan/Downloads/gui', title="Choose a song", filetypes=(("mp3 Files","*.mp3"), ))
    song = song.replace("C:/Users/vkvan/Downloads/gui/", "")
    song = song.replace(".mp3", "")
    playlist.insert(END, song)


# add many songs
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='C:/Users/vkvan/Downloads/gui', title="Choose a song", filetypes=(("mp3 Files","*.mp3"), ))

    # loop through the song list to correct name
    for song in songs:
        song = song.replace("C:/Users/vkvan/Downloads/gui/", "")
        song = song.replace(".mp3", "")
        playlist.insert(END, song)


# play the song
def play():
    # set stopped variable to false so song can play
    global stopped
    stopped = False

    song = playlist.get(ACTIVE)
    song = f'C:/Users/vkvan/Downloads/gui/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # call the play_time function to get song length
    play_time()


# created a global stopped variable
global stopped
stopped = False


# stop the song
def stop():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # stop song from playing
    pygame.mixer.music.stop()
    playlist.select_clear(ACTIVE)

    # clear the status bar
    status_bar.config(text='')

    # set stop variable to true
    global stopped
    stopped = True


# create global pause variable
global paused
paused = False


# pause and unpause the song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


# play the next song in playlist
def next_song():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # get the current song tuple number
    next_one = playlist.curselection()

    # add one to the current song number
    next_one = next_one[0]+1

    # grab the song title from the playlist
    song = playlist.get(next_one)

    # format the song title and play it
    song = f'C:/Users/vkvan/Downloads/gui/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # move active bar in playlist
    playlist.selection_clear(0, END)
    playlist.activate(next_one)

    # set active bar to next song
    playlist.selection_set(next_one, last=None)


# play the previous song
def prev_song():
    # reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)

    # get the current song tuple number
    next_one = playlist.curselection()

    # add one to the current song number
    next_one = next_one[0]-1

    # grab the song title from the playlist
    song = playlist.get(next_one)

    # format the song title and play it
    song = f'C:/Users/vkvan/Downloads/gui/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # move active bar in playlist
    playlist.selection_clear(0, END)
    playlist.activate(next_one)

    # set active bar to next song
    playlist.selection_set(next_one, last=None)


# remove one song
def remove_one_song():
    stop()
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()


# remove all songs
def remove_all_songs():
    stop()
    playlist.delete(0, END)
    pygame.mixer.music.stop()


# create slider function
def slide(x):
    song = playlist.get(ACTIVE)
    song = f'C:/Users/vkvan/Downloads/gui/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


# volume slider function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())


# create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# the volume frame
volume_frame = LabelFrame(master_frame, text='Volume')
volume_frame.grid(row=0, column=1)


# create playlist box
playlist = Listbox(master_frame, bg="black", fg="white", width=125, height=15, selectbackground="white", selectforeground="black")
playlist.grid(row=0, column=0)

# define player control button
back_button_img = PhotoImage(file='C:/Users/vkvan/Downloads/gui/backward.png')
forward_button_img = PhotoImage(file='C:/Users/vkvan/Downloads/gui/forward.png')
play_button_img = PhotoImage(file='C:/Users/vkvan/Downloads/gui/Play.png')
pause_button_img = PhotoImage(file='C:/Users/vkvan/Downloads/gui/pause.png')
stop_button_img = PhotoImage(file='C:/Users/vkvan/Downloads/gui/stop.png')

# create player control frames
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column= 0, pady=20)

# create player control buttons
back_button = Button(controls_frame, image=back_button_img, borderwidth=0, command=prev_song)
pause_button = Button(controls_frame, image=pause_button_img, borderwidth=0, command=lambda: pause(paused))
play_button = Button(controls_frame, image=play_button_img, borderwidth=0, command=play)
stop_button = Button(controls_frame, image=stop_button_img, borderwidth=0, command=stop)
forward_button = Button(controls_frame, image=forward_button_img, borderwidth=0, command=next_song)

back_button.grid(row=0, column=0, padx=12)
forward_button.grid(row=0, column=4, padx=12)
play_button.grid(row=0, column=2, padx=12)
pause_button.grid(row=0, column=1, padx=12)
stop_button.grid(row=0, column=3, padx=12)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add song menu
add_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to Playlist", command=add_song)

# add many songs
add_song_menu.add_command(label="Add many songs to Playlist", command=add_many_song)

# delete song menu
remove_song_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Remove Song", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove selected song", command=remove_one_song)
remove_song_menu.add_command(label="Remove all songs", command=remove_all_songs)

# create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=CENTER, font=("Arial", 20))
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# create music position slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=20)

# create volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume, length=210)
volume_slider.pack(pady=10)

root.mainloop()
