CREATE TABLE students(
student_id INT PRIMARY KEY,
name VARCHAR(100),
department VARCHAR(50),
parent_phone VARCHAR(20),
mentor_id INT
);

CREATE TABLE attendance(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
total_classes INT,
attended_classes INT,
percentage FLOAT
);

CREATE TABLE marks(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
subject VARCHAR(100),
marks INT,
exam_type VARCHAR(20)
);

CREATE TABLE academic_summary(
student_id INT,
sgpa FLOAT,
cgpa FLOAT,
backlogs INT
);

CREATE TABLE fees(
id INT AUTO_INCREMENT PRIMARY KEY,
student_id INT,
fee_type VARCHAR(50),
amount INT,
due_date DATE,
status VARCHAR(20)
);