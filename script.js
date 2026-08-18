const form = document.getElementById("predict-form");
const submitBtn = document.getElementById("submit-btn");
const resultBox = document.getElementById("result");
const errorBox = document.getElementById("error");
const gaugeFill = document.getElementById("gauge-fill");
const scoreValueEl = document.getElementById("score-value");
const scoreLabelEl = document.getElementById("score-label");

// Served from the same FastAPI app, so a relative path works everywhere.
const API_URL = "/predict";

const CIRCUMFERENCE = 2 * Math.PI * 70; // r=70 in the SVG

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  resultBox.classList.add("hidden");
  errorBox.classList.add("hidden");
  gaugeFill.style.strokeDashoffset = CIRCUMFERENCE; // reset before next reveal
  submitBtn.disabled = true;
  submitBtn.querySelector(".btn-label").textContent = "Predicting…";

  const formData = new FormData(form);

  const payload = {
    Age: parseInt(formData.get("Age"), 10),
    Gender: formData.get("Gender"),
    Country: formData.get("Country"),
    Academic_Level: formData.get("Academic_Level"),
    Most_Used_Platform: formData.get("Most_Used_Platform"),
    Purpose_Of_Use: formData.get("Purpose_Of_Use"),
    Avg_Daily_Usage_Hours: parseFloat(formData.get("Avg_Daily_Usage_Hours")),
    Daily_Unlocks: parseInt(formData.get("Daily_Unlocks"), 10),
    Study_Hours: parseFloat(formData.get("Study_Hours")),
    Physical_Activity_Hours: parseFloat(formData.get("Physical_Activity_Hours")),
    Sleep_Hours_Per_Night: parseFloat(formData.get("Sleep_Hours_Per_Night")),
    Stress_Level: formData.get("Stress_Level"),
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Request failed with status ${response.status}`);
    }

    const data = await response.json();
    revealScore(data.Mental_Health_Score);
  } catch (err) {
    errorBox.textContent = `Error: ${err.message}`;
    errorBox.classList.remove("hidden");
  } finally {
    submitBtn.disabled = false;
    submitBtn.querySelector(".btn-label").textContent = "Predict Score";
  }
});

function revealScore(score) {
  // Assumes a 0–10 score range; clamp defensively in case the model
  // occasionally predicts slightly outside that band.
  const clamped = Math.max(0, Math.min(10, score));
  const ratio = clamped / 10;

  // Color band: teal = good, amber = moderate, coral = concerning.
  let color = "#5EEAD4";
  let label = "Looking good";
  if (ratio < 0.4) {
    color = "#FB7185";
    label = "Needs attention";
  } else if (ratio < 0.7) {
    color = "#FBBF6A";
    label = "Room to improve";
  }

  gaugeFill.style.stroke = color;
  scoreLabelEl.style.color = color;
  scoreLabelEl.style.background = `${color}1F`;
  scoreLabelEl.style.borderColor = `${color}55`;
  scoreLabelEl.textContent = label;

  resultBox.classList.remove("hidden");

  // Animate the ring fill
  requestAnimationFrame(() => {
    const offset = CIRCUMFERENCE * (1 - ratio);
    gaugeFill.style.strokeDashoffset = offset;
  });

  // Count-up animation for the number
  const duration = 900;
  const start = performance.now();
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    scoreValueEl.textContent = (eased * score).toFixed(2);
    if (progress < 1) requestAnimationFrame(tick);
    else scoreValueEl.textContent = score.toFixed(2);
  }
  requestAnimationFrame(tick);
}
