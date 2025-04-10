from faker import Faker
import random
from datetime import datetime, timedelta, date
import os
import calendar
print("Saving to:", os.getcwd())

fake = Faker()
Faker.seed(5)

company_names = [
    "TechNova", "GreenPulse", "OptimaBank", "FutureFund", "Skyline Ventures", "Quantum Invest",
    "BlueHorizon", "EcoWealth", "Velocity Capital", "Zenith Tech", "PrimeSecure", "Stellar Assets",
]

risk_tolerance = ["Low", "Medium", "Moderate", "High"]



NUM_INVESTORS = 150
PID_START = 1
AID_STOCKS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
AID_FUNDS = [11, 12, 13, 14]
AID_BONDS = [15, 16, 17, 18]

sql_statements = []
pid_counter = PID_START

for i in range(NUM_INVESTORS):
    name = fake.unique.name()
    phone = fake.unique.msisdn()[:8]
    gender = random.choice(['Male', 'Female'])
    dob = fake.date_of_birth(minimum_age=25, maximum_age=45).strftime('%Y-%m-%d')
    income = round(random.uniform(60000, 1500000),0)
    company = random.choice(company_names)

    sql_statements.append(
        f"INSERT INTO Investor (Phone, Name, Gender, DoB, Annual_Income, Company) VALUES ('{phone}', '{name}', '{gender}', '{dob}', {income}, '{company}');"
    )

    answers = [random.choice(['A', 'B', 'C', 'D']) for _ in range(5)]
    rt = random.choice(risk_tolerance)
    sql_statements.append( 
        f"INSERT INTO RiskTolerance (Risk_Level, Phone, Q1, Q2, Q3, Q4, Q5) VALUES ('{rt}', '{phone}', '{answers[0]}', '{answers[1]}', '{answers[2]}', '{answers[3]}', '{answers[4]}');"
    )

    goal = random.choice(['Buy a car', 'Retirement', 'Pay debt', 'Travel fund', 'Education', 'Start a business', 'Increase savings', 'Marriage', 'Buy a house'])
    goal_amt = random.randint(20000, 300000)
    start_date = datetime(2024, 2, 1)
    end_date = datetime(2024, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    timeline = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
    created = '2024-01-01'
    sql_statements.append(
        f"INSERT INTO FinancialGoal (Goal, Phone, Amount, Timeline, Created_Date) VALUES ('{goal}', '{phone}', {goal_amt}, '{timeline}', '{created}');"
    )

    num_portfolios = random.randint(1,4)
    for j in range(num_portfolios):
        pid = pid_counter
        sql_statements.append(
            f"INSERT INTO Portfolio (Market_Value, Fee, Inception_Date, Annualised_Returns, Phone) VALUES (0, 0, '2024-01-01', 0, '{phone}');"
        )

        stock_ids = random.sample(AID_STOCKS, 2)
        fund_id = random.choice(AID_FUNDS)
        bond_id = random.choice(AID_BONDS)

        stock_alloc = round(random.uniform(0.15, 0.30), 2)
        stock_alloc2 = round(random.uniform(0.10, 0.25), 2)
        fund_alloc = round(random.uniform(0.25, 0.35), 2)
        bond_alloc = round(1.0 - stock_alloc - stock_alloc2 - fund_alloc, 2)

        sql_statements.append(
            f"INSERT INTO StockInPortfolio (Asset_ID, PID, Start_Date, Allocation_Ratio, Post_Trade_Company) VALUES ({stock_ids[0]}, {pid}, '2024-01-01', {stock_alloc}, 'AutoGen');"
        )
        sql_statements.append(
            f"INSERT INTO StockInPortfolio (Asset_ID, PID, Start_Date, Allocation_Ratio, Post_Trade_Company) VALUES ({stock_ids[1]}, {pid}, '2024-01-01', {stock_alloc2}, 'AutoGen');"
        )
        sql_statements.append(
            f"INSERT INTO FundInPortfolio (Asset_ID, PID, Start_Date, Allocation_Ratio, Post_Trade_Company) VALUES ({fund_id}, {pid}, '2024-01-01', {fund_alloc}, 'AutoGen');"
        )
        sql_statements.append(
            f"INSERT INTO BondInPortfolio (Asset_ID, PID, Start_Date, Allocation_Ratio, Post_Trade_Company) VALUES ({bond_id}, {pid}, '2024-01-01', {bond_alloc}, 'AutoGen');"
        )

        

        invested_value = 0
        base = random.randint(5000, 100000)
        invested_value += base
        sql_statements.append(f"INSERT INTO InvestedValue (Date, PID, Phone, Amount) VALUES ('2024-01-01', {pid}, '{phone}', {base});")
        for aid in [*stock_ids, fund_id, bond_id]:
            sql_statements.append(f"INSERT INTO TransactionLog (DateTime, Asset_ID, PID, Type, Fee) VALUES ('2024-01-01', {aid}, {pid}, 'Buy', 50);")
        months = random.sample(range(12), k=random.randint(2, 4))
        for m in range(12):
            year = 2024
            month = m + 1
            max_day = calendar.monthrange(year, month)[1]
            day = random.randint(2, max_day)

            random_date = date(year, month, day)
            date_str = random_date.strftime('%Y-%m-%d')
            if m in months:
                value = base * random.randint(1, 2)
                invested_value += value
            sql_statements.append(f"INSERT INTO InvestedValue (Date, PID, Phone, Amount) VALUES ('{date_str}', {pid}, '{phone}', {invested_value});")
            sql_statements.append(f"INSERT INTO TransactionLog (DateTime, Asset_ID, PID, Type, Fee) VALUES ('{date_str}', {stock_ids[0]}, {pid}, 'TopUp', 50);")
            sql_statements.append(f"INSERT INTO TransactionLog (DateTime, Asset_ID, PID, Type, Fee) VALUES ('{date_str}', {stock_ids[1]}, {pid}, 'TopUp', 50);")
            sql_statements.append(f"INSERT INTO TransactionLog (DateTime, Asset_ID, PID, Type, Fee) VALUES ('{date_str}', {fund_id}, {pid}, 'TopUp', 50);")
            sql_statements.append(f"INSERT INTO TransactionLog (DateTime, Asset_ID, PID, Type, Fee) VALUES ('{date_str}', {bond_id}, {pid}, 'TopUp', 50);")
        
        
        target_sum = random.uniform(-0.3 * invested_value, 2.7 * invested_value)
        weights = [random.random() for _ in range(12)]
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        values = [round(target_sum * w, 2) for w in normalized_weights]
        diff = round(target_sum - sum(values), 2)
        values[-1] += diff

        for n in range(12):
            match n:
                case 0:
                    date_str = '2024-01-31'
                case 1:
                    date_str = '2024-02-29'
                case 2:
                    date_str = '2024-03-31'
                case 3:
                    date_str = '2024-04-30'
                case 4:
                    date_str = '2024-05-31'
                case 5:
                    date_str = '2024-06-30'
                case 6:
                    date_str = '2024-07-31'
                case 7:
                    date_str = '2024-08-31'
                case 8:
                    date_str = '2024-09-30'
                case 9:
                    date_str = '2024-10-31'
                case 10:
                    date_str = '2024-11-30'
                case 11:
                    date_str = '2024-12-31'
            ugl = values[n]
            sql_statements.append(f"INSERT INTO UnrealisedGainLoss (Date, PID, Phone, Amount) VALUES ('{date_str}', {pid}, '{phone}', {ugl});")

        annualised_returns = target_sum/invested_value
        market_value = target_sum + invested_value
        fee = market_value*0.0088

        sql_statements.append(f"UPDATE Portfolio SET Market_Value = {market_value}, Annualised_Returns = {annualised_returns}, FEE = {fee} WHERE PID = {pid};")

        pid_counter+=1
        


with open("python_populate.sql", "w") as file:
    for statement in sql_statements:
        file.write(statement + "\n")
print("SQL script written to python_populate.sql ✅")