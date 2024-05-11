$(document).ready(function () {
  searchProduct();
});

function searchProduct() {
  $("#btn-search-product").click(function (e) {
    e.preventDefault();
    const search = $("#search-input").val();
    const encodeSearch = encodeURI(search);
    setTimeout(function () {
      window.location.href = `/KitchenAmenitiesStore/products?search=${encodeSearch}`;
    }, 0);
  });
}
