$(document).ready(function () {


  $('#drop-vehiculos').select2();
  let td_placa = document.getElementById("td_placa")
  let td_tipo = document.getElementById("td_tipo")
  let td_modelo = document.getElementById("td_modelo")
  let td_marca = document.getElementById("td_marca")
  let td_km = document.getElementById("td_km")
  let td_obs = document.getElementById("td_obs")
  let operador = document.getElementById("td_operador")

  var datos = {
    items: {
      vehiculo_id: "",
      placa: "",
      llanta_id: "",
      llanta_codigo: "",
      posicion: "",
      ubicacion: "",
      repuesto: ""

    }
  }
  $('#drop-vehiculos').on("change", function (e) {


    datos.items.vehiculo_id = ""
    datos.items.placa = ""
    datos.items.llanta_id = ""
    datos.items.llanta_codigo = ""
    datos.items.posicion = ""
    datos.items.repuesto = ""

    let data = {
      id: e.target.options[e.target.selectedIndex].value

    }
    oldURL = window.location.href

    let deleteDrop = document.getElementsByClassName("drag-drop")
    const removeElements = (elms) => elms.forEach(el => el.remove());

    removeElements(document.querySelectorAll(".modal"));
    removeElements(document.querySelectorAll(".drag-drop"));

    removeElements(document.querySelectorAll(".drag"));
    if (document.getElementById("background_tipo") != null) {
      document.getElementById("background_tipo").parentNode.removeChild(document.getElementById(
        "background_tipo"))
    }
    if (document.getElementById("myImg") != null) {
      document.getElementById("myImg").parentNode.removeChild(document.getElementById(
        "myImg"))
    }
    td_placa.textContent = "-"
    td_tipo.textContent = "-"
    td_modelo.textContent = "-"
    td_marca.textContent = "-"
    td_km.textContent = "-"
    td_obs.textContent = "-"
    operador.textContent = "-"

    // If your expected result is "http://foo.bar/?x=1&y=2&x=42"

    // If your expected result is "http://foo.bar/?x=42&y=2"
    fetch("../hoja-movimientos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken
      },
      body: JSON.stringify(data)
    }).then(data => data.json()).then(

    ).then(response => {
      console.log(response);
      if (response.status == 200) {

        document.getElementById("container-grid").classList.add("container-drag")
        let backgroud_img = document.createElement("div")
        backgroud_img.classList.add("img")
        backgroud_img.id = "background_tipo"
        backgroud_img.style.background = 'transparent url(' + response.vehiculo.tipo_vehiculo.image + ') no-repeat center center'
        document.getElementById("container-grid").append(backgroud_img)


        let backgroud_img2 = document.createElement("img")
        backgroud_img2.classList.add("img2")
        backgroud_img2.id = "myImg"
        backgroud_img2.src = response.vehiculo.tipo_vehiculo.image2

        let modal = document.createElement("div")
        modal.classList.add("modal")
        modal.id = "myModal"
        let content = document.createElement("img")
        content.classList.add("modal-content-vehiculo")
        content.id = "img01"
        modal.append(content)
        backgroud_img2.addEventListener("click", function () {
          modal.style.display = "block"
          content.src = this.src
          content.alt=this.alt
        })
        modal.addEventListener("click", function (param) {
          img01.className += " out";

          setTimeout(function () {
            modal.style.display = "none";
            img01.className = "modal-content-vehiculo";

          }, 400);

        })
        document.getElementById("container-grid").append(backgroud_img)
        document.getElementById("container-grid").append(backgroud_img2)
        document.getElementById("container-grid").append(modal)



        datos.items.vehiculo_id = response.vehiculo.id
        datos.items.placa = response.vehiculo.placa

        td_placa.textContent = response.vehiculo.placa
        td_tipo.textContent = response.vehiculo.tipo_vehiculo.descripcion
        td_modelo.textContent = response.vehiculo.modelo_vehiculo.descripcion
        td_marca.textContent = response.vehiculo.modelo_vehiculo["marca-vehiculo"].descripcion
        td_km.textContent = response.vehiculo.km
        td_obs.textContent = response.vehiculo.obs
        operador.textContent = response.vehiculo.created_by.persona

        for (let i = 0; i < response.pos.length; i++) {
          let parent = document.createElement("div")
          parent.style.transform = `translate(${response.pos[i].posx}px,${response.pos[i].posy}px)`
          parent.dataset.posicion = response.pos[i].posicion
          if (response.pos[i].repuesto == true) {
            parent.classList.add("drag", "bordeado", "re", )
          } else {
            parent.classList.add("drag", "bordeado")

          }
          for (let a = 0; a < response.llantas.length; a++) {
            if (response.llantas[a].posicion == response.pos[i].posicion) {
              let dragdrop = document.createElement("div")
              if (response.pos[i].repuesto == true) {
                dragdrop.classList.add("repuesto", "verLlanta", "drag-drop", "yes-drop")
                dragdrop.dataset.repuesto=true
              } else {
                dragdrop.classList.add("llanta", "verLlanta", "drag-drop", "yes-drop")
                dragdrop.dataset.repuesto=false

              }
              dragdrop.dataset.llanta = response.llantas[a].id
              dragdrop.dataset.codigo = response.llantas[a].codigo
              dragdrop.dataset.posicion = response.llantas[a].posicion
              parent.dataset.posicion = response.llantas[a].posicion
              dragdrop.dataset.repuesto = response.llantas[a].repuesto
              let dragdropSon = document.createElement("div")
              dragdropSon.classList.add("d-flex", "justify-content-center", "flex-wrap", "align-items-center")
              let posicion = document.createElement("div")
              posicion.classList.add("w-100")
              posicion.style.fontSize = "0.6em"
              posicion.textContent = "Pos :" + response.llantas[a].posicion
              let codigo = document.createElement("div")
              codigo.style.fontSize = "0.6em"
              codigo.style.color = "#000"
              codigo.textContent = response.llantas[a].codigo
              dragdropSon.append(posicion)
              dragdropSon.append(codigo)
              dragdrop.append(dragdropSon)
              console.log(response.llantas[a].id);
              dragdrop.addEventListener("dblclick", function () {
                fetch("../../viewLlanta/" + response.llantas[a].id + "/").then(
                  $.confirm({
                    title: 'Detalles del Neumático',
                    content: 'URL: ../../viewLlanta/' + response.llantas[a].id + "/",
                    type: 'dark',
                    theme: "material",
                    icon: 'fas fa-compact-disc',
                    animation: 'left',
                    closeAnimation: 'right',
                    columnClass: "col-md-6 col-md-offset-3",
                    typeAnimated: true,
                    buttons: {
  
                      close: function () {}
                    }
                  })
                )
  
  
  
              })
              parent.append(dragdrop)
              
            
            }
           

          }
          if(!parent.hasChildNodes()){
            parent.addEventListener("click", function AbriModantaje(event) {
              let repuesto
              let titulo
  
                if(event.target.classList.contains('re')){
                  repuesto=1
                titulo="Montar Neumático de Repuesto"
              }else{
                repuesto=0
                  titulo="Montar Neumático"
              }
              let url = " ../../montaje?" + new URLSearchParams({
                posicion: response.pos[i].posicion,
                repuesto,
                vehiculo: response.vehiculo.id,
                placa: response.vehiculo.placa
              })
         
              fetch(url).then(
                $.confirm({
                  title: titulo,
                  content: 'URL:' + url,
                  type: 'dark',
                  theme: "material",
                  icon: 'fas fa-compact-disc',
                  animation: 'left',
                  closeAnimation: 'right',
                  columnClass: "col-lg-6 col-md-6 col-md-offset-3",
                  containerFluid: true, // this will add 'container-fluid' instead of 'container'
  
                  typeAnimated: true,
                  buttons: {
                    guardar: {
                      btnClass: 'btn-success',
                      keys: ['enter', 'shift'],
                      action: function () {
                        let form = this.$content[0].ownerDocument
                        let id_llanta = form.getElementById("id_llanta")
                        let llanta = form.getElementById("id_neu")
  
                        let profundidad = form.getElementById("id_profundidad")
                        let km = form.getElementById("id_km")
                        let data = new FormData(form.forms[1])
                        let error = 0
                        if (km.value == "") {
                          form.getElementById("invalid_km").innerHTML =
                            "Este campo es requerido"
                          km.classList.add("is-invalid")
                          error = 1
                        }
                        if (id_llanta.value == "") {
                          form.getElementById("invalid_llanta").innerHTML =
                            "Este campo es requerido"
                          llanta.classList.add("is-invalid")
                          error = 1
                        }
                        if (profundidad.value == "") {
                          form.getElementById("invalid_profundidad").innerHTML =
                            "Este campo es requerido"
                          profundidad.classList.add("is-invalid")
                          error = 1
  
                        }
                        if (!validatePunto(profundidad.value)) {
                          form.getElementById("invalid_profundidad").innerHTML =
                            "Este campo debe tener un punto y 2 decimales."
                          profundidad.classList.add("is-invalid")
                          error = 1
  
                        }
  
                        if (error == 0) {
                          fetch('../../montaje/', {
                            method: "POST",
                            headers: {
                              'X-CSRFToken': csrftoken
                            },
                            body: data
  
                          }).then(data => data.json()).then(response => {
                            if (response.status == 200) {
                              const Toast = Swal.mixin({
                                toast: true,
                                position: 'top-end',
                                showConfirmButton: false,
                                timer: 3000,
                                timerProgressBar: true,
                                didOpen: (toast) => {
                                  toast.addEventListener('mouseenter', Swal.stopTimer)
                                  toast.addEventListener('mouseleave', Swal
                                    .resumeTimer)
                                }
                              })
  
                              Toast.fire({
                                icon: 'success',
                                title: 'Operacion realizada correctamente'
                              })
                              this.close()
                              let dragdrop = document.createElement("div")
                              dragdrop.addEventListener("dblclick", function () {
                                fetch("../../viewLlanta/" + response.id + "/").then(
                                  $.confirm({
                                    title: 'Detalles del Neumático',
                                    content: 'URL: ../../viewLlanta/' + response
                                      .id + "/",
                                    type: 'dark',
                                    theme: "material",
                                    icon: 'fas fa-compact-disc',
                                    animation: 'left',
                                    closeAnimation: 'right',
                                    columnClass: "col-md-6 col-md-offset-3",
                                    typeAnimated: true,
                                    buttons: {
  
                                      close: function () {}
                                    }
                                  })
                                )
  
                              })
                              console.log(event)
                              if (event.target.classList.contains('re')) {
                                console.log("Es repuesto")
                                dragdrop.classList.add("repuesto", "verLlanta", "drag-drop",
                                  "yes-drop")
                              } else {
                                console.log("no es repuesto")
                                dragdrop.classList.add("llanta", "verLlanta", "drag-drop",
                                  "yes-drop")
  
                              }
                              dragdrop.dataset.llanta = response.id
                              dragdrop.dataset.codigo = response.codigo
                              parent.dataset.posicion = response.posicion
                           
                              let dragdropSon = document.createElement("div")
                              dragdropSon.classList.add("d-flex", "justify-content-center",
                                "flex-wrap", "align-items-center")
                              let posicion = document.createElement("div")
                              posicion.classList.add("w-100")
                              posicion.style.fontSize = "0.6em"
                              posicion.textContent = "Pos :" + response.posicion
                              let codigo = document.createElement("div")
                              codigo.style.fontSize = "0.6em"
                              codigo.style.color = "#000"
                              codigo.textContent = response.codigo
                              dragdropSon.append(posicion)
                              dragdropSon.append(codigo)
                              dragdrop.append(dragdropSon)
                              event.target.append(dragdrop)
                              event.target.removeEventListener("click", AbriModantaje)
                            } else {
                              notificacion(2000, "Ha ocurrido un error!", "error")
                            }
  
                          })
  
                        } else {
                          notificacion(2000, "Revise los campos!", "error")
  
                        }
                        return false
                      }
                    },
                    close: function () {
  
                    }
                  }
                }))
  
            })
          }
          document.getElementById("container-grid").append(parent)

        }
      }
    })
  })
  $('#tablaMovimientos').DataTable({
    responsive: true,
    "searching": false,
    "paging": false,
    "ordering": true,
    "info": false
  });


  var drag_pos = {
    x: 0,
    y: 0
  }

  function dragging(e) {
    drag_pos.x += e.dx;
    drag_pos.y += e.dy;

    e.target.style.transform = 'translate(' + drag_pos.x + 'px, ' + drag_pos.y + 'px)';
  }

  function dragged(e) {
    drag_pos.x = 0;
    drag_pos.y = 0;
    e.target.style.transform = 'translate(0px, 0px)';
    e.target.setAttribute('data-x', 0)
    e.target.setAttribute('data-y', 0)
    e.target.classList.remove("can-drop")
  }

  function dragMoveListener(event) {
    var target = event.target
    // keep the dragged position in the data-x/data-y attributes
    var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
    var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy
    // translate the element
    target.style.webkitTransform =
      target.style.transform =
      'translate(' + x + 'px, ' + y + 'px)'

    // update the posiion attributes
    target.setAttribute('data-x', x)
    target.setAttribute('data-y', y)
  }
  interact('.dropzone').dropzone({
    // only accept elements matching this CSS selector
    accept: '.yes-drop',
    // Require a 75% element overlap for a drop to be possible
    overlap: 0.75,

    // listen for drop related events:

    ondropactivate: function (event) {
      // add active dropzone feedback
      event.target.classList.add('drop-active')
      console.log("ondropactivate");
      // dragged(event.dragEvent)
    },
    ondragenter: function (event) {
      var draggableElement = event.relatedTarget
      var dropzoneElement = event.target

      // feedback the possibility of a drop
      dropzoneElement.classList.add('drop-target')
      draggableElement.classList.add('can-drop')
      // draggableElement.textContent = 'Enviar'
      console.log("ondragenter");

    },
    ondragleave: function (event) {
      // remove the drop feedback style
      event.target.classList.remove('drop-target')
      event.relatedTarget.classList.remove('can-drop')
      // event.relatedTarget.textContent =event.relatedTarget.attributes[1].textContent
      console.log("ondragleave");

    },
    ondrop: function (event) {
      console.log(event)
      event.relatedTarget.classList.add('can-drop')
      let id = event.relatedTarget.dataset.llanta;
      let codigo = event.relatedTarget.dataset.codigo;

      let posicion = event.relatedTarget.parentNode.dataset.posicion;
      let repuesto = event.relatedTarget.dataset.repuesto;
      datos.items.llanta_id = id
      datos.items.llanta_codigo = codigo
      datos.items.posicion = posicion
      datos.items.ubicacion = event.currentTarget.dataset.id
      datos.items.repuesto = repuesto
      let url = " ../../desmontaje?" + new URLSearchParams({
        llanta: datos.items.llanta_id,
        codigo: datos.items.llanta_codigo,
        posicion: datos.items.posicion,
        vehiculo: datos.items.vehiculo_id,
        placa: datos.items.placa,
        ubicacion: datos.items.ubicacion,
        repuesto: datos.items.repuesto,

      })
      fetch(url).then(
        $.confirm({
          title: 'Desmontaje del Neumático',
          content: 'URL:' + url,
          type: 'dark',
          theme: "material",
          icon: 'fas fa-compact-disc',
          animation: 'left',
          closeAnimation: 'right',
          columnClass: "col-lg-6 col-md-6 col-md-offset-3",
          containerFluid: true, // this will add 'container-fluid' instead of 'container'

          typeAnimated: true,
          buttons: {
            guardar: {
              btnClass: 'btn-success',
              keys: ['enter', 'shift'],
              action: function () {
                let form = this.$content[0].ownerDocument
                let id_llanta = form.getElementById("id_llanta")
                let profundidad = form.getElementById("id_profundidad")
                let km = form.getElementById("id_km")
                let estado = form.getElementById("id_estado")
                let obs = form.getElementById("id_obs")
                let data = new FormData(form.forms[1])
                let error = 0
                if (km.value == "") {
                  form.getElementById("invalid_km").innerHTML = "Este campo es requerido"
                  km.classList.add("is-invalid")
                  error = 1
                }
                if (profundidad.value == "") {
                  form.getElementById("invalid_profundidad").innerHTML = "Este campo es requerido"
                  profundidad.classList.add("is-invalid")
                  error = 1

                }
                if (!validatePunto(profundidad.value)) {
                  form.getElementById("invalid_profundidad").innerHTML =
                    "Este campo debe tener un punto y 2 decimales."
                  profundidad.classList.add("is-invalid")
                  error = 1

                }
                if (obs.value == 0) {
                  form.getElementById("invalid_obs").innerHTML = "Este campo es requerido"
                  obs.classList.add("is-invalid")
                  error = 1

                }
                if (estado.value == 0) {
                  form.getElementById("invalid_estado").innerHTML = "Este campo es requerido"
                  estado.classList.add("is-invalid")
                  error = 1

                }
                if (error == 0) {
                  fetch('../../desmontaje/', {
                    method: "POST",
                    headers: {
                      'X-CSRFToken': csrftoken
                    },
                    body: data

                  }).then(data => data.json()).then(response => {
                    if (response.status == 200) {
                      const Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true,
                        didOpen: (toast) => {
                          toast.addEventListener('mouseenter', Swal.stopTimer)
                          toast.addEventListener('mouseleave', Swal.resumeTimer)
                        }
                      })

                      Toast.fire({
                        icon: 'success',
                        title: 'Operacion realizada correctamente'
                      })
                      this.close()
                      event.relatedTarget.parentNode.addEventListener("click", function AbriModantaje(param) {
                        console.log("montaje despues de soltar llanta");
                        console.log(param)
                        let url = " ../../montaje?" + new URLSearchParams({
                          posicion: param.target.dataset.posicion,
                          vehiculo: datos.items.vehiculo_id,
                          placa: datos.items.placa,

                        })
                        fetch(url).then(
                          $.confirm({
                            title: 'Montaje del Neumático',
                            content: 'URL:' + url,
                            type: 'dark',
                            theme: "material",
                            icon: 'fas fa-compact-disc',
                            animation: 'left',
                            closeAnimation: 'right',
                            columnClass: "col-lg-6 col-md-6 col-md-offset-3",
                            containerFluid: true, // this will add 'container-fluid' instead of 'container'

                            typeAnimated: true,
                            buttons: {
                              guardar: {
                                btnClass: 'btn-success',
                                keys: ['enter', 'shift'],
                                action: function () {
                                  let form = this.$content[0].ownerDocument
                                  let id_llanta = form.getElementById("id_llanta")
                                  let llanta = form.getElementById("id_neu")

                                  let profundidad = form.getElementById("id_profundidad")
                                  let km = form.getElementById("id_km")
                                  let data = new FormData(form.forms[1])
                                  let error = 0
                                  if (km.value == "") {
                                    form.getElementById("invalid_km").innerHTML =
                                      "Este campo es requerido"
                                    km.classList.add("is-invalid")
                                    error = 1
                                  }
                                  if (id_llanta.value == "") {
                                    form.getElementById("invalid_llanta").innerHTML =
                                      "Este campo es requerido"
                                    llanta.classList.add("is-invalid")
                                    error = 1
                                  }
                                  if (profundidad.value == "") {
                                    form.getElementById("invalid_profundidad").innerHTML =
                                      "Este campo es requerido"
                                    profundidad.classList.add("is-invalid")
                                    error = 1

                                  }
                                  if (!validatePunto(profundidad.value)) {
                                    form.getElementById("invalid_profundidad").innerHTML =
                                      "Este campo debe tener un punto y 2 decimales."
                                    profundidad.classList.add("is-invalid")
                                    error = 1

                                  }

                                  if (error == 0) {
                                    fetch('../../montaje/', {
                                      method: "POST",
                                      headers: {
                                        'X-CSRFToken': csrftoken
                                      },
                                      body: data

                                    }).then(data => data.json()).then(response => {
                                      console.log(response);
                                      if (response.status == 200) {
                                        const Toast = Swal.mixin({
                                          toast: true,
                                          position: 'top-end',
                                          showConfirmButton: false,
                                          timer: 3000,
                                          timerProgressBar: true,
                                          didOpen: (toast) => {
                                            toast.addEventListener('mouseenter', Swal.stopTimer)
                                            toast.addEventListener('mouseleave', Swal
                                              .resumeTimer)
                                          }
                                        })

                                        Toast.fire({
                                          icon: 'success',
                                          title: 'Operacion realizada correctamente'
                                        })
                                        this.close()
                                        let dragdrop = document.createElement("div")
                                        dragdrop.addEventListener("dblclick", function () {
                                          fetch("../../viewLlanta/" + response.id + "/").then(
                                            $.confirm({
                                              title: 'Detalles del Neumático',
                                              content: 'URL: ../../viewLlanta/' + response
                                                .id + "/",
                                              type: 'dark',
                                              theme: "material",
                                              icon: 'fas fa-compact-disc',
                                              animation: 'left',
                                              closeAnimation: 'right',
                                              columnClass: "col-md-6 col-md-offset-3",
                                              typeAnimated: true,
                                              buttons: {

                                                close: function () {}
                                              }
                                            })
                                          )

                                        })
                                        console.log(param)
                                        if (param.target.classList.contains('re')) {
                                          console.log("Es repuesto depues de soltar")
                                          dragdrop.classList.add("repuesto", "verLlanta", "drag-drop",
                                            "yes-drop")
                                        } else {
                                          console.log("No es repuesto depues de soltar")

                                          dragdrop.classList.add("llanta", "verLlanta", "drag-drop",
                                            "yes-drop")

                                        }
                                        dragdrop.dataset.llanta = response.id
                                        dragdrop.dataset.codigo = response.codigo
                                        dragdrop.dataset.posicion = response.posicion
                                        let dragdropSon = document.createElement("div")
                                        dragdropSon.classList.add("d-flex", "justify-content-center",
                                          "flex-wrap", "align-items-center")
                                        let posicion = document.createElement("div")
                                        posicion.classList.add("w-100")
                                        posicion.style.fontSize = "0.6em"
                                        posicion.textContent = "Pos :" + response.posicion
                                        let codigo = document.createElement("div")
                                        codigo.style.fontSize = "0.6em"
                                        codigo.style.color = "#000"
                                        codigo.textContent = response.codigo
                                        dragdropSon.append(posicion)
                                        dragdropSon.append(codigo)
                                        dragdrop.append(dragdropSon)
                                        param.target.append(dragdrop)
                                        param.target.removeEventListener("click", AbriModantaje)
                                      } else {
                                        notificacion(2000, "Ha ocurrido un error!", "error")
                                      }

                                    })

                                  } else {
                                    notificacion(2000, "Revise los campos!", "error")

                                  }
                                  return false
                                }
                              },
                              close: function () {

                              }
                            }
                          }))
                      })
                      event.relatedTarget.parentNode.removeChild(event.relatedTarget)

                    } else {
                      notificacion(2000, "Ha ocurrido un error!", "error")
                    }
                  })
                } else {
                  notificacion(2000, "Revise los campos!", "error")

                }
                return false
              }
            },
            close: function () {
              dragged(event.dragEvent)
              datos.items.llanta_id = ""
              datos.items.llanta_codigo = ""
              datos.items.posicion = ""
            }
          }
        })
      )

    },
    ondropdeactivate: function (event) {
      if (!event.relatedTarget.classList.contains('can-drop')) {
        dragged(event.dragEvent)

      }


      event.target.classList.remove('drop-active')
      event.target.classList.remove('drop-target')

    }
  })

  interact('.drag-drop')
    .draggable({
      inertia: true,

      autoScroll: true,
      // dragMoveListener from the dragging demo above
      listeners: {

        move: dragMoveListener,

      }
    })
});