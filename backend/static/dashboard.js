const state = {
    role: null,
    userId: null,
};

const loginCard = document.getElementById("login-card");
const profileCard = document.getElementById("profile-card");
const userIdInput = document.getElementById("user-id");
const passwordInput = document.getElementById("password");
const loginError = document.getElementById("login-error");
const roleLabel = document.getElementById("role-label");
const profileTitle = document.getElementById("profile-title");
const backendState = document.getElementById("backend-state");
const pageTitle = document.getElementById("page-title");
const eyebrow = document.getElementById("eyebrow");
const mentorView = document.getElementById("mentor-view");
const adminView = document.getElementById("admin-view");
const metricOneLabel = document.getElementById("metric-one-label");
const metricTwoLabel = document.getElementById("metric-two-label");
const metricOne = document.getElementById("metric-one");
const metricTwo = document.getElementById("metric-two");
const alertsList = document.getElementById("alerts-list");
const mentorStudents = document.getElementById("mentor-students");
const adminStudents = document.getElementById("admin-students");
const actionStatus = document.getElementById("action-status");
const assignStatus = document.getElementById("assign-status");

function setBackendStatus(text, ok) {
    backendState.textContent = text;
    backendState.className = ok ? "state ok" : "state";
}

async function getJson(url, options) {
    const response = await fetch(url, options);
    if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
    }
    return response.json();
}

function rupeeText(value) {
    return String(value || "").replace("â‚¹", "₹");
}

function renderMentorStudents(students) {
    mentorStudents.innerHTML = "";
    if (!students.length) {
        mentorStudents.innerHTML = "<tr><td colspan='7'>No students assigned.</td></tr>";
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
            <td>${rupeeText(student.fees)}</td>
        `;
        mentorStudents.appendChild(row);
    });
}

function renderAlerts(alerts) {
    alertsList.innerHTML = "";
    if (!alerts.length) {
        alertsList.innerHTML = "<div class='empty'>No active alerts for this mentor.</div>";
        return;
    }

    alerts.forEach((alert) => {
        const item = document.createElement("article");
        item.className = `alert ${String(alert.severity).toLowerCase()}`;
        item.innerHTML = `
            <div>
                <strong>${alert.type}</strong>
                <span>Student ${alert.student_id}</span>
            </div>
            <p>${rupeeText(alert.message)}</p>
            <small>${alert.severity}</small>
        `;
        alertsList.appendChild(item);
    });
}

function renderAdminStudents(students) {
    adminStudents.innerHTML = "";
    if (!students.length) {
        adminStudents.innerHTML = "<tr><td colspan='7'>No students found.</td></tr>";
        return;
    }

    students.forEach((student) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${student.student_id}</td>
            <td>${student.name}</td>
            <td>${student.mentor_id}</td>
            <td>${student.attendance}%</td>
            <td>${student.sgpa}</td>
            <td>${student.cgpa}</td>
            <td>${rupeeText(student.fees)}</td>
        `;
        adminStudents.appendChild(row);
    });
}

async function loadMentorDashboard() {
    pageTitle.textContent = "Mentor Dashboard";
    eyebrow.textContent = `Mentor ID ${state.userId}`;
    mentorView.classList.remove("hidden");
    adminView.classList.add("hidden");

    const [studentData, alertData] = await Promise.all([
        getJson(`/mentor/${state.userId}/students`),
        getJson(`/mentor/${state.userId}/alerts`),
    ]);

    const students = studentData.students || [];
    const alerts = alertData.alerts || [];
    renderMentorStudents(students);
    renderAlerts(alerts);

    metricOneLabel.textContent = "Students";
    metricTwoLabel.textContent = "Alerts";
    metricOne.textContent = students.length;
    metricTwo.textContent = alerts.length;
}

async function loadAdminDashboard() {
    pageTitle.textContent = "Admin Dashboard";
    eyebrow.textContent = "Flask Dashboard";
    mentorView.classList.add("hidden");
    adminView.classList.remove("hidden");

    const [studentData, mentorData] = await Promise.all([
        getJson("/students"),
        getJson("/mentors"),
    ]);

    const students = studentData.students || [];
    const mentors = mentorData.mentors || [];
    renderAdminStudents(students);

    metricOneLabel.textContent = "Students";
    metricTwoLabel.textContent = "Mentors";
    metricOne.textContent = students.length;
    metricTwo.textContent = mentors.length;
}

async function refreshDashboard() {
    try {
        setBackendStatus("Loading data...", false);
        if (state.role === "Admin") {
            await loadAdminDashboard();
        } else {
            await loadMentorDashboard();
        }
        setBackendStatus("Backend connected", true);
    } catch (error) {
        console.error(error);
        setBackendStatus("Backend error", false);
    }
}

function showSession(role, userId) {
    state.role = role;
    state.userId = userId;
    loginCard.classList.add("hidden");
    profileCard.classList.remove("hidden");
    roleLabel.textContent = role;
    profileTitle.textContent = role === "Admin" ? "Administrator" : `Mentor ${userId}`;
    refreshDashboard();
}

document.getElementById("login-btn").addEventListener("click", () => {
    const userId = userIdInput.value.trim();
    const password = passwordInput.value;
    loginError.textContent = "";

    if (userId === "admin" && password === "admin") {
        showSession("Admin", "admin");
        return;
    }

    if (/^\d+$/.test(userId) && password === "mentor") {
        showSession("Mentor", userId);
        return;
    }

    loginError.textContent = "Invalid login. Use 101/mentor or admin/admin.";
});

document.getElementById("logout-btn").addEventListener("click", () => {
    state.role = null;
    state.userId = null;
    loginCard.classList.remove("hidden");
    profileCard.classList.add("hidden");
});

document.getElementById("run-attendance").addEventListener("click", async () => {
    actionStatus.textContent = "Running attendance check...";
    const result = await getJson("/trigger-attendance", { method: "POST" });
    actionStatus.textContent = result.message || "Attendance check completed.";
});

document.getElementById("run-fees").addEventListener("click", async () => {
    actionStatus.textContent = "Running fee reminders...";
    const result = await getJson("/trigger-fees", { method: "POST" });
    actionStatus.textContent = result.message || "Fee reminders completed.";
});

document.getElementById("assign-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    assignStatus.textContent = "Assigning student...";
    const payload = {
        student_id: document.getElementById("assign-student").value,
        mentor_id: document.getElementById("assign-mentor").value,
    };
    const result = await getJson("/assign-mentor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    assignStatus.textContent = result.message || "Student assigned.";
    await refreshDashboard();
});

setBackendStatus("Ready", true);
