import tkinter as tk
import tkinter.ttk as ttk
import os
import main  
root = tk.Tk()
root.geometry("400x400")
lb = tk.Listbox(root,width=150)
lb.pack()
 
 
def ffplay(event):
 if lb.curselection():
  file = lb.curselection()[0]
  lst=[]
  for i in os.listdir():
    if ".mp4" in i:lst.append(i)
  lst.reverse()
  print(file,lst[file])
  main.output_video(lst[file])
  os.startfile("test.mp4")
  main.delete_folder()
 
for file in os.listdir():
 if file.endswith(".mp4"):
  lb.insert(0, file)
 
bstart = ttk.Button(root, text="Start movie")
bstart.pack()
 
bstart.bind("<ButtonPress-1>", ffplay)
root.mainloop()