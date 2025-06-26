# Group Bill Splitter

An AI Agent aimed at helping business school students better prioritize their time, interests, and focus areas amidst abundant distraction and opportunity. 

## ✨ Features

- Daily scraping of WhatsApp, Canvas, and 12twenty to 

## 🚀 Quick Start

### Prerequisites

[TECH STACK GOES HERE]

### 1. Setup Environment

[ENV setup goes here]

This script will:
- Create `.env` files with all required variables
- Start Supabase services
- Install dependencies
- Guide you through API key configuration

### 2. Configure API Keys

[API KEY Information goes here]

### 3. Start Services

[Startup information goes here]

### 4. Start a chat (?)



## 🛠️ Development Commands

# Start all services

# Stop all services  

# Restart services (useful when making changes)

# View logs

## 🔧 Manual Development Setup

If you prefer manual setup:

```bash
# 1. Start Supabase

# 2. Upload function secrets


# 3. Start Edge Functions


# 4. Start React app (in another terminal)


## 📖 How It Works

### 1. Setup Priorities
- User sets quarterly priorities for their time in the program. This would include: 
  - Social interests: Parties, Outdoor activities, Games nights, etc. 
  - Career interests: Alumni panels, recruiting events, career management center workshops, etc. 
  - Academic interests: Courses to investegate, due dates for assignments, group meetings, etc. 
- Application takes those priorities as keywords to scan sources for suggested events prioritizing the top 1-2 items to focus on per category per week. 

### 2. Setup Cadence
- User sets the frequency with which they would liks summarized reminders of their activity
- Cadence determines the frequency with which they will be reminded of those opporutnities

### 3. Data Scraping
- Based on user preferecnes, data sources are scraped daily for new opportunities and formatted for easy consumption. 

### 4. Communication Cadence
- User is reminded of the important items they should be attending based on their cadence preferences. 
- Chat will check in based on the chosen cadence to see if those items are accomplished and then can help the user re-balance priorities for the future. 




## 🏗️ Architecture

- **Frontend**: Email notifications (sendgrid) or WhatsApp chat, or Slack
- **Backend/Automation Engine**: FastAPI + Celery for scheduling reminders
- **Storage**: Supabase (?)
- **Auth**: Supabase Auth with magic link/OTP

## 📊 Database Schema

### Core Tables


### Key Features


## 🔒 Security & Privacy

- **Authentication**: Magic link/OTP-based login
- **Authorization**: Row-level security on all data
- **Data Privacy**: Users only access bills they're involved in
- **File Security**: Receipt images in private storage buckets
- **API Security**: Rate limiting and CORS protection
