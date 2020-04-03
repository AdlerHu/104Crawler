CREATE TABLE job(
	`job_name`		VARCHAR(70),
	`company_name`	VARCHAR(70),
	`salary`			VARCHAR(20),
    `job_description`	VARCHAR(700),
	`company_page`	VARCHAR(50),
	`address`			VARCHAR(50),
	`link`			VARCHAR(70),
	`MS_SQL`			VARCHAR(1) DEFAULT '0',
	`MySQL`			VARCHAR(1) DEFAULT '0',
	`JavaScript`		VARCHAR(1) DEFAULT '0',
	`C_sharp`			VARCHAR(1) DEFAULT '0',
	`HTML`			VARCHAR(1) DEFAULT '0',
	`ASPNET`			VARCHAR(1) DEFAULT '0',
	`Java`			VARCHAR(1) DEFAULT '0',
	`jQuery`			VARCHAR(1) DEFAULT '0',
	`Oracle`			VARCHAR(1) DEFAULT '0',
	`Linux`			VARCHAR(1) DEFAULT '0',
    
	PRIMARY KEY (job_name, company_name)
);

drop table job;

INSERT INTO job	(job_name, company_name, salary, job_description, company_page, address, link)
VALUES			('DB工程師', 'Adler Ltd.', '100000', 'Awesome', 'https://github.com/AdlerHu', '新竹市東大路1號', 'https://google.com'); 

delete  from job where company_name = 'Adler Ltd.'; 

UPDATE mysql.user SET Grant_priv='Y', Super_priv='Y' WHERE User='root';
FLUSH PRIVILEGES;

alter user 'root'@'localhost' identified with mysql_native_password by 'root';


# Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY -- column.  To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.

