"""
Seed script — Populates the database with sample government schemes.
Run: python -m backend.seed
"""
from backend.database import SessionLocal, engine
from backend.models import Scheme, Base

# Create tables
Base.metadata.create_all(bind=engine)


def seed_data():
    db = SessionLocal()

    schemes = [
        Scheme(
            name="PM Awas Yojana (PMAY)",
            category="Housing",
            description="A flagship mission providing subsidized housing for the urban and rural poor in India.",
            benefits="Financial assistance for building or improving a house. Interest subsidy on home loans up to ₹2.67 lakh.",
            eligibility_criteria="Family income less than ₹18L (EWS, LIG, MIG). Must not own a pucca house in India.",
            application_process="Apply online through PMAY portal (pmaymis.gov.in) or via local municipal office.",
            documents_required="Aadhaar card, Income proof, Address proof, Bank details, Passport-size photos.",
            contact_info="Toll-free: 1800-11-3377",
            min_age=18, max_age=100, max_income=1800000,
            target_categories="SC,ST,OBC,General",
            website="https://pmaymis.gov.in/"
        ),
        Scheme(
            name="Ayushman Bharat (PM-JAY)",
            category="Health",
            description="The world's largest health insurance scheme providing coverage up to ₹5 lakh per family per year.",
            benefits="Cashless and paperless access to health services at empanelled hospitals. Coverage for pre and post-hospitalization.",
            eligibility_criteria="Identified based on SECC data for rural and urban areas. Covers bottom 40% of population.",
            application_process="Check eligibility at mera.pmjay.gov.in, CSCs, or empanelled hospitals.",
            documents_required="Aadhaar card, Ration card, Any government ID proof.",
            contact_info="National Helpline: 14555",
            min_age=0, max_age=100, max_income=500000,
            target_categories="SC,ST,OBC,General",
            website="https://pmjay.gov.in/"
        ),
        Scheme(
            name="Post Matric Scholarship",
            category="Education",
            description="Financial assistance for students belonging to SC/ST/OBC categories pursuing higher education.",
            benefits="Tuition fee waiver, monthly maintenance allowance, and book/stationery grants.",
            eligibility_criteria="Family income should not exceed ₹2.5 lakh per annum. Must belong to reserved category.",
            application_process="Apply through National Scholarship Portal (scholarships.gov.in).",
            documents_required="Caste certificate, Income certificate, Last year marksheet, Bank passbook, Aadhaar card.",
            contact_info="NSP Helpdesk: 0120-6619540",
            min_age=15, max_age=35, max_income=250000,
            target_categories="SC,ST,OBC",
            website="https://scholarships.gov.in/"
        ),
        Scheme(
            name="PM Kaushal Vikas Yojana (PMKVY)",
            category="Skill Development",
            description="Flagship scheme enabling large numbers of youth to take up industry-relevant skill training and certification.",
            benefits="Free skill training, industry-recognized certification, and assistance in job placement.",
            eligibility_criteria="Youth between 15-45 years. Unemployed or school/college dropouts eligible.",
            application_process="Register at a PMKVY training center or online at pmkvyofficial.org.",
            documents_required="Aadhaar card, Educational documents, Passport-size photos.",
            contact_info="Helpline: 088000-55555",
            min_age=15, max_age=45, max_income=0,
            target_categories="All",
            website="https://www.pmkvyofficial.org/"
        ),
        Scheme(
            name="MGNREGA",
            category="Employment",
            description="Mahatma Gandhi National Rural Employment Guarantee Act provides 100 days of guaranteed wage employment per year to rural households.",
            benefits="Guaranteed 100 days of employment. Minimum wage payment. Unemployment allowance if work not provided within 15 days.",
            eligibility_criteria="Adult members of rural households willing to do unskilled manual work.",
            application_process="Apply at your nearest Gram Panchayat office. Register for a job card.",
            documents_required="Aadhaar card, Address proof, Passport-size photos, Bank or Post Office account details.",
            contact_info="Helpline: 1800-345-22-44",
            min_age=18, max_age=65, max_income=0,
            target_categories="All",
            website="https://nrega.nic.in/"
        ),
        Scheme(
            name="PM Ujjwala Yojana",
            category="Welfare",
            description="Provides free LPG connections to women from Below Poverty Line (BPL) families to replace unclean cooking fuels.",
            benefits="Free LPG connection, first refill free, and EMR option for subsequent refills.",
            eligibility_criteria="Women belonging to BPL households. Income below ₹1 lakh per year.",
            application_process="Apply at nearest LPG distributor with BPL certificate.",
            documents_required="BPL card, Aadhaar card, Bank account passbook, Passport-size photo.",
            contact_info="Helpline: 1800-266-6696",
            min_age=18, max_age=100, max_income=100000,
            target_categories="All",
            website="https://www.pmuy.gov.in/"
        ),
    ]

    # Clear existing to avoid duplicates
    db.query(Scheme).delete()
    db.add_all(schemes)
    db.commit()
    db.close()
    print("[OK] Database seeded with 6 government schemes!")


if __name__ == "__main__":
    seed_data()
