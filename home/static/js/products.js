$(document).ready(function () {
  responseNewProducts();
});

function responseNewProducts() {
  $.ajax({
    url: `${getBaseUrlAPI()}/products/new`,
    type: "GET",
    success: function (response) {
      console.log(response);
    },
  });
}

function getBaseUrlAPI() {
  const baseUrlAPI = "http://127.0.0.1:8000/api/v1";
  return baseUrlAPI;
}
