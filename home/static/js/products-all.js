$(document).ready(function () {
  responseAllProducts();
  showMoreProducts();
});

function responseAllProducts() {
  var page = 1;
  $.ajax({
    url: `/api/v1/products?page=${page}`,
    type: "GET",
    success: function (response) {
      if (response.message === "Success") {
        var products = response.data.items;
        products.forEach(function (product) {
          var productHtml = `
            <div class="col-lg-3 col-md-4 col-sm-6 mix oranges fresh-meat">
              <div class="featured__item">
                <div class="featured__item__pic set-bg" data-setbg="${product.image}" style="background-image: url(${product.image})">
                  <ul class="featured__item__pic__hover">
                    <li><a class="add-cart" href="/KitchenAmenitiesStore/checkout/${product.id}"><i class="fa fa-shopping-cart"></i></a></li>
                  </ul>
                </div>
                <div class="featured__item__text">
                  <h6><a href="/KitchenAmenitiesStore/products/${product.id}">${product.name}</a></h6>
                  <h5>${product.price} VNĐ</h5>
                </div>
              </div>
            </div>
          `;
          $("#product-all-list").append(productHtml);
          $("#page_number").val(response.data.page);
        });
      }
      if (response.data.has_next_page === false) {
        $("#show-more-products").hide();
      }
    },
  });
}

function showMoreProducts() {
  $("#show-more-products").click(function () {
    const pageCurrent = $("#page_number").val();
    $.ajax({
      url: `/api/v1/products?page=${pageCurrent + 1}`,
      type: "GET",
      success: function (response) {
        if (response.message === "Success") {
          var products = response.data.items;
          products.forEach(function (product) {
            var productHtml = `
                <div class="col-lg-3 col-md-4 col-sm-6 mix oranges fresh-meat">
                  <div class="featured__item">
                    <div class="featured__item__pic set-bg" data-setbg="${product.image}" style="background-image: url(${product.image})">
                      <ul class="featured__item__pic__hover">
                        <li><a class="add-cart" href="/KitchenAmenitiesStore/checkout/${product.id}"><i class="fa fa-shopping-cart"></i></a></li>
                      </ul>
                    </div>
                    <div class="featured__item__text">
                      <h6><a href="/KitchenAmenitiesStore/products/${product.id}">${product.name}</a></h6>
                      <h5>${product.price} VNĐ</h5>
                    </div>
                  </div>
                </div>
              `;
            $("#product-all-list").append(productHtml);
            $("#page_number").val(response.data.page);
          });
        }
        if (response.data.has_next_page === false) {
          $("#show-more-products").hide();
        }
      },
    });
  });
}
