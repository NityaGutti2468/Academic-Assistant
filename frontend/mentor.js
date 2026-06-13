const API_BASE_URL = "";

const mentorForm = document.getElementById("mentor-form");
const mentorInput = document.getElementById("mentor-id");
const backendState = document.getElementById("backend-state");
const studentsCount = document.getElementById("students-count");
const alertsCount = document.getElementById("alerts-count");
const avgCgpa = document.getElementById("avg-cgpa");
const alertsList = document.getElementById("alerts-list");
const studentsTable = document.getElementById("students-table");

function setBackendState(text, isConnected) {
    backendState.textContent = text;
    backendState.className = isConnected ? "state connected" : "state";
}

function renderAlerts(alerts) {
    alertsList.innerHTML = "";

    if (!alerts.length) {
        alertsList.innerHTML = "<div class='empty-state'>No active alerts for this mentor.</div>";
        return;
    }

    alerts.forEach((alert) => {
        const item = document.createElement("article");
        item.className = `alert-item ${String(alert.severity).toLowerCase()}`;
        item.innerHTML = `
            <div>
                <strong>${alert.type}</strong>
                <span>Student ${alert.student_id}</span>
            </div>
            <p>${alert.message}</p>
            <small>${alert.severity}</small>
        `;
        alertsList.appendChild(item);
    });
}

function renderStudents(students) {
    studentsTable.innerHTML = "";

    if (!students.length) {
        studentsTable.innerHTML = "<tr><td colspan='7'>No students assigned.</td></tr>";
        return;
    }

    students.forEach((student) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${student.student_id}</td>
            <td>${student.name}</td>
            <td>${student.attendance}%</td>
            <td>${student.sgpa}</td>
            <td>${student.cgpa}</td>
            <td>${student.backlogs}</td>
            <td>${student.fees}</td>
        `;
        studentsTable.appendChild(row);
    });
}

function updateMetrics(students, alerts) {
    studentsCount.textContent = students.length;
    alertsCount.textContent = alerts.length;

    const cgpas = students
        .map((student) => Number(student.cgpa))
        .filter((value) => Number.isFinite(value));
    const average = cgpas.length
        ? cgpas.reduce((sum, value) => sum + value, 0) / cgpas.length
        : 0;
    avgCgpa.textContent = average.toFixed(2);
}

async function loadMentorDashboard(mentorId) {
    setBackendState("Loading...", false);

    try {
        const [studentsResponse, alertsResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/mentor/${encodeURIComponent(mentorId)}/students`),
            fetch(`${API_BASE_URL}/mentor/${encodeURIComponent(mentorId)}/alerts`),
        ]);

        if (!studentsResponse.ok || !alertsResponse.ok) {
            throw new Error("Backend returned an error");
        }

        const studentsData = await studentsResponse.json();
        const alertsData = await alertsResponse.json();
        const students = studentsData.students || [];
        const alerts = alertsData.alerts || [];

        renderStudents(students);
        renderAlerts(alerts);
        updateMetrics(students, alerts);
        setBackendState("Backend connected", true);
    } catch (error) {
        console.error(error);
        renderStudents([]);
        renderAlerts([]);
        updateMetrics([], []);
        setBackendState("Backend not connected", false);
    }
}

mentorForm.addEventListener("submit", (event) => {
    event.preventDefault();
    loadMentorDashboard(mentorInput.value || "101");
});

loadMentorDashboard("101");
