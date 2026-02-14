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
        # EXISTING SCHEMES (6)
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

        # NEW SCHEMES - EDUCATION (5)
        Scheme(
            name="Begum Hazrat Mahal Girls Scholarship",
            category="Education",
            description="Scholarship for minority community girls pursuing higher education from class 9 to post-graduation.",
            benefits="₹5,000 to ₹12,000 per year based on class level. Helps cover tuition and educational expenses.",
            eligibility_criteria="Girls from minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi). Family income below ₹2 lakh.",
            application_process="Apply online through National Scholarship Portal.",
            documents_required="Minority community certificate, Income certificate, Previous year marksheet, Bank details, Aadhaar.",
            contact_info="Maulana Azad Education Foundation: 011-23357271",
            min_age=12, max_age=30, max_income=200000,
            target_categories="Minorities",
            website="https://maef.nic.in/"
        ),
        Scheme(
            name="Mid-Day Meal Scheme",
            category="Education",
            description="Provides free lunch to students in government and government-aided schools to improve nutrition and school enrollment.",
            benefits="Nutritious cooked meal during school days. Improves health, attention span, and attendance.",
            eligibility_criteria="All students studying in Classes I to VIII in government and aided schools.",
            application_process="Automatic enrollment upon school admission. No separate application required.",
            documents_required="School admission proof.",
            contact_info="State Education Department",
            min_age=5, max_age=15, max_income=0,
            target_categories="All",
            website="https://mdm.nic.in/"
        ),
        Scheme(
            name="National Means-cum-Merit Scholarship",
            category="Education",
            description="Financial assistance to meritorious students from economically weaker sections to prevent dropouts at Class VIII.",
            benefits="₹12,000 per annum (₹1,000 per month) for classes 9 to 12.",
            eligibility_criteria="Scored minimum 55% in Class VII. Family income below ₹3.5 lakh per annum.",
            application_process="Apply through NSP portal or respective state portals.",
            documents_required="Class VII marksheet, Income certificate, Bank passbook, Aadhaar, School certificate.",
            contact_info="NSP Helpline: 0120-6619540",
            min_age=13, max_age=18, max_income=350000,
            target_categories="All",
            website="https://scholarships.gov.in/"
        ),
        Scheme(
            name="Beti Bachao Beti Padhao",
            category="Education",
            description="Campaign to address declining child sex ratio and promote education for girl children.",
            benefits="Awareness campaigns, improved access to quality education, and prevention of gender-based discrimination.",
            eligibility_criteria="All girl children, particularly in districts with low child sex ratio.",
            application_process="Benefits accessed through associated schemes like Sukanya Samriddhi Yojana.",
            documents_required="Birth certificate, Aadhaar, Bank account.",
            contact_info="Women & Child Development Ministry: 011-23388612",
            min_age=0, max_age=21, max_income=0,
            target_categories="Girl Child",
            website="https://wcd.nic.in/"
        ),
        Scheme(
            name="Samagra Shiksha Abhiyan",
            category="Education",
            description="Integrated scheme for school education from pre-school to senior secondary level.",
            benefits="Free textbooks, uniforms, scholarships for girls and SC/ST students, infrastructure improvement.",
            eligibility_criteria="Students in government and aided schools from pre-primary to Class XII.",
            application_process="Via school or state education department.",
            documents_required="School enrollment certificate.",
            contact_info="State Education Department",
            min_age=3, max_age=18, max_income=0,
            target_categories="All",
            website="https://samagra.education.gov.in/"
        ),

        # NEW SCHEMES - HEALTH (3)
        Scheme(
            name="Rashtriya Swasthya Bima Yojana (RSBY)",
            category="Health",
            description="Health insurance scheme for BPL families providing cashless insurance for hospitalization.",
            benefits="Coverage of ₹30,000 per family per year for most diseases requiring hospitalization.",
            eligibility_criteria="BPL families as per SECC data.",
            application_process="Enroll at designated enrollment stations with BPL card.",
            documents_required="BPL card, Aadhaar, Ration card, Family photo.",
            contact_info="State Health Department",
            min_age=0, max_age=100, max_income=120000,
            target_categories="BPL",
            website="https://www.rsby.gov.in/"
        ),
        Scheme(
            name="Janani Suraksha Yojana (JSY)",
            category="Health",
            description="Safe motherhood intervention under NHM promoting institutional delivery among poor pregnant women.",
            benefits="Cash assistance for delivery in institutions. ₹1,400 for rural areas, ₹1,000 for urban areas.",
            eligibility_criteria="Pregnant women belonging to BPL families. All pregnant women in LPS (Low Performing States).",
            application_process="Register at nearest Anganwadi or health center during pregnancy.",
            documents_required="BPL card, Pregnancy registration card, Bank account, Aadhaar.",
            contact_info="National Health Mission: 011-23063286",
            min_age=18, max_age=45, max_income=150000,
            target_categories="Women,BPL",
            website="https://nhm.gov.in/"
        ),
        Scheme(
            name="Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
            category="Health",
            description="Accidental insurance scheme offering coverage of ₹2 lakh at a premium of ₹12 per year.",
            benefits="₹2 lakh on accidental death or permanent total disability. ₹1 lakh for partial permanent disability.",
            eligibility_criteria="Age 18-70 years. Must have savings bank account.",
            application_process="Enroll through bank or online banking portal with auto-debit consent.",
            documents_required="Aadhaar, Bank account, Consent form.",
            contact_info="Bank Branch or Financial Services Department",
            min_age=18, max_age=70, max_income=0,
            target_categories="All",
            website="https://www.jansuraksha.gov.in/"
        ),

        # NEW SCHEMES - AGRICULTURE (4)
        Scheme(
            name="PM-KISAN (Kisan Samman Nidhi)",
            category="Agriculture",
            description="Income support to all landholding farmers providing ₹6,000 per year in three equal installments.",
            benefits="Direct cash transfer of ₹2,000 every four months into bank account.",
            eligibility_criteria="All landholding farmer families. Land ownership record required.",
            application_process="Register online at pmkisan.gov.in or through Common Service Centers.",
            documents_required="Aadhaar, Bank account passbook, Land ownership documents.",
            contact_info="PM-KISAN Helpline: 155261 / 011-24300606",
            min_age=18, max_age=100, max_income=0,
            target_categories="Farmers",
            website="https://pmkisan.gov.in/"
        ),
        Scheme(
            name="Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            category="Agriculture",
            description="Crop insurance scheme protecting farmers against crop loss due to natural calamities, pests, and diseases.",
            benefits="Comprehensive risk coverage from pre-sowing to post-harvest. Low premium rates (1.5-2% of sum insured).",
            eligibility_criteria="All farmers including sharecroppers and tenant farmers growing notified crops.",
            application_process="Apply through banks, CSCs, or agriculture department within cutoff dates.",
            documents_required="Land records, Bank account, Aadhaar, Sowing certificate.",
            contact_info="Toll-free: 1800-180-1551",
            min_age=18, max_age=100, max_income=0,
            target_categories="Farmers",
            website="https://pmfby.gov.in/"
        ),
        Scheme(
            name="Kisan Credit Card (KCC)",
            category="Agriculture",
            description="Credit facility for farmers to meet cultivation expenses and purchase agricultural inputs.",
            benefits="Easy credit access at low interest (7% with 3% subvention). Flexible repayment. Insurance coverage.",
            eligibility_criteria="Farmers owning cultivable land. Tenant farmers, oral lessees, and sharecroppers also eligible.",
            application_process="Apply at banks with land records and ID proof.",
            documents_required="Land ownership documents, Aadhaar, PAN, Passport-size photos.",
            contact_info="Respective Bank Branch",
            min_age=18, max_age=75, max_income=0,
            target_categories="Farmers",
            website="https://www.kcc.gov.in/"
        ),
        Scheme(
            name="Soil Health Card Scheme",
            category="Agriculture",
            description="Provides soil health cards to farmers with nutrient status and fertilizer recommendations.",
            benefits="Free soil testing. Customized fertilizer recommendations. Improves soil health and reduces input costs.",
            eligibility_criteria="All farmers in India.",
            application_process="Contact local agriculture office or Krishi Vigyan Kendra for soil sample collection.",
            documents_required="Aadhaar, Land records.",
            contact_info="Agriculture Department",
            min_age=18, max_age=100, max_income=0,
            target_categories="Farmers",
            website="https://soilhealth.dac.gov.in/"
        ),

        # NEW SCHEMES - EMPLOYMENT (3)
        Scheme(
            name="Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)",
            category="Employment",
            description="Placement-linked skill development scheme for rural poor youth.",
            benefits="Free residential skill training, placement assistance, post-placement support.",
            eligibility_criteria="Rural youth aged 15-35 years from poor families. Priority to SC/ST/minorities/women.",
            application_process="Contact Project Implementing Agencies (PIAs) or visit DDU-GKY centers.",
            documents_required="Aadhaar, Age proof, Income certificate, Caste certificate (if applicable).",
            contact_info="DDU-GKY Helpline: 1800-180-1011",
            min_age=15, max_age=35, max_income=100000,
            target_categories="SC,ST,OBC,Minorities,Women",
            website="https://ddugky.gov.in/"
        ),
        Scheme(
            name="Pradhan Mantri Rojgar Protsahan Yojana (PMRPY)",
            category="Employment",
            description="Incentivizes employers to generate new employment by paying employers' EPS contribution.",
            benefits="Government pays 12% employer contribution to EPF for new employees earning up to ₹15,000/month.",
            eligibility_criteria="New employees registered with EPFO earning up to ₹15,000 per month.",
            application_process="Employers apply online through EPFO portal.",
            documents_required="Aadhaar, UAN, Bank details.",
            contact_info="EPFO: 1800-118-005",
            min_age=18, max_age=60, max_income=0,
            target_categories="All",
            website="https://www.epfindia.gov.in/"
        ),
        Scheme(
            name="National Career Service (NCS)",
            category="Employment",
            description="One-stop solution for employment and career-related services including job matching, career counseling, and skill development.",
            benefits="Free job portal, career counseling, vocational guidance, skill gap identification.",
            eligibility_criteria="All job seekers and employers across India.",
            application_process="Register on NCS portal with email and mobile number.",
            documents_required="Educational certificates, Resume, Aadhaar.",
            contact_info="NCS Helpline: 1800-425-1514",
            min_age=15, max_age=65, max_income=0,
            target_categories="All",
            website="https://www.ncs.gov.in/"
        ),

        # NEW SCHEMES - WOMEN & CHILD (4)
        Scheme(
            name="Sukanya Samriddhi Yojana",
            category="Women & Child",
            description="Small deposit savings scheme for girl child offering high interest rate and tax benefits.",
            benefits="8.2% interest rate (tax-free). Maturity amount can be used for education/marriage of girl child.",
            eligibility_criteria="Girl child below 10 years of age. One account per girl, maximum two girls per family.",
            application_process="Open account at post office or authorized banks with birth certificate.",
            documents_required="Girl child's birth certificate, Guardian's ID and address proof, Aadhaar, Photos.",
            contact_info="Post Office / Bank Branch",
            min_age=0, max_age=10, max_income=0,
            target_categories="Girl Child",
            website="https://www.nsiindia.gov.in/"
        ),
        Scheme(
            name="Pradhan Mantri Matru Vandana Yojana (PMMVY)",
            category="Women & Child",
            description="Maternity benefit scheme providing cash incentive for first living child to pregnant and lactating mothers.",
            benefits="₹5,000 in three installments for wage loss during delivery and childcare.",
            eligibility_criteria="Pregnant women and lactating mothers for first living child. Registered with Anganwadi.",
            application_process="Register at Anganwadi center during pregnancy.",
            documents_required="Pregnancy registration card, Aadhaar, Bank account, MCP card.",
            contact_info="Women & Child Development: 011-23382393",
            min_age=18, max_age=45, max_income=0,
            target_categories="Women",
            website="https://pmmvy.wcd.gov.in/"
        ),
        Scheme(
            name="Mahila Shakti Kendra",
            category="Women & Child",
            description="Provides community support for rural women through engagement at village and block levels.",
            benefits="Skill development, employment, digital literacy, health and nutrition awareness.",
            eligibility_criteria="Rural women across India.",
            application_process="Contact district or block level resource centers.",
            documents_required="Aadhaar, Address proof.",
            contact_info="Women & Child Development Ministry",
            min_age=18, max_age=60, max_income=0,
            target_categories="Women",
            website="https://wcd.nic.in/"
        ),
        Scheme(
            name="One Stop Centre Scheme",
            category="Women & Child",
            description="Support services for women affected by violence including shelter, medical aid, and legal assistance.",
            benefits="24x7 support, emergency response, medical aid, legal counseling, psycho-social counseling.",
            eligibility_criteria="Women affected by violence, both in private and public spaces, regardless of age or caste.",
            application_process="Walk-in to One Stop Centre or call 181 Women Helpline.",
            documents_required="No documents required for emergency assistance.",
            contact_info="Women Helpline: 181",
            min_age=0, max_age=100, max_income=0,
            target_categories="Women",
            website="https://wcd.nic.in/"
        ),

        # NEW SCHEMES - SENIOR CITIZENS (3)
        Scheme(
            name="Indira Gandhi National Old Age Pension Scheme (IGNOAPS)",
            category="Senior Citizens",
            description="Monthly pension for senior citizens living below poverty line.",
            benefits="₹200-500 per month based on age (60-79 years: ₹200, 80+: ₹500). States may provide additional amount.",
            eligibility_criteria="BPL citizens aged 60 years and above.",
            application_process="Apply through local Panchayat or Municipal office.",
            documents_required="Age proof, BPL card, Aadhaar, Bank account, Income certificate.",
            contact_info="District Social Welfare Office",
            min_age=60, max_age=120, max_income=0,
            target_categories="BPL,Senior Citizens",
            website="https://nsap.nic.in/"
        ),
        Scheme(
            name="Pradhan Mantri Vaya Vandana Yojana (PMVVY)",
            category="Senior Citizens",
            description="Pension scheme for senior citizens providing assured return of 7.75% per annum.",
            benefits="Assured pension of ₹1,000 to ₹10,000 per month for 10 years. Loan facility available.",
            eligibility_criteria="Senior citizens aged 60 years and above.",
            application_process="Purchase from LIC through online or offline mode.",
            documents_required="Age proof, PAN card, Aadhaar, Bank details, Address proof.",
            contact_info="LIC: 022-68276827",
            min_age=60, max_age=100, max_income=0,
            target_categories="Senior Citizens",
            website="https://www.licindia.in/"
        ),
        Scheme(
            name="Senior Citizen Savings Scheme (SCSS)",
            category="Senior Citizens",
            description="Savings scheme offering regular income with highest safety for senior citizens.",
            benefits="8.2% interest rate. Quarterly interest payout. Tax deduction under Section 80C.",
            eligibility_criteria="Individuals aged 60 years and above. Retired civilians/defense personnel (55-60 years).",
            application_process="Open account at post office or authorized banks.",
            documents_required="Age proof, ID proof, Address proof, Recent photograph.",
            contact_info="Post Office / Bank Branch",
            min_age=55, max_age=100, max_income=0,
            target_categories="Senior Citizens",
            website="https://www.indiapost.gov.in/"
        ),

        # NEW SCHEMES - BUSINESS/MSME (4)
        Scheme(
            name="MUDRA Loan Scheme",
            category="Business",
            description="Provides loans to micro and small business enterprises through three categories: Shishu, Kishore, Tarun.",
            benefits="Loans up to ₹10 lakh. Shishu: up to ₹50K, Kishore: ₹50K-₹5L, Tarun: ₹5L-₹10L. No collateral required.",
            eligibility_criteria="Non-corporate, non-farm small/micro enterprises. Existing or new businesses.",
            application_process="Apply through banks, NBFCs, or MFIs with business plan.",
            documents_required="Business plan, Aadhaar, PAN, Address proof, Bank statements, Business registration.",
            contact_info="MUDRA Helpline: 1800-180-MUDRA",
            min_age=18, max_age=70, max_income=0,
            target_categories="All",
            website="https://www.mudra.org.in/"
        ),
        Scheme(
            name="Startup India",
            category="Business",
            description="Initiative to build strong ecosystem for nurturing innovation and startups providing tax benefits and funding support.",
            benefits="Tax exemption for 3 years, self-certification, IPR fast-tracking, funding support, mentorship.",
            eligibility_criteria="Entity incorporated as private limited or LLP. Turnover <₹100 crore. Working on innovation/tech.",
            application_process="Register on Startup India portal with incorporation certificate.",
            documents_required="Incorporation certificate, Description of business, Pitch deck, Funding details.",
            contact_info="Startup India: 1800-115-565",
            min_age=18, max_age=100, max_income=0,
            target_categories="All",
            website="https://www.startupindia.gov.in/"
        ),
        Scheme(
            name="Stand-Up India",
            category="Business",
            description="Facilitates bank loans between ₹10 lakh to ₹1 crore for SC/ST and women entrepreneurs.",
            benefits="Composite loan for greenfield manufacturing/services/trading. Margin money up to 25%. Credit guarantee.",
            eligibility_criteria="SC/ST and/or women entrepreneurs above 18 years. For greenfield enterprise in manufacturing/services/trading.",
            application_process="Apply through bank branches with business plan.",
            documents_required="Business plan, Project report, Aadhaar, PAN, Caste certificate (if applicable), Address proof.",
            contact_info="Stand-Up India Portal: 1800-180-1111",
            min_age=18, max_age=70, max_income=0,
            target_categories="SC,ST,Women",
            website="https://www.standupmitra.in/"
        ),
        Scheme(
            name="Credit Guarantee Scheme (CGS)",
            category="Business",
            description="Provides collateral-free credit to micro and small enterprises through credit guarantee coverage.",
            benefits="Credit guarantee coverage up to 85% of sanctioned amount. Maximum guarantee of ₹5 crore.",
            eligibility_criteria="Micro and small enterprises. New as well as existing units.",
            application_process="Through lending institutions (banks/NBFCs) covered under CGS.",
            documents_required="Business registration, Project report, Bank statements, Aadhaar, PAN.",
            contact_info="CGTMSE: 022-2300 3193",
            min_age=18, max_age=70, max_income=0,
            target_categories="All",
            website="https://www.cgtmse.in/"
        ),

        # NEW SCHEMES - HOUSING (2)
        Scheme(
            name="Pradhan Mantri Gramin Awaas Yojana",
            category="Housing",
            description="Provides financial assistance to rural poor for construction of pucca houses with basic amenities.",
            benefits="₹1.2 lakh in plains, ₹1.3 lakh in hilly/difficult areas. Includes toilet, LPG connection, electricity.",
            eligibility_criteria="Houseless or living in kutcha houses. BPL families in rural areas.",
            application_process="Register through Gram Panchayat or online portal.",
            documents_required="Aadhaar, Job card/BPL card, Bank account, Land ownership proof.",
            contact_info="Rural Development Ministry: 1800-11-6446",
            min_age=18, max_age=100, max_income=0,
            target_categories="Rural,BPL",
            website="https://pmayg.nic.in/"
        ),
        Scheme(
            name="RAY - Rajiv Awas Yojana",
            category="Housing",
            description="Aims to make India slum-free by providing affordable housing and basic civic infrastructure.",
            benefits="In-situ development of slums, affordable housing, property rights, basic amenities.",
            eligibility_criteria="Slum dwellers in cities. Identified slum areas for redevelopment.",
            application_process="Through state/UT governments and urban local bodies.",
            documents_required="Proof of slum residence, Aadhaar, Income certificate.",
            contact_info="Ministry of Housing & Urban Affairs",
            min_age=18, max_age=100, max_income=300000,
            target_categories="Urban Poor,Slum Dwellers",
            website="https://mohua.gov.in/"
        ),
    ]

    # Clear existing to avoid duplicates
    db.query(Scheme).delete()
    db.add_all(schemes)
    db.commit()
    db.close()
    print(f"[OK] Database seeded with {len(schemes)} government schemes!")


if __name__ == "__main__":
    seed_data()
