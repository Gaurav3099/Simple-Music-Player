from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

#Initialize pygame
pygame.mixer.init()

#Function  to deal with time
def play_time():
	#ckeck if stopped
	if stopped:
		return

	current_time = pygame.mixer.music.get_pos() / 1000 
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
	#status_bar.config(text=f'Time Elasped : {converted_current_time} of {converted_song_length}')
	#my_label.config(text=converted_current_time)
	#my_label.after(1000, play_time)

	#Find current song length
	song = playlist_box.get(ACTIVE)
	song = f'D:/Exp/Projects/Python/music player/music/{song}.mp3'
	song_mut = MP3(song)
	global song_length 
	song_length = song_mut.info.length
	#convert to time format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
	#my_label.config(text = converted_song_length)

	#set slider length to song length
	#song_slider.config(to=song_length)
	#my_label.config(text=song_slider.get())

	#check song length
	if int(song_slider.get()) == int(song_length):
		stop()

	elif paused == True:
		#if paused end
		song_slider.config(value=current_time)
	else:
		#move slider
		next_time = int(song_slider.get()) + 1
		song_slider.config(to = song_length, value=next_time)
		#conver slider pos to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
		status_bar.config(text=f'Time Elasped : {converted_current_time} of {converted_song_length}')

	#loop to check time every sec
	if current_time >= 1:
		status_bar.config(text=f'Time Elasped : {converted_current_time} of {converted_song_length}')
	status_bar.after(1000, play_time)


def add_song():
	song = filedialog.askopenfilename(initialdir='music/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	#Strip out directory structure
	song = song.replace("D:/Exp/Projects/Python/music player/music/","")
	song = song.replace(".mp3", "")
	playlist_box.insert(END, song)

def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='music/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	
	#Loop song list
	for song in songs:

		#Strip out directory structure
		song = song.replace("D:/Exp/Projects/Python/music player/music/","")
		song = song.replace(".mp3", "")
		playlist_box.insert(END, song)

def delete_song():
	#Delete highlighted song from playlist
	playlist_box.delete(ANCHOR)

def delete_all_songs():
	#Delete all songs from playlist
	playlist_box.delete(0, END)

#Create play function
def play():
	global stopped 
	stopped = False

	#Reconstruct
	song = playlist_box.get(ACTIVE)
	song = f'D:/Exp/Projects/Python/music player/music/{song}.mp3'
	# my_label.config(text=song)
	#loadsongs with pygame
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops=0)
	#Get song time
	play_time()

#Stop function
global stopped
stopped = False

def stop():
	pygame.mixer.music.stop()
	#Clear playlist bar
	playlist_box.selection_clear(ACTIVE)
	status_bar.config(text='')
	song_slider.config(value = 0)

	global stopped
	stopped=True

global paused 
paused = False
#Pause 
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		#Unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		#Pause
		pygame.mixer.music.pause()
		paused = True

#Create function to play next song
def next_song():
	#reset slider pos and status bar
	status_bar.config(text='')
	song_slider.config(value=0)

	next_one = playlist_box.curselection()
	#my_label.config(text=next_one)
	next_one = next_one[0] + 1

	#grab the song title from playlist
	song = playlist_box.get(next_one)
	song=f'D:/Exp/Projects/Python/music player/music/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	#clear active bar in playlist
	playlist_box.selection_clear(0, END)
	playlist_box.activate(next_one)
	playlist_box.selection_set(next_one, last=None)

def prev_song():
	status_bar.config(text='')
	song_slider.config(value=0)

	next_one = playlist_box.curselection()
	#my_label.config(text=next_one)
	next_one = next_one[0] - 1

	#grab the song title from playlist
	song = playlist_box.get(next_one)
	song=f'D:/Exp/Projects/Python/music player/music/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	#clear active bar in playlist
	playlist_box.selection_clear(0, END)
	playlist_box.activate(next_one)
	playlist_box.selection_set(next_one, last=None)

#volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#slide function
def slide(x):
	song = playlist_box.get(ACTIVE)
	song = f'D:/Exp/Projects/Python/music player/music/{song}.mp3'
	# my_label.config(text=song)
	#loadsongs with pygame
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops=0, start=song_slider.get())

#Create main Frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#Create Playlist Box
playlist_box = Listbox(main_frame, bg="black", fg="red", width=60, selectbackground="red", selectforeground='black')
playlist_box.grid(row = 0, column=0)

#volume frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=10)

#volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=125, value=0.5, command=volume)
volume_slider.pack(pady=10)


#create song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

#Define Button Images For Controls
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png') 
pause_btn_img = PhotoImage(file='images/pause50.png') 
play_btn_img = PhotoImage(file='images/play50.png') 
stop_btn_img = PhotoImage(file='images/stop50.png') 

#Create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

#Create Play/Stop etc Buttons
back_button = Button(control_frame, image=back_btn_img, command=prev_song)
forward_button = Button(control_frame, image=forward_btn_img, command=next_song)
play_button = Button(control_frame, image=play_btn_img, command=play)
pause_button = Button(control_frame, image=pause_btn_img, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=4, padx=10)
play_button.grid(row=0, column=1, padx=10)
pause_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=3, padx=10)

# Create Main Menu
my_menu = Menu(root)
root.config(menu=my_menu)


#Create Add song dropdown
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
add_song_menu.add_command(label="Add many songs to Playlist", command=add_many_songs)

#Create Delete song menu dropdown
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all song from playlist", command=delete_all_songs)

#Create Status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill = X, side=BOTTOM, ipady=2)

#Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()