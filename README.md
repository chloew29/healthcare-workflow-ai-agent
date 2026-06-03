# Healthcare Workflow AI Agent

An AI-agent-style healthcare operations platform that simulates patient access, appointment routing, prior authorization checks, billing/claims workflow review, human escalation flags, and agent performance analytics.

This project is designed as a HealthTech portfolio project for entry-level healthcare data analyst, healthcare business analyst, clinical operations analyst, patient access analyst, revenue cycle analyst, and AI workflow analyst roles.

## Project Overview

Healthcare organizations receive high volumes of repetitive administrative requests related to appointment scheduling, insurance approval, referrals, billing, claims, and patient account questions. These workflows are time-consuming for staff and often require structured routing, rule checking, and human review.

This project demonstrates how an AI-agent-style workflow can classify synthetic patient requests, route them to the correct operational tool, generate structured outputs, flag high-risk or incomplete cases for human review, and track operational performance through an analytics dashboard.

## Business Problem

Hospitals and health systems need better ways to evaluate whether AI agents actually improve operations. A healthcare AI agent should not only respond to messages. It should also:

* Identify the request type
* Route the case to the correct workflow
* Use structured operational data
* Flag incomplete or high-risk cases for human review
* Track automation performance
* Estimate staff time saved
* Monitor token-level cost
* Support audit-style logging

This project focuses on the data and operations layer behind healthcare AI agent deployment.

## Key Features

* Patient request classification
* Appointment scheduling workflow simulation
* Prior authorization rule checking
* Billing and claims workflow simulation
* Human escalation flag for high-risk or incomplete cases
* Automated batch simulation of synthetic patient requests
* Audit-style agent logs
* Agent performance dashboard
* Auto-resolution rate tracking
* Escalation rate tracking
* Estimated staff time saved
* Token-level cost tracking
* Healthcare AI safety disclaimer

## Agent Workflows

### 1. Patient Access / Appointment Workflow

The agent classifies appointment-related requests and checks synthetic appointment and provider availability data.

Example request:

```text
I need to schedule a cardiology appointment next week.
```

Example output:

```text
Intent: appointment
Department: Cardiology
Tool Used: Appointment Tool
Outcome: Appointment option found
Escalation: No
```

### 2. Prior Authorization Workflow

The agent checks synthetic payer rules to determine whether a procedure may require prior authorization and whether the case should be escalated.

Example request:

```text
I have Kaiser HMO and need an MRI. Do I need approval?
```

Example output:

```text
Intent: prior_authorization
Payer: Kaiser HMO
Procedure: MRI
Prior Auth Required: Yes
Denial Risk: High
Escalation: Yes
```

### 3. Billing / Claims Workflow

The agent simulates billing and claims review using synthetic revenue cycle data.

Example request:

```text
Why was my claim denied?
```

Example output:

```text
Intent: billing_claims
Tool Used: Billing / Claims Tool
Outcome: Claim status and denial reason checked
Escalation: Yes
```

## Sample Agent Output Table

| Input Request                                          | Detected Intent     | Tool Used             | Escalation | Outcome                     |
| ------------------------------------------------------ | ------------------- | --------------------- | ---------- | --------------------------- |
| I need to schedule a cardiology appointment next week. | appointment         | Appointment Tool      | No         | Appointment option found    |
| I have Kaiser HMO and need an MRI.                     | prior_authorization | Prior Auth Tool       | Yes        | Human review needed         |
| I have Blue Shield PPO and need a specialist visit.    | prior_authorization | Prior Auth Tool       | No/Yes     | Prior authorization checked |
| Why was my claim denied?                               | billing_claims      | Billing / Claims Tool | Yes        | Claim status reviewed       |
| I need help with my bill.                              | billing_claims      | Billing / Claims Tool | Yes        | Billing workflow checked    |

## Batch Simulation

The platform includes an automated batch simulation feature. Instead of testing one request at a time, the system can automatically process a batch of synthetic healthcare requests and update the dashboard.

Example simulation result:

```text
Total Requests: 53
Auto-Resolved Rate: 49.1%
Escalation Rate: 50.9%
Estimated Staff Time Saved: 393 minutes
Estimated Token Cost: $0.1060
```

## Performance Metrics

The dashboard tracks:

* Total request volume
* Request type distribution
* Auto-resolution rate
* Escalation rate
* Estimated staff minutes saved
* Estimated token cost
* Average staff time saved by intent
* Escalation rate by intent
* Token cost by intent
* Audit-style agent logs

These metrics help evaluate whether an AI agent is improving operational efficiency or creating too many cases that still require human review.

## Tech Stack

* Python
* Streamlit
* Pandas
* Synthetic healthcare operations data
* Rule-based agent routing
* CSV-based data storage
* Operational analytics dashboard

## Project Structure

```text
healthcare-workflow-ai-agent/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   ├── appointments.csv
│   ├── providers.csv
│   ├── payer_rules.csv
│   ├── claims.csv
│   └── agent_logs.csv
├── utils/
│   ├── agent_tools.py
│   ├── data_loader.py
│   └── analytics.py
├── sql/
├── notebooks/
└── screenshots/
```

## Healthcare AI Safety Design

This project is designed for educational and portfolio purposes only.

Safety controls include:

* Uses synthetic healthcare operations data only
* Does not contain PHI
* Does not provide medical advice
* Does not provide diagnosis or treatment recommendations
* Does not make real insurance decisions
* Does not schedule real appointments
* Flags high-risk, unsupported, or incomplete cases for human review
* Stores audit-style logs for review and performance monitoring

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

## Example Use Cases

This project is relevant to:

* Healthcare Data Analyst
* HealthTech Analyst
* Clinical Operations Analyst
* Patient Access Analyst
* Revenue Cycle Analyst
* Claims Analyst
* Prior Authorization Analyst
* Healthcare Business Analyst
* Healthcare IT Analyst
* AI Workflow Analyst

## Resume Summary

Built an AI-agent-style healthcare operations platform that classifies synthetic patient requests and routes them to appointment scheduling, prior authorization, or billing/claims workflows. Automated batch simulation of 50+ synthetic healthcare requests and developed an operations analytics dashboard tracking auto-resolution rate, escalation rate, staff time saved, token-level cost, and human escalation patterns.

## Future Improvements

* Add LLM-based intent classification
* Add LangChain or LangGraph tool routing
* Add SQLite database support
* Add billing and denial trend analytics
* Add downloadable executive report
* Add Power BI or Tableau dashboard version
* Add human feedback review workflow
* Add model output quality evaluation
