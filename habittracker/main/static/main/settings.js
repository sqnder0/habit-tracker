const createFormToggler = document.querySelector(".toggle_create_habit");
const createForm = document.querySelector(".create_habit_form");
const createBtn = document.querySelector(".create_habit");
const habitList = document.querySelector("#habit_list");

habitList.addEventListener("click", (event) => {
  const target = event.target;

  // Edit button
  if (target.closest(".edit_habit")) {
    const btn = target.closest(".edit_habit");
    const habitInfo = btn.parentElement;
    const editForm = habitInfo.parentElement.querySelector("form");
    habitInfo.classList.toggle("d-none");
    editForm.classList.toggle("d-none");
  }

  // Save button
  if (target.closest(".save_habit")) {
    event.preventDefault();
    const btn = target.closest(".save_habit");
    const form = btn.closest("form");
    const habitId = form.querySelector(".habit_id").id;
    const name = form.querySelector(`#habit_${habitId}_name`).value;
    const time = form.querySelector(`#habit_${habitId}_time`).value;
    const description = form.querySelector(`#habit_${habitId}_description`).value;
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch("/update_habit/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ habit_id: habitId, habit_name: name, timestamp: time, habit_description: description }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success === "success") {
          const habit_name_el = form.parentElement.querySelector(".habit_name");
          const habit_time_el = form.parentElement.querySelector(".habit_time");
          const habit_info = form.parentElement.querySelector(".habit_info");

          habit_name_el.textContent = name;
          habit_time_el.textContent = toAmPm(time);

          form.classList.toggle("d-none");
          habit_info.classList.toggle("d-none");
        }
      })
      .catch(console.error);
  }

  // Delete button
  if (target.closest(".delete_habit")) {
    event.preventDefault();
    const btn = target.closest(".delete_habit");
    const form = btn.closest("form");
    const habitId = form.querySelector(".habit_id").id;
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch("/delete_habit/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
      body: JSON.stringify({ habit_id: habitId }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success === "success") form.parentElement.remove();
      })
      .catch(console.error);
  }
});

createFormToggler.addEventListener("click", (event) => {
  createFormToggler.classList.toggle("d-none");
  createForm.classList.toggle("d-none");
});

createBtn.addEventListener("click", (event) => {
  event.preventDefault();

  const habitName = createForm.querySelector("#habit_name").value;
  const timestamp = createForm.querySelector("#habit_time").value;
  const description = createForm.querySelector("#habit_description").value;
  const csrfToken = createForm.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch("/create_habit/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      habit_name: habitName,
      timestamp: timestamp,
      habit_description: description,
    }),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Network error");
      return response.json();
    })
    .then((data) => {
      if (data.success == "success") {
        const habitId = data.habit_id;

        const habitDiv = document.createElement("div");
        habitDiv.classList.add("bg-secondary-subtle", "mb-2");

        const habitInfo = document.createElement("div");
        habitInfo.classList.add("d-flex", "px-2", "align-items-center", "habit_info");

        const span = document.createElement("span");

        const nameSpan = document.createElement("span");
        nameSpan.classList.add("habit_name");
        nameSpan.innerText = habitName;

        const timeSpan = document.createElement("span");
        timeSpan.classList.add("habit_time");

        console.log(timestamp);
        timeSpan.innerText = toAmPm(timestamp);

        span.appendChild(nameSpan);
        span.appendChild(document.createTextNode(" (0): "));
        span.appendChild(timeSpan);

        habitInfo.appendChild(span);

        const editBtn = document.createElement("button");
        editBtn.classList.add("btn", "ms-auto", "edit_habit");
        editBtn.innerHTML = '<i class="bi bi-pencil-fill"></i>';
        habitInfo.appendChild(editBtn);

        const editForm = document.createElement("form");
        editForm.classList.add("edit_form", "p-3", "d-none");

        const csrfInput = document.createElement("input");
        csrfInput.type = "hidden";
        csrfInput.name = "csrfmiddlewaretoken";
        csrfInput.value = csrfToken;
        editForm.appendChild(csrfInput);

        const habitIdInput = document.createElement("input");
        habitIdInput.classList.add("d-none", "habit_id");
        habitIdInput.id = habitId;
        editForm.appendChild(habitIdInput);

        const nameDiv = document.createElement("div");
        nameDiv.classList.add("d-flex", "mb-3");

        const nameInput = document.createElement("input");
        nameInput.classList.add("form-control", "w-50");
        nameInput.type = "text";
        nameInput.value = habitName;
        nameInput.id = `habit_${habitId}_name`;
        nameDiv.appendChild(nameInput);

        const timeInput = document.createElement("input");
        timeInput.classList.add("form-control", "time-input");
        timeInput.type = "time";
        timeInput.value = timestamp;
        timeInput.id = `habit_${habitId}_time`;
        nameDiv.appendChild(timeInput);

        editForm.appendChild(nameDiv);

        const descriptionInput = document.createElement("textarea");
        descriptionInput.classList.add("form-control", "mb-3");
        descriptionInput.id = `habit_${habitId}_description`;
        descriptionInput.innerText = description;
        editForm.appendChild(descriptionInput);

        const btnDiv = document.createElement("div");
        btnDiv.classList.add("d-flex");

        const saveBtn = document.createElement("button");
        saveBtn.classList.add("save_habit", "btn", "btn-success");
        saveBtn.innerHTML = '<i class="bi bi-floppy"></i> Save';
        btnDiv.appendChild(saveBtn);

        const deleteBtn = document.createElement("button");
        deleteBtn.classList.add("delete_habit", "btn", "btn-danger", "ms-auto");
        deleteBtn.innerHTML = '<i class="bi bi-trash"></i> Delete';
        btnDiv.appendChild(deleteBtn);

        editForm.appendChild(btnDiv);

        habitDiv.appendChild(habitInfo);
        habitDiv.appendChild(editForm);

        habitList.appendChild(habitDiv);

        createForm.classList.toggle("d-none");
        createFormToggler.classList.toggle("d-none");

        loadBtns();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

function toAmPm(time24) {
  let [hours, minutes] = time24.split(":").map(Number);
  let ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12 || 12; // convert 0 -> 12, 13 -> 1
  return `${hours}:${minutes.toString().padStart(2, "0")} ${ampm}`;
}
