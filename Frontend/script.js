async function fetchGoals() {
  const res = await fetch("/api/goals");
  const goals = await res.json();
  const goalList = document.getElementById("goalList");
  goalList.innerHTML = "";
  goals.forEach(g => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${g.goal}</span>
      <button onclick="deleteGoal(${g.id})">Delete</button>
    `;
    goalList.appendChild(li);
  });
}

async function addGoal() {
  const goalInput = document.getElementById("goalInput");
  const goalText = goalInput.value.trim();
  if (!goalText) return alert("Please enter a goal.");

  await fetch("/api/goals", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal: goalText })
  });
  goalInput.value = "";
  fetchGoals();
}

async function deleteGoal(id) {
  await fetch(`/api/goals/${id}`, { method: "DELETE" });
  fetchGoals();
}

// Load goals on page load
fetchGoals();