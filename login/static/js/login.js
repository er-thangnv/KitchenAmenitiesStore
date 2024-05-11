$(document).ready(function () {
  document
    .getElementById("procession_login")
    .addEventListener("click", function (event) {
      event.preventDefault();
      var email = $("#email").val();
      var password = $("#password").val();
      if (email.trim() === "" || isValidEmail(email) == false) {
        Toastify({
          text: "Email là bắt buộc",
          duration: 3000,
          newWindow: true,
          close: true,
          gravity: "top",
          position: "center",
          backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
        }).showToast();
      } else if (password.trim() === "") {
        Toastify({
          text: "Mật khẩu là bắt buộc",
          duration: 3000,
          newWindow: true,
          close: true,
          gravity: "top",
          position: "center",
          backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
        }).showToast();
      } else {
        const formData = {
          email: email,
          password: password,
        };
        callAPILogin(formData);
      }
    });
});

function isValidEmail(email) {
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function callAPILogin(formData) {
  $.ajax({
    url: `${getBaseUrlAPI()}/auth/login/`,
    type: "POST",
    data: formData,
    success: function (response) {
      if (response.message === "Login is successfully") {
        setTimeout(function () {
          window.location.href = "/KitchenAmenitiesStore/home/";
        }, 0);
        Toastify({
          text: "Đăng nhập thành công",
          duration: 3000,
          newWindow: true,
          close: true,
          gravity: "top",
          position: "center",
          backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
        }).showToast();
      } else if (response.message === "Account is not verification") {
        Toastify({
          text: "Vui lòng xác nhận email trước khi đăng nhập",
          duration: 3000,
          newWindow: true,
          close: true,
          gravity: "top",
          position: "center",
          backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
        }).showToast();
      } else {
        Toastify({
          text: "Email hoặc mật khẩu chưa chính xác",
          duration: 3000,
          newWindow: true,
          close: true,
          gravity: "top",
          position: "center",
          backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
        }).showToast();
      }
    },
  });
}

function getBaseUrlAPI() {
  const baseUrlAPI = "http://127.0.0.1:8000/api/v1";
  return baseUrlAPI;
}
