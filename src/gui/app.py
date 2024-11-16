import tkinter as tk

def main():
    root = tk.Tk()
    root.title("GitHub Issue Exporter")

    label = tk.Label(root, text="Hello Tkinter!")
    label.pack(pady=25, padx=25)

    root.mainloop()


if __name__ == "__main__":
    main()
