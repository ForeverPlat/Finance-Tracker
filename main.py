from db import TransactionDB
from ui import App

def main():
    db = TransactionDB()
    app = App(db)
    app.mainloop()
    db.close()

if __name__ == "__main__":
    main()
