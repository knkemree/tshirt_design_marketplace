$(document).ready(function(){
    $( ".cz-preview-item:first" ).addClass('active');
    $( ".cz-thumblist-item:first" ).addClass('active');

    function apply_current_price(){
      $.ajax({
        url : '{% url "essentials:change_place" %}', // the endpoint
        data : {
          'product_id':$('#productid').val(),
          'place_id': $('.cz-thumblist-item.active').attr('id'),
          'method_id': $( "#technique" ).val(),
          'size_id': $('#size-selector').val(),
          'color_id': $('input[name=colorid]:checked', '#post-color').val(),
        }, // data sent with the post request
        dataType: 'json',
        // handle a successful response
        success : function(data) {
            // console.log(data.price_all_included); 
            $('#price').text("$"+data.price_all_included);
        },       
      });
    };

    $('#post-placement').on('click', function(event){
      event.preventDefault(); 
      apply_current_price();
    });


    var variant_add_to_cart_url //set global variable otherwise undefined


    function ajax_dynamic_canvas(){
      $.ajax({ 
        url: "{% url 'essentials:dynamic_canvas' %}",
        data: {
          'product_id': $('#productid').val(),
        },
        dataType: 'json',
        success: function(data){
          var place_id = $('.cz-thumblist-item.active').attr('id') ;
          console.log(data[place_id].top); // another sanity check
          $("#drawingArea").css({ top: data[place_id].top });
          $("#drawingArea").css({ left: data[place_id].left });
          $("#drawingArea").css({ width: data[place_id].width });
          $("#drawingArea").css({ height: data[place_id].height });
          $("#canvas-container").css({ height: data[place_id].height });
          $("#canvas-container").css({ width: data[place_id].width });
          h = parseInt(data[place_id].height, 10)
          w = parseInt(data[place_id].width, 10)
          canvas.setWidth(w);
          canvas.setHeight(h)
        }}
      )
    };

    setTimeout(ajax_dynamic_canvas(),1000);

    function apply_placement_id(){
      var placement_id = $('.cz-thumblist-item.active').attr('id');
      $( "#id_placement" ).val(placement_id);
    };

    $('.cz-thumblist-item').on('click', function(event){
      var place_id = $('.cz-thumblist-item.active').attr('id');
      apply_placement_id();
      ajax_dynamic_canvas();
    });

    setTimeout(apply_placement_id(),1000);

    function ajax_change_method(){
      var tech = $( "#technique" ).val();
      $( "#id_technique" ).val(tech);
      $.ajax({ 
        url: "{% url 'essentials:change_method' %}",
        data: {
          'product_id':$('#productid').val(),
          'place_id': $('.cz-thumblist-item.active').attr('id'),
          'method_id': $( "#technique" ).val(),
          'size_id': $('#size-selector').val(),
          'color_id': $('input[name=colorid]:checked', '#post-color').val(),
        },
        dataType: 'json',
        success: function(data){
          // console.log(data.price_all_included); 
          $('#price').text("$"+data.price_all_included);
        }
      });

    };

    // send ajax request on load print metodunu saptamak icin
    ajax_change_method();

    // send ajax request on change print metodunu saptamak icin
    $(document).on('change', '#post-technique',function(e){
      var tech = $( "#technique" ).val();
      $( "#id_technique" ).val(tech);
      ajax_change_method();
    });

    function change_image_color(){
      var codeOrTexture = $('input[name=hexOrTexture]', '#post-color').val();
      console.log('code or texture?')
      console.log(codeOrTexture)
      let texture = codeOrTexture.startsWith("/");
      console.log(texture)
      if (texture) {
        document.getElementById("tshirt-div").style.backgroundImage = "url(" + codeOrTexture + ")";
        $(".thumbnail_image").css("background-image", "url(" + codeOrTexture + ")");

      } else {
        document.getElementById("tshirt-div").style.backgroundColor = codeOrTexture;
        $(".thumbnail_image").css("background-color", codeOrTexture);
      };
    };

    change_image_color();

    function ajax_change_size(){
      $.ajax({
        url:'{% url "essentials:change_size" %}',
        data:{
            product_id:$('#productid').val(),
            size:$('#size-selector').val(),
            'method_id': $( "#technique" ).val(),
            'place_id': $('.cz-thumblist-item.active').attr('id'),
            'color_id': $('input[name=colorid]:checked', '#post-color').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]', '#post-size').val(),
        },
        success: function (data) {

            // apply color options
            $('#appendHere').html(data.rendered_table);

            //apply price
            $('#price').text("$"+data.price_all_included);

            // aplly add to cart
            variant_add_to_cart_url = data.variant_add_to_cart_url

            // apply color
            let texture = data.color_id.startsWith("/");
            console.log(texture)

            if (texture) {
            document.getElementById("tshirt-div").style.backgroundImage = "url(" + data.color_id + ")";
            $(".thumbnail_image").css("background-image", "url(" + data.color_id + ")");
            
            } else {
              if(document.getElementById("tshirt-div").style.backgroundImage){
                $("#tshirt-div").css('background-image', 'none');
                $(".thumbnail_image").css('background-image', 'none');
              };
              document.getElementById("tshirt-div").style.backgroundColor = data.color_id;
              $(".thumbnail_image").css("background-color", data.color_id);
            };
        },
        error: function (data) {
            alert("Got an error! " + data);
        }
      });
      
    };

    $(document).on('change', '#post-size',function(e){
      e.preventDefault();
      ajax_change_size();
    });

    function ajax_change_color(){
      $.ajax({ 
        url: "{% url 'essentials:change_color' %}",
        data: {
            'product_id':$('#productid').val(),
            'place_id': $('.cz-thumblist-item.active').attr('id'),
            'method_id': $( "#technique" ).val(),
            'size_id': $('#size-selector').val(),
            'color_id': $('input[name=colorid]:checked', '#post-color').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]', '#post-color').val(),
        },
        dataType: 'json',
        success:  function(data){
            let texture = data.color_id.startsWith("/");
            console.log('calisan burasi')
            console.log(data.color_id)  
            console.log(texture)
            if (texture) {
            document.getElementById("tshirt-div").style.backgroundImage = "url(" + data.color_id + ")";
            $(".thumbnail_image").css("background-image", "url(" + data.color_id + ")");
            
            } else {
              if(document.getElementById("tshirt-div").style.backgroundImage){
                $("#tshirt-div").css('background-image', 'none');
                $(".thumbnail_image").css('background-image', 'none');
              };
              document.getElementById("tshirt-div").style.backgroundColor = data.color_id;
              $(".thumbnail_image").css("background-color", data.color_id);
            };

            $('#price').text("$"+data.price_all_included);

            variant_add_to_cart_url = data.variant_add_to_cart_url
            console.log(data);
        }
      });
    };


    $('input[name=colorid]', '#post-color').change(function(){
      setTimeout(ajax_change_color(),1000)
      // ajax_change_color();
    });

    function add_to_cart() {
      canvas.discardActiveObject();
      canvas.renderAll();
      $(document.body).css({'cursor' : 'wait'});
      $( "#addtocartButton" ).addClass('disabled');
      var add_to_cart_form = $('#addtocartform');
      var action = add_to_cart_form.attr('action');
      var method = add_to_cart_form.attr('method');
      var cart_data = add_to_cart_form.serialize();
      $.ajax({
          url : variant_add_to_cart_url, // the endpoint
          type : method, // http method
          data : cart_data, // data sent with the post request
          // handle a successful response
          success : function(data) {
              console.log("success"); // another sanity check
              location.href = '/cart/'
              $(document.body).css({'cursor' : 'default'});
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
            $(document.body).css({'cursor' : 'default'});
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    };

    $('#addtocartform').on('submit', function(event){
      event.preventDefault();
      console.log("form submitted!"); 
      rasterizeJSON();
      setTimeout(add_to_cart(),3000);
    });

    $( "#addtocartform" ).mouseover(function() {
      canvas.discardActiveObject();
      canvas.renderAll();
    });
});