The back-end codes for Our Webiste Project. We code this sql queries and making database with Fatih Alparslan Kaya. 
![Untitled (11)](https://github.com/Ogi-Z/ProjectBackend/assets/59333212/51540350-55b3-457d-96af-fef309a5a47f)

I design this Data Model Diagram for our project

For the database you can use this query for build the DB

CREATE DATABASE tempDB;

    -- User tablosunu oluşturma(

    CREATE TABLE IF NOT EXISTS Users (

        UserID SERIAL PRIMARY KEY,
    
        UserName VARCHAR(255),
    
        UserSurname VARCHAR(255),
    
        UserEmail VARCHAR(255) UNIQUE,
    
        UserPassword VARCHAR(255),
    
        UserCity VARCHAR(255),
    
        RoleID INTEGER,
    
        VerificationKey VARCHAR(100),
    
        IsVerified BOOLEAN DEFAULT FALSE
    );

    -- Blog tablosunu oluşturma

    CREATE TABLE Blog (

        BlogID SERIAL PRIMARY KEY,

        UserID INTEGER,
    
        BlogCategory VARCHAR(255),

 	BlogTitle VARCHAR(255),
    
        BlogText TEXT,

        BlogImage BYTEA,

 	 Likes INTEGER,

  	 Dislikes INTEGER, 	

        Approved BOOLEAN DEFAULT FALSE,
    
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );

    -- SoftwareUsability tablosunu oluşturma

    CREATE TABLE SoftwareUsability (

        SoftwareUsabilityID SERIAL PRIMARY KEY,
    
        UserID INTEGER,

        SoftwareUsabilitySoftware VARCHAR(255),

        SoftwareUsabilityTopicName VARCHAR(255),

        SoftwareUsabilityText TEXT,

        SoftwareUsabilityImage BYTEA,

 	 Likes INTEGER,

  	 Dislikes INTEGER,

	 Approved BOOLEAN DEFAULT FALSE,
 
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );

    -- SoftwareUsability Owner tablosunu oluşturma
    CREATE TABLE IF NOT EXISTS SoftwareOwner (

    	OwnerID SERIAL PRIMARY KEY,

    	OwnerName VARCHAR(255),
    
    	OwnerSurname VARCHAR(255),
    
    	OwnerEmail VARCHAR(255) UNIQUE,
    
    	OwnerPassword VARCHAR(255),

    	OwnersSoftware VARCHAR(255),
    
    	OwnerCity VARCHAR(255),
    
    	RoleID INTEGER,
    
    	VerificationKey VARCHAR(100),
    
    	IsVerified BOOLEAN DEFAULT FALSE

    );
    
    -- SoftwareUsabilityComments Tablosunu oluşturma
    CREATE TABLE softwareusabilitycomments (
    
    	commentid SERIAL PRIMARY KEY,
    
    	userid INTEGER NOT NULL,
    
    	softwareusabilityid INTEGER NOT NULL,
    
    	commenttext TEXT NOT NULL,
    
    	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


);

If you wanna test the code you can use Postman for POST and GET request for functions that declared in our project proposal

For example when we try add_user function
-SELECT POST FUNCTION IN POSTMAN 

-TYPE THE LINK "http://127.0.0.1:5000/add_user"

-SELECT BODY

-SELECT raw

-PASTE THIS
(

    {
        "username": "Ogi",
        "usersurname": "Ogi",
        "useremail": "ogi@example.com",
        "userpassword": "123",
        "usercity": "Ankara",
        "role_id": 0
    }

);
