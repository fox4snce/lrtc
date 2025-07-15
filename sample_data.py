from app import app, db, Challenge
from datetime import datetime, timedelta

def create_sample_challenges():
    with app.app_context():
        # Clear existing challenges
        Challenge.query.delete()
        
        # Sample challenges
        challenges = [
            {
                'title': 'The Dred Scott Decision: Slavery and Citizenship',
                'description': 'In 1857, the Supreme Court ruled that African Americans could not be citizens and that Congress could not ban slavery in territories. This decision helped precipitate the Civil War.',
                'constitutional_context': 'The Dred Scott case involved a slave who sued for his freedom after living in free territories. The Supreme Court, led by Chief Justice Roger Taney, ruled that:\n1. African Americans could not be citizens of the United States\n2. Congress had no power to ban slavery in territories\n3. The Missouri Compromise was unconstitutional\n\nThis decision was based on the Court\'s interpretation of the Constitution\'s original meaning and the Fifth Amendment\'s due process clause.',
                'problem_statement': 'The Supreme Court used constitutional interpretation to deny citizenship rights and expand slavery. The decision showed how constitutional language could be interpreted to support deeply unjust outcomes. How could the Constitution have been written differently to prevent such interpretations?',
                'relevant_amendments': 'Fifth Amendment: "No person shall be...deprived of life, liberty, or property, without due process of law..."\n\nArticle I, Section 8: Congress has power to "make all Laws which shall be necessary and proper..."\n\nArticle IV, Section 2: "The Citizens of each State shall be entitled to all Privileges and Immunities of Citizens in the several States."',
                'end_date': datetime.now() + timedelta(days=14)
            },
            {
                'title': 'Japanese Internment: Executive Power and Civil Liberties',
                'description': 'During WWII, Executive Order 9066 authorized the internment of over 120,000 Japanese Americans, most of whom were U.S. citizens.',
                'constitutional_context': 'In 1942, President Franklin Roosevelt issued Executive Order 9066, which authorized the military to exclude "any or all persons" from designated areas. This led to the forced relocation and internment of Japanese Americans.\n\nThe Supreme Court upheld this in Korematsu v. United States (1944), ruling that the need to protect against espionage outweighed individual rights. The Court deferred to the military\'s judgment about wartime necessity.',
                'problem_statement': 'The executive branch used wartime emergency powers to deprive citizens of their constitutional rights without due process. The Supreme Court deferred to military judgment rather than protecting civil liberties. How could the Constitution better balance national security with individual rights?',
                'relevant_amendments': 'Fifth Amendment: "No person shall be...deprived of life, liberty, or property, without due process of law..."\n\nFourteenth Amendment: "No State shall...deprive any person of life, liberty, or property, without due process of law..."\n\nArticle II, Section 2: The President is "Commander in Chief of the Army and Navy..."\n\nArticle I, Section 9: "The privilege of the Writ of Habeas Corpus shall not be suspended, unless when in Cases of Rebellion or Invasion the public Safety may require it."',
                'end_date': datetime.now() + timedelta(days=21)
            },
            {
                'title': 'Watergate Scandal: Executive Privilege and Congressional Oversight',
                'description': 'The Watergate scandal revealed how executive privilege could be used to obstruct congressional investigations and hide presidential misconduct.',
                'constitutional_context': 'During the Watergate investigation, President Nixon claimed executive privilege to withhold tapes and documents from Congress and the special prosecutor. The Supreme Court ruled in United States v. Nixon (1974) that executive privilege is not absolute and must yield to the need for evidence in criminal proceedings.\n\nThe case established that the President is not above the law, but left many questions about the scope of executive privilege unanswered.',
                'problem_statement': 'Executive privilege was used to obstruct legitimate congressional oversight and criminal investigations. The Constitution provides few clear limits on executive privilege, allowing presidents to potentially hide misconduct. How could the Constitution better define the boundaries between executive privilege and congressional oversight?',
                'relevant_amendments': 'Article I, Section 2: The House "shall have the sole Power of Impeachment."\n\nArticle I, Section 3: The Senate "shall have the sole Power to try all Impeachments."\n\nArticle II, Section 4: "The President...shall be removed from Office on Impeachment for, and Conviction of, Treason, Bribery, or other high Crimes and Misdemeanors."\n\nArticle II, Section 2: The President "shall have Power to grant Reprieves and Pardons for Offences against the United States..."',
                'end_date': datetime.now() + timedelta(days=10)
            },
            {
                'title': 'Post-9/11 Surveillance: Privacy Rights vs. National Security',
                'description': 'After 9/11, the government expanded surveillance programs, raising questions about the balance between security and privacy rights.',
                'constitutional_context': 'Following the 9/11 attacks, Congress passed the USA PATRIOT Act, which expanded government surveillance powers. The National Security Agency (NSA) implemented mass surveillance programs, including bulk collection of phone records and internet communications.\n\nThe Supreme Court has ruled on some aspects of surveillance, but many programs remain secret. The tension between security needs and Fourth Amendment privacy rights continues to be debated.',
                'problem_statement': 'Modern technology allows unprecedented government surveillance capabilities. The Fourth Amendment\'s protections against unreasonable searches were written for physical searches, not digital surveillance. How could the Constitution be updated to protect privacy in the digital age while allowing necessary security measures?',
                'relevant_amendments': 'Fourth Amendment: "The right of the people to be secure in their persons, houses, papers, and effects, against unreasonable searches and seizures, shall not be violated..."\n\nFirst Amendment: "Congress shall make no law...abridging the freedom of speech..."\n\nArticle I, Section 8: Congress has power to "provide for the common Defence..."\n\nArticle II, Section 2: The President is "Commander in Chief of the Army and Navy..."',
                'end_date': datetime.now() + timedelta(days=28)
            }
        ]
        
        # Create challenges
        for challenge_data in challenges:
            challenge = Challenge(**challenge_data)
            db.session.add(challenge)
        
        db.session.commit()
        print(f"Created {len(challenges)} sample challenges!")

if __name__ == '__main__':
    create_sample_challenges() 