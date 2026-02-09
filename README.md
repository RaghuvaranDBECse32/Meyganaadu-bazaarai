🚀 Project Title

CloudShield AI – AWS-Based Intelligent Threat Detection & Honeypot System

📌 Overview

CloudShield AI is a cloud-native security platform that deploys an intelligent honeypot to detect, analyze, and respond to malicious activities in real time. Built using Python and AWS services, the system captures attacker behavior, logs events securely, and provides actionable insights through an API-driven architecture.

The project is designed using Kiro’s Spec → Design workflow, generating structured requirements.md and design.md artifacts as required by the challenge.

🎯 Problem Statement

Traditional security systems often detect attacks after damage is done. There is a need for a proactive, intelligent system that:

Attracts attackers safely

Monitors their behavior

Analyzes threats in real time

Stores and visualizes security insights securely

💡 Solution

CloudShield AI deploys a decoy honeypot service hosted on AWS that simulates vulnerable endpoints. When attackers interact with it:

Requests are captured and analyzed

Suspicious patterns are identified

Logs are stored securely

Alerts and reports are generated via APIs

🧠 Key Features

🕵️ Intelligent Honeypot Simulation

☁️ Fully Cloud-Native (AWS)

🔐 Secure Logging & Threat Storage

📊 API-based Threat Insights

⚙️ Scalable & Serverless Architecture

🛠️ Tech Stack
Language

Python

Backend

FastAPI / Flask

AWS Services

AWS Lambda – Core logic

API Gateway – Expose APIs

DynamoDB – Attack logs & metadata

S3 – Store reports/artifacts

CloudWatch – Monitoring & alerts

IAM – Secure access control

🧩 Architecture (High Level)

Attacker interacts with honeypot endpoint

API Gateway forwards request

Lambda analyzes request behavior

Logs stored in DynamoDB

Alerts & metrics sent to CloudWatch

Insights accessible via REST API
