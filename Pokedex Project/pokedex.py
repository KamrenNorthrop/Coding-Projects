import os
import json
import time
import random
import requests
import pypokedex
import tkinter as tk
from io import BytesIO
from tkinter import messagebox
from PIL import Image, ImageTk
from catch_rates import catch_rates_dict

#TODO: Code store front for game transactions. Items, currency decrement on transaction, add item to player inventory.

class Pokedex:
    def __init__(self):
        self.inventory = []
        self._currency = 100
        self.pokeball = 100
        self.greatball = 5
        self.ultraball = 1

        #1 = pokeball, 2 = greatball, 3 = ultraball, 4 = masterball
        self.pokeballs = {
            1 : 255,
            2 : 200,
            3 : 150,
        }

#----------GETTERS----------#
    def get_pokeball_modifier(self, pokeball_choice):
        return self.pokeballs.get(pokeball_choice, 255)
    
    def get_inventory(self):
        if self.inventory:
            return self.inventory
        else:
            return None
        
    def get_catch_rate(self, id):
        if id >= 1 and id <= 1025:
            return catch_rates_dict.get(id)
        
        return None
    
    def get_currency(self):
        return self._currency
    
#----------SETTERS----------#
    @property
    def currency(self):
        return self._currency
    
    @currency.setter    
    def currency(self, amount):
        self._currency = round(amount, 2)


#----------General Functions----------#
    def start(self):
        self.window = tk.Tk()
        self.window.geometry("700x600")
        self.window.title("Pokedex")
        self.window.configure(bg="black")
        self.window.resizable(True, True)

        self.entry_field = tk.Label(self.window, text="Pokedex Logic", font=("Arial", 24), bg="black", fg="white")
        self.entry_field_box = tk.Entry(self.window, font=("Arial", 24), width=15)
        self.entry_field.pack(padx=10, pady=10)
        self.entry_field_box.pack(pady=10)
        self.entry_field_box.after(20, lambda: self.entry_field_box.focus_force())

        button_frame = tk.Frame(self.window, bg="black")
        button_frame.pack(side="top", pady=10)

        search_button = tk.Button(button_frame, text="Search (Enter)", font=("Arial", 14), command=lambda: self.on_click(self.entry_field_box.get()), bg="black", fg="white")
        self.window.bind("<Return>", lambda event: self.on_click(self.entry_field_box.get()))
        search_button.pack(side="left", padx=10, pady=10)

        exit_button = tk.Button(button_frame, text="Exit (Esc)", font=("Arial", 14), command=self.window.destroy, bg="black", fg="white")
        self.window.bind("<Escape>", lambda event: self.window.destroy())
        exit_button.pack(side="right", padx=10, pady=10)

        self.window.mainloop()


    def print_pokemon(self, pokemon):
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Label) and widget != self.entry_field and widget != self.entry_field_box:
                widget.destroy()

        if pokemon:
            try:
                image = Image.open(BytesIO(requests.get(pokemon.sprites.front["default"]).content)).convert("RGBA")
                tk_image = ImageTk.PhotoImage(image.resize((150, 150), Image.ANTIALIAS))
            except Exception as e:
                print(f"Error loading image: {e}")
                tk_image = None

            image_label = tk.Label(self.window, image=tk_image, bg="black")
            image_label.image = tk_image
            image_label.pack(pady=10)

            info_label = tk.Label(self.window, text=f"ID:{pokemon.dex} - {pokemon.name.capitalize()}\nType: {', '.join(t.capitalize() for t in pokemon.types)}\nAbilities: {', '.join(a.name.replace('-', ' ').title() for a in pokemon.abilities)}", font=("Arial", 16), bg="black", fg="white")
            info_label.pack(pady=10)

    #Search by dex ID and name.
    def search_pokemon(self, pokemon_name):
        try:
            if str(pokemon_name).isdigit():
                return pypokedex.get(dex=int(pokemon_name)) #dex id
            else:
                return pypokedex.get(name=str(pokemon_name).lower()) #name
        except Exception as e:
            print(f"Error in search: {e}")
            return None
    

    def display_pokemon(self, pokemon):
        self.window = tk.Tk()
        self.window.geometry("700x600")
        self.window.title("Pokedex")
        self.window.configure(bg="black")
        self.window.resizable(True, True)
        self.window.focus_force()

        self.info_label = tk.Label(self.window, text=f"You caught a wild {pokemon.name.capitalize()}!", font=("Arial", 24), bg="black", fg="white")
        self.info_label.pack(padx=10, pady=10)

        self.info_label2 = tk.Label(self.window, text=f"{pokemon.name.capitalize()} was added to your inventory.", font=("arial", 16), bg="black", fg="white")
        self.info_label2.pack(padx=5, pady=5)

        earned_currency = self.add_currency(pokemon)
        self.info_label3 = tk.Label(self.window, text=f"You earned {earned_currency} schmeckles.", font=("arial", 16), bg="black", fg="white")
        self.info_label3.pack(padx=5, pady=5)

        try:
            image = Image.open(BytesIO(requests.get(pokemon.sprites.front["default"]).content)).convert("RGBA")
            tk_image = ImageTk.PhotoImage(image.resize((150, 150), Image.ANTIALIAS))
        except Exception as e:
            print(f"Error loading image: {e}")
            tk_image = None

        image_label = tk.Label(self.window, image=tk_image, bg="black")
        image_label.image = tk_image
        image_label.pack(pady=10)

        info_label = tk.Label(self.window, text=f"ID: {pokemon.dex}\n {pokemon.name.capitalize()}\nType: {', '.join(t.capitalize() for t in pokemon.types)}\nAbilities: {', '.join(a.name.replace('-', ' ').title() for a in pokemon.abilities)}", font=("Arial", 16), bg="black", fg="white")
        info_label.pack(pady=10)

        button_frame = tk.Frame(self.window, bg="black")
        button_frame.pack(side="top", pady=10)

        exit_button = tk.Button(button_frame, text="Exit (Esc)", font=("Arial", 14), command=self.window.destroy, bg="black", fg="white")
        self.window.bind("<Escape>", lambda event: self.window.destroy())
        exit_button.pack(side="right", padx=10, pady=10)

        self.window.mainloop()


    def find_pokemon(self):
        poke_id = random.randint(-500, 1501)

        if poke_id >= 1 and poke_id <= 1025:
            pokemon = self.search_pokemon(poke_id)
        else:
            pokemon = None
            
        return pokemon
    

    def catch_pokemon(self, pokemon, ball_modifier):
        f = 4
        base_catch_rate = catch_rates_dict.get(pokemon.dex, 3)
        
        catch_probability = 1 + (((base_catch_rate + 1) * ball_modifier + f + 1256) / (ball_modifier + 1))
        catch_percent = min(catch_probability / 255, 1.0)

        return random.random() < catch_percent

    def guarantee_catch(self, pokemon):
        self.inventory.append({
            "id": pokemon.dex,
            "name": pokemon.name
        })
        self.display_pokemon(pokemon)
        self.inventory = sorted(self.inventory, key=lambda x: x["id"])
        return 

    def on_click(self, args):
        if args.isdigit():
            pokemon = self.search_pokemon(int(args))
        else:
            pokemon = self.search_pokemon(str(args).lower())

        if pokemon:
            self.print_pokemon(pokemon)
        else:
            messagebox.showerror("Error", "Pokemon not found. Please check the name or Dex ID.")

    def add_currency(self, pokemon):
        earned_currency = (255 / self.get_catch_rate(pokemon.dex)) * 10
        self._currency += earned_currency
        self._currency = round(self._currency, 2)
        return round(earned_currency, 2)


    #----------SAVING / LOADING----------#
     #Are files the same?
    def has_changes(self, current_inventory, filename="pokedex_save.json"):
        if not os.path.exists(filename):
            return True
        
        with open(filename, "r") as file:
            saved_inventory = json.load(file)

        return current_inventory != saved_inventory
    
    #Save game to JSON file.
    def save_game(self, filename="pokedex_save.json"):
        save_data = {
            "inventory": self.inventory,
            "currency": self._currency,
            "pokeball": self.pokeball,
            "greatball": self.greatball,
            "ultraball": self.ultraball
        }
        with open(filename, "w") as file:
            json.dump(save_data, file)
        print(f"Game saved to {filename}.\n")

    #Load game from JSON file.
    def load_game(self, filename="pokedex_save.json"):
        try:
            with open(filename, "r") as file:
                save_data = json.load(file)  # Load everything as a dict

            self.inventory = save_data.get("inventory", [])
            self._currency = save_data.get("currency", 0)
            self.pokeball = save_data.get("pokeball", 10)
            self.greatball = save_data.get("greatball", 5)
            self.ultraball = save_data.get("ultraball", 2)

            print(f"Game loaded from {filename}.")

        except FileNotFoundError:
            print(f"No save file found at {filename}. Starting a new game.")
            self.inventory = []
            self._currency = 0
            self.pokeball = 100
            self.greatball = 5
            self.ultraball = 2

        except json.JSONDecodeError:
            print("Error loading save file. Starting a new game.")
            self.inventory = []
            self._currency = 0
            self.pokeball = 100
            self.greatball = 5
            self.ultraball = 2

        except Exception as e:
            print(f"An error occurred while loading the game: {e}")
            self.inventory = []
            self._currency = 0
            self.pokeball = 100
            self.greatball = 5
            self.ultraball = 2

        return self.inventory
    
#----------PROMPTS----------#
    def pokeball_choice_prompt(self):
        print(f"""
What Pokeball would you like to use?
    1. Pokeball: {self.pokeball} remaining
    2. Greatball: {self.greatball} remaining
    3. Ultraball: {self.ultraball} remaining
    """)
        

        ball_choice = input("Enter your choice: ").strip()

        if ball_choice == "1" and self.pokeball > 0:
            self.pokeball -= 1
        elif ball_choice == "2" and self.greatball > 0:
            self.greatball -= 1
        elif ball_choice == "3" and self.ultraball > 0:
            self.ultraball -= 1
        else:
            print("You have none of those left!")
            return None

        return ball_choice
    
    def main_menu_prompt(self):
        print("""
What would you like to do?
    1. Search for Pokemon
    2. Pokedex Search
    3. Inventory
    4. Shop
    5. Save & Exit
        """)

        choice = input("\nEnter your choice: ").strip()
        return choice  
    
    def save_game_prompt(self):
        choice = True
        while choice:
            options = ["yes", "no", "y", "n"]
            usr_choice = input("Would you like to save your game? (y/n) ").strip().lower()

            if usr_choice not in options:
                print("Invalid choice. Please try again.")
                continue

            if usr_choice == "yes" or usr_choice == "y":
                print("Saving current game...\n")
                time.sleep(2)
                self.save_game()
                choice = False
            return
    
    def load_game_prompt(self):
        if os.path.exists("pokedex_save.json"):
            choice = True
            while choice:
                options = ["yes", "no", "y", "n"]
                print("If you wish to start a new game, select 'No' and your previous game will be overwritten when saved.")
                usr_choice = input("Would you like to load a previous game? (y/n) ").strip().lower()
                
                if usr_choice not in options:
                    print("Invalid choice. Please try again.")
                    continue

                if usr_choice == "yes" or usr_choice == "y":
                    print("Loading previous game...\n")
                    time.sleep(2)
                    self.load_game()
                    choice = False
                return
            
    def shop_prompt(self):
            #1 = pokeball, 2 = greatball, 3 = ultraball
        item_prices = {
            "1": 5.99,
            "2": 49.99,
            "3": 99.99,
        }
        shopping = True

        while shopping:
            print(f"Welcome to the shop!\n")
            print(f"You currently have {self._currency} schmeckles.\n")
            print(f"What would you like to buy?")
            print(f"    1. Pokeball - 9.99 schmeckles: {self.pokeball} remaining")
            print(f"    2. Greatball - 49.99 schmeckles: {self.greatball} remaining")
            print(f"    3. Ultraball - 99.99 schmeckles: {self.ultraball} remaining")
            print(f"    4. Exit shop")

            options = ["1", "2", "3", "4"]
            usr_choice = input("Enter your choice: ").strip()
            if usr_choice not in options:
                print("Invalid choice. Please try again.")
                return
            
            price = item_prices.get(usr_choice)

            if usr_choice == "1" or usr_choice == "2" or usr_choice == "3":
                print("How many would you like to buy?")
                quantity = input("Enter your choice: ").strip()
                quantity = int(quantity)
                if quantity <= 0:
                    print("Invalid quantity. Please try again.")
                    continue

            #TODO: Finish choices 1-4
            #TODO: Add choice to buy variable number of items
            if usr_choice == "1":
                total_price = price * quantity
                if total_price > self._currency:
                    print("You don't have enough schmeckles for that!")
                    continue

                self._currency = round((self._currency - total_price), 2)
                self.pokeball += quantity
                print(f"You bought {quantity} Pokeballs!")

            if usr_choice == "2":
                total_price = price * quantity
                if total_price > self._currency:
                    print("You don't have enough schmeckles for that!")
                    continue
        
                self._currency = round((self._currency - total_price), 2)
                self.greatball += quantity
                print(f"You bought {quantity} Greatballs!")

            if usr_choice == "3":
                total_price = price * quantity
                if total_price > self._currency:
                    print("You don't have enough schmeckles for that!")
                    continue

                self._currency = round((self._currency - total_price), 2)
                self.ultraball += quantity
                print(f"You bought {quantity} Ultraballs!")

            if usr_choice == "4":
                return
                
            options = ["y", "n"]    
            print("Would you like to buy more? (y/n)")
            buy_more = input("Enter your choice: ").strip()

            if buy_more not in options:
                print("Invalid choice. Please try again.")
                continue

            if buy_more == "y":
                continue
            else:
                shopping = False
                print("Thank you for shopping!")
        return