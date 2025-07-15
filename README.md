# Let's Rewrite the Constitution!

A competitive, gamified platform where users practice logical thinking and precise language creation by tackling constitutional problems. The goal is to teach people how to think systematically about rules, laws, and governance while engaging with real democratic issues.

## 🎯 Core Concept

This is a puzzle game where players:
- Receive historical constitutional crises to solve
- Write precise constitutional language to fix problems
- Vote on others' solutions with mandatory explanations
- Learn logical thinking and rule-writing skills
- Build a community of constitutional thinkers

## 🚀 Features

### Game Mechanics
- **Challenge System**: Historical constitutional problems with time limits
- **Submission System**: Users write constitutional language and reasoning
- **Voting System**: Upvote/downvote with required explanations
- **Discussion System**: Reddit-style comments and replies
- **Gamification**: Points, levels, leaderboards, and achievements

### Educational Goals
- **Logical Thinking**: Train users to identify problems and create systematic solutions
- **Precise Language**: Practice writing clear, unambiguous rules that actually work
- **Rule Creation**: Understand how laws and governance systems function
- **Critical Analysis**: Examine why existing systems fail and how to improve them
- **Democratic Engagement**: Connect with constitutional issues through active problem-solving

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the website**:
   Open your browser and go to `http://localhost:5000`

## 👤 Getting Started

### First Time Setup
1. **Set up secure admin account**:
   ```bash
   # Set a secure setup token (use a strong random string)
   export ADMIN_SETUP_TOKEN="your-secure-random-token-here"
   
   # Run the app
   python app.py
   
   # Visit http://localhost:5000/setup_admin
   # Enter your admin email, password, and the setup token
   # Remove the environment variable after setup for security
   ```

2. **Login as admin** to create your first challenge:
   - Go to `http://localhost:5000/admin/create_challenge`
   - Create a constitutional challenge for the community

### For Regular Users
1. **Register** a new account at `http://localhost:5000/register`
2. **Browse challenges** at `http://localhost:5000/challenges`
3. **Submit solutions** to constitutional problems
4. **Vote and comment** on others' submissions
5. **Earn points** and climb the leaderboard

## 🎮 How to Play

### 1. Choose a Challenge
Browse active constitutional challenges. Each challenge presents a real historical problem that needs constitutional language to solve.

### 2. Write Your Solution
- **Constitutional Language**: Write precise, formal language like the U.S. Constitution
- **Reasoning**: Explain your logical thinking and why your solution works
- **Consider Edge Cases**: Think about unintended consequences

### 3. Vote and Discuss
- **Vote on submissions** with required explanations
- **Comment and discuss** solutions with other players
- **Learn from feedback** and improve your thinking

### 4. Earn Points
- Submit solutions: +10 points
- Vote on submissions: +1-2 points
- Comment on submissions: +1 point
- Level up as you earn more points

## 🏗️ Technical Architecture

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **SQLite**: Database (can be changed to PostgreSQL/MySQL for production)

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icons
- **Custom CSS**: Styled components and animations

### Database Models
- **User**: User accounts, points, levels
- **Challenge**: Constitutional problems and context
- **Submission**: User solutions with voting
- **Vote**: User votes with explanations
- **Comment**: Discussion threads

## 📁 Project Structure

```
constitution/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── design.txt            # Original design document
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── challenges.html   # Challenge listing
│   ├── challenge_detail.html  # Individual challenge view
│   ├── submit_solution.html   # Solution submission form
│   ├── submission_detail.html # Submission view with voting
│   ├── profile.html      # User profile page
│   ├── leaderboard.html  # Points leaderboard
│   └── create_challenge.html  # Admin challenge creation
└── constitution_game.db  # SQLite database (created automatically)
```

## 🎯 Example Challenges

The platform is designed for challenges like:
- **Electoral College Reform**: Fix the winner-takes-all system
- **Campaign Finance**: Regulate political spending
- **Presidential Impeachment**: Clarify the process
- **Supreme Court Term Limits**: Address lifetime appointments
- **Voting Rights**: Protect against disenfranchisement
- **Emergency Powers**: Limit executive authority

## 🎨 Design Philosophy

### Reddit-Style Interface
- **Submission posts** with voting
- **Threaded discussions** under each submission
- **Mandatory explanations** for votes
- **Community moderation** through voting

### Educational Focus
- **Process over product**: Learning to think systematically
- **Clear criteria**: Focus on logical reasoning and precise language
- **Community learning**: Learn from others' approaches
- **Gamification**: Make learning engaging and competitive

## 🔧 Customization

### Adding New Challenges
1. Login as admin
2. Go to `/admin/create_challenge`
3. Fill out the challenge form with:
   - Historical context
   - Clear problem statement
   - Relevant constitutional text
   - Reasonable time limit

### Modifying Scoring
Edit the point values in `app.py`:
- Submission points (line ~150)
- Voting points (lines ~180-185)
- Comment points (line ~200)

### Styling
Modify `templates/base.html` CSS variables:
- `--primary-color`: Main brand color
- `--secondary-color`: Accent color
- `--accent-color`: Highlight color

## 🚀 Deployment

### For Production
1. **Change the secret key** in `app.py`
2. **Use a production database** (PostgreSQL/MySQL)
3. **Set up a web server** (nginx + gunicorn)
4. **Configure environment variables** for sensitive data
5. **Set up SSL certificates** for HTTPS

### Example Production Setup
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🤝 Contributing

This is an educational project designed to teach logical thinking and constitutional literacy. Feel free to:
- Add new challenge types
- Improve the UI/UX
- Enhance the gamification system
- Add new educational features

## 📚 Educational Value

This platform teaches:
- **Systematic problem-solving** through constitutional puzzles
- **Precise language skills** by writing legal text
- **Critical analysis** of governance systems
- **Democratic literacy** through hands-on practice
- **Logical reasoning** in complex scenarios

## 🎉 Success Metrics

The platform succeeds when users:
- Develop better logical thinking skills
- Learn to write clear, enforceable rules
- Understand constitutional governance better
- Engage with democratic issues constructively
- Build a community of thoughtful problem-solvers

---

**Let's Rewrite the Constitution!** - Teaching logical thinking through constitutional problem-solving. 