# Arts Day Event Management System

A beautiful web application for managing Arts Day events at College of Engineering Cherthala. Features separate student and admin portals with modern UI design.

## Features

### 🎭 Student Portal
- **Student Registration**: Easy signup with department selection
- **Event Browsing**: View available on-stage and off-stage events
- **Event Registration**: One-click registration for events
- **Personal Dashboard**: Track registered events and status
- **Responsive Design**: Works perfectly on mobile and desktop

### ⚙️ Admin Portal
- **Secure Login**: Protected admin access
- **Event Creation**: Create on-stage and off-stage events with detailed information
- **Event Management**: View all events with registration statistics
- **Participant Tracking**: Monitor on-stage participants with search functionality
- **Real-time Updates**: Live registration counts and event status

### 🎨 Design Features
- **Modern UI**: Glass-morphism design with gradient backgrounds
- **Responsive Layout**: Mobile-first design approach
- **Smooth Animations**: Engaging user interactions
- **Accessibility**: WCAG-compliant color contrasts and navigation
- **Professional Branding**: College of Engineering Cherthala themed

## Event Types

### 🎭 On-Stage Events
Live performances in front of audience:
- Dance competitions
- Music performances
- Drama and theater
- Stand-up comedy
- Poetry recitation

### 🎨 Off-Stage Events
Creative works and competitions:
- Art exhibitions
- Photography contests
- Creative writing
- Craft competitions
- Digital art

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with Glass-morphism effects
- **Security**: Password hashing with Werkzeug

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Clone or download the project files**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - The database will be automatically created on first run

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default admin password after first login for security.

## Project Structure

```
arts-day-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── instance/
│   └── artsday.db        # SQLite database (auto-created)
├── static/
│   └── style.css         # Additional CSS styles
└── templates/
    ├── landing.html      # Beautiful landing page
    ├── student_portal.html
    ├── student_register.html
    ├── student_login.html
    ├── student_dashboard.html
    ├── admin_portal.html
    ├── admin_login.html
    ├── admin_dashboard.html
    ├── create_event.html
    ├── admin_events.html
    ├── onstage_participants.html
    └── base.html         # Base template
```

## Database Schema

### Tables
- **admins**: Admin user accounts
- **students**: Student registrations
- **events**: Event information (on-stage/off-stage)
- **registrations**: Student event registrations

## Usage Guide

### For Students
1. Visit the landing page
2. Click "Student Portal"
3. Register as a new student or login with existing email
4. Browse available events in your dashboard
5. Register for events with one click
6. Track your registrations

### For Admins
1. Visit the landing page
2. Click "Admin Portal"
3. Login with admin credentials
4. Create new events with detailed information
5. Manage existing events and view statistics
6. Monitor on-stage participants

## Customization

### Changing College Information
Edit the following files to customize for your institution:
- `templates/landing.html`: Update college name and branding
- `templates/student_register.html`: Modify department options
- `app.py`: Update any hardcoded references

### Styling Modifications
- Main styles are embedded in each template for easy customization
- Additional global styles in `static/style.css`
- Color scheme uses CSS custom properties for easy theming

### Adding Features
The modular Flask structure makes it easy to add:
- Email notifications
- Event categories
- File uploads
- Payment integration
- Advanced reporting

## Security Features

- Password hashing for admin accounts
- SQL injection prevention with parameterized queries
- Session management for user authentication
- Input validation and sanitization
- CSRF protection ready (can be enhanced)

## Browser Support

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

This is a complete, production-ready system. For enhancements:
1. Test thoroughly before deploying
2. Backup the database before major changes
3. Follow Flask best practices
4. Maintain responsive design principles

## License

Open source - feel free to modify and use for your institution's needs.

## Support

For technical issues:
1. Check the Flask application logs
2. Verify database connectivity
3. Ensure all dependencies are installed
4. Check browser console for frontend errors

---

**Arts Day 2026 - College of Engineering Cherthala**
*Celebrate Creativity • Showcase Talent • Build Memories*