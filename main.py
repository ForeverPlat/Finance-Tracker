from typing import Tuple
from Settings import *
import customtkinter as ctk
import sqlite3

con = sqlite3.connect("tracking.db")
cursor = con.cursor()

#change this to total, transaction, category, comment
cursor.execute('CREATE TABLE IF NOT EXISTS tracking (total REAL, "transaction" TEXT, category TEXT, comment TEXT)')

cursor.execute('SELECT COUNT(*) FROM tracking')
row_count = cursor.fetchone()[0]

if row_count == 0:
    initial_data = '''INSERT INTO tracking (total, "transaction", category, comment) VALUES (?, ?, ?, ?)'''
    initial_insert_tuple = (0.0, "", "", "")

    cursor.execute(initial_data, initial_insert_tuple)
    con.commit()


#App
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        #creating window
        self.geometry('400x400')
        self.title('')
        self.iconbitmap('blank.ico')
        self.resizable(False, False)

        #creating grid configuration
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)


        #Instantiate the widgets
        frame_one = FrameOne(self)
        user_entry = UserEntry(frame_one)
        frame_two = FrameTwo(self, user_entry)
        title_label = TitleLabel(frame_one)
        choice_addition_button = ChoiceAdditionButton(frame_one.button_frame, user_entry, frame_two)
        choice_subtraction_button = ChoiceSubtractionButton(frame_one.button_frame, user_entry, frame_two)
        

        #make widgets visable
        frame_one.show()
        frame_two.show()
        title_label.show()
        user_entry.show()
        choice_addition_button.show()
        choice_subtraction_button.show()

        self.mainloop()


class FrameOne(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = 'transparent')

        #creating grid configuration
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(0, weight = 1)

        # Create a dedicated button frame for the buttons in row 2
        self.button_frame = ctk.CTkFrame(self, fg_color = 'transparent')
        self.button_frame.grid(row=2, column=0, sticky='w', padx=10)

        # Configure the grid of the button frame to hold two buttons side by side
        self.button_frame.rowconfigure(0, weight = 1)
        self.button_frame.columnconfigure(0, weight = 1)
        self.button_frame.columnconfigure(1, weight = 1)


    def show(self):
        self.grid(row = 0, column = 0, sticky = 'nsew', pady = 150)

    def hide(self):
        self.grid_forget()


#Creates 'Current Balance ($)' label, this labels text will change as need
class TitleLabel(ctk.CTkLabel):
    def __init__(self, parent):
        font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE, weight='bold')
        super().__init__(master = parent, font = font, text_color = WHITE)

        self.configure(text = 'Current Balance ($)')

    def text_for_addition(self):
        self.configure(text = 'Add Balance ($)')

    def text_for_subtraction(self):
        self.configure(text = 'Subtract Balance ($)')

    def show(self):
        self.grid(row = 0, column = 0, sticky = 'sw', padx = 10)

#Creates Users Entry
'''The plan is to use the same entry for all the functions
simply using different variables will be what decides how the 
entry will function'''
class UserEntry(ctk.CTkEntry):
    def __init__(self, parent):
        self.default_font = ctk.CTkFont(family = FONT, size = ENTRY_TEXT_SIZE, weight = 'bold')
        super().__init__(master = parent, font = self.default_font, text_color = WHITE, border_width = 0, fg_color = 'transparent', height = 40)

        self.total = 0.00
        self.insert(0, f"{self.total:.2f}")
        self.configure(state = "disabled")

    #helps in the creation of default entry text
    def temp_text(self, e):
        self.delete(0,"end")

        self.configure(font=self.default_font)

       
    def text_for_addition(self):
        addition_font = ctk.CTkFont(family = FONT, size = TEMP_ENTRY_TEXT_SIZE, weight='bold')

        self.configure(text_color = GREEN, state = "normal", font = addition_font)
        self.delete(0, "end")              # Clear any existing text
        self.insert(0, "Enter Amount")
        self.bind("<FocusIn>", self.temp_text)

    def text_for_subtraction(self):
        subtraction_font = ctk.CTkFont(family = FONT, size = TEMP_ENTRY_TEXT_SIZE, weight='bold')

        self.configure(text_color = RED, state = "normal", font = subtraction_font)
        self.delete(0, "end")              # Clear any existing text
        self.insert(0, "Enter Amount")
        self.bind("<FocusIn>", self.temp_text)

    def get_entered_value(self):
        value = float(self.get())
        return value

    def show_current_balance(self):
        self.delete(0, "end")        
        self.insert(0, f"{self.total:.2f}")
        self.configure(text_color = WHITE, font = self.default_font, state = "disabled")

    def show(self):
        self.grid(row = 1, column = 0, sticky = 'w', padx = 5)


'''    def get_entered_addition_value(self):
        self.added_value = self.get()
        self.total += float(self.added_value)


    def get_entered_subtraction_value(self):
        self.subtracted_value = self.get()
        self.total -= float(self.subtracted_value)'''



#Creates the two button options
class ChoiceAdditionButton(ctk.CTkButton):
    def __init__(self, parent, user_entry, frame_two):
        super().__init__(master = parent, width = 1, text = '+', text_color = GREEN, fg_color = 'transparent', command = self.combined_commands)
        self.user_entry = user_entry
        self.frame_two = frame_two
        
    def combined_commands(self):
        #need to add the function that hides the subtraction options
        self.change_text_for_addition()
        self.frame_two.hide_subtraction_options()
        self.frame_two.show_addition_options()


    def change_text_for_addition(self):
        self.user_entry.text_for_addition()

    def show_addition_sections(self):
        pass

    def show(self):
        # Place button in the button frame at row 0, column 0
        self.grid(row=0, column=0, sticky='w')
    
    def hide(self):
        #should simply make button invisible and disable there functionallity, should be called when this button is clicked
        pass


class ChoiceSubtractionButton(ctk.CTkButton):
    def __init__(self, parent, user_entry, frame_two):
        super().__init__(master = parent, width = 1, text = '-', text_color = RED, fg_color = 'transparent', command = self.combined_commands)
        self.user_entry = user_entry
        self.frame_two = frame_two

    '''Needs a a combinned command function, this function should hide what is currently know has frame two (the addition options) and display the subtraction options'''
    def combined_commands(self):
        #need to add the function that hides the subtraction options
        self.change_text_for_subtraction()
        self.frame_two.hide_addition_options()
        self.frame_two.show_subtraction_options()

    def change_text_for_subtraction(self):
        #will call the funtion in entry that changes the color of the entries text
        self.user_entry.text_for_subtraction()



    def show(self):
        self.grid(row = 0, column = 1, sticky = 'w', padx = 10)
    
    def hide(self):
        #should simply make button invisible and disable there functionallity, should be called when this button is clicked
        pass


class FrameTwo(ctk.CTkFrame):
    def __init__(self, parent, user_entry):
        super().__init__(master = parent, fg_color = 'transparent')
        self.user_entry = user_entry

        #creating grid configuration
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.columnconfigure(0, weight = 1)

        '''need one Var that is changed based on which button was last clicked'''

        self.option_string = ""
        self.comment_text = ""


        #this fucntion should store the 
        def option_choice(button_text):
            #make this store into the data base
            self.option_string = button_text
            print(self.option_string)

            if self.option_string == "":
                self.add_value_button.configure(state = "disabled")
                self.subtract_value_button.configure(state = "disabled")
            else:
                self.add_value_button.configure(state = "normal")
                self.subtract_value_button.configure(state = "normal")
        
        #comment and button frame for gird purposes
        self.comment_frame = ctk.CTkFrame(self, fg_color = 'transparent')

        #grid system for the comment frame
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)       

        #creating sudo version of radio buttons for addition
        self.work_button = ctk.CTkButton(self, text = 'Work', fg_color = 'transparent', anchor="w", command = lambda: option_choice("Work"))
        self.allowance_button = ctk.CTkButton(self, text = 'Allowance', fg_color = 'transparent', anchor="w", command = lambda: option_choice("Allowance"))
        self.gifts_button = ctk.CTkButton(self, text = 'Gifts', fg_color = 'transparent', anchor="w", command = lambda: option_choice("Gift"))


        #this button will need its own fucntion seperate from the rest
        self.add_value_button = ctk.CTkButton(self.comment_frame, width = 10,text = '+', state = 'disabled', text_color = GREEN, fg_color = 'transparent', anchor="e", command = self.combined_addition_commands) 


        #creating sudo version of radio buttons for subtraction
        self.school_button = ctk.CTkButton(self, text = 'School', fg_color = 'transparent', anchor="w", command = lambda: option_choice("School"))
        self.food_button = ctk.CTkButton(self, text = 'Food', fg_color = 'transparent', anchor="w", command = lambda: option_choice("Food"))
        self.clothes_button = ctk.CTkButton(self, text = 'Clothes', fg_color = 'transparent', anchor="w", command = lambda: option_choice("Clothes"))

        #this button will need its own fucntion seperate from the rest
        self.subtract_value_button = ctk.CTkButton(self.comment_frame, width = 10, text = '-', state = 'disabled', text_color = RED, fg_color = 'transparent', anchor="e", command = self.combined_subtraction_commands) 


        #other button for both addition and subtraction
        self.other_button = ctk.CTkButton(self, text = 'Other', fg_color = 'transparent', anchor="w", command = lambda: option_choice("Other"))


        self.comment = ctk.CTkEntry(self.comment_frame, text_color = WHITE, width = 110)


    def combined_addition_commands(self):
        #need to add the function that hides the subtraction options
        self.value = self.user_entry.get_entered_value()

        self.hide_addition_options()
        self.hide_subtraction_options()

        self.get_comment()

        self.inserted_value = ("+" + str(self.value))

        self.insert_to_database()
        self.reset_option_choice()

        self.user_entry.total += self.value

        self.user_entry.show_current_balance()

                
        

    def combined_subtraction_commands(self):
        #need to add the function that hides the subtraction options
        self.value = self.user_entry.get_entered_value()

        self.hide_addition_options()
        self.hide_subtraction_options()

        self.get_comment()

        self.inserted_value = ("-" + str(self.value))

        self.insert_to_database()
        self.reset_option_choice()

        self.user_entry.total -= self.value

        self.user_entry.show_current_balance()


    def get_comment(self):
        self.comment_text = self.comment.get()
        print(self.comment_text)

    def insert_to_database(self):

        #can use an if statement to determine whether or no to add transaction to total
        #cursor.execute("SELECT title FROM transaction")

        #for row in cursor.execute('SELECT * FROM tracking'):
            #this take index 1 of the row and the slices it
        #    latestRow = row
        
        #most_recent_transaction_operator = latestRow[1][0:1]

        #most_recent_transaction = float(row[1][1:])
        #most_recent_total = float(row[0])

        #if most_recent_transaction != 0.0:
            #if most_recent_transaction_operator == "+":
            #    new_total = most_recent_total +  most_recent_transaction
            #elif most_recent_transaction_operator == "-":
            #    new_total = most_recent_total -  most_recent_transaction

            #self.user_entry.total = new_total


        #change this to total, transaction, category, comment
        data_insert_initial = '''INSERT INTO tracking (total, "transaction", category, comment) VALUES (?,?,?,?)'''

        print(self.user_entry.total)
        # Prepare the data to be inserted
        data_insert_tuple = (self.user_entry.total, self.inserted_value, self.option_string, self.comment_text)

        cursor.execute(data_insert_initial, data_insert_tuple)
        con.commit()

    def reset_option_choice(self):
        self.option_string = ""
        self.add_value_button.configure(state = 'disabled')
        self.subtract_value_button.configure(state = 'disabled')
        
    def show(self):
        # Place button in the button frame at row 0, column 1
        self.grid(row=0, column=1, sticky='nsew', pady = 55)


    def show_addition_options(self):
        self.work_button.grid(row = 0, column = 0)
        self.allowance_button.grid(row = 1, column = 0)
        self.gifts_button.grid(row = 2, column = 0)
        self.other_button.grid(row = 3, column = 0)
        self.comment_frame.grid(row = 4, column = 0)
        self.comment.grid(row = 0, column = 0)
        self.add_value_button.grid(row = 0, column = 1)

    def show_subtraction_options(self):
        self.school_button.grid(row = 0, column = 0) 
        self.food_button.grid(row = 1, column = 0) 
        self.clothes_button.grid(row = 2, column = 0) 
        self.other_button.grid(row = 3, column = 0)
        self.comment_frame.grid(row = 4, column = 0)
        self.comment.grid(row = 0, column = 0)
        self.subtract_value_button.grid(row = 0, column = 1) 

    def hide_addition_options(self):
        self.work_button.grid_forget()
        self.allowance_button.grid_forget()
        self.gifts_button.grid_forget() 
        self.other_button.grid_forget()
        self.add_value_button.grid_forget()
        self.comment_frame.grid_forget()


    def hide_subtraction_options(self):
        self.school_button.grid_forget()
        self.food_button.grid_forget()
        self.clothes_button.grid_forget() 
        self.other_button.grid_forget()
        self.subtract_value_button.grid_forget()
        self.comment_frame.grid_forget()






#Creates the radio buttons for the Add and Minus



#Creates the button to do the calculations

App()

cursor.close()
con.close()