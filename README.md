# InteractiveCareShareDocs

## Introduction 
InteractiveCareShareDocs API Project! This is document management system that users to efficiently manage and collaborate on various document formats. Users can upload, download, manage, and share documents of various formats (pdf, docx, txt, etc.).

### Requirements

- Python 3.8.0
- MySQL Connector 2.2.0
- MySQL 8.0
- Database Migration

## Documentation
[Google Drive Link](https://drive.google.com/file/d/1palqhTaE51DqOrduDhA6Z_wDkirys9gc/view?usp=sharing)

### Installation

A step-by-step guide on how to get the development environment running

**1. Clone the repository**

     git clone https://github.com/Sagorhowlader/InteractiveCareShareDocs.git

**2. Navigate to the project directory**

    cd InteractiveCareShareDocs

**3. Install the dependencies**

    pip install -r requirements.txt

**3. Database migration**

**import the `doc_management_db.sql` your database**

**4. Before running the code, you need to upload the `.env` `.evn.local` in the `InteractiveCareShareDocs` file and change the database credential for development edit `.env.local` file** 

    ENV_TYPE=local //set local for development enviroment
    SECRET_KEY=[SECRET KEY]
    DEBUG=True // set True for development eniroment
    DATABASE_NAME= [DATABASE NAME]
    DATABASE_USER= [DATABASE USER]
    DATABASE_PASSWORD=[DATABASE PASSWORD]
    DATABASE_HOST=[DATABASE HOST]


**5. Running the development server**   
    
    python manage.py runserver



### Key Feature
- User Registration
- Document Management
- Document Sharing
- File Download


