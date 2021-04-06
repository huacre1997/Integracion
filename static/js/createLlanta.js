  $(document).ready(function () {
 
    $("#btn-click").on("click", function (param) {
      document.getElementById("btn-click").disabled = true

      $("#submit-form").click()
    })
    $("#inspeccion-form").on("submit", function (e) {
      e.preventDefault()
      if (objeto.items.length === 0) {
        notificacion(2000, "Debes ingresar almenos na llanta!", "error")
        return false;
      }

      var parameters = new FormData(this);
      parameters.append("objeto", JSON.stringify(objeto.items))
      $.ajax({
        type: "POST",
        url: $(this).attr("action"),
        data: parameters,
        dataType: "json",
        processData: false,
        contentType: false,
        success: function (response) {
          document.getElementById("btn-click").disabled = false
          if (response.status = 200) {
            notificacion(1500, "Genial!", "success", "Datos Guardados!")
          } else {
            notificacion(1500, "Error", "error", "Ese usuario no existe")

          }
        }
      }).done(function (data) {


      }).fail(function (jqXHR, textStatus, errorThrown) {
        alert("done:" + textStatus + ': ' + errorThrown);
      }).always(function (data) {

      });;

    });

    var tablaLLantas
    var data = {
      ubicacion: "",
      codigo: "",
      vehiculo: {
        disabled:false,
        placa:""
      },
      posicion:{
        disabled:false,
        numero:""
      },
      marca: "",
      modelo: "",
      medida: "",
      estado: "",
      repuesto:  {
        disabled:false,
        r:false
      },
      cubierta: {
        categoria: "",
        fech_ren: "",
        km: 0,
        costo: 0.00,
        altura: 0.00,
        altura_ini: 0.00,
        altura_fin: 0.00,
        nro_reencauchado: null,
        renovadora: null,
        ancho_banda: null,
        modelo_banda: null
      }
    }
    var objeto = {

      items: [],
      
      list: function () {

        tablaLLantas = $("#tablaLlanta").removeAttr('width').DataTable({
          searching: false,
          ordering: false,
          paging: false,
          data: this.items,
          destroy: true,
          "scrollX": true,
          autoWidth: false,
          columns: [

            {
              "data": 'ubicacion',
              className: "middle",
            },
            {
              "data": 'codigo',
              className: "middle"
            },
            {
              "data": 'vehiculo.placa',
              className: "middle"
            },
            {
              "data": 'posicion.numero',
              className: "middle"
            },
            {
              "data": "repuesto.r",
              className: "middle text-center"

            },
            {
              "data": "marca",
              className: "middle"

            },
            {
              "data": "modelo",
              className: "middle"

            },
            {
              "data": 'medida',
              className: "middle"
            },
            {
              "data": 'estado',
              className: "middle"
            },

            {
              "data": 'cubierta.fech_ren',
              className: "middle"
            },
            {
              "data": 'cubierta.km',
              className: "middle"
            },
            {
              "data": 'cubierta.costo',
              className: "middle"
            },
            {
              "data": 'cubierta.altura_ini',
              className: "middle"
            },

            {
              "data": 'cubierta.altura_fin',
              className: "middle"
            },
            {
              "data": null,
              className: "middle"
            },
          ],
          columnDefs: [

            {
              targets: [0],
              width: 150,
              render: function (data, type, row) {
                var $select = $('<select name="ubicacion"  class="form-select">' +
                  ' <option value="0">Seleccione...</option>' +
                  '{% for i in ubicacion  %}' +
                  '<option value="{{i.id}}">{{i.descripcion}}</option>' +
                  '{% endfor %}' +
                  '</select>');
                $select.find('option[value="' + row.ubicacion + '"]').attr('selected', 'selected');
                return $select[0].outerHTML


              }
            },
            {
              targets: [1],
              render: function (data, type, row) {
           
                return `<input type="text" name="codigo" class="form-control" maxlength="100" value="${data}">`;
                
              }
            },
            {
              targets: [2],
              width: 150,

              render: function (data, type, row) {
                console.log(data)
                if(row.data!=""){
                if(row.vehiculo.disabled)
                {
                  var $select = $('<select name="vehiculo"  class="form-select">' +
        
                  '</select>');
                $select.find('option[value="' + row.vehiculo + '"]').attr('selected', 'selected');
                return $select[0].outerHTML

                  }
                  else{
                    var $select = $('<select name="vehiculo" disabled  class="form-select">' +
                  ' <option value="0">Seleccione...</option>' +
                  '{% for i in vehiculo  %}' +
                  '<option value="{{i.id}}">{{i.placa}}</option>' +
                  '{% endfor %}' +
                  '</select>');
                $select.find('option[value="' + row.vehiculo + '"]').attr('selected', 'selected');
                return $select[0].outerHTML
                  }
              
                }else{
                  var $select = $('<select name="vehiculo"  class="form-select">' +
                  ' <option value="0">Seleccione...</option>' +
                  '{% for i in vehiculo  %}' +
                  '<option value="{{i.id}}">{{i.placa}}</option>' +
                  '{% endfor %}' +
                  '</select>');
                return $select[0].outerHTML
                }

              }
            },
            {
              targets: [3],
              width: 50,

              render: function (data, type, row) {
                if(row.data!=""){

                if(row.posicion.disabled)
                  {
                    return `<input type="text" name="posicion" value="${data}" class="form-control" >`;

                  }
                  else{
                    return `<input type="text" name="posicion" disabled  class="form-control">`;

                  }}else{
                    return `<input type="text" name="posicion"  class="form-control">`;

                  }
              }
            },
            {
              targets: [4],
              render: function (data, type, row) {
                console.log(row)
                if(row.data!=""){

               if(row.repuesto.disabled){
                return `<div class="form-check"> <input type="checkbox" name="repuesto"  disabled class="form-check-input"></div>`;

               }else{
                return `<div class="form-check"> <input type="checkbox" name="repuesto"   class="form-check-input"></div>`;

               }
              }else{
                return `<div class="form-check"> <input type="checkbox" name="repuesto"  class="form-check-input"></div>`;

              }
              }
            },
            {
              targets: [5],
              width: 150,

              render: function (data, type, row) {
                var $select = $('<select name="marca_llanta"  class="form-select">' +
                  ' <option value="0">Seleccione...</option>' +
                  '{% for i in marca_llanta  %}' +
                  '{% if  i.activo and not i.eliminado or obj.modelo_llanta.marca_llanta.id == i.id %}' +
                  '<option value="{{i.id}}">{{i.descripcion}}</option>' +
                  '{% endif %}' +
                  '{% endfor %}' +
                  '</select>');
                $select.find('option[value="' + row.marca + '"]').attr('selected', 'selected');
                return $select[0].outerHTML


              }
            },
            {
              targets: [6],
              width: 150,

              render: function (data, type, row) {
                var $select = $('<select name="modelo_llanta"  class="form-select">' +
                  ' <option value="0">Seleccione...</option>' +

                  '</select>');
                $select.find('option[value="' + row.modelo + '"]').attr('selected', 'selected');
                return $select[0].outerHTML


              }
            },
            {
              targets: [7],
              width: 220,

              render: function (data, type, row) {
                var $select = $('<select name="medida_llanta"  class="form-select">' +
                  ' <option value="0">Seleccione...</option>' +

                  '{% for i in medida_llanta  %}' +
                  '{% if  i.activo and not i.eliminado or obj.medida_llanta.id == i.id %}' +
                  '<option value="{{i.id}}" {% if obj.medida_llanta.id == i.id %}selected{% endif %}>Medida {{i.medida}}-{{i.profundidad}}' +
                  '{% if i.capas %}' +
                  '-{{i.capas}}' +
                  '{% else %}' +
                  '{% endif %}' +
                  '</option>' +
                  '{% endif %}' +
                  '{% endfor %}' +
                  '</select>');
                $select.find('option[value="' + row.medida + '"]').attr('selected', 'selected');
                return $select[0].outerHTML


              }
            },
            {
              targets: [8],
              width: 180,

              render: function (data, type, row) {

                var $select = $('<select name="estado_llanta"  class="form-select">' +
                  ' <option value="0">Seleccione...</option>' +
                  '{% for i in estado  %}' +
                  '<option value="{{i.0}}">{{i.1}}</option>' +
                  '{% endfor %}' +
                  '</select>');
                $select.find('option[value="' + row.estado + '"]').attr('selected', 'selected');
                return $select[0].outerHTML
              }
            },
            {
              targets: [9],
              render: function (data, type, row) {

                return `<input type="date" name="fech_ren" class="form-control" value="${data}" style="width:200px">`;

              }
            },
            {
              targets: [10],
              render: function (data, type, row) {

                return `<input type="number" name="km" min="0.00" step="0.01" class="form-control" value="${data}">` ;

              }
            },
            {
              targets: [11],
              render: function (data, type, row) {

                return `<input type="number" name="costo" step="0.01" class="form-control" value="${data}">`;

              }
            },
            {
              targets: [12],
              render: function (data, type, row) {

                return `<input type="number" name="a_inicial" step="0.01" class="form-control" value="${data}" >`;

              }
            },
            {
              targets: [13],
              render: function (data, type, row) {

                return `<input type="number" name="a_final" step="0.01" class="form-control" value="${data}">`;

              }
            },
            {
              targets: [14],
              render: function (data, type, row) {

                return `<button class="btn btn-primary btn-add"><i class="fas fa-plus"></i></button>`;

              }
            },
          ],
          "language": {

            "processing": '<div class="spinner-border text-primary" style="width: 3rem; height: 3rem; role="status"><span class="sr-only">Loading...</span></div>',
            "lengthMenu": "Mostrar _MENU_ registros",
            "zeroRecords": "No se encontraron resultados",
            "emptyTable": "Ningún dato disponible en esta tabla",
            "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
            "infoFiltered": "(filtrado de un total de _MAX_ registros)",
            "search": "Buscar:",
            "infoThousands": ",",
            "loadingRecords": "Cargando...",

          },
          initComplete: function (settings, json) {
            $("#tablaLlanta tbody").on("click",".btn-add", function (e) {
              console.log("aclick tabla")
                $(this).children().remove()
                $(this).append('<i class="fas fa-check"></i>')
                $(this).removeClass("btn-primary").addClass("btn-success")
                var tr = tablaLLantas.cell($(this).closest("td", "li")).index()
                data.ubicacion=$("td:eq(0)", tablaLLantas.row(tr.row).node()).children().val()
                data.codigo=$("td:eq(1)", tablaLLantas.row(tr.row).node()).children().val()
                data.vehiculo.placa=$("td:eq(2)", tablaLLantas.row(tr.row).node()).children().val()
                data.vehiculo.disabled=false
                data.posicion.numero=$("td:eq(3)", tablaLLantas.row(tr.row).node()).children().val()
                data.posicion.disabled=false
                data.repuesto.r=$("td:eq(4)", tablaLLantas.row(tr.row).node()).children().is(":checked")
                data.repuesto.disabled=false
                data.marca=$("td:eq(5)", tablaLLantas.row(tr.row).node()).children().val()
                data.modelo=$("td:eq(6)", tablaLLantas.row(tr.row).node()).children().val()
                data.medida=$("td:eq(7)", tablaLLantas.row(tr.row).node()).children().val()
                data.estado=$("td:eq(8)", tablaLLantas.row(tr.row).node()).children().val()
                data.cubierta.fech_ren=$("td:eq(9)", tablaLLantas.row(tr.row).node()).children().val()
                data.cubierta.km=$("td:eq(10)", tablaLLantas.row(tr.row).node()).children().val()
                data.cubierta.costo=$("td:eq(11)", tablaLLantas.row(tr.row).node()).children().val()
                data.cubierta.altura_ini=$("td:eq(12)", tablaLLantas.row(tr.row).node()).children().val()
                data.cubierta.altura_fin=$("td:eq(13)", tablaLLantas.row(tr.row).node()).children().val()

                objeto.items.push(data)
                objeto.list()
                console.log(objeto.items)
                 data = {
      ubicacion: "",
      codigo: "",
      vehiculo: {
        disabled:false,
        placa:""
      },
      posicion:{
        disabled:false,
        numero:""
      },
      marca: "",
      modelo: "",
      medida: "",
      estado: "",
      repuesto:  {
        disabled:false,
        r:false
      },
      cubierta: {
        categoria: "",
        fech_ren: "",
        km: 0,
        costo: 0.00,
        altura: 0.00,
        altura_ini: 0.00,
        altura_fin: 0.00,
        nro_reencauchado: null,
        renovadora: null,
        ancho_banda: null,
        modelo_banda: null
      }}
                tablaLLantas.row.add(data).draw()
            })
            $(".dataTables_scrollBody").mousewheel(function(event, delta) {

this.scrollLeft -= (delta * 50);

event.preventDefault();

});
            $("#tablaLlanta tbody").on("change", "select[name='marca_llanta']", function (e) {
              e.preventDefault();
              select = $(this).parent().next().children()
              select.empty();
              select.append($("<option>", {
                value: "",
                text: " --------- "
              }));
           
               fetch( '/catalogos/render-option-llanta/'+$(this).val()).then(res=> res.json()).then(data=>{
          console.log(data)
          select.prop("disabled", false)
          $.each(data, function (index, valuex) {
            if (!valuex.eliminado && valuex.activo) {
              let opcion = document.createElement("option")
              opcion.value = valuex.id
              opcion.textContent = valuex.descripcion
              select.append(opcion)

            }
          });
          // if ($("#id_marca_llanta").val() == marca2) {
          //   let array4 = document.getElementById("id_modelo_llanta").options
          //   let options4 = []
          //   for (let i = 0; i < array4.length; i++) {
          //     const element4 = array4[i].value;
          //     options4.push(element4)
          //   }

          //   if (options4.includes(modelo2) != true) {

          //     let option4 = document.createElement("option")
          //     option4.textContent = "{{obj.modelo_llanta.descripcion}}"
          //     option4.selected = true
          //     option4.value = modelo2

          //     $("#id_modelo_llanta").append(option4)

          //   } else {
          //     document.getElementById('id_modelo_llanta').value = modelo2;

          //   }
          // }

          select.prop("disabled", false)

                })
             
         
                
            
           
            })
            $("#tablaLlanta tbody ").on("change", "select[name='ubicacion']", function (e) {
              e.preventDefault();
              select = $(this).parent()
              console.log($(this).children()[$(this).val()].innerHTML)
              if($(this).children()[$(this).val()].innerHTML!="MONTADO"){
                select.next().next().children().prop("disabled",true).val("")
                select.next().next().next().children().prop("disabled",true).val("")
                select.next().next().next().next().children().children().prop("disabled",true).val("")
              }else{
                select.next().next().children().prop("disabled",false)
                select.next().next().next().children().prop("disabled",false)
                select.next().next().next().next().children().children().prop("disabled",false)
              }
           
       
             
         
                
            
           
            })





          }
        });
      }
    }



    objeto.list()
    tablaLLantas.row.add(data).draw()

  });
