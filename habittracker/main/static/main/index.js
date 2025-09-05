const expandBtns = document.querySelectorAll(".expand-habit");

expandBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    btn.classList.toggle("rotate-270");
    const form = btn.closest("form");
    const expandMe = form.querySelector(".expandable");

    if (expandMe.classList.contains("d-none")) {
      expandMe.classList.toggle("d-none");
      setTimeout(() => {
        expandMe.classList.toggle("show");
      }, 100);
    } else {
      expandMe.classList.toggle("show");
      setTimeout(() => {
        expandMe.classList.toggle("d-none");
      }, 600);
    }
  });
});
