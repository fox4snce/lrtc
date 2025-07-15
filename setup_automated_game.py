#!/usr/bin/env python3
"""
Script to set up the automated constitutional game with sample challenges.
This will add challenges and start the automated game progression.
"""

from app import app, db, Challenge
from datetime import datetime, timedelta

def setup_automated_game():
    with app.app_context():
        # Clear existing challenges
        Challenge.query.delete()
        db.session.commit()
        
        # Sample challenges for automated game
        challenges_data = [
            {
                "title": "Electoral College Reform: Fixing the Winner-Takes-All System",
                "description": "The current Electoral College system allows a candidate to win all of a state's electoral votes even with a slim majority. This creates 'swing states' and can result in a president who lost the popular vote. How can we fix this?",
                "constitutional_context": "The Electoral College was established in Article II, Section 1 of the Constitution and modified by the 12th Amendment. Currently, 48 states use a winner-takes-all system where the candidate with the most votes in a state gets all of that state's electoral votes. Only Maine and Nebraska use a district-based system.",
                "problem_statement": "The winner-takes-all system creates several problems: 1) It makes most states irrelevant in presidential elections, 2) It can result in a president who lost the popular vote, 3) It encourages candidates to focus only on swing states, 4) It can lead to strategic voting rather than sincere voting. How can we reform this system to be more democratic and representative?",
                "relevant_amendments": "Article II, Section 1: 'Each State shall appoint, in such Manner as the Legislature thereof may direct, a Number of Electors...' and the 12th Amendment establishing the current Electoral College process."
            },
            {
                "title": "Campaign Finance Reform: Money in Politics",
                "description": "The Supreme Court's Citizens United decision opened the floodgates for unlimited corporate and union spending in elections. How can we regulate campaign finance while respecting free speech?",
                "constitutional_context": "The First Amendment protects freedom of speech, including political speech. The Supreme Court has ruled that spending money on political campaigns is a form of protected speech. However, unlimited spending can create corruption or the appearance of corruption, and can drown out the voices of ordinary citizens.",
                "problem_statement": "Current campaign finance laws allow unlimited spending by super PACs and dark money groups, while individual contribution limits remain low. This creates a system where wealthy interests have disproportionate influence over elections and policy. How can we balance free speech rights with the need to prevent corruption and ensure equal access to the political process?",
                "relevant_amendments": "First Amendment: 'Congress shall make no law... abridging the freedom of speech...' and the 14th Amendment's equal protection clause."
            },
            {
                "title": "Supreme Court Term Limits: Addressing Lifetime Appointments",
                "description": "Supreme Court justices serve for life, which can lead to strategic retirement timing and increasingly partisan nominations. How can we reform the system?",
                "constitutional_context": "Article III, Section 1 states that federal judges 'shall hold their Offices during good Behaviour,' which has been interpreted as lifetime appointments. This was designed to ensure judicial independence, but modern politics have created new challenges.",
                "problem_statement": "Lifetime appointments create several problems: 1) Justices may serve for 30+ years, making each nomination extremely high-stakes, 2) Strategic retirements can be timed for political advantage, 3) The confirmation process has become increasingly partisan, 4) Long tenures can lead to justices serving well past their prime. How can we maintain judicial independence while addressing these issues?",
                "relevant_amendments": "Article III, Section 1: 'The Judges, both of the supreme and inferior Courts, shall hold their Offices during good Behaviour...'"
            },
            {
                "title": "Presidential Impeachment: Clarifying the Process",
                "description": "The impeachment process is vague and has been used inconsistently throughout history. How can we make it clearer and more effective?",
                "constitutional_context": "Article II, Section 4 states that the President 'shall be removed from Office on Impeachment for, and Conviction of, Treason, Bribery, or other high Crimes and Misdemeanors.' However, 'high Crimes and Misdemeanors' is not clearly defined, leading to partisan interpretations.",
                "problem_statement": "The impeachment process suffers from several issues: 1) 'High Crimes and Misdemeanors' is not clearly defined, 2) The process is highly politicized, 3) There's no clear standard for what constitutes an impeachable offense, 4) The process can be used as a political weapon. How can we create a clearer, more objective impeachment process?",
                "relevant_amendments": "Article II, Section 4: 'The President, Vice President and all civil Officers of the United States, shall be removed from Office on Impeachment for, and Conviction of, Treason, Bribery, or other high Crimes and Misdemeanors.'"
            },
            {
                "title": "Voting Rights Protection: Preventing Disenfranchisement",
                "description": "Voter suppression and disenfranchisement remain significant problems. How can we strengthen voting rights protections?",
                "constitutional_context": "The 15th Amendment prohibits denying the right to vote based on race, the 19th Amendment extends voting rights to women, and the 26th Amendment sets the voting age at 18. However, various state laws and practices can still effectively disenfranchise voters.",
                "problem_statement": "Despite constitutional protections, voting rights face ongoing challenges: 1) Voter ID laws can disproportionately affect certain groups, 2) Gerrymandering can dilute voting power, 3) Polling place closures can create barriers, 4) Felon disenfranchisement laws vary by state. How can we strengthen constitutional protections for voting rights?",
                "relevant_amendments": "15th Amendment: 'The right of citizens of the United States to vote shall not be denied or abridged... on account of race, color, or previous condition of servitude.' 19th Amendment: Extends voting rights to women. 26th Amendment: Sets voting age at 18."
            }
        ]
        
        # Add challenges to database
        for i, challenge_data in enumerate(challenges_data):
            challenge = Challenge(
                title=challenge_data["title"],
                description=challenge_data["description"],
                constitutional_context=challenge_data["constitutional_context"],
                problem_statement=challenge_data["problem_statement"],
                relevant_amendments=challenge_data["relevant_amendments"],
                start_date=datetime.utcnow() + timedelta(hours=i*24),  # Stagger start times
                end_date=datetime.utcnow() + timedelta(hours=(i+1)*24),  # 24-hour duration
                is_active=False,
                is_finished=False,
                challenge_order=i
            )
            db.session.add(challenge)
        
        try:
            db.session.commit()
            print("✅ Successfully set up automated game with 5 challenges!")
            print("\nChallenges added:")
            for i, challenge_data in enumerate(challenges_data):
                print(f"{i+1}. {challenge_data['title']}")
            
            print("\n🎮 To start the automated game:")
            print("1. Login as admin (username: admin, password: admin123)")
            print("2. Go to http://localhost:5000/admin/manage_game")
            print("3. Click 'Start Game' to begin the automated progression")
            print("\n⏰ Each challenge will run for 24 hours, then automatically progress to the next one.")
            print("🏆 Winners will be automatically selected based on votes.")
            print("🔄 When all challenges are done, the game will loop back to the first challenge.")
            
        except Exception as e:
            print(f"❌ Error setting up game: {e}")
            db.session.rollback()

if __name__ == "__main__":
    setup_automated_game() 