# Conference Management System – Frappe App

## Overview

**conference_management** is a custom Frappe application designed to manage conferences, sessions, attendees, and registrations in a structured and scalable manner.

The system demonstrates real-world business logic implementation using Frappe best practices and is suitable for production-grade use as well as interview assessments.

It includes:

- Robust server-side validations
- Session scheduling and capacity management
- Mock payment processing with retry support
- Attendee session recommendations
- Search APIs
- Centralized API request logging

> All APIs are currently **guest-accessible** for testing and integration purposes.

---

## Key Features

---

## Conference & Session Management

### Conference

Create and manage conferences with the following fields:

- `conference_name`
- `start_date`
- `end_date`
- `location`
- `status` (Upcoming, Ongoing, Completed, Cancelled)
- `description`

**Automatic Status Management**
- Status is updated dynamically based on the current date.

---

### Session

Sessions are linked to conferences and include:

- `session_name`
- `conference` (Link)
- `start_time` (Datetime)
- `end_time` (Datetime)
- `speaker`
- `max_attendees`

#### Validations

- Prevent overlapping sessions within the same conference
- Ensure session start and end times fall within the conference date range
- Enforce logical datetime order (`start_time < end_time`)

---

## Attendee Management

### Attendee

Stores attendee information:

- `attendee_name`
- `email`
- `phone_number`
- `organization`
- `preferences` (Child table linking preferred sessions)

---

## Registration Management

### Registration

Registers attendees for specific conference sessions.

Fields:

- `conference`
- `session`
- `attendee`
- `registration_date`
- `payment_status` (Pending, Paid, Failed)

#### Client-side Behavior

- `registration_datetime` defaults to current date
- Session field shows only sessions belonging to the selected conference

#### Validations

- Prevent attendees from registering for overlapping sessions
- Prevent registration when session capacity (`max_attendees`) is exceeded
- Enforce session–conference consistency

---

## Payment Simulation

### Mock Payment Gateway

- Simulates payment processing with an **80% success rate**
- Automatically updates `payment_status`
- Supports retry when payment status is `Failed`
- Prevents reprocessing when status is `Paid`

### Payment Status Flow



### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app --branch develop https://github.com/Jishnusuni/conference_management 
bench install-app conference_management
```
