$(document).ready(function () {
  responseTrademarksList();
});

function responseTrademarksList() {
  $.ajax({
    url: `${getBaseUrlAPI()}/trademarks/`,
    type: "GET",
    success: function (response) {
      if (response.message === "Success") {
        const trademarks = response.data;
        const container = $(".categories__slider.owl-carousel");
        trademarks.forEach(function (trademark) {
          //   const div = $(`
          // <div class="col-lg-3">
          //     <div class="categories__item set-bg" data-setbg="${trademark.link_info}">
          //         <h5><a href="#">${trademark.name}</a></h5>
          //     </div>
          // </div>
          // `);
          //   container.append(div);
        });
      }
    },
  });
}

function getBaseUrlAPI() {
  const baseUrlAPI = "http://127.0.0.1:8000/api/v1";
  return baseUrlAPI;
}
