import tkinter as tk
from tkinter import messagebox
import random
import datetime

class HangmanGame:
    def __init__(self, master, word_list, language):
        self.master = master
        self.master.title("Hangman Game" if language == "English" else "Igra vješala")
        self.language = language
        self.word_list = word_list
        self.word = random.choice(word_list)
        self.guesses = ''
        self.max_attempts = 6

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.draw_gallows()
        self.draw_word()
        self.draw_buttons()

        #tr3
        home_button = tk.Button(self.master, text="Home", command=self.go_home)
        home_button.pack(pady=10)

    def draw_gallows(self):
        self.canvas.create_line(100, 350, 300, 350)
        self.canvas.create_line(200, 350, 200, 100)
        self.canvas.create_line(200, 100, 250, 100)
        self.canvas.create_line(250, 100, 250, 150)

    def draw_word(self):
        self.word_display = tk.Label(self.master, text=self.get_display_word(), font=("Helvetica", 24))
        self.word_display.pack()

    def get_display_word(self):
        displayed_word = ''
        for letter in self.word:
            if letter in self.guesses:
                displayed_word += letter + ' '
            else:
                displayed_word += '_ '
        return displayed_word

    def draw_buttons(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        alphabet = "a", "b", "c", "č", "ć", "d", "dž", "đ", "e", "f", "g", "h", "i", "j", "k", "l", "lj", "m", "n", "nj", "o", "p", "q", "r", "s", "š", "t", "u", "v", "w", "x", "y", "z", "ž"
        for char in alphabet:
            tk.Button(self.button_frame, text=char.upper(), command=lambda c=char: self.make_guess(c)).pack(side=tk.LEFT)

    def make_guess(self, letter):
        if letter not in self.guesses:
            self.guesses += letter
            if letter not in self.word:
                self.max_attempts -= 1
                self.draw_hangman()
            self.update_display()
            if self.check_win():
                self.show_win_dialog()
            elif self.max_attempts == 0:
                self.show_loss_dialog()

    def draw_hangman(self):
        if self.max_attempts == 5:
            self.canvas.create_oval(225, 150, 275, 200)
        elif self.max_attempts == 4:
            self.canvas.create_line(250, 200, 250, 275)
        elif self.max_attempts == 3:
            self.canvas.create_line(250, 225, 225, 250)
        elif self.max_attempts == 2:
            self.canvas.create_line(250, 225, 275, 250)
        elif self.max_attempts == 1: 
            self.canvas.create_line(250, 275, 225, 300)
        elif self.max_attempts == 0:
            self.canvas.create_line(250, 275, 275, 300)

    def update_display(self):
        self.word_display.config(text=self.get_display_word())

    def check_win(self):
        return all(letter in self.guesses for letter in self.word)

    def show_win_dialog(self):
        if self.check_win():
            messagebox.showinfo("Congratulations", "You've guessed the word!")
            self.master.destroy()
    
    def show_win_dialog(self):
        win_dialog = tk.Toplevel(self.master)
        win_dialog.title("Winner!" if self.language == "English" else "Pobjednik!")
    
        tk.Label(win_dialog, text="Congratulations, you won!" if self.language == "English" else "Čestitamo, pobjedili ste!").pack()
        tk.Label(win_dialog, text="Enter your name:" if self.language == "English" else "Unesite svoje ime:").pack()
        self.player_name_entry = tk.Entry(win_dialog)
        self.player_name_entry.pack()
        tk.Button(win_dialog, text="Save", command=lambda: [self.save_winner(), win_dialog.destroy()]).pack()
        
    def save_winner(self):
        player_name = self.player_name_entry.get()
        with open("winners.txt", "a") as file:
            file.write(f"{player_name}, {datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}\n")  # Sprema ime pobjednika i vrijeme pobjede u datoteku
        messagebox.showinfo("Win saved" if self.language == "English" else "Pobjeda spremljena", 
                            "Your victory has been saved to the 'winners.txt' file" if self.language == "English"
                            else "Vaša pobjeda je spremljena u datoteku 'pobjednici.txt'")   
        
    def show_loss_dialog(self):
        messagebox.showinfo("Hangman Game" if self.language == "English" else "Igra vješala", 
                            f"The word was: {self.word}\nGame Over!")

    def go_home(self):
        self.master.destroy()  
        root = tk.Tk()  
        LanguageSelection(root)

    
        
class TwoPlayerGame:
    def __init__(self, master, language):
        self.master = master
        self.master.title("Two Player Hangman" if language == "English" else "Igra vješala za dva igrača")
        self.language = language
        master.minsize(300, 300)

        # Stanje igre
        self.player1_name = ""
        self.player2_name = ""
        self.player1_score = 0
        self.player2_score = 0
        self.max_score = 3
        self.current_word = ""
        self.current_player = 1

        self.setup_initial_screen()

    def setup_initial_screen(self):
        tk.Label(self.master, text="Enter Player 1's name:" if self.language == "English" else "Unesite ime igrača 1:").pack()
        self.player1_entry = tk.Entry(self.master)
        self.player1_entry.pack()
        tk.Label(self.master, text="Enter Player 2's name:" if self.language == "English" else "Unesite ime igrača 2:").pack()
        self.player2_entry = tk.Entry(self.master)
        self.player2_entry.pack()
        tk.Button(self.master, text="Start Game", command=self.start_game).pack()


    def start_game(self):
        self.player1_name = self.player1_entry.get()
        self.player2_name = self.player2_entry.get()

        if not self.player1_name or not self.player2_name:
            messagebox.showerror("Error", "Please enter names for both players.")
            return

        self.master.withdraw()
        self.play_round()

    def play_round(self):
        """Pokretanje novog kruga igre. Igrači unose nove riječi za pogađanje."""
        
        if hasattr(self, 'round_root') and self.round_root.winfo_exists():
            self.round_root.destroy()

        self.round_root = tk.Toplevel(self.master)
        self.round_root.geometry("300x100")

        if self.current_player == 1:
            tk.Label(self.round_root, text="Player 1, enter a word for Player 2 to guess:" if self.language == "English" else "Igrač 1, unesite riječ za pogađanje Igrača 2:").pack(),
            self.word_entry = tk.Entry(self.round_root)
            self.word_entry.pack()
            tk.Button(self.round_root, text="Start", command=self.start_game_for_player2).pack()
        else:
            tk.Label(self.round_root, text=f"Player 2, enter a word for Player 1 to guess:" if self.language == "English" else f"Igrač 2, unesite riječ za pogađanje Igrača 1:").pack()
            self.word_entry = tk.Entry(self.round_root)
            self.word_entry.pack()
            tk.Button(self.round_root, text="Start", command=self.start_game_for_player1).pack()

    def start_game_for_player2(self):
        self.current_word = self.word_entry.get().lower()
        self.round_root.destroy()
        self.start_hangman_game()

    def start_game_for_player1(self):
        self.current_word = self.word_entry.get().lower()
        self.round_root.destroy()
        self.start_hangman_game()

    def start_hangman_game(self):
        hangman_window = tk.Toplevel()
        self.game = HangmanGame(hangman_window, [self.current_word], self.language)
        self.game.show_win_dialog = self.handle_win
        self.game.show_loss_dialog = self.handle_loss

    def handle_win(self):
        """Obrada u slučaju pobjede u trenutnoj rundi."""
        if self.game.check_win():
            
            if self.current_player == 1:
                self.player2_score += 1  
            else:
                self.player1_score += 1  

        
        self.game.master.destroy()

        
        if self.player1_score >= self.max_score:
            self.save_winner(self.player1_name)
        elif self.player2_score >= self.max_score:
            self.save_winner(self.player2_name)
        else:
            
            self.current_player = 1 if self.current_player == 2 else 2
            self.play_round()

    
    def handle_loss(self):
        """Obrada u slučaju poraza u trenutnoj rundi."""
        
        losing_player = self.player1_name if self.current_player == 2 else self.player2_name
        if self.language == "English":
            message = f"{losing_player} did not guess the word. The word was: {self.game.word}"
        else:
            message = f"{losing_player} nije pogodio/la riječ. Riječ je bila: {self.game.word}"

        
        loss_dialog = tk.Toplevel(self.master)
        loss_dialog.title("Game Over" if self.language == "English" else "Kraj igre")
        tk.Label(loss_dialog, text=message, wraplength=280).pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
       
        self.game.master.destroy()

        
        tk.Button(loss_dialog, text="Continue", command=lambda: self.continue_game(loss_dialog)).pack(pady=10)


    def continue_game(self, dialog):
        """Nastavak igre nakon završetka runde."""
        dialog.destroy() 
        
        self.current_player = 1 if self.current_player == 2 else 2
        self.play_round()

    def save_winner(self, player_name):
        with open("winners.txt", "a") as file:
            file.write(f"{player_name}, {datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}\n")
        messagebox.showinfo("Winner", f"Congratulations {player_name}, you won the game!")
        self.master.destroy()
        root = tk.Tk()
        LanguageSelection(root)


class LanguageSelection: 
    def __init__(self, master):
        self.master = master
        self.master.title("Language Selection")  
        master.minsize(300,300)
        

        
        tk.Label(master, text="Choose a language:").pack()
        tk.Button(master, text="English", command=lambda: self.select_language("English")).pack()
        tk.Button(master, text="Hrvatski", command=lambda: self.select_language("Hrvatski")).pack()
        tk.Button(master, text="Winners", command=self.show_winners).pack(pady=10)
        
    
    def select_language(self, language):
        self.master.destroy()  
        root = tk.Tk()  
        if language == "English":
            EnglishGame(root)  
        else:
            CroatianGame(root)  

    def show_winners(self):
        winners_window = tk.Toplevel(self.master)
        winners_window.title("Winners List")
    
        try:
            with open("winners.txt", "r") as file:
                winners = file.readlines()
        except FileNotFoundError:
            winners = ["No winners yet."]
    
        tk.Label(winners_window, text="Winners List:").pack()
        tk.Label(winners_window, text="").pack()
    
        for winner in winners:
            tk.Label(winners_window, text=winner.strip()).pack()
        
        tk.Button(winners_window, text="Close", command=winners_window.destroy).pack()


class EnglishGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")  
        master.minsize(300,300)

       
        
        tk.Label(master, text="Choose a difficulty:").pack()
        tk.Button(master, text="Easy", command=self.choose_category).pack()
        tk.Button(master, text="Hard", command=self.choose_hard_category).pack()
        tk.Button(master, text="Two Player", command=self.two_player_mode).pack()

        
    
    def choose_category(self):
        self.master.destroy()  
        root = tk.Tk()  
        EnglishCategoryWindow(root)  
        
    
    def choose_hard_category(self):
        self.master.destroy() 
        root = tk.Tk()  
        EnglishHardCategoryWindow(root)  

    def two_player_mode(self):
        self.master.destroy()
        root = tk.Tk()
        TwoPlayerGame(root, "English")


class EnglishCategoryWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Category Selection - Easy Level")  
        master.minsize(350,200)
   
        
        
        tk.Label(master, text="Choose a category:").pack()
        tk.Button(master, text="Tools", command=lambda: self.select_category("Tools")).pack()
        tk.Button(master, text="Domestic Animals", command=lambda: self.select_category("Domestic Animals")).pack()
        tk.Button(master, text="Male Names", command=lambda: self.select_category("Male Names")).pack()
        tk.Button(master, text="Female Names", command=lambda: self.select_category("Female Names")).pack()

        
    
    def select_category(self, category):
        self.master.destroy()  
        root = tk.Tk()  

        word_list = []
        category_found = False

        
        try:
            with open("library_english_easy.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    
                    if line.startswith("#"):
                        current_category = line[1:].strip()  
                        category_found = (current_category.lower() == category.lower())  
                    elif category_found and line:  
                        word_list.append(line.lower())
                    elif category_found and line == "":  
                        break

        except FileNotFoundError:
            messagebox.showerror("Error", "Library file not found!")
            return

        if word_list:
            HangmanGame(root, word_list, "English")  
        else:
            messagebox.showerror("Error", f"No words found for category '{category}'.")




class EnglishHardCategoryWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Category Selection - Hard Level")  
        master.minsize(350,200)
        
        
        tk.Label(master, text="Choose a category:").pack()
        tk.Button(master, text="Tools", command=lambda: self.select_category("Tools")).pack()
        tk.Button(master, text="Domestic Animals", command=lambda: self.select_category("Domestic Animals")).pack()
        tk.Button(master, text="Male Names", command=lambda: self.select_category("Male Names")).pack()
        tk.Button(master, text="Female Names", command=lambda: self.select_category("Female Names")).pack()
        
    def select_category(self, category):
        self.master.destroy()  

        word_list = []
        category_found = False

        
        try:
            with open("library_english_hard.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    
                    if line.startswith("#"):
                        current_category = line[1:].strip()  
                        category_found = (current_category.lower() == category.lower())  
                    elif category_found and line:  
                        word_list.append(line.lower())
                    elif category_found and line == "":  
                        break

        except FileNotFoundError:
            messagebox.showerror("Error", "Library file not found!")
            return

        if word_list:
            HangmanGame(root, word_list, "English")  
        else:
            messagebox.showerror("Error", f"No words found for category '{category}'.")



class CroatianGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Igra vješala")  
        master.minsize(300,300)
        
        
        tk.Label(master, text="Odaberite težinu:").pack()
        tk.Button(master, text="Lagano", command=self.choose_category).pack()
        tk.Button(master, text="Teško", command=self.choose_hard_category).pack()
        tk.Button(master, text="Igra za dva igrača", command=self.two_player_mode).pack()
        
    
    def choose_category(self):
        self.master.destroy()  
        root = tk.Tk()  
        CroatianCategoryWindow(root)  
        
    
    def choose_hard_category(self):
        self.master.destroy()  
        root = tk.Tk()  
        CroatianHardCategoryWindow(root)  
        
    def two_player_mode(self):
        self.master.destroy()
        root = tk.Tk()
        TwoPlayerGame(root, "Hrvatski")


class CroatianCategoryWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Odabir kategorije - Lagano")  
        master.minsize(350,200)
        
        
        tk.Label(master, text="Odaberite kategoriju:").pack()
        tk.Button(master, text="Alat", command=lambda: self.select_category("Alat")).pack()
        tk.Button(master, text="Domaće životinje", command=lambda: self.select_category("Domaće životinje")).pack()
        tk.Button(master, text="Muška imena", command=lambda: self.select_category("Muška imena")).pack()
        tk.Button(master, text="Ženska imena", command=lambda: self.select_category("Ženska imena")).pack()

        
    
    def select_category(self, category):
        self.master.destroy()  
        root = tk.Tk()  

        word_list = []
        category_found = False

        
        try:
            with open("library_lagano.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    
                    if line.startswith("#"):
                        current_category = line[1:].strip()  
                        category_found = (current_category.lower() == category.lower())  
                    elif category_found and line:  
                        word_list.append(line.lower())
                    elif category_found and line == "":  
                        break

        except FileNotFoundError:
            messagebox.showerror("Error", "Library file not found!")
            return

        if word_list:
            HangmanGame(root, word_list, "Hrvatski")  
        else:
            messagebox.showerror("Error", f"Nema dostupnih riječi za kategoriju '{category}'.")


        

class CroatianHardCategoryWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Odabir kategorije - Teško") 
        master.minsize(300,300)
        
        tk.Label(master, text="Odaberite kategoriju:").pack()
        tk.Button(master, text="Alat", command=lambda: self.select_category("Alat")).pack()
        tk.Button(master, text="Domaće životinje", command=lambda: self.select_category("Domaće životinje")).pack()
        tk.Button(master, text="Muška imena", command=lambda: self.select_category("Muška imena")).pack()
        tk.Button(master, text="Ženska imena", command=lambda: self.select_category("Ženska imena")).pack()

    #tesko    
    def select_category(self, category):
        self.master.destroy()  
        root = tk.Tk()  

        word_list = []
        category_found = False

        
        try:
            with open("library_tesko.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    
                    if line.startswith("#"):
                        current_category = line[1:].strip()  
                        category_found = (current_category.lower() == category.lower())  
                    elif category_found and line:  
                        word_list.append(line.lower())
                    elif category_found and line == "": 
                        break

        except FileNotFoundError:
            messagebox.showerror("Error", "Library file not found!")
            return

        if word_list:
            HangmanGame(root, word_list, "Hrvatski")  
        else:
            messagebox.showerror("Error", f"Nema dostupnih riječi za kategoriju '{category}'.")



root = tk.Tk()                
LanguageSelection(root)       
root.mainloop()               