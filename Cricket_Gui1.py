import sqlite3
from tkinter import *
from tkinter import ttk, messagebox, filedialog

# =========================================================
# Assignment Title : Cricket Team Management System
# Student Name     : Nagasai Chintalapati
# Student Number   : A00316625
# Course           : Software Design with Ai and Cloud Computing
# =========================================================

# == Color Scheme ==
colors = {
    'primary': '#FFFFFF',
    'secondary': '#2E8B57',
    'accent1': '#0B75A6',
    'accent2': '#FF8C00',
    'dark_bg': '#F7F9FB',
    'light_bg': '#FFFFFF',
    'text_light': '#222222',
    'muted': '#6B7280'
}

def create_button(master, text, command=None, width=10,):
    btn = Button(
        master,
        text=text,
        bg=colors['secondary'],
        fg='white',
        activebackground=colors['accent2'],
        activeforeground='white',
        relief="flat",
        command=command,
        padx=6,
        pady=4,
        width=width,
        bd=0,
        cursor="hand2",
    )

    def on_enter(e):
        btn['bg'] = colors['accent1']
    def on_leave(e):
        btn['bg'] = colors['secondary']

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# == Utility Functions ==
def safe_int(v, default=0):
    try:
        return int(v)
    except:
        try:
            return int(float(v))
        except:
            return default

def safe_float(v, default=0.0):
    try:
        return float(v)
    except:
        return default

# ==  Display Dialog (From GUI2) ==
def displayDialog(parent, data_list, title="Cricket Data"):
    window = Toplevel(parent)
    window.geometry("1400x700")
    window.title(f"{title}")
    window.configure(bg=colors['dark_bg'])

    header = Label(window, text=title, font=("Segoe UI", 16, "bold"),
                   fg=colors['secondary'], bg=colors['dark_bg'])
    header.pack(pady=10)

    control_frame = Frame(window, bg=colors['dark_bg'])
    control_frame.pack(fill=X, padx=10, pady=5)

    export_btn = create_button(control_frame, "Export Data",
                               command=lambda: export_data(window, data_list, title))
    export_btn.pack(side=LEFT, padx=5)

    close_btn = create_button(control_frame, "Close", command=window.destroy)
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
        if "Player Statistics" in title:
            columns = ['Player ID', 'Name', 'Team', 'Role', 'Total Runs', 'Total Wickets', 'Avg Strike Rate', 'Avg Economy']
        elif "Team Standings" in title:
            columns = ['Team Name', 'Wins', 'Losses', 'Draws', 'Points', 'Win %']
        elif "Top Performers" in title:
            columns = ['Player Name', 'Team', 'Total Runs', 'Total Wickets', 'Matches Played']
        elif "Match Schedule" in title:
            columns = ['Match ID', 'Team 1', 'Team 2', 'Date', 'Venue', 'Match Type', 'Result']
        elif "Financial" in title:
            columns = ['Team Name', 'Players', 'Total Salary', 'Avg Salary', 'Budget', 'Remaining']
        elif "Nationality" in title:
            columns = ['Nationality', 'Player Count', 'Avg Age', 'Avg Salary']
        elif "Player Performance" in title:
            columns = ['Player Name', 'Team', 'Total Runs', 'Total Wickets', 'Avg SR', 'Avg ER', 'Matches']
        elif "Venue" in title:
            columns = ['Venue', 'Matches', 'Avg Total Runs', 'Tournaments']
        elif "Team Squads" in title:
            columns = ['Team Name', 'Total Players', 'Batsmen', 'Bowlers', 'All-rounders', 'Wicketkeepers', 'Avg Age']
        elif "Analytics" in title or "Comparison" in title:
            if "Run Scorers" in title:
                columns = ['Player Name', 'Team', 'Total Runs', 'Matches', 'Avg Strike Rate']
            elif "Wicket Takers" in title:
                columns = ['Player Name', 'Team', 'Total Wickets', 'Avg Economy', 'Matches']
            elif "Player Comparison" in title:
                columns = ['Player Name', 'Team', 'Runs', 'Wickets', 'Strike Rate', 'Economy Rate']
            elif "Team Performance" in title:
                columns = ['Team Name', 'Total Matches', 'Wins', 'Losses', 'Draws', 'Win %']
            elif "Player Roles" in title:
                columns = ['Role', 'Player Count', 'Avg Age', 'Avg Salary', 'Max Salary']
            elif "Match Venue" in title:
                columns = ['Venue', 'Matches Played', 'Avg Runs', 'Avg Wickets', 'Tournaments']
            else:
                columns = [f'Column {i+1}' for i in range(len(data_list[0]))]
        else:
            columns = [f'Column {i+1}' for i in range(len(data_list[0]))]

        tree['columns'] = columns
        tree.heading('#0', text='Index')
        tree.column('#0', width=60, anchor='center')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor='center')

        for i, row in enumerate(data_list):
            tree.insert('', 'end', text=str(i + 1), values=row)

    configure_treeview_columns()

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background=colors['light_bg'],
                    foreground=colors['text_light'],
                    fieldbackground=colors['light_bg'],
                    font=('Segoe UI', 9))
    style.configure("Treeview.Heading",
                    background=colors['secondary'],
                    foreground='white',
                    font=('Segoe UI', 10, 'bold'))
    style.map("Treeview",
              background=[('selected', colors['accent1'])],
              foreground=[('selected', 'white')])

    status_text = f"Displaying {len(data_list)} records" if data_list else " No records found"
    status_bar = Label(window, text=status_text, font=("Segoe UI", 10),
                       fg=colors['secondary'], bg=colors['dark_bg'], anchor=W)
    status_bar.pack(fill=X, side=BOTTOM, padx=10, pady=5)

def export_data(parent, data_list, title):
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if filename:
        with open(filename, 'w') as f:
            if "Player" in title:
                f.write("Player ID,Name,Team,Role,Total Runs,Total Wickets,Avg Strike Rate,Avg Economy\n")
            elif "Team" in title:
                f.write("Team Name,Wins,Losses,Draws,Points,Win Percentage\n")
            elif "Match" in title:
                f.write("Match ID,Team 1,Team 2,Date,Venue,Result\n")
            else:
                f.write("Data Export\n")
            for row in data_list:
                f.write(','.join(map(str, row)) + '\n')
        messagebox.showinfo("Success", f"Data exported to {filename}")

# == Database Start ==
con = sqlite3.connect(":memory:", check_same_thread=False)
cur = con.cursor()

def init_db():
    try:
        cur.execute("DROP TABLE IF EXISTS Teams")
        cur.execute("DROP TABLE IF EXISTS Players")
        cur.execute("DROP TABLE IF EXISTS Matches")
        cur.execute("DROP TABLE IF EXISTS Performances")

        cur.execute("""
            CREATE TABLE Teams(
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT UNIQUE NOT NULL,
                coach_name TEXT, assistant_coach TEXT, home_ground TEXT,
                founded_year INTEGER, team_budget REAL, contact_email TEXT,
                wins INTEGER DEFAULT 0, losses INTEGER DEFAULT 0, draws INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE Players(
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, age INTEGER, nationality TEXT, role TEXT,
                team_id INTEGER, batting_style TEXT, bowling_style TEXT,
                debut_date TEXT, salary REAL, contact TEXT, email TEXT,
                FOREIGN KEY(team_id) REFERENCES Teams(team_id)
            )
        """)
        cur.execute("""
            CREATE TABLE Matches(
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team1_id INTEGER, team2_id INTEGER, match_date TEXT, venue TEXT,
                match_type TEXT, tournament_name TEXT, umpires TEXT, man_of_match INTEGER,
                team1_score INTEGER, team2_score INTEGER, team1_wickets INTEGER, team2_wickets INTEGER,
                result TEXT,
                FOREIGN KEY(team1_id) REFERENCES Teams(team_id),
                FOREIGN KEY(team2_id) REFERENCES Teams(team_id),
                FOREIGN KEY(man_of_match) REFERENCES Players(player_id)
            )
        """)
        cur.execute("""
            CREATE TABLE Performances(
                performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER, match_id INTEGER, runs_scored INTEGER DEFAULT 0,
                balls_faced INTEGER DEFAULT 0, fours INTEGER DEFAULT 0, sixes INTEGER DEFAULT 0,
                wickets_taken INTEGER DEFAULT 0, overs_bowled REAL DEFAULT 0, runs_conceded INTEGER DEFAULT 0,
                maidens INTEGER DEFAULT 0, catches INTEGER DEFAULT 0, stumpings INTEGER DEFAULT 0,
                strike_rate REAL DEFAULT 0, economy_rate REAL DEFAULT 0,
                FOREIGN KEY(player_id) REFERENCES Players(player_id),
                FOREIGN KEY(match_id) REFERENCES Matches(match_id)
            )
        """)
        teams = [
            ("Mumbai Indians", "Mahela Jayawardene", "Shane Bond", "Wankhede Stadium", 2008, 5000000, "admin@mumbaiindians.com", 5, 2, 1),
            ("Chennai Super Kings", "Stephen Fleming", "Lakshmipathy Balaji", "M. A. Chidambaram Stadium", 2008, 4800000, "info@chennaisuperkings.com", 4, 3, 1),
            ("Royal Challengers Bangalore", "Sanjay Bangar", "Adam Griffith", "M. Chinnaswamy Stadium", 2008, 5200000, "contact@rcb.com", 3, 4, 1),
            ("Kolkata Knight Riders", "Chandrakant Pandit", "Bharat Arun", "Eden Gardens", 2008, 4700000, "support@kkr.in", 6, 1, 1),
            ("Delhi Capitals", "Ricky Ponting", "Pravin Amre", "Arun Jaitley Stadium", 2008, 4500000, "info@delhicapitals.com", 2, 5, 1),
            ("Punjab Kings", "Anil Kumble", "Jonty Rhodes", "PCA Stadium", 2008, 4300000, "contact@punjabkings.com", 1, 6, 1)
        ]
        cur.executemany("INSERT INTO Teams(team_name, coach_name, assistant_coach, home_ground, founded_year, team_budget, contact_email, wins, losses, draws) VALUES (?,?,?,?,?,?,?,?,?,?)", teams)

        players = [
            ("Rohit Sharma", 36, "Indian", "Batsman", 1, "Right-handed", "Right-arm offbreak", "2007-06-23", 1500000, "+91-9876543210", "rohit@mi.com"),
            ("Jasprit Bumrah", 30, "Indian", "Bowler", 1, "Right-handed", "Right-arm fast", "2016-01-23", 1100000, "+91-9876543214", "bumrah@mi.com"),
            ("Suryakumar Yadav", 33, "Indian", "Batsman", 1, "Right-handed", "Right-arm offbreak", "2010-03-14", 900000, "+91-9876543220", "surya@mi.com"),
            ("Ishan Kishan", 25, "Indian", "Wicketkeeper", 1, "Left-handed", "N/A", "2016-01-23", 800000, "+91-9876543221", "ishan@mi.com"),
            ("MS Dhoni", 42, "Indian", "Wicketkeeper", 2, "Right-handed", "Right-arm medium", "2004-12-23", 1200000, "+91-9876543211", "dhoni@csk.com"),
            ("Ravindra Jadeja", 35, "Indian", "All-rounder", 2, "Left-handed", "Left-arm orthodox", "2009-02-08", 1000000, "+91-9876543215", "jadeja@csk.com"),
            ("Virat Kohli", 35, "Indian", "Batsman", 3, "Right-handed", "Right-arm medium", "2008-08-18", 1700000, "+91-9876543212", "kohli@rcb.com"),
            ("Glenn Maxwell", 35, "Australian", "All-rounder", 3, "Right-handed", "Right-arm offbreak", "2012-02-05", 1200000, "+91-9876543223", "maxwell@rcb.com"),
            ("Shreyas Iyer", 29, "Indian", "Batsman", 4, "Right-handed", "Right-arm offbreak", "2014-11-14", 900000, "+91-9876543213", "iyer@kkr.com"),
            ("Andre Russell", 35, "West Indian", "All-rounder", 4, "Right-handed", "Right-arm fast", "2010-05-22", 1100000, "+91-9876543225", "russell@kkr.com"),
        ]
        cur.executemany("INSERT INTO Players(name, age, nationality, role, team_id, batting_style, bowling_style, debut_date, salary, contact, email) VALUES (?,?,?,?,?,?,?,?,?,?,?)", players)

        matches = [
            (1, 2, "2024-03-26", "Wankhede Stadium", "T20", "IPL 2024", "Kumar Dharmasena, Nitin Menon", 1, 185, 178, 6, 9, "Mumbai Indians won by 7 runs"),
            (3, 4, "2024-03-27", "M. Chinnaswamy Stadium", "T20", "IPL 2024", "Chris Gaffaney, Virender Sharma", 3, 192, 188, 4, 8, "Royal Challengers won by 4 runs"),
            (1, 3, "2024-03-28", "Eden Gardens", "T20", "IPL 2024", "Anil Chaudhary, Paul Reiffel", 5, 175, 172, 5, 10, "Kolkata Knight Riders won by 3 wickets"),
        ]
        cur.executemany("INSERT INTO Matches(team1_id, team2_id, match_date, venue, match_type, tournament_name, umpires, man_of_match, team1_score, team2_score, team1_wickets, team2_wickets, result) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", matches)

        performances = [
            (1, 1, 85, 54, 8, 3, 0, 0, 0, 0, 1, 0, 157.4, 0),
            (2, 1, 12, 18, 1, 0, 3, 4.0, 28, 1, 0, 0, 66.7, 7.0),
            (5, 1, 15, 12, 1, 1, 1, 3.2, 25, 0, 2, 0, 125.0, 7.8),
            (8, 2, 78, 42, 6, 4, 0, 0, 0, 0, 0, 0, 185.7, 0),
            (11, 2, 45, 32, 4, 2, 2, 4.0, 30, 1, 1, 0, 140.6, 7.5),
        ]
        cur.executemany("INSERT INTO Performances(player_id, match_id, runs_scored, balls_faced, fours, sixes, wickets_taken, overs_bowled, runs_conceded, maidens, catches, stumpings, strike_rate, economy_rate) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", performances)
        con.commit()
    except Exception as e:
        print("DB init error:", e)

init_db()

# == Global Variables ==
current_player = 0
current_team = 0
current_match = 0
current_performance = 0

# == Display Functions ==
def displayPlayer(index):
    global current_player
    cur.execute("SELECT * FROM Players")
    allPlayers = cur.fetchall()
    if not allPlayers:
        return
    index = max(0, min(index, len(allPlayers)-1))
    player = allPlayers[index]
    current_player = index
    entry_player_id.delete(0, END); entry_player_id.insert(END, player[0])
    entry_player_name.delete(0, END); entry_player_name.insert(END, player[1])
    entry_player_age.delete(0, END); entry_player_age.insert(END, player[2] or "")
    entry_player_role.delete(0, END); entry_player_role.insert(END, player[4] or "")
    entry_player_team.delete(0, END); entry_player_team.insert(END, player[5] or "")
    entry_player_salary.delete(0, END); entry_player_salary.insert(END, player[9] or "")

def displayTeam(index):
    global current_team
    cur.execute("SELECT * FROM Teams")
    allTeams = cur.fetchall()
    if not allTeams:
        return
    index = max(0, min(index, len(allTeams)-1))
    team = allTeams[index]
    current_team = index
    entry_team_id.delete(0, END); entry_team_id.insert(END, team[0])
    entry_team_name.delete(0, END); entry_team_name.insert(END, team[1])
    entry_team_coach.delete(0, END); entry_team_coach.insert(END, team[2] or "")
    entry_team_budget.delete(0, END); entry_team_budget.insert(END, team[6] or "")
    entry_team_wins.delete(0, END); entry_team_wins.insert(END, team[8] or "")
    entry_team_losses.delete(0, END); entry_team_losses.insert(END, team[9] or "")

def displayMatch(index):
    global current_match
    cur.execute("SELECT * FROM Matches")
    allMatches = cur.fetchall()
    if not allMatches:
        return
    index = max(0, min(index, len(allMatches)-1))
    match = allMatches[index]
    current_match = index
    entry_match_id.delete(0, END); entry_match_id.insert(END, match[0])
    entry_match_team1.delete(0, END); entry_match_team1.insert(END, match[1])
    entry_match_team2.delete(0, END); entry_match_team2.insert(END, match[2])
    entry_match_date.delete(0, END); entry_match_date.insert(END, match[3] or "")
    entry_match_venue.delete(0, END); entry_match_venue.insert(END, match[4] or "")
    entry_match_result.delete(0, END); entry_match_result.insert(END, match[12] or "")

def displayPerformance(index):
    global current_performance
    cur.execute("SELECT * FROM Performances")
    allPerformances = cur.fetchall()
    if not allPerformances:
        return
    index = max(0, min(index, len(allPerformances)-1))
    performance = allPerformances[index]
    current_performance = index
    entry_perf_id.delete(0, END); entry_perf_id.insert(END, performance[0])
    entry_perf_player.delete(0, END); entry_perf_player.insert(END, performance[1])
    entry_perf_match.delete(0, END); entry_perf_match.insert(END, performance[2])
    entry_perf_runs.delete(0, END); entry_perf_runs.insert(END, performance[3])
    entry_perf_wickets.delete(0, END); entry_perf_wickets.insert(END, performance[7])
    entry_perf_catches.delete(0, END); entry_perf_catches.insert(END, performance[10])

# == Player Functions ==
def nextPlayerCmd():
    global current_player
    cur.execute("SELECT * FROM Players")
    allPlayers = cur.fetchall()
    if current_player < len(allPlayers) - 1:
        current_player += 1
        displayPlayer(current_player)

def prevPlayerCmd():
    global current_player
    if current_player > 0:
        current_player -= 1
        displayPlayer(current_player)

def clearPlayerCmd():
    entry_player_id.delete(0, END)
    entry_player_name.delete(0, END)
    entry_player_age.delete(0, END)
    entry_player_role.delete(0, END)
    entry_player_team.delete(0, END)
    entry_player_salary.delete(0, END)

def insertPlayerCmd():
    name = entry_player_name.get(); age = entry_player_age.get()
    role = entry_player_role.get(); team_id = entry_player_team.get()
    salary = entry_player_salary.get()
    if not name or not team_id:
        messagebox.showwarning("Warning", "Name and Team ID are required!")
        return
    try:
        cur.execute("INSERT INTO Players(name, age, nationality, role, team_id, batting_style, bowling_style, debut_date, salary, contact, email) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (name, safe_int(age), None, role, safe_int(team_id), None, None, None, safe_float(salary), None, None))
        con.commit()
        cur.execute("SELECT * FROM Players")
        allPlayers = cur.fetchall()
        displayPlayer(len(allPlayers) - 1)
        messagebox.showinfo("Success", "Player added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding player: {e}")

def updatePlayerCmd():
    player_id = entry_player_id.get()
    name = entry_player_name.get(); age = entry_player_age.get()
    role = entry_player_role.get(); team_id = entry_player_team.get()
    salary = entry_player_salary.get()
    if not player_id:
        messagebox.showwarning("Warning", "Please select a player to update")
        return
    try:
        cur.execute("UPDATE Players SET name=?, age=?, role=?, team_id=?, salary=? WHERE player_id=?",
                    (name, safe_int(age), role, safe_int(team_id), safe_float(salary), safe_int(player_id)))
        con.commit()
        messagebox.showinfo("Success", "Player updated successfully!")
        displayPlayer(current_player)
    except Exception as e:
        messagebox.showerror("Error", f"Error updating player: {e}")

def deletePlayerCmd():
    player_id = entry_player_id.get()
    if not player_id:
        messagebox.showwarning("Warning", "Please select a player to delete")
        return
    if messagebox.askyesno("Confirm", "Delete this player?"):
        try:
            cur.execute("DELETE FROM Players WHERE player_id=?", (safe_int(player_id),))
            con.commit()
            messagebox.showinfo("Success", "Player deleted")
            clearPlayerCmd()
            displayPlayer(0)
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting player: {e}")

# == Team Functions ==
def nextTeamCmd():
    global current_team
    cur.execute("SELECT * FROM Teams")
    allTeams = cur.fetchall()
    if current_team < len(allTeams) - 1:
        current_team += 1
        displayTeam(current_team)

def prevTeamCmd():
    global current_team
    if current_team > 0:
        current_team -= 1
        displayTeam(current_team)

def clearTeamCmd():
    entry_team_id.delete(0, END)
    entry_team_name.delete(0, END)
    entry_team_coach.delete(0, END)
    entry_team_budget.delete(0, END)
    entry_team_wins.delete(0, END)
    entry_team_losses.delete(0, END)

def insertTeamCmd():
    name = entry_team_name.get(); coach = entry_team_coach.get()
    budget = entry_team_budget.get(); wins = entry_team_wins.get(); losses = entry_team_losses.get()
    if not name:
        messagebox.showwarning("Warning", "Team Name is required!")
        return
    try:
        cur.execute("INSERT INTO Teams(team_name, coach_name, team_budget, wins, losses) VALUES (?,?,?,?,?)",
                    (name, coach, safe_float(budget), safe_int(wins), safe_int(losses)))
        con.commit()
        cur.execute("SELECT * FROM Teams")
        allTeams = cur.fetchall()
        displayTeam(len(allTeams) - 1)
        messagebox.showinfo("Success", "Team added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding team: {e}")

def updateTeamCmd():
    team_id = entry_team_id.get(); name = entry_team_name.get(); coach = entry_team_coach.get()
    budget = entry_team_budget.get(); wins = entry_team_wins.get(); losses = entry_team_losses.get()
    if not team_id:
        messagebox.showwarning("Warning", "Please select a team to update")
        return
    try:
        cur.execute("UPDATE Teams SET team_name=?, coach_name=?, team_budget=?, wins=?, losses=? WHERE team_id=?",
                    (name, coach, safe_float(budget), safe_int(wins), safe_int(losses), safe_int(team_id)))
        con.commit()
        messagebox.showinfo("Success", "Team updated successfully!")
        displayTeam(current_team)
    except Exception as e:
        messagebox.showerror("Error", f"Error updating team: {e}")

def deleteTeamCmd():
    team_id = entry_team_id.get()
    if not team_id:
        messagebox.showwarning("Warning", "Please select a team to delete")
        return
    if messagebox.askyesno("Confirm", "Delete team and all associated players & matches?"):
        try:
            cur.execute("DELETE FROM Players WHERE team_id=?", (safe_int(team_id),))
            cur.execute("DELETE FROM Matches WHERE team1_id=? OR team2_id=?", (safe_int(team_id), safe_int(team_id)))
            cur.execute("DELETE FROM Teams WHERE team_id=?", (safe_int(team_id),))
            con.commit()
            messagebox.showinfo("Success", "Team deleted")
            clearTeamCmd()
            displayTeam(0)
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting team: {e}")

# == Match Functions ==
def nextMatchCmd():
    global current_match
    cur.execute("SELECT * FROM Matches")
    allMatches = cur.fetchall()
    if current_match < len(allMatches) - 1:
        current_match += 1
        displayMatch(current_match)

def prevMatchCmd():
    global current_match
    if current_match > 0:
        current_match -= 1
        displayMatch(current_match)

def clearMatchCmd():
    entry_match_id.delete(0, END)
    entry_match_team1.delete(0, END)
    entry_match_team2.delete(0, END)
    entry_match_date.delete(0, END)
    entry_match_venue.delete(0, END)
    entry_match_result.delete(0, END)

def insertMatchCmd():
    team1 = entry_match_team1.get(); team2 = entry_match_team2.get()
    date = entry_match_date.get(); venue = entry_match_venue.get(); result = entry_match_result.get()
    if not team1 or not team2:
        messagebox.showwarning("Warning", "Team IDs are required!")
        return
    try:
        cur.execute("INSERT INTO Matches(team1_id, team2_id, match_date, venue, result) VALUES (?,?,?,?,?)",
                    (safe_int(team1), safe_int(team2), date, venue, result))
        con.commit()
        cur.execute("SELECT * FROM Matches")
        allMatches = cur.fetchall()
        displayMatch(len(allMatches) - 1)
        messagebox.showinfo("Success", "Match added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding match: {e}")

def updateMatchCmd():
    match_id = entry_match_id.get()
    team1 = entry_match_team1.get(); team2 = entry_match_team2.get()
    date = entry_match_date.get(); venue = entry_match_venue.get(); result = entry_match_result.get()
    if not match_id:
        messagebox.showwarning("Warning", "Please select a match to update")
        return
    try:
        cur.execute("UPDATE Matches SET team1_id=?, team2_id=?, match_date=?, venue=?, result=? WHERE match_id=?",
                    (safe_int(team1), safe_int(team2), date, venue, result, safe_int(match_id)))
        con.commit()
        messagebox.showinfo("Success", "Match updated successfully!")
        displayMatch(current_match)
    except Exception as e:
        messagebox.showerror("Error", f"Error updating match: {e}")

def deleteMatchCmd():
    match_id = entry_match_id.get()
    if not match_id:
        messagebox.showwarning("Warning", "Please select a match to delete")
        return
    if messagebox.askyesno("Confirm", "Delete match and associated performances?"):
        try:
            cur.execute("DELETE FROM Performances WHERE match_id=?", (safe_int(match_id),))
            cur.execute("DELETE FROM Matches WHERE match_id=?", (safe_int(match_id),))
            con.commit()
            messagebox.showinfo("Success", "Match deleted")
            clearMatchCmd()
            displayMatch(0)
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting match: {e}")

# == Performance Functions ==
def nextPerformanceCmd():
    global current_performance
    cur.execute("SELECT * FROM Performances")
    allPerformances = cur.fetchall()
    if current_performance < len(allPerformances) - 1:
        current_performance += 1
        displayPerformance(current_performance)

def prevPerformanceCmd():
    global current_performance
    if current_performance > 0:
        current_performance -= 1
        displayPerformance(current_performance)

def clearPerformanceCmd():
    entry_perf_id.delete(0, END)
    entry_perf_player.delete(0, END)
    entry_perf_match.delete(0, END)
    entry_perf_runs.delete(0, END)
    entry_perf_wickets.delete(0, END)
    entry_perf_catches.delete(0, END)

def insertPerformanceCmd():
    player_id = entry_perf_player.get(); match_id = entry_perf_match.get()
    runs = entry_perf_runs.get(); wickets = entry_perf_wickets.get(); catches = entry_perf_catches.get()
    if not player_id or not match_id:
        messagebox.showwarning("Warning", "Player ID and Match ID are required!")
        return
    try:
        cur.execute("INSERT INTO Performances(player_id, match_id, runs_scored, wickets_taken, catches) VALUES (?,?,?,?,?)",
                    (safe_int(player_id), safe_int(match_id), safe_int(runs), safe_int(wickets), safe_int(catches)))
        con.commit()
        cur.execute("SELECT * FROM Performances")
        allPerformances = cur.fetchall()
        displayPerformance(len(allPerformances) - 1)
        messagebox.showinfo("Success", "Performance added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding performance: {e}")

def updatePerformanceCmd():
    perf_id = entry_perf_id.get(); player_id = entry_perf_player.get(); match_id = entry_perf_match.get()
    runs = entry_perf_runs.get(); wickets = entry_perf_wickets.get(); catches = entry_perf_catches.get()
    if not perf_id:
        messagebox.showwarning("Warning", "Please select a performance to update")
        return
    try:
        cur.execute("UPDATE Performances SET player_id=?, match_id=?, runs_scored=?, wickets_taken=?, catches=? WHERE performance_id=?",
                    (safe_int(player_id), safe_int(match_id), safe_int(runs), safe_int(wickets), safe_int(catches), safe_int(perf_id)))
        con.commit()
        messagebox.showinfo("Success", "Performance updated successfully!")
        displayPerformance(current_performance)
    except Exception as e:
        messagebox.showerror("Error", f"Error updating performance: {e}")

def deletePerformanceCmd():
    perf_id = entry_perf_id.get()
    if not perf_id:
        messagebox.showwarning("Warning", "Please select a performance to delete")
        return
    if messagebox.askyesno("Confirm", "Delete this performance?"):
        try:
            cur.execute("DELETE FROM Performances WHERE performance_id=?", (safe_int(perf_id),))
            con.commit()
            messagebox.showinfo("Success", "Performance deleted")
            clearPerformanceCmd()
            displayPerformance(0)
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting performance: {e}")

# == Report Functions ==
def reportPlayerStatsCmd():
    cur.execute("""
        SELECT p.player_id, p.name, t.team_name, p.role,
               COALESCE(SUM(pr.runs_scored),0) total_runs,
               COALESCE(SUM(pr.wickets_taken),0) total_wickets,
               COALESCE(ROUND(AVG(pr.strike_rate),2),0) avg_sr,
               COALESCE(ROUND(AVG(pr.economy_rate),2),0) avg_er
        FROM Players p
        LEFT JOIN Teams t ON p.team_id=t.team_id
        LEFT JOIN Performances pr ON p.player_id=pr.player_id
        GROUP BY p.player_id
        ORDER BY total_runs DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Player Statistics Report")

def reportTeamStandingsCmd():
    cur.execute("""
        SELECT team_name, wins, losses, draws, (wins*2 + draws) as points,
               ROUND((wins * 100.0 / (wins + losses + draws)), 2) as win_percentage
        FROM Teams
        ORDER BY points DESC, wins DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Team Standings Report")

def reportTopPerformersCmd():
    cur.execute("""
        SELECT p.name, t.team_name, COALESCE(SUM(pr.runs_scored),0) total_runs,
               COALESCE(SUM(pr.wickets_taken),0) total_wickets, COUNT(pr.match_id) matches_played
        FROM Players p
        LEFT JOIN Performances pr ON p.player_id = pr.player_id
        LEFT JOIN Teams t ON p.team_id = t.team_id
        GROUP BY p.player_id
        ORDER BY total_runs DESC, total_wickets DESC
        LIMIT 15
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Top Performers Report")

def reportMatchScheduleCmd():
    cur.execute("""
        SELECT m.match_id, t1.team_name, t2.team_name, m.match_date, m.venue, m.match_type, m.result
        FROM Matches m
        LEFT JOIN Teams t1 ON m.team1_id=t1.team_id
        LEFT JOIN Teams t2 ON m.team2_id=t2.team_id
        ORDER BY m.match_date DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Match Schedule Report")

def reportFinancialCmd():
    cur.execute("""
        SELECT t.team_name, COUNT(p.player_id) player_count,
               COALESCE(SUM(p.salary),0) total_salary, COALESCE(ROUND(AVG(p.salary),2),0) avg_salary,
               t.team_budget, COALESCE(t.team_budget - SUM(p.salary), t.team_budget) budget_remaining
        FROM Teams t
        LEFT JOIN Players p ON t.team_id=p.team_id
        GROUP BY t.team_id
        ORDER BY total_salary DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Financial Report")

def reportNationalityCmd():
    cur.execute("""
        SELECT nationality, COUNT(*) player_count, ROUND(AVG(age),2) avg_age, ROUND(AVG(salary),2) avg_salary
        FROM Players
        GROUP BY nationality
        ORDER BY player_count DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Nationality Report")

def reportPlayerPerformanceCmd():
    cur.execute("""
        SELECT p.name, t.team_name,
               COALESCE(SUM(pr.runs_scored),0) total_runs,
               COALESCE(SUM(pr.wickets_taken),0) total_wickets,
               COALESCE(ROUND(AVG(pr.strike_rate),2),0) avg_sr,
               COALESCE(ROUND(AVG(pr.economy_rate),2),0) avg_er,
               COUNT(pr.match_id) matches_played
        FROM Players p
        LEFT JOIN Teams t ON p.team_id=t.team_id
        LEFT JOIN Performances pr ON p.player_id=pr.player_id
        GROUP BY p.player_id
        ORDER BY total_runs DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Player Performance Report")

def reportVenueCmd():
    cur.execute("""
        SELECT venue, COUNT(*) matches_played,
               ROUND(AVG(COALESCE(team1_score,0) + COALESCE(team2_score,0)),2) avg_total_runs,
               COUNT(DISTINCT tournament_name) tournaments_hosted
        FROM Matches
        GROUP BY venue
        ORDER BY matches_played DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Venue Report")

def reportTeamSquadsCmd():
    cur.execute("""
        SELECT t.team_name,
               COUNT(p.player_id) total_players,
               SUM(CASE WHEN p.role='Batsman' THEN 1 ELSE 0 END) batsmen,
               SUM(CASE WHEN p.role='Bowler' THEN 1 ELSE 0 END) bowlers,
               SUM(CASE WHEN p.role='All-rounder' THEN 1 ELSE 0 END) all_rounders,
               SUM(CASE WHEN p.role='Wicketkeeper' THEN 1 ELSE 0 END) wicketkeepers,
               ROUND(AVG(p.age),2) avg_age
        FROM Teams t
        LEFT JOIN Players p ON t.team_id=p.team_id
        GROUP BY t.team_id
        ORDER BY total_players DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Team Squads Report")

# == Analytics Functions ==
def analyticsTopRunScorers():
    cur.execute("""
        SELECT p.name, t.team_name, SUM(pr.runs_scored) as total_runs, 
               COUNT(pr.match_id) as matches, ROUND(AVG(pr.strike_rate), 2) as avg_strike_rate
        FROM Players p
        JOIN Performances pr ON p.player_id = pr.player_id
        JOIN Teams t ON p.team_id = t.team_id
        GROUP BY p.player_id
        ORDER BY total_runs DESC
        LIMIT 15
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Top Run Scorers Analytics")

def analyticsTopWicketTakers():
    cur.execute("""
        SELECT p.name, t.team_name, SUM(pr.wickets_taken) as total_wickets,
               ROUND(AVG(pr.economy_rate), 2) as avg_economy, COUNT(pr.match_id) as matches
        FROM Players p
        JOIN Performances pr ON p.player_id = pr.player_id
        JOIN Teams t ON p.team_id = t.team_id
        GROUP BY p.player_id
        ORDER BY total_wickets DESC
        LIMIT 15
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Top Wicket Takers Analytics")

def analyticsPlayerComparison():
    cur.execute("""
        SELECT p.name, t.team_name,
               SUM(pr.runs_scored) as runs,
               SUM(pr.wickets_taken) as wickets,
               ROUND(AVG(pr.strike_rate), 2) as strike_rate,
               ROUND(AVG(pr.economy_rate), 2) as economy_rate
        FROM Players p
        JOIN Performances pr ON p.player_id = pr.player_id
        JOIN Teams t ON p.team_id = t.team_id
        GROUP BY p.player_id
        ORDER BY runs + (wickets * 25) DESC
        LIMIT 20
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Player Performance Comparison Analytics")

def analyticsTeamPerformance():
    cur.execute("""
        SELECT t.team_name,
               COUNT(m.match_id) as total_matches,
               SUM(CASE WHEN m.result LIKE t.team_name || '%' THEN 1 ELSE 0 END) as wins,
               SUM(CASE WHEN m.result NOT LIKE t.team_name || '%' AND m.result NOT LIKE 'Draw%' THEN 1 ELSE 0 END) as losses,
               SUM(CASE WHEN m.result LIKE 'Draw%' THEN 1 ELSE 0 END) as draws,
               ROUND((SUM(CASE WHEN m.result LIKE t.team_name || '%' THEN 1 ELSE 0 END) * 100.0 / COUNT(m.match_id)), 2) as win_percentage
        FROM Teams t
        LEFT JOIN Matches m ON t.team_id = m.team1_id OR t.team_id = m.team2_id
        GROUP BY t.team_id
        ORDER BY wins DESC, win_percentage DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Team Performance Analytics")

def analyticsPlayerRoles():
    cur.execute("""
        SELECT role, 
               COUNT(*) as player_count,
               ROUND(AVG(age), 2) as avg_age,
               ROUND(AVG(salary), 2) as avg_salary,
               MAX(salary) as max_salary
        FROM Players
        GROUP BY role
        ORDER BY player_count DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Player Roles Analytics")

def analyticsMatchVenue():
    cur.execute("""
        SELECT venue,
               COUNT(*) as matches_played,
               ROUND(AVG(team1_score + team2_score), 2) as avg_runs_per_match,
               ROUND(AVG(team1_wickets + team2_wickets), 2) as avg_wickets_per_match,
               COUNT(DISTINCT tournament_name) as tournaments_hosted
        FROM Matches
        GROUP BY venue
        ORDER BY matches_played DESC
    """)
    rows = cur.fetchall()
    displayDialog(window, rows, "Match Venue Analytics")

# == Main Window ==
window = Tk()
window.title("Cricket Management - A00316625")
window.geometry("980x660")
window.configure(bg=colors['dark_bg'])

# == Notebook ==
notebook = ttk.Notebook(window)
notebook.pack(fill=BOTH, expand=True, padx=8, pady=8)

style = ttk.Style()
style.theme_use('default')
style.configure("TNotebook", background=colors['dark_bg'])
style.configure("TNotebook.Tab", background=colors['secondary'], foreground='white', padding=[10,6], font=('Segoe UI',9,'bold'))
style.map("TNotebook.Tab", background=[("selected", colors['accent1'])], foreground=[("selected", 'white')])

# == Dashboard Tab ==
tab_dashboard = Frame(notebook, bg=colors['dark_bg'])
notebook.add(tab_dashboard, text="📊 Dashboard")

Label(tab_dashboard, text="🏏 Cricket Management System", font=("Segoe UI",14,"bold"), fg=colors['secondary'], bg=colors['dark_bg']).pack(pady=8)
stats_frame = Frame(tab_dashboard, bg=colors['light_bg'], bd=1, relief="solid")
stats_frame.pack(fill=X, padx=12, pady=6)
stats_text = Text(stats_frame, height=6, bg=colors['light_bg'], fg=colors['text_light'], font=("Segoe UI",9), wrap=WORD, padx=8, pady=8)
stats_text.pack(fill=X, padx=6, pady=6)

def refresh_stats():
    total_players = cur.execute("SELECT COUNT(*) FROM Players").fetchone()[0]
    total_teams = cur.execute("SELECT COUNT(*) FROM Teams").fetchone()[0]
    total_matches = cur.execute("SELECT COUNT(*) FROM Matches").fetchone()[0]
    total_runs = cur.execute("SELECT SUM(runs_scored) FROM Performances").fetchone()[0] or 0
    total_wickets = cur.execute("SELECT SUM(wickets_taken) FROM Performances").fetchone()[0] or 0
    highest_paid = cur.execute("SELECT name FROM Players ORDER BY salary DESC LIMIT 1").fetchone()
    highest_paid = highest_paid[0] if highest_paid else "N/A"
    best_batsman = cur.execute("SELECT p.name FROM Players p JOIN Performances pr ON p.player_id=pr.player_id GROUP BY p.player_id ORDER BY SUM(pr.runs_scored) DESC LIMIT 1").fetchone()
    best_batsman = best_batsman[0] if best_batsman else "N/A"
    best_bowler = cur.execute("SELECT p.name FROM Players p JOIN Performances pr ON p.player_id=pr.player_id GROUP BY p.player_id ORDER BY SUM(pr.wickets_taken) DESC LIMIT 1").fetchone()
    best_bowler = best_bowler[0] if best_bowler else "N/A"
    out = f"""SYSTEM OVERVIEW

 Total Players: {total_players}
 Total Teams: {total_teams}
 Total Matches: {total_matches}
 Total Runs: {total_runs}
 Total Wickets: {total_wickets}
 Highest Paid: {highest_paid}
 Top Batsman: {best_batsman}
 Top Bowler: {best_bowler}

Use tabs to manage data and view analytics."""
    stats_text.configure(state=NORMAL)
    stats_text.delete("1.0", END)
    stats_text.insert(END, out)
    stats_text.configure(state=DISABLED)

refresh_stats()
db_btns = Frame(tab_dashboard, bg=colors['dark_bg'])
db_btns.pack(pady=6)
create_button(db_btns, "Refresh Stats", refresh_stats, width=14).pack(side=LEFT, padx=6)
create_button(db_btns, "View Analytics", lambda: notebook.select(6), width=14).pack(side=LEFT, padx=6)

# == Players Tab ==
tab_players = Frame(notebook, bg=colors['dark_bg'])
notebook.add(tab_players, text="👥 Players")
frame_players = Frame(tab_players, bg=colors['dark_bg'])
frame_players.pack(fill=BOTH, expand=True, padx=10, pady=10)
Label(frame_players, text="Player Management", fg=colors['secondary'], bg=colors['dark_bg'], font=("Segoe UI",12,"bold")).pack(pady=4)

player_frame = LabelFrame(frame_players, text="Player Details", bg=colors['light_bg'], fg=colors['text_light'], padx=6, pady=6)
player_frame.pack(fill=X, padx=6, pady=6)
labels = ["Player ID", "Name", "Age", "Role", "Team ID", "Salary"]
entries = []
for i, text in enumerate(labels):
    lbl = Label(player_frame, text=text, bg=colors['light_bg'], fg=colors['text_light'], font=("Segoe UI",9))
    lbl.grid(row=i//2, column=(i%2)*2, sticky=W, padx=6, pady=2)
    ent = Entry(player_frame, width=20, font=("Segoe UI",9))
    ent.grid(row=i//2, column=(i%2)*2+1, padx=6, pady=2)
    entries.append(ent)
entry_player_id, entry_player_name, entry_player_age, entry_player_role, entry_player_team, entry_player_salary = entries

button_frame = Frame(player_frame, bg=colors['light_bg'])
button_frame.grid(row=99, column=0, columnspan=6, pady=6)
btns = [
    ("First", lambda: displayPlayer(0)),
    ("Prev", prevPlayerCmd),
    ("Next", nextPlayerCmd),
    ("Last", lambda: displayPlayer(len(cur.execute("SELECT * FROM Players").fetchall()) - 1)),
    ("Save", updatePlayerCmd),
    ("Add", insertPlayerCmd),
    ("Delete", deletePlayerCmd),
    ("Clear", clearPlayerCmd)
]
for i, (txt, cmd) in enumerate(btns):
    b = create_button(button_frame, txt, cmd, width=9)
    b.grid(row=0, column=i, padx=3)

# == Teams Tab ==
tab_teams = Frame(notebook, bg=colors['dark_bg'])
notebook.add(tab_teams, text="🏏 Teams")
frame_teams = Frame(tab_teams, bg=colors['dark_bg'])
frame_teams.pack(fill=BOTH, expand=True, padx=10, pady=10)
Label(frame_teams, text="Team Management", fg=colors['secondary'], bg=colors['dark_bg'], font=("Segoe UI",12,"bold")).pack(pady=4)

team_frame = LabelFrame(frame_teams, text="Team Details", bg=colors['light_bg'], fg=colors['text_light'], padx=6, pady=6)
team_frame.pack(fill=X, padx=6, pady=6)
labels_team = ["Team ID", "Team Name", "Coach", "Budget", "Wins", "Losses"]
entries_team = []
for i, text in enumerate(labels_team):
    lbl = Label(team_frame, text=text, bg=colors['light_bg'], fg=colors['text_light'], font=("Segoe UI",9))
    lbl.grid(row=i//2, column=(i%2)*2, sticky=W, padx=6, pady=2)
    ent = Entry(team_frame, width=20, font=("Segoe UI",9))
    ent.grid(row=i//2, column=(i%2)*2+1, padx=6, pady=2)
    entries_team.append(ent)
entry_team_id, entry_team_name, entry_team_coach, entry_team_budget, entry_team_wins, entry_team_losses = entries_team

team_button_frame = Frame(team_frame, bg=colors['light_bg'])
team_button_frame.grid(row=99, column=0, columnspan=6, pady=6)
team_btns = [
    ("First", lambda: displayTeam(0)),
    ("Prev", prevTeamCmd),
    ("Next", nextTeamCmd),
    ("Last", lambda: displayTeam(len(cur.execute("SELECT * FROM Teams").fetchall()) - 1)),
    ("Save", updateTeamCmd),
    ("Add", insertTeamCmd),
    ("Delete", deleteTeamCmd),
    ("Clear", clearTeamCmd)
]
for i, (txt, cmd) in enumerate(team_btns):
    b = create_button(team_button_frame, txt, cmd, width=9)
    b.grid(row=0, column=i, padx=3)

# == Matches Tab ==
tab_matches = Frame(notebook, bg=colors['dark_bg'])
notebook.add(tab_matches, text="⚡ Matches")
frame_matches = Frame(tab_matches, bg=colors['dark_bg'])
frame_matches.pack(fill=BOTH, expand=True, padx=10, pady=10)
Label(frame_matches, text="Match Management", fg=colors['secondary'], bg=colors['dark_bg'], font=("Segoe UI",12,"bold")).pack(pady=4)

match_frame = LabelFrame(frame_matches, text="Match Details", bg=colors['light_bg'], fg=colors['text_light'], padx=6, pady=6)
match_frame.pack(fill=X, padx=6, pady=6)
labels_match = ["Match ID", "Team 1", "Team 2", "Date", "Venue", "Result"]
entries_match = []
for i, text in enumerate(labels_match):
    lbl = Label(match_frame, text=text, bg=colors['light_bg'], fg=colors['text_light'], font=("Segoe UI",9))
    lbl.grid(row=i//2, column=(i%2)*2, sticky=W, padx=6, pady=2)
    ent = Entry(match_frame, width=20, font=("Segoe UI",9))
    ent.grid(row=i//2, column=(i%2)*2+1, padx=6, pady=2)
    entries_match.append(ent)
entry_match_id, entry_match_team1, entry_match_team2, entry_match_date, entry_match_venue, entry_match_result = entries_match

match_button_frame = Frame(match_frame, bg=colors['light_bg'])
match_button_frame.grid(row=99, column=0, columnspan=6, pady=6)
match_btns = [
    ("First", lambda: displayMatch(0)),
    ("Prev", prevMatchCmd),
    ("Next", nextMatchCmd),
    ("Last", lambda: displayMatch(len(cur.execute("SELECT * FROM Matches").fetchall()) - 1)),
    ("Save", updateMatchCmd),
    ("Add", insertMatchCmd),
    ("Delete", deleteMatchCmd),
    ("Clear", clearMatchCmd)
]
for i, (txt, cmd) in enumerate(match_btns):
    b = create_button(match_button_frame, txt, cmd, width=9)
    b.grid(row=0, column=i, padx=3)

# == Performances Tab ==
tab_performances = Frame(notebook, bg=colors['dark_bg'])
notebook.add(tab_performances, text="🎯 Performances")
frame_performances = Frame(tab_performances, bg=colors['dark_bg'])
frame_performances.pack(fill=BOTH, expand=True, padx=10, pady=10)
Label(frame_performances, text="Performance Management", fg=colors['secondary'], bg=colors['dark_bg'], font=("Segoe UI",12,"bold")).pack(pady=4)

perf_frame = LabelFrame(frame_performances, text="Performance Details", bg=colors['light_bg'], fg=colors['text_light'], padx=6, pady=6)
perf_frame.pack(fill=X, padx=6, pady=6)
labels_perf = ["Perf ID", "Player ID", "Match ID", "Runs", "Wickets", "Catches"]
entries_perf = []
for i, text in enumerate(labels_perf):
    lbl = Label(perf_frame, text=text, bg=colors['light_bg'], fg=colors['text_light'], font=("Segoe UI",9))
    lbl.grid(row=i//2, column=(i%2)*2, sticky=W, padx=6, pady=2)
    ent = Entry(perf_frame, width=20, font=("Segoe UI",9))
    ent.grid(row=i//2, column=(i%2)*2+1, padx=6, pady=2)
    entries_perf.append(ent)
entry_perf_id, entry_perf_player, entry_perf_match, entry_perf_runs, entry_perf_wickets, entry_perf_catches = entries_perf

perf_button_frame = Frame(perf_frame, bg=colors['light_bg'])
perf_button_frame.grid(row=99, column=0, columnspan=6, pady=6)
perf_btns = [
    ("First", lambda: displayPerformance(0)),
    ("Prev", prevPerformanceCmd),
    ("Next", nextPerformanceCmd),
    ("Last", lambda: displayPerformance(len(cur.execute("SELECT * FROM Performances").fetchall()) - 1)),
    ("Save", updatePerformanceCmd),
    ("Add", insertPerformanceCmd),
    ("Delete", deletePerformanceCmd),
    ("Clear", clearPerformanceCmd)
]
for i, (txt, cmd) in enumerate(perf_btns):
    b = create_button(perf_button_frame, txt, cmd, width=9)
    b.grid(row=0, column=i, padx=3)

# == Reports Tab ==
tab_reports = Frame(notebook, bg=colors['dark_bg'])
notebook.add(tab_reports, text="📊 Reports")
frame_reports = Frame(tab_reports, bg=colors['dark_bg'])
frame_reports.pack(fill=BOTH, expand=True, padx=10, pady=10)
Label(frame_reports, text="Reports", fg=colors['secondary'], bg=colors['dark_bg'], font=("Segoe UI",12,"bold")).pack(pady=6)

report_frame = LabelFrame(frame_reports, text="Available Reports", bg=colors['light_bg'], fg=colors['text_light'], padx=8, pady=8)
report_frame.pack(fill=X, padx=6, pady=6)

report_buttons = [
    ("Player Statistics", reportPlayerStatsCmd),
    ("Team Standings", reportTeamStandingsCmd),
    ("Top Performers", reportTopPerformersCmd),
    ("Match Schedule", reportMatchScheduleCmd),
    ("Financial Report", reportFinancialCmd),
    ("Nationality Report", reportNationalityCmd),
    ("Player Performance", reportPlayerPerformanceCmd),
    ("Venue Report", reportVenueCmd),
    ("Team Squads", reportTeamSquadsCmd)
]

for i, (txt, cmd) in enumerate(report_buttons):
    b = create_button(report_frame, txt, cmd, width=20)
    b.grid(row=i//3, column=i%3, padx=8, pady=8, sticky="nsew")

for c in range(3):
    report_frame.grid_columnconfigure(c, weight=1)

# == Analytics Tab ==
tab_analytics = Frame(notebook, bg=colors['dark_bg'])
notebook.add(tab_analytics, text="📈 Analytics")

Label(tab_analytics, text="Advanced Analytics", font=("Segoe UI",12,"bold"),
      fg=colors['secondary'], bg=colors['dark_bg']).pack(pady=6)

analytics_frame = Frame(tab_analytics, bg=colors['dark_bg'])
analytics_frame.pack(fill=BOTH, expand=True, padx=8, pady=6)

analytics_buttons = [
    ("Top Run Scorers", analyticsTopRunScorers),
    ("Top Wicket Takers", analyticsTopWicketTakers),
    ("Player Comparison", analyticsPlayerComparison),
    ("Team Performance", analyticsTeamPerformance),
    ("Player Roles", analyticsPlayerRoles),
    ("Match Venue", analyticsMatchVenue)
]

for i, (txt, cmd) in enumerate(analytics_buttons):
    create_button(analytics_frame, txt, cmd, width=20).grid(row=i//2, column=i%2, padx=6, pady=6)

# == Initialize Display ==
displayPlayer(0)
displayTeam(0)
displayMatch(0)
displayPerformance(0)
window.mainloop()