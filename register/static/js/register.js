$(document).ready(function(){
    document.getElementById("procession_register").addEventListener(
        "click",
        function (event) {
          event.preventDefault();
          var name = $("#name").val();
          var email = $("#email").val();
          var password = $("#password").val();
          var repeatPassword = $("#repeat_password").val();
          if (name.trim() === '') {
            Toastify(
                {
                    text: "Họ và tên là bắt buộc",
                    duration: 3000,
                    newWindow: true,
                    close: true,
                    gravity: "top",
                    position: "center",
                    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                }).showToast();
          } else if (email.trim() === '' || isValidEmail(email) === false) {
            Toastify(
                {
                    text: "Email là bắt buộc",
                    duration: 3000,
                    newWindow: true,
                    close: true,
                    gravity: "top",
                    position: "center",
                    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                }).showToast();
          } else if (password.trim() === '' || repeatPassword.trim() === '') {
            Toastify(
                {
                    text: "Mật khẩu là bắt buộc",
                    duration: 3000,
                    newWindow: true,
                    close: true,
                    gravity: "top",
                    position: "center",
                    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                }).showToast();
          } else if (password.trim() !== repeatPassword.trim()) {
            Toastify(
                {
                    text: "Xác nhận mật khẩu là không đúng",
                    duration: 3000,
                    newWindow: true,
                    close: true,
                    gravity: "top",
                    position: "center",
                    backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                }).showToast();
          } else {
            var formData = {
                name: name,
                email: email,
                password: password,
                repeat_password: repeatPassword,
            };
            callAPIRegister(formData);
          }
    });
});

function isValidEmail(email) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function callAPIRegister(formData) {
    $.ajax({
        url: `${getBaseUrlAPI()}/auth/register/`,
        type: 'POST',
        data: formData,
        success: function (response) {
            if (response.message === 'Register account is successfully') {
                Toastify(
                    {
                        text: "Đăng ký tài khoản thành công",
                        duration: 3000,
                        newWindow: true,
                        close: true,
                        gravity: "top",
                        position: "center",
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                    }).showToast();
            } else if (response.message === 'Email already is existing') {
                Toastify(
                    {
                        text: "Email này đã tồn tại",
                        duration: 3000,
                        newWindow: true,
                        close: true,
                        gravity: "top",
                        position: "center",
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                    }).showToast();
            }
        }
    });
}

function getBaseUrlAPI() {
    const baseUrlAPI = 'http://127.0.0.1:8000/api/v1';
    return baseUrlAPI;
}
