#!/usr/bin/env python3
"""
Script to add sample constitutional challenges to the database.
Run this after setting up the main application to populate it with example challenges.
"""

from app import app, db, Challenge
from datetime import datetime, timedelta

def add_sample_challenges():
    with app.app_context():
        # Sample Challenge 1: Electoral College Reform
        challenge1 = Challenge(
            title="Electoral College Reform: Fixing the Winner-Takes-All System",
            description="The current Electoral College system allows a candidate to win all of a state's electoral votes even with a slim majority. This creates 'swing states' and can result in a president who lost the popular vote. How can we fix this?",
            constitutional_context="The Electoral College was established in Article II, Section 1 of the Constitution and modified by the 12th Amendment. Currently, 48 states use a winner-takes-all system where the candidate with the most votes in a state gets all of that state's electoral votes. Only Maine and Nebraska use a district-based system.",
            problem_statement="The winner-takes-all system creates several problems: 1) It makes most states irrelevant in presidential elections, 2) It can result in a president who lost the popular vote, 3) It encourages candidates to focus only on swing states, 4) It can lead to strategic voting rather than sincere voting. How can we reform this system to be more democratic and representative?",
            relevant_amendments="Article II, Section 1: 'Each State shall appoint, in such Manner as the Legislature thereof may direct, a Number of Electors...' and the 12th Amendment establishing the current Electoral College process.",
            end_date=datetime.now() + timedelta(days=14),
            is_active=True
        )
        
        # Sample Challenge 2: Campaign Finance Reform
        challenge2 = Challenge(
            title="Campaign Finance Reform: Money in Politics",
            description="The Supreme Court's Citizens United decision opened the floodgates for unlimited corporate and union spending in elections. How can we regulate campaign finance while respecting free speech?",
            constitutional_context="The First Amendment protects freedom of speech, including political speech. The Supreme Court has ruled that spending money on political campaigns is a form of protected speech. However, unlimited spending can create corruption or the appearance of corruption, and can drown out the voices of ordinary citizens.",
            problem_statement="Current campaign finance laws allow unlimited spending by super PACs and dark money groups, while individual contribution limits remain low. This creates a system where wealthy interests have disproportionate influence over elections and policy. How can we balance free speech rights with the need to prevent corruption and ensure equal access to the political process?",
            relevant_amendments="First Amendment: 'Congress shall make no law... abridging the freedom of speech...' and the 14th Amendment's equal protection clause.",
            end_date=datetime.now() + timedelta(days=21),
            is_active=True
        )
        
        # Sample Challenge 3: Supreme Court Term Limits
        challenge3 = Challenge(
            title="Supreme Court Term Limits: Addressing Lifetime Appointments",
            description="Supreme Court justices serve for life, which can lead to strategic retirement timing and increasingly partisan nominations. How can we reform the system?",
            constitutional_context="Article III, Section 1 states that federal judges 'shall hold their Offices during good Behaviour,' which has been interpreted as lifetime appointments. This was designed to ensure judicial independence, but modern politics have created new challenges.",
            problem_statement="Lifetime appointments create several problems: 1) Justices may serve for 30+ years, making each nomination extremely high-stakes, 2) Strategic retirements can be timed for political advantage, 3) The confirmation process has become increasingly partisan, 4) Long tenures can lead to justices serving well past their prime. How can we maintain judicial independence while addressing these issues?",
            relevant_amendments="Article III, Section 1: 'The Judges, both of the supreme and inferior Courts, shall hold their Offices during good Behaviour...'",
            end_date=datetime.now() + timedelta(days=30),
            is_active=True
        )
        
        # Add challenges to database
        db.session.add(challenge1)
        db.session.add(challenge2)
        db.session.add(challenge3)
        
        try:
            db.session.commit()
            print("✅ Successfully added 3 sample challenges!")
            print("\nSample challenges added:")
            print("1. Electoral College Reform")
            print("2. Campaign Finance Reform") 
            print("3. Supreme Court Term Limits")
            print("\nYou can now run the application and see these challenges at http://localhost:5000/challenges")
        except Exception as e:
            print(f"❌ Error adding challenges: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_sample_challenges() 