-- Investor Table
CREATE TABLE Investor (
    Phone VARCHAR(15) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    DoB DATE NOT NULL,
    Annual_Income DECIMAL(15,2) NOT NULL,
    Company VARCHAR(100) NOT NULL
);

-- Asset Table
CREATE TABLE Asset (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Price DECIMAL(15,2) NOT NULL
);

-- RiskTolerance Table
CREATE TABLE RiskTolerance (
    Risk_Level VARCHAR(50),
    Phone VARCHAR(15) NOT NULL,
    Q1 VARCHAR(50) NOT NULL,
    Q2 VARCHAR(50) NOT NULL,
    Q3 VARCHAR(50) NOT NULL,
    Q4 VARCHAR(50) NOT NULL,
    Q5 VARCHAR(50) NOT NULL,
    PRIMARY KEY(Risk_Level, Phone),
    FOREIGN KEY (Phone) REFERENCES Investor(Phone)
);

-- FinancialGoal Table
CREATE TABLE FinancialGoal (
    Goal VARCHAR(100) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Amount DECIMAL(15,2) NOT NULL,
    Timeline DATE NOT NULL,
    Created_Date DATE NOT NULL,
    PRIMARY KEY (Goal, Phone),
    FOREIGN KEY (Phone) REFERENCES Investor(Phone)
);

-- Portfolio Table
CREATE TABLE Portfolio (
    PID INT AUTO_INCREMENT PRIMARY KEY,
    Market_Value DECIMAL(15,2) NOT NULL,
    Fee DECIMAL(10,2) NOT NULL,
    Inception_Date DATE NOT NULL,
    Annualised_Returns DECIMAL(10,2) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    FOREIGN KEY (Phone) REFERENCES Investor(Phone)
);

-- InvestedValue Table
CREATE TABLE InvestedValue (
    Date DATE NOT NULL,
    PID INT NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Amount DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (Date, PID, Phone),
    FOREIGN KEY (PID) REFERENCES Portfolio(PID),
    FOREIGN KEY (Phone) REFERENCES Investor(Phone)
);

-- UnrealisedGainLoss Table
CREATE TABLE UnrealisedGainLoss (
    Date DATE NOT NULL,
    PID INT NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Amount DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (Date, PID, Phone),
    FOREIGN KEY (PID) REFERENCES Portfolio(PID),
    FOREIGN KEY (Phone) REFERENCES Investor(Phone)
);

-- StockInPortfolio Table
CREATE TABLE StockInPortfolio (
    Asset_ID INT NOT NULL,
    PID INT NOT NULL,
    Start_Date DATE NOT NULL,
    Allocation_Ratio DECIMAL(5,2) NOT NULL,
    Post_Trade_Company VARCHAR(100) NOT NULL,
    PRIMARY KEY (Asset_ID, PID),
    FOREIGN KEY (Asset_ID) REFERENCES Asset(ID) ON DELETE CASCADE,
    FOREIGN KEY (PID) REFERENCES Portfolio(PID)
);

-- BondInPortfolio Table
CREATE TABLE BondInPortfolio (
    Asset_ID INT NOT NULL,
    PID INT NOT NULL,
    Start_Date DATE NOT NULL,
    Allocation_Ratio DECIMAL(5,2) NOT NULL,
    Post_Trade_Company VARCHAR(100) NOT NULL,
    PRIMARY KEY (Asset_ID, PID),
    FOREIGN KEY (Asset_ID) REFERENCES Asset(ID) ON DELETE CASCADE,
    FOREIGN KEY (PID) REFERENCES Portfolio(PID)
);

-- FundInPortfolio Table
CREATE TABLE FundInPortfolio (
    Asset_ID INT NOT NULL,
    PID INT NOT NULL,
    Start_Date DATE NOT NULL,
    Allocation_Ratio DECIMAL(5,2) NOT NULL,
    Post_Trade_Company VARCHAR(100) NOT NULL,
    PRIMARY KEY (Asset_ID, PID),
    FOREIGN KEY (Asset_ID) REFERENCES Asset(ID) ON DELETE CASCADE,
    FOREIGN KEY (PID) REFERENCES Portfolio(PID)
);

-- TransactionLog Table
CREATE TABLE TransactionLog (
    DateTime DATETIME NOT NULL,
    Asset_ID INT NOT NULL,
    PID INT NOT NULL,
    Type VARCHAR(50) NOT NULL,
    Fee DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (DateTime, Asset_ID, PID),
    FOREIGN KEY (PID) REFERENCES Portfolio(PID),
    FOREIGN KEY (Asset_ID) REFERENCES Asset(ID) ON DELETE CASCADE
);

-- Stock Table
CREATE TABLE Stock (
    Asset_ID INT PRIMARY KEY,
    PE_Ratio DECIMAL(10,2) NOT NULL,
    EPS DECIMAL(15,2) NOT NULL,
    EBITDA DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (Asset_ID) REFERENCES Asset(ID) ON DELETE CASCADE
);

-- Bond Table
CREATE TABLE Bond (
    Asset_ID INT PRIMARY KEY,
    Interest_Rate DECIMAL(5,2) NOT NULL,
    Maturity_Date DATE NOT NULL,
    FOREIGN KEY (Asset_ID) REFERENCES Asset(ID) ON DELETE CASCADE
);

-- Fund Table
CREATE TABLE Fund (
    Asset_ID INT PRIMARY KEY,
    Expense_Ratio DECIMAL(5,2) NOT NULL,
    Dividend_Yield DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (Asset_ID) REFERENCES Asset(ID) ON DELETE CASCADE
);
