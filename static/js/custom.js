const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
  "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];


$(document).on("click", "#helpful", function(){
    let id = $(this).attr("data-id")
    let val = $(this)
    let alert = $("#alert" + id)

    $.ajax({
        url: "/ajax/helpful-review/",
        data: {
            "id":id
        },
        dataType: "json",
        success: function(response){
            console.log("Review is helpful");
            $(".helpful"+id).hide()
            alert.text("Thanks for rating this review.")
        }
    })

})



$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),
        
        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("Comment Saved to DB...");
            
            if(res.bool == true){
                $("#review-res").html("Review added successfully, awaiting moderation.")
                $("#commentForm").hide()
                }
        }
        })
})  



$(document).on("click", "#question-btn", function(){
    let question = $("#question-input").val()
    let alert = $("#q-alert")    
    let questionDiv = $("#question-div")  
    let id = $(this).attr("data-pid")
    
    console.log(id);

    $.ajax({
        url: "/ajax/ask-question/",
        data: {
            "id":id,
            "question":question,
        },
        dataType: "json",
        success: function(response){
            if (response.bool === true){
                questionDiv.hide()
                alert.text("You question have been submited and would be answered soon.")
                Swal.fire(
                    'Question sent',
                    'successfully.',
                    'success'
                  )
            }
        },
        
    })

})




    // Add to cart functionality
    $(".add-to-cart-btn").on("click", function(){
    
        let this_val = $(this)
        let index = this_val.attr("data-index")
    
        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
    
        let product_id = $(".product-id-" + index).val()
        let product_meta_title = $(".product-meta_title-" + index).val()
        let product_is_digital = $(".product-is_digital-" + index).val()
        let product_price = $(".product-price-" + index).val()
        let product_types_choices = $(".product-types_choices-" + index).val()
        let product_shipping_amount = $(".product-shipping_amount-" + index).val()
        let product_tax_fee = $(".product-tax-fee-" + index).val()
        let product_processing_fee = $(".product-processing-fee-" + index).val()
        let product_vendor = $(".product-vendor-" + index).val() 
        let product_brand = $(".product-brand-" + index).val() 
        let product_gz_coins = $(".product-gz_coins-" + index).val() 
        let product_vendor_slug = $(".product-vendor-slug-" + index).val() 

        let product_stock_qty = $(".product-stock-qty-" + index).val() 
        let product_in_stock = $(".product-in-stock-" + index).val() 
    
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()
    
    
        console.log("Quantity:", quantity);
        console.log("Title:", product_title);
        console.log("Price:", product_price);
        console.log("Meta title:", product_meta_title);
        console.log("ID:", product_id);
        console.log("PID:", product_pid);
        console.log("Digital?:", product_is_digital);
        console.log("GZ Coins:", product_gz_coins, "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz");
        console.log("product_types_choices:", product_types_choices);
        console.log("Image:", product_image);
        console.log("product_shipping_amount:", product_shipping_amount);
        console.log("product_vendor:", product_vendor);
        console.log("product_brand:", product_brand);
        console.log("Index:", index);
        console.log("Currrent Element:", this_val);
        console.log("product_processing_fee:", product_processing_fee);
        console.log("product_tax_fee:", product_tax_fee);
        console.log("product_vendor_slug:", product_vendor_slug);
        console.log("product_stock_qty:", product_stock_qty);
        console.log("product_in_stock:", product_in_stock);

        if (parseInt(quantity) > parseInt(product_stock_qty)) {
            Swal.fire({
                icon: 'warning',
                title: 'Oops... Stock Qty Exceeded!',
                text: 'You are exceeding the stock current quantity of ' + product_stock_qty,
              })
            $(".product-quantity-"+index).val(product_stock_qty)
        } else {
            $.ajax({
                url: '/ajax/add-to-cart/',
                data: {
                    'id': product_id,
                    'product_meta_title': product_meta_title,
                    'product_is_digital': product_is_digital,
                    'product_types_choices': product_types_choices,
                    'pid': product_pid,
                    'product_types_choices': product_types_choices,
                    'image': product_image,
                    'qty': quantity,
                    'title': product_title,
                    'shipping_amount': product_shipping_amount,
                    'product_gz_coins': product_gz_coins,
                    'vendor': product_vendor,
                    'product_brand': product_brand,
                    'price': product_price,
                    'product_processing_fee': product_processing_fee,
                    'product_tax_fee': product_tax_fee,
                    'product_stock_qty': product_stock_qty,
                    'product_in_stock': product_in_stock,
                },
                dataType: 'json',
                beforeSend: function(){
                    this_val.html("<i class='fas fa-spinner fa-spin'></i>")

                },
                success: function(response){
                    // this_val.html("✓")
                    this_val.html("Added to cart <i class='fas fa-check-circle'></i>")

                    console.log("Added Product to Cart!");
                    $(".cart-items-count").text(response.totalcartitems + " Items")
        
        
                }
            })
        }

    })
    // Update item from cart
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);

		var _pQty=$(".product-qty-"+_pId).val();
        let shipping_amount = $(".product-shipping_amount-" + _pId).val()
        let product_processing_fee = $(".product-product_processing_fee-" + _pId).val()
        let product_tax_fee = $(".product-product_tax_fee-" + _pId).val()
        let product_stock_qty = $(".product-product_stock_qty-" + _pId).val()
        
        if (parseInt(_pQty) > parseInt(product_stock_qty)) {
            Swal.fire({
                icon: 'warning',
                title: 'Oops... Stock Qty Exceeded!',
                text: 'You are exceeding the stock current quantity of ' + product_stock_qty,
              })
            $(".product-qty-"+_pId).val(product_stock_qty)
        } else {
            // Ajax
            $.ajax({
                url:'/ajax/update-cart/',
                data:{
                    'id':_pId,
                    'qty':_pQty,
                    'shipping_amount':shipping_amount,
                    'product_tax_fee':product_tax_fee,
                    'product_processing_fee':product_processing_fee,
                },
                dataType:'json',
                beforeSend:function(){
                    _vm.attr('disabled',true);
                },
                success:function(res){
                    // $(".cart-list").text(res.totalitems);
                    _vm.attr('disabled',false);
                    $("#cartList").html(res.data);
                }
            });
        }

        
		// End
	});



    // Delete item from cart
	$(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/ajax/delete-from-cart/',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
                $(".cart-items-count").text(res.totalcartitems)

			}
		});
		// End
	});
    


    // $(".quantity-arrow-minus").on("click", function() {
    //     let this_val = $(this)
    //     let index = this_val.attr("data-cart-index")
    //     var quantityNum = $(".quantity-num-" + index).val();


    //     if (quantityNum > 1) {
    //         quantityNum --
    //         $(".quantity-num-" + index).val(quantityNum)
    //     }

    // })

    // $(".quantity-arrow-plus").on("click", function () {
    //     let this_val = $(this)
    //     let index = this_val.attr("data-cart-index")
    //     var quantityNum = $(".quantity-num-" + index).val();
    //     quantityNum ++
    //     $(".quantity-num-" + index).val(quantityNum)
    // })



    
    // Making Default Address
    $(document).on("click", ".make-default-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("ID is:", id);
        console.log("Element is:", this_val);

        $.ajax({
            url: "/b/make-default-address/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                console.log("Address Made Default....");
                if (response.boolean == true){

                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()

                    $("#address-alert").text("Address Changed Successfully.")

                }
            }
        })
    })


        // Making Default Billing Address
        $(document).on("click", ".make-default-billing-address", function(){
            let id = $(this).attr("data-billing-id")
            let this_val = $(this)
    
            console.log("ID is:", id);
            console.log("Element is:", this_val);
    
            $.ajax({
                url: "/b/make-billing-default-address/",
                data: {
                    "id":id
                },
                dataType: "json",
                success: function(response){
                    console.log("Address Made Default....");
                    if (response.boolean == true){
    
                        $(".check2").hide()
                        $(".action_btn2").show()
    
                        $(".check2"+id).show()
                        $(".button2"+id).hide()
    
                        $("#address-alert").text("Address Changed Successfully.")
                        $("#address-alert").addClass("alert")
    
                    }
                }
            })
        })



     // Adding to wishlist
     $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)


        console.log("PRoduct ID IS", product_id);

        $.ajax({
            url: "/b/add-to-wishlist/",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding to wishlist...")
            },
            success: function(response){
                

                if (response.data.bool === false && response.data.login_bool === true) {
                    Swal.fire({
                        title: 'Already In Wishlist',
                        width: 600,
                        icon: 'warning',
                        timer: 1000,
                        padding: '3em',
                        color: '#716add',
                        background: '#fff url(/images/trees.png)',
                        backdrop: `
                          rgba(0,0,123,0.4)
                          url("/images/nyan-cat.gif")
                          left top
                          no-repeat
                        `
                      })
                }

                if (response.data.bool === true && response.data.login_bool === true) {
                    // this_val.html("<i class='fas fa-check-circle'></i>")

                    Swal.fire({
                        title: 'Added to Wishlist',
                        width: 600,
                        icon: 'success',
                        timer: 1000,
                        padding: '3em',
                        color: '#716add',
                        background: '#fff url(/images/trees.png)',
                        backdrop: `
                          rgba(0,0,123,0.4)
                          url("/images/nyan-cat.gif")
                          left top
                          no-repeat
                        `
                      })
                }

                if (response.data.bool === null && response.data.login_bool === false) {
                    Swal.fire({
                        title: 'Login to ADD TO WISHLIST',
                        width: 600,
                        icon: 'error',
                        timer: 3000,
                        padding: '3em',
                        color: '#716add',
                        showCancelButton: true,
                        confirmButtonText: 'Login Now',
                        denyButtonText: `Go Back`,
                        background: '#fff url(/images/trees.png)',
                        backdrop: `
                          rgba(0,0,123,0.4)
                          url("/images/nyan-cat.gif")
                          left top
                          no-repeat
                        `
                      }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/user/sign-in/';
                        }
                      })
                      
                      
                }
                
                
            }
        })
    })





    $(document).on("click", "#shipped", function(){
        let id = $(this).attr("data-shipped")
        let val = $(this)
        let alert = $("#delivery_alert")

        console.log("ID:", id);    
        console.log("val:", val);  

        $.ajax({
            url: "/vendor/mark-as-shipped/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                $("#delivery_status"+id).text(response.data.status)
                alert.text("Item marked as " + ' ' + response.data.status)
                if (response.data.bool === true) {
                    console.log(response.data.status);
                }

                  Swal.fire(
                    'Item marked as ' + response.data.status,
                    'successfully.',
                    'success'
                  )
            }
        })
    
    })




    $(document).on("click", "#arrived", function(){
        let id = $(this).attr("data-arrived")
        let val = $(this)
        let alert = $("#delivery_alert")

        console.log("ID:", id);    
        console.log("val:", val);  

        $.ajax({
            url: "/vendor/mark-as-arrived/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                $("#delivery_status"+id).text(response.data.status)
                alert.text("Item marked as " + ' ' + response.data.status)
                if (response.data.bool === true) {
                    console.log(response.data.status);
                }

                Swal.fire(
                'Item marked as ' + response.data.status,
                'successfully.',
                'success'
                )
            }
        })
    })


    $(document).on("click", "#delivered", function(){
        let id = $(this).attr("data-delivered")
        let val = $(this)
        let alert = $("#delivery_alert")

        console.log("ID:", id);    
        console.log("val:", val);  

        $.ajax({
            url: "/vendor/mark-as-delivered/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                $("#delivery_status"+id).text(response.data.status)
                alert.text("Item marked as " + ' ' + response.data.status)
                if (response.data.bool === true) {
                    console.log(response.data.status);
                }

                  Swal.fire(
                    'Item marked as ' + response.data.status,
                    'successfully.',
                    'success'
                  )
            }
        })
    
    })

    

    $(document).on("click", "#accept", function(){
        let id = $(this).attr("data-accept")
        let val = $(this)

        console.log("ID:", id);    
        console.log("val:", val);  

        $.ajax({
            url: "/vendor/mark_as_accepted/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                if (response.data.bool === true) {
                    $("#status"+id).text(response.data.status)
                    console.log(response.data.status);
                }

                  Swal.fire(
                    'Offer marked as ' + response.data.status,
                    'successfully.',
                    'success'
                  )
            }
        })
    
    })

    $(document).on("click", "#reject", function(){
        let id = $(this).attr("data-reject")
        let val = $(this)

        console.log("ID:", id);    
        console.log("val:", val);  

        $.ajax({
            url: "/vendor/mark_as_rejected/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                $("#status"+id).text(response.data.status)
                if (response.data.bool === true) {
                    console.log(response.data.status);
                }

                  Swal.fire(
                    'Offer marked as ' + response.data.status,
                    'successfully.',
                    'success'
                  )
            }
        })
    
    })



    $(document).on("click", "#mark_as_seen", function(){
        let id = $(this).attr("data-noti")
        let val = $(this)
        
        console.log("ID:", id);    
        console.log("val:", val);  

        $.ajax({
            url: "/vendor/mark_as_seen/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                // $("#delivery_status"+id).text(response.data.status)
                // alert.text("Item marked as " + ' ' + response.data.status)
                if (response.data.bool === true) {
                    console.log(response.data.status);
                }

                $(".noti"+id).addClass(" d-none")

                //   Swal.fire(
                //     'Notification Removed',
                //     'successfully.',
                //     'success'
                //   )
            }
        })
    
    })



    $(document).on("click", "#cancel-order", function(){
        let id = $(this).attr("data-order-item")
        let val = $(this)
        
        console.log("ID:", id);    
        console.log("val:", val);  

        $.ajax({
            url: "/b/cancel_orderitem/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                // $("#delivery_status"+id).text(response.data.status)
                // alert.text("Item marked as " + ' ' + response.data.status)
                if (response.data.bool === true) {
                    console.log(response.data.status);
                }

                $(".orderitem"+id).text("Order Cancelled")
                $(".orderitem"+id).removeClass(" btn-danger")
                $(".orderitem"+id).addClass(" btn-success disabled")

                  Swal.fire(
                    'Order Item Cancelled',
                    'successfully.',
                    'success'
                  )
            }
        })
    
    })



    $(document).on("click", "#follow", function(){
        let id = $(this).attr("data-vendor")
        let val = $(this)
        
        console.log("ID:", id);    
        console.log("val:", val);  

        $.ajax({
            url: "/vendor/vendor_follow/",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                if (response.data.bool === true) {
                    console.log("Unfollow");
                    console.log(response.data.followers);
                    $(".followbtn"+id).text("Unfollow")
                    $("#follow_count").text(response.data.followers + " Followers(s)")

                }
                if (response.data.bool === false) {
                    console.log("Follow");
                    console.log(response.data.followers);
                    $(".followbtn"+id).text("Follow")
                    $("#follow_count").text(response.data.followers + " Followers(s)")

                }
            }
        })
    
    })


    $(document).on("click", "#send-btn", function(e){
        e.preventDefault()
        let btn_id = $(this).attr("data-send-btn")
        let input_id = $("#reply"+btn_id).val()

        
        console.log("input_id:", input_id);    
        console.log("btn_id:", btn_id);  

        $.ajax({
            url: "/vendor/send_reply/",
            data: {
                "id":btn_id,
                "reply":input_id
            },
            dataType: "json",
            success: function(response){
                if (response.data.bool === true) {
                    $(".replystatus"+btn_id).text("You Replied")
                    Swal.fire(
                        'Reply Sent',
                        'successfully.',
                        'success'
                      )
                }
            }
        })
    
    })

    $(document).on("click", "#sub-news-letter-btn", function(){
        let email = $("#news-letter-input").val()
        console.log(email);

        $.ajax({
            url:"/base/subscribe_to_newsletter/",
            typeof:"json",
            data:{
                "email":email
            },
            success: function(response){
                console.log(response.data);
                Swal.fire(
                    'Thanks for subscribing',
                    'We will start sending some goodies your way ;)',
                    'success'
                  )
            }
        })
    })



    // $(document).ready(function(){
    //     console.log("Working...")
    //     $.ajax({
    //         url:"{% url 'vendor:get_messages_ajax' reciever_id.username %}",
    //         dataType:"json",
    //         beforeSend: function() {
                
    //         },
    //         success: function(res) {
    //             console.log(res);
    //         }
    //     })
    // })