# Coma Gen-e Backend

Flask + PostgreSQL backend for **Coma Gen-e**, a university web application project focused on software-related content, blogs, user interaction and software-owner workflows.

## Overview

The API supports user registration and email verification, user and software-owner authentication, blog creation and moderation, software usability articles and comments, approval flows, PostgreSQL persistence, and REST-style endpoints consumed by the Vue frontend.

The frontend is available in [ComaGen-E-Front](https://github.com/Ogi-Z/ComaGen-E-Front).

## Tech Stack

- Python
- Flask
- PostgreSQL
- psycopg2
- Flask-CORS
- Werkzeug password hashing
- SMTP email verification

## Security & Configuration

Runtime credentials are kept out of source control and loaded from environment variables.

Copy the example configuration:

```bash
cp .env.example .env
```

Passwords are stored as hashes using Werkzeug instead of plaintext values.

> This is an educational project and is not intended to be deployed as-is in production. Production hardening would additionally include stricter CORS rules, structured validation, migrations, authorization middleware, rate limiting and automated tests.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the PostgreSQL database:

```sql
CREATE DATABASE tempDB;
```

Configure values from `.env.example`, then start the API:

```bash
python main.py
```

## Main API Areas

| Area | Example endpoints |
| --- | --- |
| Authentication | `/login`, `/ownerlogin`, `/verify`, `/verifyowner` |
| Users | `/add_user`, `/users`, `/query_user/<id>` |
| Blogs | `/add_blog`, `/blogs`, `/approveblog`, `/update_blog` |
| Software usability | `/add_softwareUsability`, `/softwareUsability`, `/approvesoftwareusability` |
| Comments | `/add_softwareUsabilityComment`, `/softwareUsabilityComments/<id>` |
| Software owners | `/add_softwareowner`, `/softwareowners`, `/query_softwareowner/<id>` |

## Data Model

![Coma Gen-e data model](https://github.com/Ogi-Z/ProjectBackend/assets/59333212/51540350-55b3-457d-96af-fef309a5a47f)

## Project Context

This project was developed as a team project with **Fatih Alparslan Kaya**. My work included backend functionality, PostgreSQL integration and the database model.
