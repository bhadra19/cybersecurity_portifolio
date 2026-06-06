const topbar = document.querySelector(".topbar");
const projects = window.PORTFOLIO_PROJECTS || [];

const state = {
  search: "",
  category: "all",
  status: "all"
};

window.addEventListener("scroll", () => {
  topbar.style.boxShadow = window.scrollY > 12
    ? "0 10px 30px rgba(23, 32, 29, 0.08)"
    : "none";
});

function unique(values) {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b));
}

function renderStats() {
  const categories = unique(projects.map((project) => project.category)).length;
  const runnable = projects.filter((project) => project.status === "Runnable").length;
  const topRated = projects.filter((project) => project.rating === 5).length;
  document.querySelector("#heroStats").innerHTML = [
    [`${projects.length}`, "separate AppSec project repositories linked from this portfolio"],
    [`${runnable}`, "runnable projects with local commands and sample inputs"],
    [`${topRated}`, `five-star projects across ${categories} AppSec categories`]
  ].map(([value, label]) => `
    <div>
      <span class="metric">${value}</span>
      <span>${label}</span>
    </div>
  `).join("");
}

function renderFilters() {
  const categoryFilter = document.querySelector("#categoryFilter");
  const categories = unique(projects.map((project) => project.category));
  categoryFilter.innerHTML = [
    `<option value="all">All categories</option>`,
    ...categories.map((category) => `<option value="${category}">${category}</option>`)
  ].join("");

  document.querySelector("#projectSearch").addEventListener("input", (event) => {
    state.search = event.target.value.trim().toLowerCase();
    renderProjects();
  });
  categoryFilter.addEventListener("change", (event) => {
    state.category = event.target.value;
    renderProjects();
  });
  document.querySelector("#statusFilter").addEventListener("change", (event) => {
    state.status = event.target.value;
    renderProjects();
  });
}

function filteredProjects() {
  return projects.filter((project) => {
    const haystack = [
      project.title,
      project.category,
      project.status,
      project.summary,
      project.run,
      ...project.tech,
      ...project.keywords
    ].join(" ").toLowerCase();
    const matchesSearch = !state.search || haystack.includes(state.search);
    const matchesCategory = state.category === "all" || project.category === state.category;
    const matchesStatus = state.status === "all" || project.status === state.status;
    return matchesSearch && matchesCategory && matchesStatus;
  });
}

function renderProjects() {
  const visible = filteredProjects();
  document.querySelector("#projectCount").textContent =
    `${visible.length} of ${projects.length} projects shown`;

  document.querySelector("#projectGrid").innerHTML = visible.map((project) => `
    <article class="card ${project.rating === 5 ? "featured" : ""}">
      <div class="card-top">
        <span class="rating">${project.rating}/5</span>
        <span class="tag">${project.category}</span>
      </div>
      <h3>${project.title}</h3>
      <p>${project.summary}</p>
      <div class="tag-row">
        ${project.tech.map((item) => `<span class="tag">${item}</span>`).join("")}
      </div>
      <p class="run-command"><strong>Run:</strong> <code>${project.run}</code></p>
      <a href="${project.repo}">Open project repo</a>
    </article>
  `).join("");
}

function renderSkills() {
  const skills = unique(projects.flatMap((project) => project.keywords));
  document.querySelector("#skillList").innerHTML =
    skills.map((skill) => `<span>${skill}</span>`).join("");
}

renderStats();
renderFilters();
renderProjects();
renderSkills();
