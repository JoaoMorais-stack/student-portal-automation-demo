const elements = {
  studentName: document.querySelector("#student-name"),
  studentMeta: document.querySelector("#student-meta"),
  overall: document.querySelector("#overall-progress"),
  courses: document.querySelector("#course-count"),
  completed: document.querySelector("#completed-count"),
  pending: document.querySelector("#pending-count"),
  courseList: document.querySelector("#course-list"),
  activityList: document.querySelector("#activity-list"),
  status: document.querySelector("#status-line"),
  runButton: document.querySelector("#run-button"),
  resetButton: document.querySelector("#reset-button"),
};

function escapeHtml(value) {
  const node = document.createElement("span");
  node.textContent = String(value);
  return node.innerHTML;
}

function courseMarkup(course) {
  const lessons = course.lessons.map((lesson) => `
    <li class="lesson ${lesson.completed ? "done" : ""}">
      <span class="lesson-state" aria-label="${lesson.completed ? "Completed" : "Pending"}">${lesson.completed ? "OK" : ""}</span>
      <div>
        <strong>${escapeHtml(lesson.title)}</strong>
        <small>${lesson.duration_minutes} min · ${lesson.completed ? "Completed" : "Pending"}</small>
      </div>
    </li>
  `).join("");

  return `
    <article class="course-card" data-accent="${escapeHtml(course.accent)}" data-progress="${course.progress}">
      <div class="course-header">
        <p class="course-code">${escapeHtml(course.code)}</p>
        <h3 class="course-title">${escapeHtml(course.title)}</h3>
        <p class="course-instructor">${escapeHtml(course.instructor)}</p>
        <div class="progress-row"><span>${course.completed_lessons} of ${course.lessons.length} lessons</span><strong>${course.progress}%</strong></div>
        <div class="progress-track" aria-label="${course.progress}% complete"><div class="progress-fill"></div></div>
      </div>
      <ul class="lesson-list">${lessons}</ul>
    </article>
  `;
}

function render(state) {
  elements.studentName.textContent = state.student.name;
  elements.studentMeta.textContent = `${state.student.program} · ${state.student.term}`;
  elements.overall.textContent = `${state.summary.overall_progress}%`;
  elements.courses.textContent = state.summary.courses;
  elements.completed.textContent = state.summary.completed;
  elements.pending.textContent = state.summary.pending;
  elements.courseList.innerHTML = state.courses.map(courseMarkup).join("");
  // O CSP (style-src 'self') bloqueia atributos style no HTML gerado; a cor e o
  // progresso de cada curso são aplicados pela CSSOM, que a política permite.
  elements.courseList.querySelectorAll(".course-card").forEach((card) => {
    card.style.setProperty("--course-accent", card.dataset.accent);
    card.style.setProperty("--progress", `${Number(card.dataset.progress) || 0}%`);
  });
}

function renderEvents(events) {
  if (!events.length) {
    elements.activityList.innerHTML = '<li><span class="activity-dot idle"></span><div><strong>No pending lessons</strong><small>The fictional portal is already complete.</small></div></li>';
    return;
  }
  elements.activityList.innerHTML = events.map((event) => `
    <li>
      <span class="activity-dot"></span>
      <div><strong>${escapeHtml(event.lesson_title)}</strong><small>${escapeHtml(event.course_title)} · mock completion recorded</small></div>
    </li>
  `).join("");
}

async function request(path, options = {}) {
  const response = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  if (!response.ok) throw new Error(`Local request failed (${response.status})`);
  return response.json();
}

async function loadState() {
  try {
    render(await request("/api/state"));
  } catch (error) {
    elements.status.textContent = error.message;
  }
}

elements.runButton.addEventListener("click", async () => {
  elements.runButton.disabled = true;
  elements.status.textContent = "Running against the authorized local mock...";
  try {
    const result = await request("/api/demo/run", { method: "POST", body: "{}" });
    render(result.state);
    renderEvents(result.events);
    elements.status.textContent = `Demo finished: ${result.events.length} pending lesson(s) processed locally.`;
  } catch (error) {
    elements.status.textContent = error.message;
  } finally {
    elements.runButton.disabled = false;
  }
});

elements.resetButton.addEventListener("click", async () => {
  elements.resetButton.disabled = true;
  elements.status.textContent = "Resetting fictional data...";
  try {
    render(await request("/api/reset", { method: "POST", body: "{}" }));
    elements.activityList.innerHTML = '<li><span class="activity-dot idle"></span><div><strong>Demo reset</strong><small>Fictional starting data was restored.</small></div></li>';
    elements.status.textContent = "Ready for a local demonstration.";
  } catch (error) {
    elements.status.textContent = error.message;
  } finally {
    elements.resetButton.disabled = false;
  }
});

loadState();

