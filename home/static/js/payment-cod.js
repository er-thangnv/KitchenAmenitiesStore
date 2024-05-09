$(document).ready(function () {
  processcingOrderCOD();
});

function processcingOrderCOD() {
  $("#btn-order").click(function (e) {
    e.preventDefault();
    const customerName = $("#customer_name").val();
    const address = $("#address").val();
    const phoneNumber = $("#phone_number").val();
    const email = $("#email").val();
    const note = $("#note").val();
    const productID = $("#product_id").val();
    const totalPrice = $("#total_price").text();
    const paymentMethod = "cod";

    if (
      customerName === "" ||
      address === "" ||
      phoneNumber === "" ||
      email === ""
    ) {
      Toastify({
        text: "Cần điền đầy đủ thông tin",
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top",
        position: "center",
        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
      }).showToast();
    } else {
      const formData = {
        customer_info: {
          customer_name: customerName,
          address: address,
          phone_number: phoneNumber,
          email: email,
          note: note,
        },
        order_info: {
          product_id: productID,
          total_price: parseFloat(totalPrice.split(" ")[0]),
          amount: 1,
        },
        payment_method: paymentMethod,
      };
      $.ajax({
        url: `/api/v1/orders`,
        type: "POST",
        data: formData,
        success: function (response) {
          if (response.message === "Success") {
            Toastify({
              text: "Đặt hàng thành công",
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
  });
}
