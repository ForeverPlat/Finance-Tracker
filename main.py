# main.py
from db import TransactionDB


def main():
    db = TransactionDB()

    while True:
        print("\n====== Finance Tracker (CLI Version) ======")
        print(f"Current Total: ${db.get_current_total():.2f}")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show History")
        print("4. Exit")
        
        choice = input("Choose an option: ").strip()

        if choice == "1":
            amount = float(input("Enter amount: "))
            db.add_transaction(amount, category="Income", comment="")
        
        elif choice == "2":
            amount = float(input("Enter amount: "))
            db.add_transaction(-amount, category="Expense", comment="")
        
        elif choice == "3":
            print("\nTransaction History:")
            for row in db.get_all():
                print(row)
        
        elif choice == "4":
            print("Exiting...")
            db.close()
            break
        
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
