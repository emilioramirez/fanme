(function() {
  $(function() {
    var $start, tour;
    $start = $("#start");
    tour = new Tour({
      onStart: function() {
        return $start.addClass("disabled", true);
      },
      onEnd: function() {
        location.href='/dash/temas_de_ayuda';
      },
      debug: true
    });
    tour.addSteps([
	{
        element: "#eventos-content",
        placement: "right",
        title: "Eventos",
        content: "Listado con todos los eventos que has creado como asi tambien a los que has sido invitado.",
        backdrop: true
      },{
        element: "#my-id-tour",
        placement: "left",
        title:"Editar evento",
        content: "Para los eventos creados por ti, tendras la opcion de editar el mismo o cancelarlo.",
        backdrop: true
      },{
        element: "#crear-evento",
        placement: "left",
        title: "Creacion de eventos",
        content: "A traves del boton de Crear Evento podras crear un nuevo evento e invitar a tus seguidores.",
        backdrop: true
      },{
        element: "#evento-trigger",
        path: "/social/evento_ayuda/"
      }
    ]);
    tour.start();
    if (tour.ended()) {
      //$('<div class="alert alert-warning"><button class="close" data-dismiss="alert">&times;</button>You ended the demo tour. <a href="#" class="start">Restart the demo tour.</a></div>').prependTo(".content").alert();
    }
    $(document).ready(function() {
      tour.restart();
    });
  });

}).call(this);
