from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///constitution_game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.Integer, default=1)
    points = db.Column(db.Integer, default=0)
    submissions_count = db.Column(db.Integer, default=0)
    votes_given = db.Column(db.Integer, default=0)
    is_blocked = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    submissions = db.relationship('Submission', backref='author', lazy=True)
    votes = db.relationship('Vote', backref='voter', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    submitted_challenges = db.relationship('Challenge', backref='submitted_by', lazy=True)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    constitutional_context = db.Column(db.Text, nullable=False)
    problem_statement = db.Column(db.Text, nullable=False)
    relevant_amendments = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    is_finished = db.Column(db.Boolean, default=False)
    winner_submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=True)
    challenge_order = db.Column(db.Integer, default=0)  # For controlling sequence
    is_approved = db.Column(db.Boolean, default=False)  # For user-submitted challenges
    submitted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Who submitted this challenge
    
    submissions = db.relationship(
        'Submission',
        backref='challenge',
        lazy=True,
        foreign_keys='Submission.challenge_id'
    )
    winner = db.relationship(
        'Submission',
        foreign_keys=[winner_submission_id],
        post_update=True
    )

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    constitutional_language = db.Column(db.Text, nullable=False)
    reasoning = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    is_winner = db.Column(db.Boolean, default=False)
    
    votes = db.relationship('Vote', backref='submission', lazy=True)
    comments = db.relationship('Comment', backref='submission', lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    comment = db.Column(db.Text, nullable=False)  # Required explanation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Automated game management functions
def end_challenge_and_select_winner(challenge_id):
    """End a challenge and select the winner based on votes"""
    with app.app_context():
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return
        
        # Get all submissions for this challenge
        submissions = Submission.query.filter_by(challenge_id=challenge_id).all()
        
        if submissions:
            # Find the submission with the highest net votes (upvotes - downvotes)
            winner = max(submissions, key=lambda s: s.upvotes - s.downvotes)
            
            # Only declare a winner if they have positive net votes
            if (winner.upvotes - winner.downvotes) > 0:
                challenge.winner_submission_id = winner.id
                winner.is_winner = True
                # Give bonus points to the winner
                winner.author.points += 50
                winner.author.level = max(1, winner.author.points // 100 + 1)
        
        challenge.is_finished = True
        challenge.is_active = False
        db.session.commit()
        
        print(f"Challenge '{challenge.title}' ended. Winner: {challenge.winner_submission_id}")

def activate_next_challenge():
    """Activate the next challenge in the sequence"""
    with app.app_context():
        # Find the next challenge to activate
        next_challenge = Challenge.query.filter_by(is_active=False, is_finished=False).order_by(Challenge.challenge_order).first()
        
        if next_challenge:
            # Set start and end times (24-hour duration)
            next_challenge.start_date = datetime.utcnow()
            next_challenge.end_date = datetime.utcnow() + timedelta(hours=24)
            next_challenge.is_active = True
            db.session.commit()
            print(f"Activated challenge: '{next_challenge.title}'")
        else:
            # If no more challenges, reset all challenges and start over
            reset_all_challenges()

def reset_all_challenges():
    """Reset all challenges to start the game loop over"""
    with app.app_context():
        challenges = Challenge.query.all()
        for i, challenge in enumerate(challenges):
            challenge.is_active = False
            challenge.is_finished = False
            challenge.winner_submission_id = None
            challenge.challenge_order = i
        
        # Reset all submissions
        submissions = Submission.query.all()
        for submission in submissions:
            submission.is_winner = False
        
        db.session.commit()
        print("Reset all challenges for new game loop")
        
        # Find and activate the first challenge (don't call activate_next_challenge to avoid recursion)
        first_challenge = Challenge.query.filter_by(challenge_order=0).first()
        if first_challenge:
            first_challenge.start_date = datetime.utcnow()
            first_challenge.end_date = datetime.utcnow() + timedelta(hours=24)
            first_challenge.is_active = True
            db.session.commit()
            print(f"Activated first challenge: '{first_challenge.title}'")

def check_and_manage_challenges():
    """Main function to check for ended challenges and manage progression"""
    with app.app_context():
        # Check for challenges that have ended
        ended_challenges = Challenge.query.filter(
            Challenge.is_active == True,
            Challenge.end_date <= datetime.utcnow(),
            Challenge.is_finished == False
        ).all()
        
        for challenge in ended_challenges:
            end_challenge_and_select_winner(challenge.id)
        
        # Check if we need to activate a new challenge
        active_challenge = Challenge.query.filter_by(is_active=True).first()
        if not active_challenge:
            activate_next_challenge()

# Schedule the challenge management job to run every minute
scheduler.add_job(
    func=check_and_manage_challenges,
    trigger=IntervalTrigger(minutes=1),
    id='challenge_manager',
    name='Check and manage challenges',
    replace_existing=True
)

# Routes
@app.route('/')
def index():
    active_challenge = Challenge.query.filter_by(is_active=True).first()
    recent_submissions = Submission.query.order_by(Submission.created_at.desc()).limit(10).all()
    return render_template('index.html', active_challenge=active_challenge, submissions=recent_submissions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/challenges')
def challenges():
    page = request.args.get('page', 1, type=int)
    challenges = Challenge.query.order_by(Challenge.challenge_order).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('challenges.html', challenges=challenges)

@app.route('/challenge/<int:challenge_id>')
def challenge_detail(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    submissions = Submission.query.filter_by(challenge_id=challenge_id).order_by(
        (Submission.upvotes - Submission.downvotes).desc()).all()
    return render_template('challenge_detail.html', challenge=challenge, submissions=submissions)

@app.route('/submit_solution', methods=['GET', 'POST'])
@login_required
def submit_solution():
    active_challenge = Challenge.query.filter_by(is_active=True).first()
    if not active_challenge:
        flash('No active challenge at the moment. Check back soon!')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        constitutional_language = request.form['constitutional_language']
        reasoning = request.form['reasoning']
        
        submission = Submission(
            title=title,
            constitutional_language=constitutional_language,
            reasoning=reasoning,
            user_id=current_user.id,
            challenge_id=active_challenge.id
        )
        
        db.session.add(submission)
        current_user.submissions_count += 1
        current_user.points += 10  # Points for submitting
        current_user.level = max(1, current_user.points // 100 + 1)
        db.session.commit()
        
        flash('Your submission has been posted!')
        return redirect(url_for('challenge_detail', challenge_id=active_challenge.id))
    
    return render_template('submit_solution.html', challenge=active_challenge)

@app.route('/submission/<int:submission_id>')
def submission_detail(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    comments = Comment.query.filter_by(submission_id=submission_id, parent_id=None).order_by(Comment.created_at.desc()).all()
    return render_template('submission_detail.html', submission=submission, comments=comments)

@app.route('/vote/<int:submission_id>', methods=['POST'])
@login_required
def vote_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    vote_type = request.form['vote_type']
    comment = request.form['comment']
    
    if not comment.strip():
        flash('You must provide an explanation for your vote!')
        return redirect(url_for('submission_detail', submission_id=submission_id))
    
    # Check if user already voted
    existing_vote = Vote.query.filter_by(user_id=current_user.id, submission_id=submission_id).first()
    
    if existing_vote:
        flash('You have already voted on this submission')
        return redirect(url_for('submission_detail', submission_id=submission_id))
    
    vote = Vote(
        user_id=current_user.id,
        submission_id=submission_id,
        vote_type=vote_type,
        comment=comment
    )
    
    if vote_type == 'upvote':
        submission.upvotes += 1
        current_user.points += 2
    else:
        submission.downvotes += 1
        current_user.points += 1
    
    current_user.votes_given += 1
    current_user.level = max(1, current_user.points // 100 + 1)
    db.session.add(vote)
    db.session.commit()
    
    flash('Your vote has been recorded!')
    return redirect(url_for('submission_detail', submission_id=submission_id))

@app.route('/comment/<int:submission_id>', methods=['POST'])
@login_required
def add_comment(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    content = request.form['content']
    parent_id = request.form.get('parent_id', type=int)
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        submission_id=submission_id,
        parent_id=parent_id
    )
    
    db.session.add(comment)
    current_user.points += 1  # Points for commenting
    current_user.level = max(1, current_user.points // 100 + 1)
    db.session.commit()
    
    flash('Comment posted!')
    return redirect(url_for('submission_detail', submission_id=submission_id))

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    submissions = Submission.query.filter_by(user_id=user.id).order_by(Submission.created_at.desc()).limit(10).all()
    return render_template('profile.html', user=user, submissions=submissions)

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).limit(20).all()
    return render_template('leaderboard.html', users=users)

# Admin routes for creating challenges
@app.route('/admin/create_challenge', methods=['GET', 'POST'])
@login_required
def create_challenge():
    if current_user.username != 'admin':  # Simple admin check
        flash('Access denied')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        challenge = Challenge(
            title=request.form['title'],
            description=request.form['description'],
            constitutional_context=request.form['constitutional_context'],
            problem_statement=request.form['problem_statement'],
            relevant_amendments=request.form['relevant_amendments'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            challenge_order=Challenge.query.count()  # Add to end of sequence
        )
        db.session.add(challenge)
        db.session.commit()
        flash('Challenge created successfully!')
        return redirect(url_for('challenges'))
    
    return render_template('create_challenge.html')

@app.route('/admin/manage_game')
@login_required
def manage_game():
    if current_user.username != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    active_challenge = Challenge.query.filter_by(is_active=True).first()
    all_challenges = Challenge.query.order_by(Challenge.challenge_order).all()
    
    return render_template('manage_game.html', active_challenge=active_challenge, challenges=all_challenges)

@app.route('/admin/start_game', methods=['POST'])
@login_required
def start_game():
    if current_user.username != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))
    
    reset_all_challenges()
    flash('Game started! First challenge is now active.')
    return redirect(url_for('manage_game'))

@app.route('/submit_challenge', methods=['GET', 'POST'])
@login_required
def submit_challenge():
    if current_user.is_blocked:
        flash('Your account has been blocked. Contact an administrator.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        challenge = Challenge(
            title=request.form['title'],
            description=request.form['description'],
            constitutional_context=request.form['constitutional_context'],
            problem_statement=request.form['problem_statement'],
            relevant_amendments=request.form['relevant_amendments'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            is_approved=False,
            submitted_by_id=current_user.id
        )
        db.session.add(challenge)
        db.session.commit()
        flash('Your challenge has been submitted for admin approval!')
        return redirect(url_for('index'))
    
    return render_template('submit_challenge.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    pending_challenges = Challenge.query.filter_by(is_approved=False).all()
    blocked_users = User.query.filter_by(is_blocked=True).all()
    active_challenge = Challenge.query.filter_by(is_active=True).first()
    total_users = User.query.count()
    total_submissions = Submission.query.count()
    
    return render_template('admin_dashboard.html', 
                         pending_challenges=pending_challenges,
                         blocked_users=blocked_users,
                         active_challenge=active_challenge,
                         total_users=total_users,
                         total_submissions=total_submissions)

@app.route('/admin/approve_challenge/<int:challenge_id>', methods=['POST'])
@login_required
def approve_challenge(challenge_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    challenge = Challenge.query.get_or_404(challenge_id)
    challenge.is_approved = True
    db.session.commit()
    flash(f'Challenge "{challenge.title}" has been approved!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject_challenge/<int:challenge_id>', methods=['POST'])
@login_required
def reject_challenge(challenge_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    challenge = Challenge.query.get_or_404(challenge_id)
    db.session.delete(challenge)
    db.session.commit()
    flash(f'Challenge "{challenge.title}" has been rejected and deleted.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/block_user/<int:user_id>', methods=['POST'])
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    user.is_blocked = True
    db.session.commit()
    flash(f'User "{user.username}" has been blocked.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/unblock_user/<int:user_id>', methods=['POST'])
@login_required
def unblock_user(user_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    user.is_blocked = False
    db.session.commit()
    flash(f'User "{user.username}" has been unblocked.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/make_admin/<int:user_id>', methods=['POST'])
@login_required
def make_admin(user_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f'User "{user.username}" is now an admin.')
    return redirect(url_for('admin_dashboard'))

@app.route('/setup_admin', methods=['GET', 'POST'])
def setup_admin():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    
    if request.method == 'POST':
        # Check if admin exists
        if admin:
            # Update existing admin
            admin.email = request.form['email']
            admin.password_hash = generate_password_hash(request.form['password'])
            flash('Admin password updated successfully!')
        else:
            # Create new admin
            admin = User(
                username='admin',
                email=request.form['email'],
                password_hash=generate_password_hash(request.form['password']),
                is_admin=True
            )
            db.session.add(admin)
            flash('Admin user created successfully!')
        
        db.session.commit()
        return redirect(url_for('login'))
    
    # Check if admin exists for display
    admin_exists = admin is not None
    return render_template('setup_admin.html', admin_exists=admin_exists)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Production configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode) 