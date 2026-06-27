from crewai import Agent,Task,Crew,Process,LLM
from crewai import Agent, Task, Crew, Process, LLM
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
import sqlite3
from datetime import datetime, timedelta
from fpdf import FPDF
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Securely fetch the API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

console = Console()

"""**Hospital Managememt System**"""

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0.3
)

# Agent 1
receptionist = Agent(
    role="Receptionist",
    goal="Register patients",
    backstory="You collect patient information.",
    llm=llm,
    verbose=True
)

# Agent 2
doctor = Agent(
    role="Doctor",
    goal="Diagnose patients",
    backstory="You are an experienced physician.",
    llm=llm,
    verbose=True
)

# Agent 3
pharmacist = Agent(
    role="Pharmacist",
    goal="Suggest medicines and precautions",
    backstory="You provide prescriptions and advice.",
    llm=llm,
    verbose=True
)

# Agent 4
billing_officer = Agent(
    role="Billing Officer",
    goal="Generate hospital bills",
    backstory="You manage patient billing.",
    llm=llm,
    verbose=True
)

# Task 1
registration_task = Task(
    description="""
    Patient Details:

    Name: Ravi
    Age: 35

    Symptoms:
    - Fever
    - Headache
    - Body Pain
        Register the patient.
    """,
    expected_output="Patient registration summary.",
    agent=receptionist
)

# Task 2
diagnosis_task = Task(
    description="""
    Analyze symptoms and provide diagnosis.
    """,
    expected_output="Doctor diagnosis report.",
    agent=doctor
)



# Task 3
medicine_task = Task(
    description="""
    Suggest medicines and precautions.
    """,
    expected_output="Prescription details.",
    agent=pharmacist
)

# Task 4
billing_task = Task(
    description="""
    Generate consultation and medicine bill.
    """,
    expected_output="Hospital bill.",
    agent=billing_officer
)

crew = Crew(
    agents=[receptionist, doctor, pharmacist, billing_officer],
    tasks=[registration_task, diagnosis_task, medicine_task, billing_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()

print("\n Final Result")
print(result)

"""**SMART Hospital Management System**"""

from crewai import Agent, Task, Crew, Process, LLM
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
import sqlite3
from datetime import datetime, timedelta
from fpdf import FPDF

console = Console()

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0.3,
    max_tokens=50
)

def init_db():
  conn = sqlite3.connect('hospital.db')
  cur = conn.cursor()
  cur.execute("""
  CREATE TABLE IF NOT EXISTS patients(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      age INTEGER,
      symptoms TEXT,
      doctor TEXT,
      appointment_date TEXT,
      visit_date TEXT
  )
  """)
  # safe migration for old databases
  try:
      cur.execute("ALTER TABLE patients ADD COLUMN visit_date TEXT")
  except:
      pass

  conn.commit()
  conn.close()

init_db()

def book_appointment(patient_name, doctor_name):
    appointment_date = (
        datetime.now() + timedelta(days=1)
    ).strftime("%d-%m-%Y")

    token = f"T{hash(patient_name) % 1000}"
    return appointment_date, token

def save_patient(name, age, symptoms, doctor, appointment_date):
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO patients (
            name, age, symptoms, doctor, appointment_date, visit_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        symptoms,
        doctor,
        appointment_date,
        datetime.now().strftime("%d-%m-%Y")
    ))

    conn.commit()
    conn.close()

def get_patient_history(patient_name):
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT symptoms, doctor, appointment_date, visit_date
        FROM patients
        WHERE name = ?
        ORDER BY id DESC
        LIMIT 5
    """, (patient_name,))

    rows = cur.fetchall()
    conn.close()
    return rows

def generate_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report_text)
    pdf.output("Patient_Report.pdf")

console.print(
    Panel.fit(
        "[bold cyan]SMART HOSPITAL MANAGEMENT SYSTEM[/bold cyan]",
        border_style="green"
    )
)

patient_name = console.input("Patient Name : ")
age = console.input("Age : ")
symptoms = console.input("Symptoms : ")

history = get_patient_history(patient_name)

if history:
    console.print(
        Panel.fit(
            "[bold green]Returning Patient Detected[/bold green]",
            border_style="green"
        )
    )

    table = Table(title="Previous Visits")
    table.add_column("Visit Date")
    table.add_column("Symptoms")
    table.add_column("Doctor")

    for row in history:
        table.add_row(row[3], row[0], row[1])
    console.print(table)

else:
    console.print(
        Panel.fit(
            "[yellow]New Patient[/yellow]",
            border_style="yellow"
        )
    )


info = Table(title="Patient Information")
info.add_column("Field", style="cyan")
info.add_column("Value", style="green")

info.add_row("Name", patient_name)
info.add_row("Age", age)
info.add_row("Symptoms", symptoms)

console.print(info)

history_text = ""
for row in history:
    history_text += f"""
Visit Date: {row[3]}
Symptoms: {row[0]}
Doctor: {row[1]}
"""

symptom_agent = Agent(
    role="Symptom Analyzer",
    goal="Analyze symptoms and detect possible disease.",
    backstory="Experienced medical triage expert.",
    llm=llm,
    verbose=True
)

doctor_agent = Agent(
    role="Doctor Recommender",
    goal="Suggest correct specialist doctor.",
    backstory="Hospital doctor allocation system.",
    llm=llm,
    verbose=True
)
precaution_agent = Agent(
    role="Medical Advisor",
    goal="Suggest precautions and home care tips.",
    backstory="Senior healthcare advisor.",
    llm=llm,
    verbose=True
)

report_agent = Agent(
    role="Report Generator",
    goal="Generate final patient report.",
    backstory="Hospital documentation expert.",
    llm=llm,
    verbose=True
)

task1 = Task(
    description=f"""
Patient Name: {patient_name}
Age: {age}
Symptoms: {symptoms}

Previous History:
{history_text}

Analyze condition and severity.
""",
    expected_output="Disease prediction and severity.",
    agent=symptom_agent
)

task2 = Task(
    description=f"Symptoms: {symptoms}\nRecommend specialist doctor.",
    expected_output="Doctor specialization.",
    agent=doctor_agent
)

task3 = Task(
    description=f"Symptoms: {symptoms}\nGive precautions.",
    expected_output="Care instructions.",
    agent=precaution_agent
)

task4 = Task(
    description="Generate final medical report.",
    expected_output="Full structured report.",
    agent=report_agent
)

crew = Crew(
    agents=[symptom_agent, doctor_agent, precaution_agent, report_agent],
    tasks=[task1, task2, task3, task4],
    process=Process.sequential,
    verbose=True
)

console.print(Rule("[bold blue]AI Analysis Started[/bold blue]"))

result = crew.kickoff()

doctor_name = "General Physician"
appointment_date, token = book_appointment(patient_name, doctor_name)

save_patient(
    patient_name,
    age,
    symptoms,
    doctor_name,
    appointment_date
)


final_report = f"""
PATIENT REPORT
------------------
Name: {patient_name}
Age: {age}
Symptoms: {symptoms}

Doctor: {doctor_name}
Appointment: {appointment_date}
Token: {token}

AI ANALYSIS:
{result}

Status: Saved Successfully
"""

generate_pdf(final_report)

console.print(
    Panel(
        final_report,
        title="[bold green]FINAL REPORT[/bold green]",
        border_style="green"
    )
)

console.print(
    Panel.fit("PDF Generated: Patient_Report.pdf", border_style="green")
)

console.print(
    Panel.fit("Saved to SQLite Database", border_style="green")
)
