document.addEventListener("DOMContentLoaded", function () {
    const ratingWidget = document.getElementById("rating-widget");
    if (ratingWidget) {
      const stars = ratingWidget.querySelectorAll(".rating-star");
      const ratingInput = document.getElementById("rating-score");
      let currentRating =
        parseInt(ratingWidget.dataset.currentRating, 10) || 0;

      function updateStars(rating) {
        stars.forEach(function (star) {
          const starScore = parseInt(star.dataset.score, 10);
          if (starScore <= rating) {
            star.classList.remove("far");
            star.classList.add("fas");
          } else {
            star.classList.remove("fas");
            star.classList.add("far");
          }
        });
      }

      updateStars(currentRating);

      stars.forEach(function (star) {
        star.addEventListener("click", function () {
          const selectedRating = parseInt(this.dataset.score, 10);
          ratingInput.value = selectedRating;
          updateStars(selectedRating);
        });
      });

      const ratingForm = document.getElementById("rating-form");
      ratingForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(ratingForm);
        fetch(ratingForm.action, {
          method: "POST",
          headers: {
            "X-CSRFToken": document.querySelector(
              "[name=csrfmiddlewaretoken]"
            ).value,
          },
          body: formData,
        })
          .then((response) => {
            if (!response.ok)
              throw new Error("Network response was not ok.");
            return response.json();
          })
          .then((data) => {
            document.getElementById("avg-rating").textContent =
              data.new_average.toFixed(2);
            alert("Thanks! Your rating has been submitted.");
          })
          .catch((error) => {
            console.error("Error submitting rating:", error);
          });
      });
    }
    // Reply Button Toggle
    const replyButtons = document.querySelectorAll(".reply-btn");
    replyButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        const commentId = this.dataset.commentId;
        const replyForm = document.getElementById(
          "reply-form-" + commentId
        );
        if (
          replyForm.style.display === "none" ||
          replyForm.style.display === ""
        ) {
          replyForm.style.display = "block";
        } else {
          replyForm.style.display = "none";
        }
      });
    });

// Report Modal Script
// Report Modal Script
const reportButtons = document.querySelectorAll(".report-btn");
const reportForm = document.getElementById("reportForm");

reportButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const type = button.dataset.type; // تحديد نوع التقرير (مشروع أو تعليق)
    const objectId = button.dataset.id; // تحديد الـ ID الخاص بالمشروع أو التعليق
    document.getElementById("reportType").value = type; // تعيين نوع التقرير في الحقل المخفي
    document.getElementById("reportObjectId").value = objectId; // تعيين الـ ID في الحقل المخفي
    document.getElementById("reportReason").value = ""; // إعادة تعيين السبب المحدد
  });
});

reportForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const formData = new FormData(reportForm);
  const objectId = document.getElementById("reportObjectId").value; // Get the objectId dynamically from the hidden input field

  // Ensure objectId is available before calling fetch
  if (objectId) {
    fetch(`/projects/${objectId}/submit_report/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value, // Add CSRF token
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Report submitted successfully.");
          const modal = bootstrap.Modal.getInstance(document.getElementById("reportModal"));
          modal.hide(); // Close the modal after submitting the report successfully
        } else {
          alert("Error: " + data.message);
        }
      })
      .catch((error) => {
        alert("An error occurred.");
        console.error(error);
      });
  } else {
    alert("Error: No object ID specified.");
  }
});
});