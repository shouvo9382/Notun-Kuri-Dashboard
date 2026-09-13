import random
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

SPORTS = {
    "Cricket": {"emoji": "\U0001F3CF", "skills": ["Batting", "Bowling", "Fielding", "Wicket-keeping", "All-rounder"], "units": {"bat_avg": "runs", "bowl_sr": "balls/wicket", "field_pct": "%"}},
    "Football": {"emoji": "\u26BD", "skills": ["Forward", "Midfielder", "Defender", "Goalkeeper"], "units": {"goals": "goals", "passes": "passes", "distance_km": "km"}},
    "Kabaddi": {"emoji": "\U0001F94B", "skills": ["Raider", "Defender", "All-rounder"], "units": {"raids": "raids", "tackles": "tackles", "super_raids": "super raids"}},
    "Badminton": {"emoji": "\U0001F3F8", "skills": ["Singles", "Doubles", "All-round"], "units": {"win_pct": "%", "smash_speed": "km/h", "rally_avg": "shots"}},
    "Swimming": {"emoji": "\U0001F3CA", "skills": ["Freestyle", "Backstroke", "Butterfly", "Breaststroke"], "units": {"time_100m": "sec", "stroke_rate": "strokes/min", "distance_m": "m"}},
    "Chess": {"emoji": "\u265F", "skills": ["Tactical", "Positional", "Aggressive", "Defensive"], "units": {"elo": "rating", "tactics_solved": "puzzles", "games_played": "games"}},
    "Athletics": {"emoji": "\U0001F3C3", "skills": ["Sprint", "Middle Distance", "Long Jump", "High Jump", "Shot Put", "Discus"], "units": {"time_100m": "sec", "distance_m": "m", "height_cm": "cm"}},
    "Martial Arts": {"emoji": "\U0001F94B", "skills": ["Striking", "Grappling", "Forms/Kata"], "units": {"wins": "wins", "techniques": "moves", "points": "points"}},
    "Volleyball": {"emoji": "\U0001F3D0", "skills": ["Spiker", "Setter", "Blocker", "Libero"], "units": {"spikes": "spikes", "aces": "aces", "digs": "digs"}},
    "Table Tennis": {"emoji": "\U0001F3D3", "skills": ["Offensive", "Defensive", "All-round"], "units": {"win_pct": "%", "serve_speed": "km/h", "spin_rate": "rpm"}},
}

DISTRICTS = {
    "Dhaka": {"pop_rank": 1, "region": "Central"},
    "Chattogram": {"pop_rank": 2, "region": "Chattogram Hill"},
    "Gazipur": {"pop_rank": 3, "region": "Central"},
    "Narayanganj": {"pop_rank": 4, "region": "Central"},
    "Rajshahi": {"pop_rank": 5, "region": "North"},
    "Sylhet": {"pop_rank": 6, "region": "North-East"},
    "Khulna": {"pop_rank": 7, "region": "South-West"},
    "Barishal": {"pop_rank": 8, "region": "South"},
    "Rangpur": {"pop_rank": 9, "region": "North"},
    "Mymensingh": {"pop_rank": 10, "region": "North-Central"},
    "Comilla": {"pop_rank": 11, "region": "Central-East"},
    "Bogra": {"pop_rank": 12, "region": "North"},
    "Cox's Bazar": {"pop_rank": 13, "region": "South-East"},
    "Jessore": {"pop_rank": 14, "region": "South-West"},
    "Dinajpur": {"pop_rank": 15, "region": "North"},
    "Tangail": {"pop_rank": 16, "region": "Central"},
    "Faridpur": {"pop_rank": 17, "region": "Central"},
    "Pabna": {"pop_rank": 18, "region": "North"},
    "Kushtia": {"pop_rank": 19, "region": "South-West"},
    "Noakhali": {"pop_rank": 20, "region": "South-East"},
}

TRAINING_CENTERS = [
    "BKSP Dhaka", "BKSP Chattogram", "BKSP Rajshahi", "BKSP Khulna",
    "BKSP Sylhet", "BKSP Rangpur", "National Sports Institute, Dhaka",
    "Divisional Training Center, Barishal", "Divisional Training Center, Mymensingh",
    "Zonal Training Center, Comilla", "Zonal Training Center, Bogra",
    "District Sports Center, Dhaka", "District Sports Center, Chattogram",
    "District Sports Center, Sylhet", "District Sports Center, Rajshahi",
]

MALE_FIRST = [
    "Tanvir", "Rakib", "Sakib", "Anis", "Farhan", "Imran", "Rafiq", "Sohel", "Alamin", "Rahat",
    "Nayeem", "Shakil", "Jahid", "Tamim", "Mushfiq", "Liton", "Mehidy", "Shoriful", "Taskin", "Mustafiz",
    "Ariful", "Rony", "Sumon", "Biplob", "Habib", "Raihan", "Shuvo", "Mithun", "Raju", "Kamal",
    "Hossain", "Jubayer", "Nafis", "Saif", "Adnan", "Zubair", "Fahim", "Abrar", "Wasi", "Humayun",
    "Rashid", "Mubin", "Tariq", "Basit", "Omar", "Farabi", "Shihab", "Nabil", "Pranto", "Zihad",
]

FEMALE_FIRST = [
    "Nigar", "Jannat", "Tasnim", "Maliha", "Farzana", "Rumana", "Shirin", "Nusrat", "Sabrina", "Mstuma",
    "Sanjida", "Roksana", "Lamia", "Tahsin", "Anika", "Bidya", "Sumaiya", "Sharmin", "Priti", "Nafisa",
    "Tanzila", "Mumtahina", "Marjia", "Faria", "Meghla", "Shapla", "Koli", "Ruma", "Anju", "Joya",
    "Rupali", "Champa", "Lily", "Runa", "Mita", "Rina", "Sathi", "Gita", "Beauty", "Papia",
    "Tuli", "Doli", "Oishe", "Ishita", "Tasnia", "Faija", "Umma", "Bushra", "Halima", "Khatija",
]

LAST_NAMES = [
    "Islam", "Ahmed", "Khan", "Hossain", "Rahman", "Ali", "Hossen", "Mia", "Sheikh", "Das",
    "Chowdhury", "Uddin", "Patel", "Biswas", "Sarker", "Iqbal", "Mahmud", "Ferdous", "Akter", "Begum",
    "Haque", "Molla", "Ghosh", "Paul", "Debnath", "Mondal", "Sarkar", "Gazi", "Jahan", "Rashid",
]

COACH_REMARKS = [
    "Exceptional talent, national team potential within 2 years",
    "Consistent performer, needs competition exposure at national level",
    "High potential athlete, requires structured training plan",
    "Natural athlete with strong fundamentals and leadership qualities",
    "Showing rapid improvement, recommend advanced training program",
    "Good technique, needs to build physical endurance",
    "Very promising for international competition, prioritize nutrition",
    "Strong competitor with excellent mental toughness",
    "Maintains steady performance under pressure, team player",
    "Exhibits leadership qualities, consider for captaincy role",
    "Raw talent that needs refinement in competitive settings",
    "Impressive recovery from setback, resilient athlete",
    "Outstanding work ethic, model for peer athletes",
    "Technical skills above average, tactical awareness developing",
    "Early developer, will benefit from age-appropriate load management",
]


def gen_name(gender):
    first = random.choice(MALE_FIRST if gender == "Male" else FEMALE_FIRST)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"


def gen_performance_history(base, months=12, volatility=3.5):
    vals = []
    current = base - random.uniform(3, 10)
    for _ in range(months):
        delta = random.gauss(1.0, volatility)
        current = max(35, min(99, current + delta))
        vals.append(round(current, 1))
    if vals[-1] < base - 8:
        vals[-1] = round(base - random.uniform(0, 3), 1)
    return vals


def gen_training_log(months=12):
    entries = []
    for m in range(months):
        hrs = round(random.uniform(12, 38), 1)
        sessions = random.randint(4, 7)
        entries.append({"month": m, "hours": hrs, "sessions": sessions})
    return entries


def gen_injury_log():
    injuries = ["None", "None", "None", "None", "None", "Knee strain", "Ankle sprain",
                "Shoulder impingement", "Back stiffness", "Hamstring pull", "Wrist strain"]
    count = 0
    log = []
    for _ in range(random.randint(0, 2)):
        inj = random.choice([i for i in injuries if i != "None"])
        month = random.randint(0, 11)
        severity = random.choice(["Mild", "Moderate"])
        recovery = random.randint(2, 6)
        log.append({"injury": inj, "month": month, "severity": severity, "recovery_weeks": recovery})
        count += 1
    return log, count


def gen_tournament_log():
    events = [
        "District Championship", "Divisional Championship", "National Junior Championship",
        "BKSP Inter-Training Center Meet", "Age-Group National Championship",
        "District School Sports", "Zonal Youth Games", "Divisional School Sports",
        "National School Championship", "BKSP Annual Meet", "Inter-District Youth Championship",
    ]
    n = random.randint(3, 12)
    log = []
    wins = 0
    for _ in range(n):
        event = random.choice(events)
        placement = random.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[10, 15, 20, 15, 12, 10, 10, 8])[0]
        if placement == 1:
            wins += 1
        log.append({"event": event, "placement": placement, "year": random.choice([2024, 2025, 2026])})
    return log, n, wins


def gen_sport_metrics(sport_name, rating):
    base = rating * 0.8
    metrics = {}
    sport = SPORTS[sport_name]
    if sport_name == "Cricket":
        metrics["batting_avg"] = round(random.uniform(15, 65) * (rating / 80), 1)
        metrics["bowling_sr"] = round(random.uniform(12, 35) * (80 / max(rating, 50)), 1)
        metrics["fielding_pct"] = round(random.uniform(70, 98), 1)
        metrics["matches"] = random.randint(8, 35)
    elif sport_name == "Football":
        metrics["goals"] = random.randint(0, 18)
        metrics["assists"] = random.randint(0, 12)
        metrics["pass_accuracy"] = round(random.uniform(55, 92), 1)
        metrics["matches"] = random.randint(10, 40)
    elif sport_name == "Kabaddi":
        metrics["raid_points"] = random.randint(15, 80)
        metrics["tackle_points"] = random.randint(10, 60)
        metrics["super_raids"] = random.randint(0, 12)
        metrics["matches"] = random.randint(10, 30)
    elif sport_name == "Badminton":
        metrics["win_pct"] = round(random.uniform(30, 85) * (rating / 80), 1)
        metrics["smash_speed"] = round(random.uniform(120, 220) * (rating / 80), 1)
        metrics["matches"] = random.randint(15, 50)
    elif sport_name == "Swimming":
        metrics["time_100m"] = round(random.uniform(55, 85) * (90 / max(rating, 50)), 2)
        metrics["stroke_rate"] = round(random.uniform(28, 48), 1)
        metrics["events_entered"] = random.randint(3, 12)
    elif sport_name == "Chess":
        metrics["elo_rating"] = round(random.uniform(800, 1800) * (rating / 80))
        metrics["tactics_solved"] = random.randint(50, 500)
        metrics["games_played"] = random.randint(20, 100)
    elif sport_name == "Athletics":
        metrics["time_100m"] = round(random.uniform(12, 18) * (75 / max(rating, 50)), 2)
        metrics["best_jump"] = round(random.uniform(3.5, 6.5) * (rating / 80), 2)
        metrics["events"] = random.randint(1, 4)
    elif sport_name == "Martial Arts":
        metrics["wins"] = random.randint(5, 30)
        metrics["losses"] = random.randint(0, 8)
        metrics["techniques_mastered"] = random.randint(15, 45)
        metrics["tournaments"] = random.randint(3, 15)
    elif sport_name == "Volleyball":
        metrics["spikes"] = random.randint(30, 150)
        metrics["aces"] = random.randint(5, 40)
        metrics["blocks"] = random.randint(10, 60)
        metrics["matches"] = random.randint(12, 40)
    elif sport_name == "Table Tennis":
        metrics["win_pct"] = round(random.uniform(35, 88) * (rating / 80), 1)
        metrics["serve_speed"] = round(random.uniform(40, 85) * (rating / 80), 1)
        metrics["matches"] = random.randint(15, 60)
    return metrics


def generate_player(pid, tier):
    gender = random.choice(["Male", "Female"])
    age = random.choices(range(8, 15), weights=[5, 8, 12, 18, 22, 20, 15])[0]
    district_name = random.choice(list(DISTRICTS.keys()))
    primary_sport = random.choice(list(SPORTS.keys()))
    secondary_sport = random.choice([s for s in SPORTS if s != primary_sport])
    name = gen_name(gender)

    if tier == "top":
        primary_rating = round(random.triangular(76, 98, 88), 1)
    else:
        primary_rating = round(random.triangular(45, 79, 62), 1)

    secondary_rating = round(max(38, primary_rating - random.uniform(8, 25)), 1)

    sport_ratings = {}
    for s in SPORTS:
        if s == primary_sport:
            sport_ratings[s] = primary_rating
        elif s == secondary_sport:
            sport_ratings[s] = secondary_rating
        else:
            sport_ratings[s] = round(random.gauss(52, 10))
            sport_ratings[s] = max(35, min(sport_ratings[s], 75))

    overall = round(np.mean(list(sport_ratings.values())), 1)

    history = gen_performance_history(primary_rating)
    trend = round(history[-1] - history[0], 2)
    consistency = round(np.std(history), 2)

    inj_log, inj_count = gen_injury_log()
    tour_log, tour_played, tour_won = gen_tournament_log()
    training_log = gen_training_log()

    medals_g = random.choices([0, 1, 2, 3, 4], weights=[30, 35, 20, 10, 5])[0]
    medals_s = random.choices([0, 1, 2, 3], weights=[35, 35, 20, 10])[0]
    medals_b = random.choices([0, 1, 2, 3, 4], weights=[25, 30, 25, 15, 5])[0]

    if tier == "top":
        stipend = random.choices([3000, 5000, 7500, 10000], weights=[20, 35, 30, 15])[0]
    else:
        stipend = 0

    att = round(random.uniform(72, 100), 1)
    train_hrs = round(np.mean([e["hours"] for e in training_log]), 1)

    if tier == "top":
        rel_risk = round(min(0.85, max(0.05, (80 - primary_rating) / 50 + inj_count * 0.08 + (100 - att) / 200 + random.uniform(-0.1, 0.1))), 2)
    else:
        rel_risk = 0

    if tier == "pipeline":
        prom_chance = round(min(0.92, max(0.05, (primary_rating - 55) / 30 + trend * 0.05 + tour_won * 0.03 + random.uniform(-0.1, 0.1))), 2)
    else:
        prom_chance = 0

    sport_metrics = gen_sport_metrics(primary_sport, primary_rating)

    return {
        "Player ID": f"NK{pid:04d}",
        "Name": name,
        "Gender": gender,
        "Age": age,
        "Date of Birth": f"{random.randint(2012, 2018):04d}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        "District": district_name,
        "Region": DISTRICTS[district_name]["region"],
        "Training Center": random.choice(TRAINING_CENTERS),
        "Primary Sport": primary_sport,
        "Skill Specialization": random.choice(SPORTS[primary_sport]["skills"]),
        "Secondary Sport": secondary_sport,
        "Tier": tier.upper(),
        "Stipend (BDT)": stipend,
        "Overall Rating": overall,
        "Primary Rating": primary_rating,
        "Secondary Rating": secondary_rating,
        **{f"Rating - {s}": sport_ratings[s] for s in SPORTS},
        "Performance Trend": trend,
        "Consistency Score": consistency,
        "Peak Rating": round(max(history), 1),
        "Lowest Rating": round(min(history), 1),
        "Tournaments Played": tour_played,
        "Tournaments Won": tour_won,
        "Win Rate": round(tour_won / max(tour_played, 1) * 100, 1),
        "Gold Medals": medals_g,
        "Silver Medals": medals_s,
        "Bronze Medals": medals_b,
        "Total Medals": medals_g + medals_s + medals_b,
        "Training Hours/Week": train_hrs,
        "Attendance %": att,
        "Hot Streak": random.randint(0, 14),
        "Injury Count": inj_count,
        "Promotion Chance": prom_chance,
        "Relegation Risk": rel_risk,
        "Performance History": history,
        "Training Log": training_log,
        "Injury Log": inj_log,
        "Tournament Log": tour_log,
        "Status": "Active" if inj_count == 0 or random.random() > 0.3 else "Recovering",
        "Coach Remarks": random.choice(COACH_REMARKS),
        **{f"Metric - {k}": v for k, v in sport_metrics.items()},
    }


def generate_all_data():
    players = []
    for i in range(1, 401):
        players.append(generate_player(i, "top"))
    for i in range(401, 801):
        players.append(generate_player(i, "pipeline"))
    return pd.DataFrame(players)


def generate_district_summary(df):
    return df.groupby("District").agg(
        Total_Athletes=("Player ID", "count"),
        Avg_Rating=("Overall Rating", "mean"),
        Max_Rating=("Overall Rating", "max"),
        Top_Tier=("Tier", lambda x: (x == "TOP").sum()),
        Pipeline_Tier=("Tier", lambda x: (x == "PIPELINE").sum()),
        Total_Medals=("Total Medals", "sum"),
        Gold=("Gold Medals", "sum"),
        Silver=("Silver Medals", "sum"),
        Bronze=("Bronze Medals", "sum"),
        Male=("Gender", lambda x: (x == "Male").sum()),
        Female=("Gender", lambda x: (x == "Female").sum()),
        Avg_Age=("Age", "mean"),
        Avg_Attendance=("Attendance %", "mean"),
        Total_Stipend=("Stipend (BDT)", "sum"),
    ).reset_index().round(1)


def generate_sport_summary(df):
    rows = []
    for sport in SPORTS:
        sdf = df[df["Primary Sport"] == sport]
        rows.append({
            "Sport": sport,
            "Athletes": len(sdf),
            "Avg Rating": round(sdf["Overall Rating"].mean(), 1),
            "Top Rating": round(sdf["Overall Rating"].max(), 1),
            "Male": (sdf["Gender"] == "Male").sum(),
            "Female": (sdf["Gender"] == "Female").sum(),
            "Avg Age": round(sdf["Age"].mean(), 1),
            "Top Tier": (sdf["Tier"] == "TOP").sum(),
            "Pipeline": (sdf["Tier"] == "PIPELINE").sum(),
            "Total Medals": sdf["Total Medals"].sum(),
            "Avg Training Hrs": round(sdf["Training Hours/Week"].mean(), 1),
            "Avg Attendance": round(sdf["Attendance %"].mean(), 1),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_all_data()
    df.to_csv("players_data.csv", index=False)
    print(f"Generated {len(df)} players across {len(SPORTS)} sports and {len(DISTRICTS)} districts")
