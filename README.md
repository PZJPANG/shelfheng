# 🏠 ShelfHeng

**ShelfHeng** is a web-based inventory management system designed to help you organize and track your belongings across multiple locations and shelves. Never lose track of your items again!

## 📝 About the Name

**ShelfHeng** combines "Shelf" + "Heng", representing a **shelf that hangs online**. Just like a physical shelf that hangs on your wall, ShelfHeng is your digital shelf that "hangs" on the web - accessible anywhere, anytime. It's where you can sort and organize your things in the cloud, making your physical belongings digitally manageable and easily searchable.

## ✨ Features

- **Multi-Location Support**: Organize items across different houses/locations
- **Shelf Management**: Create and manage shelves within each location
- **Item Tracking**: Add, search, and manage your belongings
- **User Authentication**: Secure login and registration system
- **Search Functionality**: Quickly find items by name
- **Visual Interface**: Clean, modern web interface with smooth animations

## 🎯 Problem It Solves

Have you ever:
- Bought something you already owned because you forgot where you placed it?
- Struggled to find the right tools when you were in a hurry?
- Wished you had a digital inventory of your belongings?

ShelfHeng solves these problems by providing a digital space to manage your physical shelves and belongings, making everything easy to find and track.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/shelfheng.git
   cd shelfheng
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`
   
Or, try it out instantly online at: https://shelfheng.ddns.net

## 📱 How to Use

### Getting Started
1. **Register** for a new account or **login** to an existing one
2. **Add Houses/Locations** where you store your items
3. **Create Shelves** within each house
4. **Add Items** to specific shelves
5. **Search** for items when you need them

### Key Features
- **All in One**: View all your houses and their contents from the main page
- **Quick Search**: Find items instantly by typing their name
- **Organized Storage**: Keep track of exactly where each item is stored
- **Easy Management**: Add, delete, and organize your items and locations

## 🛠️ Technical Details

### Built With
- **Backend**: Flask (Python web framework)
- **Database**: SQLite with custom database wrapper
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Session with password hashing
- **Deployment**: Ready for Railway, Render, or Heroku

### Project Structure
```
shelfheng/
├── app.py              # Main Flask application
├── database.py         # Database connection and operations
├── helpers.py          # Authentication helper functions
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── static/            # CSS, images, and other static files
├── templates/         # HTML templates
└── shelfheng.db       # SQLite database file
```

### Database Schema
- **users**: User accounts with secure password hashing
- **places**: Houses/locations where items are stored
- **shelves**: Shelves within each location
- **items**: Individual items with location and shelf information

## 🚀 Deployment

ShelfHeng is ready for deployment on popular platforms:

### Railway (Recommended)
1. Push your code to GitHub
2. Connect your repository to [Railway](https://railway.app)
3. Deploy automatically with zero configuration

### Render
1. Connect your GitHub repository to [Render](https://render.com)
2. Choose Python environment
3. Deploy with the provided Procfile

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🎨 Design Philosophy

> "If you can't measure it, you can't improve it" - Lord Kelvin

ShelfHeng is built on the principle that organization leads to efficiency. By digitally tracking your physical belongings, you can:
- Reduce time spent searching for items
- Avoid duplicate purchases
- Maintain better organization
- Have peace of mind knowing where everything is

## 👥 Team

This project was developed collaboratively by:
- **Zi Jian** ([@PZJPANG](https://github.com/PZJPANG)) 
- **Jun Bin** ([@Xaaa06](https://github.com/Xaaa06)) 

## 🎓 What We Learned

This project served as our **CS50 Final Project**, where we gained valuable hands-on experience in:

### 🔧 Development Skills
- **Local Development Environment**: Transitioned from CS50's online IDE to using Visual Studio Code locally, learning proper development workflow and environment management
- **Version Control & Collaboration**: Mastered Git and GitHub for project management, including branching, committing, and collaborative development practices
- **Full-Stack Development**: Built a complete web application from database design to user interface, integrating frontend and backend technologies

### 🚀 Deployment & DevOps
- **Server Deployment**: Successfully deployed the application using Railway for cloud hosting
- **Domain Management**: Configured custom domain using No-IP (shelfheng.ddns.net) for public access
- **Production Environment**: Learned to manage production vs development environments and handle deployment challenges

### 💻 Technical Implementation
- **Flask Framework**: Deep understanding of web application architecture, routing, and session management
- **Database Design**: Created and managed SQLite database with proper relationships between users, locations, shelves, and items
- **User Authentication**: Implemented secure login/logout functionality with password hashing
- **Responsive Design**: Built intuitive user interfaces with CSS animations and JavaScript interactions

This project represents the culmination of our CS50 journey, demonstrating practical application of computer science concepts in a real-world project.

## 🤝 Contributing

Contributions are welcome! This project is a work in progress, continuously improving through curiosity and persistence.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source.

## 🙏 Acknowledgments

- Built with Flask and modern web technologies
- Inspired by the need for better personal organization
- Designed with user experience and simplicity in mind

---

**Start organizing your life, one shelf at a time!** 🏠✨
