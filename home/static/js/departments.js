$(document).ready(function () {
  responseDepartmentsList();
});

function responseDepartmentsList() {
  $.ajax({
    url: `${getBaseUrlAPI()}/departments/`,
    type: "GET",
    success: function (response) {
      if (response.message === "Success") {
        const departments = response.data;
        const ulElement = $(".list_departments");
        departments.forEach(function (department) {
          const liElement = $("<li>");
          const aElement = $("<a>");
          aElement.text(department.name);
          aElement.attr(
            "href",
            `/KitchenAmenitiesStore/departments/${department.id}`
          );
          liElement.append(aElement);
          ulElement.append(liElement);
        });
      }
    },
  });
}

function getBaseUrlAPI() {
  const baseUrlAPI = "http://127.0.0.1:8000/api/v1";
  return baseUrlAPI;
}
