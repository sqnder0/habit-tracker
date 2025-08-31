# Habit Tracker

A powerful and intuitive web-based habit tracking application built with Django. Track your daily habits, monitor your progress, and build lasting positive routines with streak tracking and detailed analytics.

## 🌟 Features

### Core Functionality
- **Daily Habit Tracking**: Mark habits as complete or incomplete for each day
- **Streak Calculation**: Automatic calculation of current habit streaks to maintain motivation
- **User Authentication**: Secure user registration, login, and personalized habit management
- **Notes System**: Add personal notes for each habit completion to track thoughts and progress
- **Date Navigation**: View and manage habits for any past date (future dates are restricted)
- **Responsive Design**: Clean, modern interface that works on desktop and mobile devices

### Advanced Features
- **Custom Habit Creation**: Create habits with personalized names, descriptions, and preferred completion times
- **Progress Visualization**: Track your consistency and improvement over time
- **User-Specific Data**: Each user has their own private set of habits and tracking data
- **Real-time Updates**: Dynamic interface updates without page refreshes using AJAX
- **Data Persistence**: All habit data is securely stored in a SQLite database

## 📖 Usage Guide

### Getting Started
1. **Sign Up**: Create a new account or log in with existing credentials
2. **Create Habits**: Click on the gear icon and add your first habit with a name, description, and preferred time
3. **Daily Tracking**: Check off habits as you complete them each day
4. **Monitor Progress**: Watch your streaks grow and track your consistency

### Managing Habits
- **Add New Habits**: Use the interface to create habits with custom descriptions
- **Edit Habits**: Modify habit details, descriptions, and completion times
- **Delete Habits**: Remove habits you no longer want to track
- **View History**: Navigate to previous dates to see your past performance

### Understanding Streaks
The streak system calculates consecutive days where you've completed a habit:
- Streaks include today if the habit is marked complete
- If today isn't complete, the streak counts from yesterday backwards
- Missing a day breaks the streak, starting fresh from the next completion

## 🏗️ Project Structure

```
habittracker/
├── habittracker/           # Main Django project directory
│   ├── settings.py        # Django configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── main/                  # Core habit tracking app
│   ├── models.py         # Database models (Habit, Day)
│   ├── views.py          # View logic and API endpoints
│   ├── urls.py           # App-specific URL patterns
│   ├── forms.py          # Django forms
│   └── templates/        # HTML templates
├── signup/                # User authentication app
│   ├── models.py         # User-related models
│   ├── views.py          # Authentication views
│   └── templates/        # Auth templates
├── static/               # CSS, JavaScript, images
├── templates/            # Shared HTML templates
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## 🛠️ Technology Stack

- **Backend**: Django 5.2.5 (Python web framework)
- **Database**: SQLite (development), PostgreSQL ready (production)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Boostrap 5.6
- **Styling**: Custom CSS with responsive design
- **Dependencies**:
  - `django-widget-tweaks`: Enhanced form rendering
  - `python-dotenv`: Environment variable management
  - `gunicorn`: Production WSGI server

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Implement your feature or bug fix
4. **Test thoroughly**: Ensure your changes don't break existing functionality
5. **Commit your changes**: `git commit -m 'Add some amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**: Describe your changes and their benefits

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:
- Check the existing [Issues](https://github.com/sqnder0/habit-tracker/issues)
- Create a new issue with detailed information
- Include steps to reproduce any bugs

## 🔮 Future Enhancements

Planned features and improvements:
- Habit categories and tags
- Advanced analytics and charts
- Habit sharing and social features
- Export functionality for data backup
- Customizable reminder notifications

---

**Happy habit tracking!** 🎯 Start building better habits today and watch your consistency grow over time.

Made with ❤️ by [sqnder0](https://github.com/sqnder0)
