from tkinter import *
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import sqlite3

# =========================================================
# Assignment Title : Cricket Team Management System - Data Viewer
# Student Name     : Nagasai Chintalapati
# Student Number   : A00316625
# Course           : Software Design with Ai and Cloud Computing
# =========================================================

# ==  Color Scheme ==
colors = {
    'primary': '#0D0D0D',
    'secondary': '#16A085',  # Greenish-cyan buttons
    'accent1': '#27AE60',  # Bright green (hover color)
    'accent2': '#2ECC71',  # Lime green (active)
    'dark_bg': '#0B0C10',  # Background shade
    'light_bg': '#1F2833',  # Panel background
    'text_light': '#C5C6C7',  # Light grey text
    'text_bright': '#00FF88'  # Neon green accent text
}

# == Database Connection ==
con = sqlite3.connect(":memory:", check_same_thread=False)
cur = con.cursor()

def init_sample_db():
    """Initialize sample database for viewing"""
    try:
        cur.execute("DROP TABLE IF EXISTS Teams")
        cur.execute("DROP TABLE IF EXISTS Players")
        cur.execute("DROP TABLE IF EXISTS Matches")
        cur.execute("DROP TABLE IF EXISTS Performances")

        cur.execute("""
            CREATE TABLE Teams(
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT UNIQUE NOT NULL,
                coach_name TEXT, home_ground TEXT,
                wins INTEGER DEFAULT 0, losses INTEGER DEFAULT 0, draws INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE Players(
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, age INTEGER, nationality TEXT, role TEXT,
                team_id INTEGER, salary REAL
            )
        """)
        cur.execute("""
            CREATE TABLE Matches(
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team1_id INTEGER, team2_id INTEGER, match_date TEXT, venue TEXT,
                result TEXT
            )
        """)

        teams = [
            ("Mumbai Indians", "Mahela Jayawardene", "Wankhede Stadium", 5, 2, 1),
            ("Chennai Super Kings", "Stephen Fleming", "M. A. Chidambaram Stadium", 4, 3, 1),
            ("Royal Challengers Bangalore", "Sanjay Bangar", "M. Chinnaswamy Stadium", 3, 4, 1),
        ]
        cur.executemany(
            "INSERT INTO Teams(team_name, coach_name, home_ground, wins, losses, draws) VALUES (?,?,?,?,?,?)", teams)

        players = [
            ("Rohit Sharma", 36, "Indian", "Batsman", 1, 1500000),
            ("Jasprit Bumrah", 30, "Indian", "Bowler", 1, 1100000),
            ("MS Dhoni", 42, "Indian", "Wicketkeeper", 2, 1200000),
            ("Virat Kohli", 35, "Indian", "Batsman", 3, 1700000),
        ]
        cur.executemany("INSERT INTO Players(name, age, nationality, role, team_id, salary) VALUES (?,?,?,?,?,?)",
                        players)

        matches = [
            (1, 2, "2024-03-26", "Wankhede Stadium", "Mumbai Indians won by 7 runs"),
            (3, 1, "2024-03-28", "Eden Gardens", "Kolkata Knight Riders won by 3 wickets"),
        ]
        cur.executemany("INSERT INTO Matches(team1_id, team2_id, match_date, venue, result) VALUES (?,?,?,?,?)",
                        matches)

        con.commit()
    except Exception as e:
        print("DB init error:", e)


init_sample_db()

# ==  Button ==
def create_button(master, text, command=None, **kwargs):
    btn = Button(
        master,
        text=text,
        bg=colors['secondary'],
        fg=colors['text_light'],
        activebackground=colors['accent1'],
        activeforeground='black',
        relief="flat",
        font=("Consolas", 10, "bold"),
        command=command,
        padx=12, pady=6,
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2",
        **kwargs
    )

    def on_enter(e):
        btn['bg'] = colors['accent2']
        btn['fg'] = 'black'

    def on_leave(e):
        btn['bg'] = colors['secondary']
        btn['fg'] = colors['text_light']

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


# ==  Function ==
def export_data(data_list, title):
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filename:
        with open(filename, 'w') as f:
            if "Player" in title:
                f.write("Player ID,Name,Age,Nationality,Role,Team,Salary\n")
            elif "Team" in title:
                f.write("Team Name,Coach,Home Ground,Wins,Losses,Draws,Points\n")
            elif "Match" in title:
                f.write("Match ID,Team 1,Team 2,Date,Venue,Result\n")
            for row in data_list:
                f.write(','.join(map(str, row)) + '\n')
        messagebox.showinfo("Success", f"Data exported to {filename}")


# ==  View Functions ==
def view_all_players():
    cur.execute("""
        SELECT p.player_id, p.name, p.age, p.nationality, p.role, t.team_name, p.salary 
        FROM Players p 
        JOIN Teams t ON p.team_id = t.team_id 
        ORDER BY p.name
    """)
    data = cur.fetchall()
    display_data_in_viewer(data, "All Players")


def view_all_teams():
    cur.execute("""
        SELECT team_name, coach_name, home_ground, wins, losses, draws, (wins*2 + draws) as points 
        FROM Teams 
        ORDER BY points DESC
    """)
    data = cur.fetchall()
    display_data_in_viewer(data, "All Teams")


def view_all_matches():
    cur.execute("""
        SELECT m.match_id, t1.team_name, t2.team_name, m.match_date, m.venue, m.result 
        FROM Matches m 
        JOIN Teams t1 ON m.team1_id = t1.team_id 
        JOIN Teams t2 ON m.team2_id = t2.team_id 
        ORDER BY m.match_date DESC
    """)
    data = cur.fetchall()
    display_data_in_viewer(data, "All Matches")


def view_players_by_role():
    roles = ["Batsman", "Bowler", "All-rounder", "Wicketkeeper"]
    role_window = Toplevel(viewer_window)
    role_window.title("Select Role")
    role_window.geometry("300x200")
    role_window.configure(bg=colors['dark_bg'])

    Label(role_window, text="Select Player Role:", font=("Consolas", 12, "bold"),
          fg=colors['text_bright'], bg=colors['dark_bg']).pack(pady=10)

    for role in roles:
        btn = create_button(role_window, role,
                            command=lambda r=role: show_players_by_role(r, role_window),
                            width=20)
        btn.pack(pady=5)


def show_players_by_role(role, window):
    window.destroy()
    cur.execute("""
        SELECT p.player_id, p.name, p.age, p.nationality, t.team_name, p.salary 
        FROM Players p 
        JOIN Teams t ON p.team_id = t.team_id 
        WHERE p.role = ? 
        ORDER BY p.name
    """, (role,))
    data = cur.fetchall()
    display_data_in_viewer(data, f"Players - {role}")


def view_teams_by_performance():
    cur.execute("""
        SELECT team_name, wins, losses, draws, (wins*2 + draws) as points,
               ROUND((wins * 100.0 / (wins + losses + draws)), 2) as win_percentage
        FROM Teams 
        ORDER BY win_percentage DESC
    """)
    data = cur.fetchall()
    display_data_in_viewer(data, "Teams by Performance")


def view_matches_by_venue():
    cur.execute("""
        SELECT venue, COUNT(*) as match_count, 
               MIN(match_date) as first_match, MAX(match_date) as last_match
        FROM Matches 
        GROUP BY venue 
        ORDER BY match_count DESC
    """)
    data = cur.fetchall()
    display_data_in_viewer(data, "Matches by Venue")


# ==  Data Display ==
def display_data_in_viewer(data_list, title="Cricket Data"):
    window = Toplevel(viewer_window)
    window.geometry("1400x700")
    window.title(f" {title}")
    window.configure(bg=colors['dark_bg'])

    header = Label(window, text=title, font=("Consolas", 16, "bold"),
                   fg=colors['text_bright'], bg=colors['dark_bg'])
    header.pack(pady=10)

    control_frame = Frame(window, bg=colors['dark_bg'])
    control_frame.pack(fill=X, padx=10, pady=5)

    export_btn = create_button(control_frame, " Export Data",
                               command=lambda: export_data(data_list, title))
    export_btn.pack(side=LEFT, padx=5)

    close_btn = create_button(control_frame, " Close", command=window.destroy)
    close_btn.pack(side=RIGHT, padx=5)

    tree_frame = Frame(window, bg=colors['dark_bg'])
    tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    v_scroll = Scrollbar(tree_frame)
    v_scroll.pack(side=RIGHT, fill=Y)
    h_scroll = Scrollbar(tree_frame, orient=HORIZONTAL)
    h_scroll.pack(side=BOTTOM, fill=X)

    tree = ttk.Treeview(tree_frame, yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    tree.pack(fill=BOTH, expand=True)

    v_scroll.config(command=tree.yview)
    h_scroll.config(command=tree.xview)

    def configure_treeview_columns():
        if not data_list:
            tree['columns'] = ('No Data',)
            tree.heading('#0', text='Info')
            tree.heading('No Data', text='No data available')
            tree.insert('', 'end', text='No records found', values=('',))
            return

        if "Players" in title:
            if "All Players" in title:
                columns = ['Player ID', 'Name', 'Age', 'Nationality', 'Role', 'Team', 'Salary']
            else:
                columns = ['Player ID', 'Name', 'Age', 'Nationality', 'Team', 'Salary']
        elif "Teams" in title:
            if "All Teams" in title:
                columns = ['Team Name', 'Coach', 'Home Ground', 'Wins', 'Losses', 'Draws', 'Points']
            else:
                columns = ['Team Name', 'Wins', 'Losses', 'Draws', 'Points', 'Win %']
        elif "Matches" in title:
            if "All Matches" in title:
                columns = ['Match ID', 'Team 1', 'Team 2', 'Date', 'Venue', 'Result']
            else:
                columns = ['Venue', 'Match Count', 'First Match', 'Last Match']
        else:
            columns = [f'Column {i + 1}' for i in range(len(data_list[0]))]

        tree['columns'] = columns
        tree.heading('#0', text='Index')
        tree.column('#0', width=60, anchor='center')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')

        for i, row in enumerate(data_list):
            tree.insert('', 'end', text=str(i + 1), values=row)

    configure_treeview_columns()

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background=colors['light_bg'],
                    foreground=colors['text_light'],
                    fieldbackground=colors['light_bg'],
                    font=('Consolas', 10))
    style.configure("Treeview.Heading",
                    background=colors['secondary'],
                    foreground='black',
                    font=('Consolas', 11, 'bold'))
    style.map("Treeview",
              background=[('selected', colors['accent2'])],
              foreground=[('selected', 'black')])

    status_text = f"Displaying {len(data_list)} records" if data_list else " No records found"
    status_bar = Label(window, text=status_text, font=("Consolas", 10),
                       fg=colors['text_bright'], bg=colors['dark_bg'], anchor=W)
    status_bar.pack(fill=X, side=BOTTOM, padx=10, pady=5)

# == Main Viewer Window ==
def create_viewer():
    global viewer_window
    viewer_window = Tk()
    viewer_window.title("Cricket Database Viewer - A00316625")
    viewer_window.geometry("900x600")
    viewer_window.configure(bg=colors['dark_bg'])

    # Header
    header = Label(viewer_window, text="Cricket Database",
                   font=("Consolas", 20, "bold"), fg=colors['text_bright'], bg=colors['dark_bg'])
    header.pack(pady=20)

    # Description
    desc = Label(viewer_window, text="cricket data by choice",
                 font=("Consolas", 12), fg=colors['text_light'], bg=colors['dark_bg'])
    desc.pack(pady=5)

    # Main container
    main_frame = Frame(viewer_window, bg=colors['dark_bg'])
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Category sections
    categories = [
        ("PLAYER DATA", [
            ("View All Players", view_all_players),
            ("Players by Role", view_players_by_role),
        ]),
        ("TEAM DATA", [
            ("View All Teams", view_all_teams),
            ("Teams by Performance", view_teams_by_performance),
        ]),
        ("MATCH DATA", [
            ("View All Matches", view_all_matches),
            ("Matches by Venue", view_matches_by_venue),
        ])
    ]

    for category_title, buttons in categories:
        cat_frame = LabelFrame(main_frame, text=category_title,
                               bg=colors['light_bg'], fg=colors['text_bright'],
                               font=("Consolas", 12, "bold"), padx=10, pady=10)
        cat_frame.pack(fill=X, pady=10)
        btn_frame = Frame(cat_frame, bg=colors['light_bg'])
        btn_frame.pack(fill=X, padx=5, pady=5)

        for i, (btn_text, command) in enumerate(buttons):
            btn = create_button(btn_frame, btn_text, command, width=25)
            btn.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            btn_frame.grid_columnconfigure(i, weight=1)
    footer = Label(viewer_window, text="Database Viewer",
                   font=("Consolas", 10), fg=colors['text_light'], bg=colors['dark_bg'])
    footer.pack(side=BOTTOM, pady=10)

    viewer_window.mainloop()


# == Run  ==
if __name__ == "__main__":
    create_viewer()