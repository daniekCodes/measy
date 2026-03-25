# M'easy – Centralized Group Appointment Management

**M'easy** is a centralized web platform designed to solve the challenges of unorganized group coordination and information loss within traditional chat histories. The application provides a structured environment for creating, voting on, managing, and finalizing group appointments.

## Core Features

### Centralized Voting
* Users can create events where participants vote on various date and time options to reach a group consensus.

### Flexible Data Model
* The system supports indefinite appointments through the use of optional database fields.

### Dynamic Client-Side Logic
* Real-time input validation and form masks adapt dynamically based on backend data structures to prevent user errors.

### Streamlined Workflow
* The platform offers a clear path from initial event creation through the voting process to final appointment confirmation.

## Tech Stack

### Frontend
* **UI Framework**: Bootstrap 5.
* **Templating**: Jinja2 for server-side rendering.
* **Client Logic**: JavaScript for dynamic interactions and validation.

### Backend & Database
* **Language**: Python 3.12.
* **Web Framework**: Flask.
* **ORM**: SQLAlchemy with SQLite integration.

## Application Architecture

### Data Model
Relational database structure mapping complex relationships:
* **Users**: Participant and organizer management.
* **Appointments**: Core event data including descriptions and timeframes.
* **Votes & Choices**: Voting behavior and scheduling options.

### Key Routes
Flask routing provides logical navigation:
* `/`: User login.
* `/users/<user_id>`: Personal appointments overview.
* `/users/<user_id>/appointments/<appointment_id>`: Event details and editing.
* `/users/<user_id>/appointments/create`: New voting event creation.

## Development Roadmap

### Immediate Priorities
* **Authentication**: Complete login/registration system.
* **Role Management**: Admin vs. participant permissions.
* **Notifications**: Email updates for appointment changes.

### Long-term Enhancements
* **Calendar Export**: .ics format for Outlook/Google Calendar sync.
* **Mobile Optimization**: Enhanced responsive design.
* **Reminder System**: Push notifications before voting deadlines.

# M'easy – Zentrale Terminabstimmung für Gruppen

**M'easy** ist eine zentrale Webplattform, die die Herausforderungen unübersichtlicher Gruppenkoordination und Informationsverlust in Chat-Verläufen löst. Die Anwendung bietet eine strukturierte Umgebung zur Erstellung, Abstimmung, Verwaltung und Fixierung von Gruppenterminen.

## Kernfunktionen

### Zentrale Abstimmung
* Erstellung von Events, bei denen Teilnehmer über verschiedene Terminoptionen zur Konsensfindung abstimmen.

### Flexibles Datenmodell
* Unterstützung unbestimmter Termine durch den Einsatz optionaler Felder.

### Dynamische Client-Logik
* Echtzeit-Validierung mit anpassbaren Formularmasken basierend auf den Backend-Datenstrukturen.

### Strukturierter Workflow
* Ein klarer Pfad von der ersten Event-Erstellung über die Abstimmung bis hin zur finalen Terminbestätigung.

## Technischer Stack

### Frontend
* **UI-Framework**: Bootstrap 5.
* **Templating**: Jinja2 für serverseitiges Rendering.
* **Client-Logik**: Vanilla JavaScript für dynamische Interaktionen und Validierung.

### Backend & Datenbank
* **Sprache**: Python 3.12.
* **Web-Framework**: Flask.
* **ORM**: SQLAlchemy mit SQLite-Anbindung.

## Anwendungsarchitektur

### Datenmodell
Relationales Datenbankschema für komplexe Beziehungen:
* **User**: Verwaltung von Teilnehmern und Organisatoren.
* **Appointments**: Kern-Event-Daten (Beschreibungen, Zeiträume).
* **Votes & Choices**: Abstimmungsverhalten und Optionen.

### Wichtige Routen
Logische Flask-Routings:
* `/`: Benutzer-Login.
* `/users/<user_id>`: Persönliche Terminübersicht.
* `/users/<user_id>/appointments/<appointment_id>`: Event-Details und Bearbeitung.
* `/users/<user_id>/appointments/create`: Neues Abstimmungsevent.

## Entwicklungsroadmap

### Kurzfristige Prioritäten
* **Authentifizierung**: Vollständiges Login-/Registrierungssystem.
* **Rollenmanagement**: Admin- vs. Teilnehmer-Berechtigungen.
* **Benachrichtigungen**: E-Mail-Updates bei Terminänderungen.

### Langfristige Erweiterungen
* **Kalender-Export**: .ics-Format für Outlook/Google Kalender.
* **Mobile-Optimierung**: Erweiterte Responsive-Designs.
* **Erinnerungssystem**: Push-Benachrichtigungen vor Abstimmungsfristen.
