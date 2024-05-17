import tkinter as tk
from tkinter import messagebox
import json
from plans import get_plans

def validate_number(P):
    """ Validate that the entry is numeric. """
    return P.isdigit() or P == ""

def add_member_frame(container, entries_list):
    frame = tk.Frame(container)
    frame.pack(fill='x', padx=5, pady=5)

    # Age input with label
    tk.Label(frame, text="Age:").pack(side='left')
    age_entry = tk.Entry(frame, width=5, validate='key', validatecommand=(container.register(validate_number), '%P'))
    age_entry.pack(side='left', padx=5)

    # Smoker checkbox with label
    smoker_var = tk.BooleanVar()
    tk.Checkbutton(frame, text="Smoker?", variable=smoker_var, onvalue=True, offvalue=False).pack(side='left', padx=5)

    # Gender dropdown with label
    tk.Label(frame, text="Gender:").pack(side='left')
    gender_var = tk.StringVar(frame)
    gender_var.set("male")  # default value
    gender_menu = tk.OptionMenu(frame, gender_var, "male", "female", "other")
    gender_menu.pack(side='left', padx=5)

    # Zip code input with label
    tk.Label(frame, text="Zip Code:").pack(side='left')
    zip_entry = tk.Entry(frame, width=10, validate='key', validatecommand=(container.register(validate_number), '%P'))
    zip_entry.pack(side='left', padx=5)

    # Relationship dropdown with label
    tk.Label(frame, text="Relationship:").pack(side='left')
    relationship_var = tk.StringVar(frame)
    relationship_var.set("child")  # default value
    relationship_menu = tk.OptionMenu(frame, relationship_var, "spouse", "domestic partner", "child")
    relationship_menu.pack(side='left', padx=5)

    # Remove button
    def remove_member():
        frame.destroy()
        entries_list.remove((age_entry, smoker_var, gender_var, zip_entry, relationship_var))
    remove_button = tk.Button(frame, text="Remove", command=lambda: remove_member())
    remove_button.pack(side='right', padx=5)

    entries_list.append((age_entry, smoker_var, gender_var, zip_entry, relationship_var))
    return frame

def submit(applicant_details, entries_list):
    try:
        applicant_data = {
            "age": int(applicant_details['age'].get()),
            "smoker": applicant_details['smoker'].get(),
            "gender": applicant_details['gender'].get(),
            "zip": int(applicant_details['zip'].get())
        }

        family_data = []
        for entry in entries_list:
            age, smoker, gender, zip_code, relationship = entry
            member = {
                "age": int(age.get()),
                "smoker": smoker.get(),
                "gender": gender.get(),
                "zip": int(zip_code.get()),
                "relationship": relationship.get()
            }
            family_data.append(member)

        data = {
            "householdIncome": int(applicant_details['income'].get()),
            "applicant": applicant_data,
            "family": family_data
        }
        get_plans(data)
    except ValueError as e:
        messagebox.showerror("Input Error", "Please check your inputs. Ensure all ages, zip codes, and income are numbers.")

root = tk.Tk()
root.title("Insurance Plan Input Form")

applicant_details = {}
member_entries = []

# Main Applicant Details Section
tk.Label(root, text="Main Applicant Details").pack(fill='x', padx=5, pady=5)
main_frame = tk.Frame(root)
main_frame.pack(fill='x', padx=10, pady=10)

# Labels and entries for each main applicant detail
tk.Label(main_frame, text="Applicant Age:").pack(side='left')
applicant_details['age'] = tk.Entry(main_frame, width=5, validate='key', validatecommand=(root.register(validate_number), '%P'))
applicant_details['age'].pack(side='left', padx=5)

tk.Label(main_frame, text="Smoker?").pack(side='left')
applicant_details['smoker'] = tk.BooleanVar()
tk.Checkbutton(main_frame, variable=applicant_details['smoker'], onvalue=True, offvalue=False).pack(side='left', padx=5)

tk.Label(main_frame, text="Applicant Gender:").pack(side='left')
applicant_details['gender'] = tk.StringVar(main_frame)
applicant_details['gender'].set("male")  # default value
tk.OptionMenu(main_frame, applicant_details['gender'], "male", "female", "other").pack(side='left', padx=5)

tk.Label(main_frame, text="Applicant Zip Code:").pack(side='left')
applicant_details['zip'] = tk.Entry(main_frame, width=10, validate='key', validatecommand=(root.register(validate_number), '%P'))
applicant_details['zip'].pack(side='left', padx=5)

tk.Label(main_frame, text="Household Income:").pack(side='left')
applicant_details['income'] = tk.Entry(main_frame, width=10, validate='key', validatecommand=(root.register(validate_number), '%P'))
applicant_details['income'].pack(side='left', padx=5)

# Family Members Section
members_label = tk.Label(root, text="Add Family Members (optional)")
members_label.pack(fill='x', padx=5, pady=5)

members_frame = tk.Frame(root)
members_frame.pack(fill='both', expand=True, padx=10, pady=10)

add_member_button = tk.Button(root, text="Add Family Member", command=lambda: add_member_frame(members_frame, member_entries))
add_member_button.pack(pady=10)

submit_button = tk.Button(root, text="Submit", command=lambda: submit(applicant_details, member_entries))
submit_button.pack(pady=10)

root.mainloop()
