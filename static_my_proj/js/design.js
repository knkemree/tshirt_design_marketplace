

$(document).ready(function(){
    // Text formatting actions
    console.log('imhere')

    let canvas = new fabric.Canvas('tshirt-canvas');
  
    var deleteIcon = "data:image/svg+xml,%3C%3Fxml version='1.0' encoding='utf-8'%3F%3E%3C!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.1//EN' 'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'%3E%3Csvg version='1.1' id='Ebene_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' width='595.275px' height='595.275px' viewBox='200 215 230 470' xml:space='preserve'%3E%3Ccircle style='fill:%23F44336;' cx='299.76' cy='439.067' r='218.516'/%3E%3Cg%3E%3Crect x='267.162' y='307.978' transform='matrix(0.7071 -0.7071 0.7071 0.7071 -222.6202 340.6915)' style='fill:white;' width='65.545' height='262.18'/%3E%3Crect x='266.988' y='308.153' transform='matrix(0.7071 0.7071 -0.7071 0.7071 398.3889 -83.3116)' style='fill:white;' width='65.544' height='262.179'/%3E%3C/g%3E%3C/svg%3E";
    var cloneIcon = "data:image/svg+xml,%3C%3Fxml version='1.0' encoding='iso-8859-1'%3F%3E%3Csvg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 55.699 55.699' width='100px' height='100px' xml:space='preserve'%3E%3Cpath style='fill:%23010002;' d='M51.51,18.001c-0.006-0.085-0.022-0.167-0.05-0.248c-0.012-0.034-0.02-0.067-0.035-0.1 c-0.049-0.106-0.109-0.206-0.194-0.291v-0.001l0,0c0,0-0.001-0.001-0.001-0.002L34.161,0.293c-0.086-0.087-0.188-0.148-0.295-0.197 c-0.027-0.013-0.057-0.02-0.086-0.03c-0.086-0.029-0.174-0.048-0.265-0.053C33.494,0.011,33.475,0,33.453,0H22.177 c-3.678,0-6.669,2.992-6.669,6.67v1.674h-4.663c-3.678,0-6.67,2.992-6.67,6.67V49.03c0,3.678,2.992,6.669,6.67,6.669h22.677 c3.677,0,6.669-2.991,6.669-6.669v-1.675h4.664c3.678,0,6.669-2.991,6.669-6.669V18.069C51.524,18.045,51.512,18.025,51.51,18.001z M34.454,3.414l13.655,13.655h-8.985c-2.575,0-4.67-2.095-4.67-4.67V3.414z M38.191,49.029c0,2.574-2.095,4.669-4.669,4.669H10.845 c-2.575,0-4.67-2.095-4.67-4.669V15.014c0-2.575,2.095-4.67,4.67-4.67h5.663h4.614v10.399c0,3.678,2.991,6.669,6.668,6.669h10.4 v18.942L38.191,49.029L38.191,49.029z M36.777,25.412h-8.986c-2.574,0-4.668-2.094-4.668-4.669v-8.985L36.777,25.412z M44.855,45.355h-4.664V26.412c0-0.023-0.012-0.044-0.014-0.067c-0.006-0.085-0.021-0.167-0.049-0.249 c-0.012-0.033-0.021-0.066-0.036-0.1c-0.048-0.105-0.109-0.205-0.194-0.29l0,0l0,0c0-0.001-0.001-0.002-0.001-0.002L22.829,8.637 c-0.087-0.086-0.188-0.147-0.295-0.196c-0.029-0.013-0.058-0.021-0.088-0.031c-0.086-0.03-0.172-0.048-0.263-0.053 c-0.021-0.002-0.04-0.013-0.062-0.013h-4.614V6.67c0-2.575,2.095-4.67,4.669-4.67h10.277v10.4c0,3.678,2.992,6.67,6.67,6.67h10.399 v21.616C49.524,43.26,47.429,45.355,44.855,45.355z'/%3E%3C/svg%3E%0A"
    
    var deleteImg = document.createElement('img');
    deleteImg.src = deleteIcon;
    var cloneImg = document.createElement('img');
    cloneImg.src = cloneIcon;
  
    fabric.Object.prototype.transparentCorners = true;
    fabric.Object.prototype.cornerColor = '#B2CCFF';
    fabric.Object.prototype.cornerStyle = 'circle';
    fabric.Object.prototype.cornerSize = 10;
  
    var fonts = ["Graduate",'Bangers','Boogaloo','Caveat','Caveat Brush','Chela One','Cherry Swash','Coiny','Concert One','Creepster','Fredoka One','Germania One','Knewave','Montserrat','Open Sans','Oswald','Permanent Marker','Rammetto One','Shrikhand','Spicy Rice','Vampiro One','Vollkorn','Wendy One'];
  
    // When the user clicks on upload a custom picture
    document.getElementById('id_uploaded_image').addEventListener("change", function(e){
      console.log('image changed')
        var reader = new FileReader();  
        
        reader.onload = function (event){
            var imgObj = new Image();
            imgObj.src = event.target.result;
            $('#id_design').val(e.target.result);
            // When the picture loads, create the image in Fabric.js
            imgObj.onload = function () {
                var img = new fabric.Image(imgObj);
  
                img.scaleToHeight(100);
                img.scaleToWidth(100);  
                canvas.centerObject(img);
                canvas.add(img);
                canvas.renderAll();
            };
        };
  
        // If the user selected a picture, load it
        if(e.target.files[0]){
            reader.readAsDataURL(e.target.files[0]);
        }
    }, false);
  
    // When the user selects a picture that has been added and press the DEL key
    // The object will be removed !
    document.addEventListener("keydown", function(e) {
        var keyCode = e.keyCode;
        if(keyCode == 46){
            canvas.remove(canvas.getActiveObject());
            $("#text-string").val("");
        }
    }, false);
  
    $('#fill').change(function(){
        var obj = canvas.getActiveObject();
  
        if(obj){
            // old api
            // obj.setFill($(this).val());
            obj.set("fill", this.value);
        }
        canvasModifiedCallback();
        canvas.renderAll();
        });
  
    $('#stroke').change(function(){
    var obj = canvas.getActiveObject();
  
    if(obj){
        // old api
        // obj.setFill($(this).val());
        obj.set("stroke", this.value);
    }
    canvasModifiedCallback();
    canvas.renderAll();
    });
  
    $('#shadow').change(function(){
    var obj = canvas.getActiveObject();
  
    if(obj){
        // old api
        // obj.setFill($(this).val());
        // Create shadow object 
        var shadow = new fabric.Shadow({ 
            color: this.value, 
            affectStroke: false,
            
            blur: 5, 
        });
        obj.set("shadow", shadow);
    }
    canvasModifiedCallback();
    canvas.renderAll();
  
    });
  
    
    // Add text
    function Addtext(text) {
        var iTextSample = new fabric.IText(text, {
            left: 50,
            top: 50,
            width: 150,
            fontSize: 50,
            fontFamily: 'Times New Roman',
            fill: '#333',
            // lineHeight: 1.1,
            strokeWidth: 4,
            shadow: shadow,
            paintFirst: 'stroke', // stroke behind fill
            // styles: {
            //     0: {
            //     0: { textDecoration: 'underline', fontSize: 80 },
            //     1: { textBackgroundColor: 'red' }
            //     },
            //     1: {
            //     0: { textBackgroundColor: 'rgba(0,255,0,0.5)' },
            //     4: { fontSize: 20 }
            //     }
            // }
            });
        iTextSample.setControlsVisibility({
            mt: false, // middle top disable
            mb: false, // midle bottom
            ml: false, // middle left
            mr: false, // I think you get it
        });
        
        
  
        canvas.on('text:changed', function(opt) {
            
            var iTextSample = opt.target;
            if ( iTextSample.width >  250) {
                    iTextSample.fontSize *=  250 / ( iTextSample.width + 1);
                    iTextSample.width =  250;
            };
              
  
          });
        
        canvas.add(iTextSample).setActiveObject(iTextSample);
        canvas.centerObject(iTextSample);
        
    };
  
    
  
    fonts.unshift('Times New Roman');
    // Populate the fontFamily select
    var select = document.getElementById("font-family");
        fonts.forEach(function(font) {
        var option = document.createElement('option');
        option.innerHTML = font;
        option.value = font;
        option.style.fontFamily = font;
        select.appendChild(option);
    });
    
  
    // Apply selected font on change
    document.getElementById('font-family').onchange = function() {
    if (this.value !== 'Times New Roman') {
        loadAndUse(this.value);
        canvasModifiedCallback();
        canvas.requestRenderAll();
    } else {
        canvas.getActiveObject().set("stroke", this.value);
        canvas.requestRenderAll();
    }
    };
  
    
  
    function loadAndUse(font) {
    var myfont = new FontFaceObserver(font)
    myfont.load()
        .then(function() {
        // when font is loaded, use it.
        canvas.getActiveObject().set("fontFamily", font);
        canvas.requestRenderAll();
        }).catch(function(e) {
        alert("Can't load " + font +". Did you choose the text?");
        });
    };
  
    function  renderIcon(icon){                            
        return function renderIcon(ctx, left, top, styleOverride, fabricObject) {
        var size = this.cornerSize;
        ctx.save();
        ctx.translate(left, top);
        ctx.rotate(fabric.util.degreesToRadians(fabricObject.angle));
        ctx.drawImage(icon, -size/2, -size/2, size, size);
        ctx.restore();
        }
    }
  
    fabric.Object.prototype.controls.deleteControl = new fabric.Control({
        x: 0.5,
        y: -0.5,
        // offsetY: -16,
        // offsetX: 16,
        offsetY: 0,
        offsetX: 0,
        cursorStyle: 'pointer',
        mouseUpHandler: deleteObject,
        render: renderIcon(deleteImg),
        cornerSize: 18
    });
  
    fabric.Object.prototype.controls.clone = new fabric.Control({
        x: -0.5,
        y: -0.5,
        // offsetY: -16,
        // offsetX: -16,
        offsetY: -12,
        offsetX: -12,
        cursorStyle: 'pointer',
        mouseUpHandler: cloneObject,
        render: renderIcon(cloneImg),
        cornerSize: 14
    });
  
    function deleteObject(eventData, target) {
            var canvas = target.canvas;
                canvas.remove(target);
            canvas.requestRenderAll();
        }
  
    function cloneObject(eventData, target) {
        var canvas = target.canvas;
        target.clone(function(cloned) {
        cloned.left += 10;
        cloned.top += 10;
        canvas.add(cloned);
        });
    }
  
    $(document).ready(function() {
    $('#text-font-size').keyup(function() {
        var val = $(this).val();
        if (isNaN(val)) {
        alert('please enter number');
        $(this).val('');
        }
        var activeObject = canvas.getActiveObject();
        activeObject.fontSize = val;
        canvas.renderAll();
    });
    $('#add-text-btn').click(function() {
        if ($('#text-font-size').val()) {
        var txtfontsize = $('#text-font-size').val();
        } else {
        var txtfontsize = 40;
        }
        var message = $('#add-text-value').val();
        var txtfontfamily = $('#font-family').val();
        var new_text = new fabric.IText(message, {
        left: 100,
        top: 100,
        fontSize: txtfontsize,
        lockUniScaling: true,
        fontFamily: txtfontfamily,
        fill: '#000'
        });
        canvas.add(new_text);
        canvas.setActiveObject(new_text);
    });

    var canvasModifiedCallback = function() {
      console.log('canvas modified!');
      var dataUrl = canvas.toDataURL();
      $('#id_design').val(dataUrl);
      canvas.renderAll();
      var mockup_id = $(".cz-preview-item.active :input").val();
      $('#id_mockup').val(mockup_id)
      
      var node = document.getElementById('tshirt-div');
      domtoimage.toPng(node).then(function (dataUrl) {
          
          var img = new Image();
          var options = {
          quality: 0.99,
          };
          img.src = dataUrl;
          document.body.appendChild(img);
          $('#id_end_product_img').val(dataUrl) 
          
      }).catch(function (error) {
        console.error('oops, something went wrong!', error);
      });
    };
  
    canvas.on('object:added', canvasModifiedCallback);
    canvas.on('object:removed', canvasModifiedCallback);
    canvas.on('object:modified', canvasModifiedCallback);
  
    canvas.on('object:selected', function(options) {
        if (options.target) {
        $("textarea#add-text-value").val(options.target.text);
        $("#text-font-size").val(options.target.fontSize);
        }
    });
  
    canvas.on('object:scaling', function(event) {
        if (event.target) {
        $("textarea#add-text-value").val(event.target.text);
        $("#text-font-size").val((event.target.fontSize * event.target.scaleX).toFixed(0));
        }
    });
  
    canvas.on('object:modified', function(event) {
        if (event.target) {
        event.target.fontSize *= event.target.scaleX;
        event.target.fontSize = event.target.fontSize.toFixed(0);
        event.target.scaleX = 1;
        event.target.scaleY = 1;
        event.target._clearCache();
        $("textarea#add-text-value").val(event.target.text);
        $("#text-font-size").val(event.target.fontSize);
        }
    });
    canvas.on({
         'object:moving': function(e) {		  	
            e.target.opacity = 0.5;
          },
          'object:modified': function(e) {		  	
            e.target.opacity = 1;
          },
         
         'selection:cleared':onSelectedCleared
       });
  
    });
  
    
  canvas.on('mouse:move', function(e) {
    //turn off selection
    canvas.selection = false;
  });
  canvas.on('object:removed', function(e) {
    //turn off selection
    canvas.getActiveObject();
    canvas.selection = false;
  });

  $('#btn-underline').on('click', function(){
    dtEditText('underline');
  });
  $('#btn-bold').on('click', function(){
    dtEditText('bold');
  });
  $('#btn-italic').on('click', function(){
    dtEditText('italic');
  }); 

  // Functions
  function dtEditText(action) {
      var a = action;
      var o = canvas.getActiveObject();
      var t;

      // If object selected, what type?
      if (o) {
          t = o.get('type');
      }

      if (o && t === 'i-text') {
          switch(a) {
              case 'bold':				
                  var isBold = dtGetStyle(o, 'fontWeight') === 'bold';
                  dtSetStyle(o, 'fontWeight', isBold ? '' : 'bold');
              break;

              case 'italic':
                  var isItalic = dtGetStyle(o, 'fontStyle') === 'italic';
                  dtSetStyle(o, 'fontStyle', isItalic ? '' : 'italic');
              break;

              case 'underline':
                  var isUnderline = dtGetStyle(o, 'textDecoration') === 'underline';
                  dtSetStyle(o, 'textDecoration', isUnderline ? '' : 'underline');
              break;
              canvas.renderAll();
          }
      }
  }

  // Get the style
  function dtGetStyle(object, styleName) {
      return object[styleName];
  }

  // Set the style
  function dtSetStyle(object, styleName, value) {
      object[styleName] = value;
      object.set({dirty: true});
      canvas.renderAll();
  }
})  

  function rasterizeJSON(){
    // raterized = JSON.stringify(canvas.toObject());
    raterized = JSON.stringify(canvas.toDatalessJSON());
    // localStorage.setItem('Kanvas', raterized);
    // sessionStorage.setItem("lastname", raterized);
    $('#id_json_data').val(raterized);
  }

  function saveCanvasToJSON() {
    const json = JSON.stringify(canvas);
    localStorage.setItem('Kanvas', json);

  }

  function loadCanvasFromJSON() {
    const CANVAS = localStorage.getItem('Kanvas');
    canvas.loadFromJSON(CANVAS, () => {
      console.log('CANVAS untar');
      console.log(CANVAS);

      // making sure to render canvas at the end
      canvas.renderAll();

      // and checking if object's "name" is preserved
      console.log('this.canvas.item(0).name');
      console.log(canvas);
    });
  }

  $('#loadFromJSON').on('click', function(){
    loadCanvasFromJSON();
  })

  $('#saveToLocal').on('click', function(){
    saveCanvasToJSON();
  })

  $('#toJson').on('click', function(){
    console.log(JSON.stringify(canvas.toSVG()))
  })

  $('#add-text').on('click', function(){
    var text = $('#text-string').val();
    if(text != ''){
      Addtext(text);
      $('#text-string').val('')
    }else{
      alert('Text area empty')
      $('#text-string').val('')
    };

    
  })
