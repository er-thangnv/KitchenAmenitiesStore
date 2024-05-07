$(document).ready(function () {
  logOutUser();
});

function logOutUser() {
  $("#logout-link").click(function (e) {
    e.preventDefault();
    $.ajax({
      url: `${getBaseUrlAPI()}/users/log-out`,
      type: "GET",
      success: function (response) {
        if (response.message === "Success") {
          setTimeout(function () {
            window.location.href = "/KitchenAmenitiesStore/home/";
          }, 0);
        }
      },
    });
  });
}

function getBaseUrlAPI() {
  const baseUrlAPI = "http://127.0.0.1:8000/api/v1";
  return baseUrlAPI;
}
