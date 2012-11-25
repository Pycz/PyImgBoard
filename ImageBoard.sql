DROP TABLE IF EXISTS "boards";
CREATE TABLE "boards" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "name" TEXT NOT NULL  DEFAULT "Random", "adr" TEXT NOT NULL  UNIQUE  DEFAULT "b", "treads_name" TEXT NOT NULL , "records_name" TEXT NOT NULL , "category_id" INTEGER NOT NULL );
INSERT INTO "boards" VALUES(1,'Random','b','B','B',1);
DROP TABLE IF EXISTS "categorys";
CREATE TABLE "categorys" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "name" TEXT NOT NULL  DEFAULT "Misc");
INSERT INTO "categorys" VALUES(1,'Misc');
DROP TABLE IF EXISTS "recordsB";
CREATE TABLE recordsB
        (
            "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , 
            "timestamp" DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP,
             "name" TEXT NOT NULL  DEFAULT "Anonymous",
             "email" TEXT DEFAULT "",
             "title" TEXT DEFAULT "",
             "post" TEXT NOT NULL  DEFAULT "", 
            "image" TEXT DEFAULT "", 
            "tread_id" INTEGER NOT NULL 
        );
INSERT INTO "recordsB" VALUES(1,'2012-11-25 01:34:02','Anonymous','','','','',1);
INSERT INTO "recordsB" VALUES(2,'2012-11-25 01:34:04','Anonymous','','','','',1);
DROP TABLE IF EXISTS "treadsB";
CREATE TABLE treadsB 
        (
            "id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , 
            "last_time" DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP
        );
