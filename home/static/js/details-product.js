$(document).ready(function () {
  var images = document.querySelectorAll(".product__details__pic__slider img");

  images.forEach(function (image) {
    image.addEventListener("click", function () {
      var imgSrc = this.getAttribute("src");

      var modal = document.getElementById("imageModal");
      var modalImg = document.getElementById("img01");
      modal.style.display = "block";
      modalImg.src = imgSrc;

      var span = document.getElementsByClassName("close")[0];
      span.onclick = function () {
        modal.style.display = "none";
      };
    });
  });
});
