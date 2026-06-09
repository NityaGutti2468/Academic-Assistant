CREATE TABLE students(
student_id INT PRIMARY KEY,
roll_no VARCHAR(20),
name VARCHAR(100),
department VARCHAR(50),
program VARCHAR(50),
semester INT,
section VARCHAR(10),
email VARCHAR(100),
phone VARCHAR(20),
parent_name VARCHAR(100),
parent_phone VARCHAR(20),
address VARCHAR(255),
admission_year INT,
mentor_id INT,
status VARCHAR(20)
);

CREATE TABLE attendance(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
total_classes INT,
attended_classes INT,
percentage FLOAT
);

CREATE TABLE courses(
course_code VARCHAR(20) PRIMARY KEY,
course_name VARCHAR(100),
department VARCHAR(50),
semester INT,
credits FLOAT,
faculty VARCHAR(100)
);

CREATE TABLE marks(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
subject VARCHAR(100),
marks INT,
credits FLOAT,
exam_type VARCHAR(20),
semester INT
);

CREATE TABLE semester_results(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
semester_no INT,
semester_label VARCHAR(50),
exam_month VARCHAR(20),
passed_count INT,
failed_count INT,
overall_result VARCHAR(20),
sgpa FLOAT,
percentage FLOAT,
total_grade_points FLOAT,
total_credits FLOAT
);

CREATE TABLE academic_summary(
student_id INT,
sgpa FLOAT,
cgpa FLOAT,
backlogs INT,
credits_earned INT,
academic_standing VARCHAR(50)
);

CREATE TABLE fees(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
fee_type VARCHAR(50),
amount INT,
due_date DATE,
status VARCHAR(20),
semester INT
);

CREATE TABLE assignments(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
course_code VARCHAR(20),
title VARCHAR(100),
score INT,
max_score INT,
status VARCHAR(30)
);

CREATE TABLE student_notes(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
mentor_id INT,
note_type VARCHAR(50),
note TEXT,
created_at DATE
);

CREATE TABLE scholarships(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
name VARCHAR(100),
amount INT,
status VARCHAR(30),
renewal_due DATE
);

CREATE TABLE fee_payments(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
receipt_no VARCHAR(50),
fee_type VARCHAR(50),
amount INT,
paid_on DATE,
mode VARCHAR(30)
);

CREATE TABLE alert_logs(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
type VARCHAR(50),
severity VARCHAR(20),
message TEXT,
created_at DATE,
status VARCHAR(20)
);
